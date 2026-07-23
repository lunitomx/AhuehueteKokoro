#!/usr/bin/env python3
"""Portable, local-first governed graph runtime for Kokoro E58.

The module deliberately has no provider, network, or project-package
dependency.  It stores an append-only sequence of atomically renamed JSON
events and derives the current run state by replaying that sequence.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import hashlib
import json
import os
import re
import stat
import subprocess
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import growth_diagnosis

SCHEMA_VERSION = 1
WORKFLOW_ID = "growth-diagnosis-v1"
RUNTIME_VERSION = "0.2.0-alpha.1"
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_ARTIFACT_BYTES = 4 * 1024 * 1024
RUN_ID_RE = re.compile(r"^run-[0-9a-f]{24}$")
EVENT_FILE_RE = re.compile(
    r"^(?P<sequence>[0-9]{6})-(?P<kind>[a-z_]+)-(?P<event_id>evt-[0-9a-f]{32})\.json$"
)
SECRET_FIELD_RE = re.compile(
    r"(?:^|[_-])(token|secret|password|passwd|api[_-]?key|private[_-]?key)(?:$|[_-])",
    re.IGNORECASE,
)
HIGH_CONFIDENCE_CREDENTIAL_PATTERNS = (
    re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{50,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"GOCSPX-[A-Za-z0-9_-]{20,}"),
    re.compile(r"EAA[A-Za-z0-9]{40,}"),
    re.compile(r"sk-(?:proj|svcacct)-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
)
NODES = ("plan", "execute", "critique", "verify", "human_gate")
AGENT_NODES = frozenset({"plan", "execute", "critique", "verify"})
STATUSES = frozenset({"active", "blocked", "waiting_human", "complete", "abandoned"})
TERMINAL_STATUSES = frozenset({"complete", "abandoned"})
ROLES = {
    "plan": "planner",
    "execute": "operator",
    "critique": "critic",
    "verify": "verifier",
    "human_gate": "user",
}


class GraphError(RuntimeError):
    """A safe, user-facing graph error with a deterministic exit code."""

    def __init__(self, message: str, code: int = 2) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class WorkflowSpec:
    """The only built-in workflow definition in E58."""

    schema_version: int
    workflow_id: str
    initial_node: str
    nodes: tuple[str, ...]
    roles: dict[str, str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "workflow_id": self.workflow_id,
            "initial_node": self.initial_node,
            "nodes": list(self.nodes),
            "roles": dict(self.roles),
            "transitions": {
                "plan": {"accepted": "execute"},
                "execute": {"accepted": "critique"},
                "critique": {"accepted": "verify"},
                "verify": {"pass": "human_gate", "fail": "human_gate"},
                "human_gate": {
                    "approve_after_pass": "complete",
                    "revise": "execute",
                },
            },
            "terminal_statuses": sorted(TERMINAL_STATUSES),
        }


WORKFLOW = WorkflowSpec(
    schema_version=SCHEMA_VERSION,
    workflow_id=WORKFLOW_ID,
    initial_node="plan",
    nodes=NODES,
    roles=ROLES,
)


@dataclass(frozen=True)
class RunPaths:
    """Canonical filesystem locations for one run."""

    workspace: Path
    root: Path
    run: Path
    inputs: Path
    events: Path
    inbox: Path
    artifacts: Path
    state: Path
    run_metadata: Path


def canonical_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically and reject non-finite numbers."""

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise GraphError("JSON value is not canonicalizable", 2) from exc


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _digest_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def _package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_origin(target: Path) -> str | None:
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or None


def _reject_symlink_components(path: Path, stop: Path) -> None:
    """Reject symlinks from stop (exclusive) to path (inclusive)."""

    try:
        relative = path.relative_to(stop)
    except ValueError as exc:
        raise GraphError("path is outside the allowed workspace", 2) from exc
    current = stop
    for part in relative.parts:
        current = current / part
        try:
            if current.is_symlink():
                raise GraphError("symlink paths are not accepted", 2)
        except OSError as exc:
            raise GraphError("path could not be inspected", 2) from exc


def _contained_path(raw: Path, root: Path, *, must_exist: bool = True) -> Path:
    root = root.resolve()
    candidate = raw if raw.is_absolute() else Path.cwd() / raw
    candidate = candidate.absolute()
    if must_exist and not candidate.exists():
        raise GraphError("path does not exist", 2)
    resolved = candidate.resolve(strict=False)
    if resolved != root and root not in resolved.parents:
        raise GraphError("path is outside the allowed workspace", 2)
    _reject_symlink_components(candidate, root)
    return candidate


def _validate_workspace(target: Path) -> Path:
    if not target.exists() or not target.is_dir():
        raise GraphError("target workspace must be an existing directory", 2)
    target = target.resolve()
    package = _package_root()
    if target == package or package in target.parents:
        raise GraphError("graph runs cannot be created in the Kokoro package", 2)
    remote = _git_origin(target)
    if remote and "ahuehuetekokoro" in remote.lower():
        raise GraphError("public AhuehueteKokoro checkout cannot host graph runs", 2)
    marker = target / ".kokoro" / ".gitignore"
    if not marker.is_file() or marker.is_symlink():
        raise GraphError("workspace must be initialized with Kokoro memory first", 2)
    return target


def _run_id(idempotency_key: str) -> str:
    if not idempotency_key or len(idempotency_key) > 256:
        raise GraphError(
            "idempotency key is required and must be at most 256 characters", 2
        )
    return "run-" + _digest_text(idempotency_key)[:24]


def _paths(target: Path, run_id: str) -> RunPaths:
    if not RUN_ID_RE.fullmatch(run_id):
        raise GraphError("invalid run id", 2)
    root = target / ".kokoro" / "local" / "agent-runs"
    run = root / run_id
    return RunPaths(
        workspace=target,
        root=root,
        run=run,
        inputs=run / "inputs",
        events=run / "events",
        inbox=run / "inbox",
        artifacts=run / "artifacts",
        state=run / "state.json",
        run_metadata=run / "run.json",
    )


@contextlib.contextmanager
def _mutation_lock(paths: RunPaths) -> Iterator[None]:
    """Serialize mutations when the host provides POSIX advisory locking."""

    paths.root.mkdir(parents=True, exist_ok=True)
    lock_path = paths.root / ".agent-graph.lock"
    handle = lock_path.open("a+", encoding="utf-8")
    try:
        try:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        except (ImportError, OSError):
            pass
        yield
    finally:
        try:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except (ImportError, OSError):
            pass
        handle.close()


def _fsync_directory(directory: Path) -> None:
    try:
        fd = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temp.open("wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        _fsync_directory(path.parent)
    except OSError as exc:
        with contextlib.suppress(OSError):
            temp.unlink(missing_ok=True)
        raise GraphError("atomic persistence failed", 4) from exc


def _write_json(path: Path, value: Any) -> None:
    _atomic_write(path, canonical_bytes(value) + b"\n")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GraphError("persisted JSON evidence is malformed", 4) from exc
    if not isinstance(value, dict):
        raise GraphError("persisted JSON evidence must be an object", 4)
    return cast(dict[str, Any], value)


def _secret_field(path: tuple[str, ...]) -> bool:
    return any(SECRET_FIELD_RE.search(part) for part in path)


def _contains_secret_like(value: Any, path: tuple[str, ...] = ()) -> bool:
    if _secret_field(path):
        return True
    if isinstance(value, dict):
        mapping = cast(dict[object, Any], value)
        return any(
            _contains_secret_like(item, path + (str(key),))
            for key, item in mapping.items()
        )
    if isinstance(value, list):
        items = cast(list[Any], value)
        return any(_contains_secret_like(item, path) for item in items)
    if isinstance(value, str):
        return any(
            pattern.search(value) for pattern in HIGH_CONFIDENCE_CREDENTIAL_PATTERNS
        )
    return False


def _read_candidate(
    path: Path, root: Path, maximum: int
) -> tuple[bytes, dict[str, Any]]:
    candidate = _contained_path(path, root)
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(candidate, flags)
    except OSError as exc:
        raise GraphError("candidate file could not be opened safely", 2) from exc
    try:
        first = os.fstat(fd)
        if not stat.S_ISREG(first.st_mode):
            raise GraphError("candidate must be a regular file", 2)
        if first.st_size > maximum:
            raise GraphError("candidate file is too large", 2)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, min(65536, maximum + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > maximum:
                raise GraphError("candidate file is too large", 2)
        second = os.fstat(fd)
        if (first.st_ino, first.st_dev, first.st_size, first.st_mtime_ns) != (
            second.st_ino,
            second.st_dev,
            second.st_size,
            second.st_mtime_ns,
        ):
            raise GraphError("candidate changed while it was being read", 2)
    except OSError as exc:
        raise GraphError("candidate file could not be read safely", 2) from exc
    finally:
        os.close(fd)
    raw = b"".join(chunks)
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GraphError("candidate must contain valid JSON", 2) from exc
    if not isinstance(value, dict):
        raise GraphError("candidate JSON must be an object", 2)
    if _contains_secret_like(value):
        raise GraphError("candidate contains secret-like data", 2)
    return raw, cast(dict[str, Any], value)


def _state_snapshot(state: dict[str, Any] | None) -> dict[str, Any] | None:
    if state is None:
        return None
    return {
        "status": state["status"],
        "node": state["current_node"],
        "revision": state["revision"],
    }


def _initial_state(run_id: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "runtime_version": RUNTIME_VERSION,
        "run_id": run_id,
        "workflow_id": WORKFLOW_ID,
        "status": "active",
        "current_node": "plan",
        "revision": 1,
        "verification_verdict": None,
        "blocker": None,
        "last_sequence": 1,
        "last_event_sha256": None,
        "accepted_nodes": [],
        "artifacts": [],
        "input_sha256": None,
        "input_size": None,
        "approval_allowed": False,
    }


def _next_state(
    state: dict[str, Any] | None, kind: str, payload: dict[str, Any]
) -> dict[str, Any]:
    if kind == "run_started":
        if state is not None:
            raise GraphError("run_started cannot follow an existing event", 4)
        run_id = payload.get("run_id")
        if not isinstance(run_id, str) or not RUN_ID_RE.fullmatch(run_id):
            raise GraphError("run_started has an invalid run id", 4)
        result = _initial_state(run_id)
        result["input_sha256"] = payload.get("input_sha256")
        result["input_size"] = payload.get("input_size")
        return result
    if state is None:
        raise GraphError("event chain does not start with run_started", 4)
    result = json.loads(json.dumps(state))
    node = payload.get("node")
    current_node = result["current_node"]
    status = result["status"]
    if kind == "node_blocked":
        if node != current_node or current_node not in AGENT_NODES:
            raise GraphError("blocked event does not match the current node", 4)
        if status not in {"active", "blocked"}:
            raise GraphError("blocked event has an illegal prestate", 4)
        result["status"] = "blocked"
        result["blocker"] = payload.get("blocker")
    elif kind == "node_completed":
        if node != current_node or current_node not in AGENT_NODES:
            raise GraphError("node_completed does not match the current node", 4)
        if status not in {"active", "blocked"}:
            raise GraphError("node_completed has an illegal prestate", 4)
        result["blocker"] = None
        result["accepted_nodes"].append(
            {
                "node": node,
                "revision": result["revision"],
                "artifact": payload.get("artifact"),
            }
        )
        if node == "verify":
            verdict = payload.get("verification_verdict")
            if verdict not in {"pass", "fail"}:
                raise GraphError("verify completion requires pass or fail", 4)
            result["verification_verdict"] = verdict
            result["status"] = "waiting_human"
            result["current_node"] = "human_gate"
            result["approval_allowed"] = verdict == "pass"
        else:
            next_nodes = {
                "plan": "execute",
                "execute": "critique",
                "critique": "verify",
            }
            result["current_node"] = next_nodes[cast(str, node)]
            result["status"] = "active"
    elif kind == "human_approved":
        if current_node != "human_gate" or status != "waiting_human":
            raise GraphError("human approval has an illegal prestate", 4)
        if result["verification_verdict"] != "pass":
            raise GraphError("human approval cannot follow failed verification", 4)
        result["status"] = "complete"
        result["current_node"] = None
        result["approval_allowed"] = False
    elif kind == "revision_requested":
        if current_node != "human_gate" or status != "waiting_human":
            raise GraphError("revision has an illegal prestate", 4)
        if result["revision"] != 1:
            raise GraphError("E58 allows only one user revision", 4)
        result["revision"] = 2
        result["status"] = "active"
        result["current_node"] = "execute"
        result["verification_verdict"] = None
        result["blocker"] = None
        result["approval_allowed"] = False
    elif kind == "run_abandoned":
        if status in TERMINAL_STATUSES or current_node is None:
            raise GraphError("terminal runs cannot be abandoned", 4)
        result["status"] = "abandoned"
        result["current_node"] = None
        result["blocker"] = None
        result["approval_allowed"] = False
    else:
        raise GraphError("unsupported event kind", 4)
    return result


def reduce_event(state: dict[str, Any] | None, event: dict[str, Any]) -> dict[str, Any]:
    """Purely apply one validated event to a state projection."""

    if event.get("schema_version") != SCHEMA_VERSION:
        raise GraphError("unsupported event schema", 4)
    expected_prior = _state_snapshot(state)
    if event.get("prior") != expected_prior:
        raise GraphError("event prior state does not match replay state", 4)
    next_state = _next_state(state, str(event.get("kind")), event.get("payload", {}))
    if event.get("next") != _state_snapshot(next_state):
        raise GraphError("event next state does not match reducer", 4)
    next_state["last_sequence"] = event.get("sequence")
    next_state["last_event_sha256"] = event.get("event_sha256")
    artifact = event.get("artifact")
    if artifact is not None:
        next_state["artifacts"].append(artifact)
    return next_state


def _event_hash(event: dict[str, Any]) -> str:
    unsigned = dict(event)
    unsigned.pop("event_sha256", None)
    return sha256_bytes(canonical_bytes(unsigned))


def _event_id() -> str:
    return "evt-" + uuid.uuid4().hex


def _event_filename(sequence: int, kind: str, event_id: str) -> str:
    return f"{sequence:06d}-{kind}-{event_id}.json"


def _event_files(paths: RunPaths) -> list[Path]:
    if not paths.events.is_dir():
        raise GraphError("event ledger is missing", 4)
    found: list[tuple[int, Path]] = []
    for path in paths.events.iterdir():
        if path.name.startswith(".") and path.name.endswith(".tmp"):
            continue
        match = EVENT_FILE_RE.fullmatch(path.name)
        if not match or path.is_symlink() or not path.is_file():
            raise GraphError("event ledger contains an invalid file", 4)
        found.append((int(match.group("sequence")), path))
    return [path for _sequence, path in sorted(found)]


def _verify_artifact(paths: RunPaths, artifact: dict[str, Any]) -> None:
    relative = artifact.get("path")
    expected_sha = artifact.get("sha256")
    expected_size = artifact.get("size")
    if (
        not isinstance(relative, str)
        or not isinstance(expected_sha, str)
        or not isinstance(expected_size, int)
    ):
        raise GraphError("event artifact metadata is malformed", 4)
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise GraphError("event artifact path is unsafe", 4)
    actual = _contained_path(paths.run / relative, paths.run)
    if not actual.is_file():
        raise GraphError("accepted artifact is missing", 4)
    try:
        raw = actual.read_bytes()
    except OSError as exc:
        raise GraphError("accepted artifact cannot be read", 4) from exc
    if len(raw) != expected_size or sha256_bytes(raw) != expected_sha:
        raise GraphError("accepted artifact digest does not match the ledger", 4)


def _load_ledger(paths: RunPaths) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    events = _event_files(paths)
    if not events:
        raise GraphError("event ledger is empty", 4)
    state: dict[str, Any] | None = None
    loaded: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    previous_hash: str | None = None
    for expected_sequence, path in enumerate(events, start=1):
        match = EVENT_FILE_RE.fullmatch(path.name)
        if match is None or int(match.group("sequence")) != expected_sequence:
            raise GraphError("event sequence is missing or out of order", 4)
        event = _read_json(path)
        if event.get("run_id") != paths.run.name:
            raise GraphError("event belongs to a different run", 4)
        if event.get("sequence") != expected_sequence:
            raise GraphError("event sequence field does not match its filename", 4)
        if event.get("event_id") != match.group("event_id"):
            raise GraphError("event id does not match its filename", 4)
        if event.get("kind") != match.group("kind"):
            raise GraphError("event kind does not match its filename", 4)
        if event.get("previous_event_sha256") != previous_hash:
            raise GraphError("event hash chain is broken", 4)
        if event.get("event_sha256") != _event_hash(event):
            raise GraphError("event hash is invalid", 4)
        key_hash = event.get("idempotency_key_sha256")
        if not isinstance(key_hash, str) or key_hash in seen_keys:
            raise GraphError("event idempotency key is duplicated or malformed", 4)
        seen_keys.add(key_hash)
        artifact = event.get("artifact")
        if artifact is not None:
            _verify_artifact(paths, artifact)
        state = reduce_event(state, event)
        loaded.append(event)
        previous_hash = event["event_sha256"]
    if state is None:
        raise GraphError("event ledger has no state", 4)
    return loaded, state


def _projection_matches(paths: RunPaths, state: dict[str, Any]) -> bool:
    if not paths.state.is_file() or paths.state.is_symlink():
        return False
    try:
        return _read_json(paths.state) == state
    except GraphError:
        return False


def _write_projection(paths: RunPaths, state: dict[str, Any]) -> None:
    _write_json(paths.state, state)


def _lookup_idempotency(
    events: list[dict[str, Any]], key: str, request_sha256: str
) -> dict[str, Any] | None:
    key_sha = _digest_text(key)
    matches = [
        event for event in events if event.get("idempotency_key_sha256") == key_sha
    ]
    if not matches:
        return None
    event = matches[0]
    if event.get("request_sha256") != request_sha256:
        raise GraphError("idempotency key conflict", 4)
    return {
        "replayed": True,
        "event": event,
        "exit_code": int(event.get("result_exit_code", 0)),
    }


def _request_sha(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def _make_event(
    state: dict[str, Any] | None,
    *,
    run_id: str,
    kind: str,
    payload: dict[str, Any],
    idempotency_key: str,
    request_sha256: str,
    artifact: dict[str, Any] | None,
    exit_code: int,
) -> dict[str, Any]:
    next_state = _next_state(state, kind, payload)
    event = {
        "schema_version": SCHEMA_VERSION,
        "sequence": 1 if state is None else int(state["last_sequence"]) + 1,
        "event_id": _event_id(),
        "run_id": run_id,
        "kind": kind,
        "occurred_at": _utc_now(),
        "prior": _state_snapshot(state),
        "next": _state_snapshot(next_state),
        "idempotency_key_sha256": _digest_text(idempotency_key),
        "request_sha256": request_sha256,
        "previous_event_sha256": None if state is None else state["last_event_sha256"],
        "payload": payload,
        "artifact": artifact,
        "result_exit_code": exit_code,
    }
    event["event_sha256"] = _event_hash(event)
    return event


def _persist_event(paths: RunPaths, event: dict[str, Any]) -> None:
    filename = _event_filename(
        int(event["sequence"]), str(event["kind"]), str(event["event_id"])
    )
    target = paths.events / filename
    if target.exists():
        raise GraphError("event filename already exists", 4)
    _atomic_write(target, canonical_bytes(event) + b"\n")


def _result(
    state: dict[str, Any],
    *,
    exit_code: int,
    replayed: bool = False,
    packet: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "exit_code": exit_code,
        "replayed": replayed,
        "state": state,
    }
    if packet is not None:
        result["packet"] = packet
    return result


def _role_packet(state: dict[str, Any]) -> dict[str, Any] | None:
    node = state.get("current_node")
    if node is None:
        return None
    stored_artifacts = cast(list[dict[str, Any]], state.get("artifacts", []))
    artifacts = [item["path"] for item in stored_artifacts if "path" in item]
    if node == "human_gate":
        decisions = (
            ["approve", "revise"] if state.get("approval_allowed") else ["revise"]
        )
        decisions.append("close --abandon")
        return {
            "schema_version": SCHEMA_VERSION,
            "workflow_id": WORKFLOW_ID,
            "mode": "single-host-sequential",
            "run_id": state["run_id"],
            "node": node,
            "role": ROLES[node],
            "objective": "Present the verification bundle and request only a legal user decision.",
            "inputs": artifacts,
            "expected_output": "NodeResult",
            "expected_result_path": f"inbox/human-gate-r{state['revision']}.json",
            "constraints": [
                "approval is host-attested, not authenticated identity",
                "do not mutate external systems",
            ],
            "allowed_decisions": decisions,
            "verification_verdict": state.get("verification_verdict"),
        }
    objectives = {
        "plan": "Inventory evidence across Suelo, Semilla, Germinación and Cosecha.",
        "execute": "Choose one limiting bottleneck and create a seven-day diagnosis plan.",
        "critique": "Find unsupported claims, skipped gates and unsafe recommendations.",
        "verify": "Check structure, evidence, privacy and the no-external-action boundary.",
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "workflow_id": WORKFLOW_ID,
        "mode": "single-host-sequential",
        "run_id": state["run_id"],
        "node": node,
        "role": ROLES[node],
        "objective": objectives[node],
        "inputs": artifacts or ["inputs/start.json"],
        "expected_output": "NodeResult",
        "expected_result_path": f"inbox/{node}-r{state['revision']}.json",
        "constraints": [
            "do not mutate external systems",
            "return JSON schema_version=1",
        ],
    }


def start_run(
    target: Path, workflow_id: str, input_file: Path, idempotency_key: str
) -> dict[str, Any]:
    target = _validate_workspace(target)
    if workflow_id != WORKFLOW_ID:
        raise GraphError("unsupported workflow", 2)
    run_id = _run_id(idempotency_key)
    paths = _paths(target, run_id)
    raw, input_value = _read_candidate(input_file, target, MAX_INPUT_BYTES)
    input_sha = sha256_bytes(raw)
    request_sha = _request_sha(
        {"workflow_id": workflow_id, "input_sha256": input_sha, "input_size": len(raw)}
    )
    with _mutation_lock(paths):
        if paths.run.exists():
            events, state = _load_ledger(paths)
            replay = _lookup_idempotency(events, idempotency_key, request_sha)
            if replay is None:
                raise GraphError(
                    "run id already exists with a different start request", 4
                )
            return _result(
                state,
                exit_code=replay["exit_code"],
                replayed=True,
                packet=_role_packet(state),
            )
        paths.run.mkdir(parents=True)
        for directory in (paths.inputs, paths.events, paths.inbox, paths.artifacts):
            directory.mkdir()
        _write_json(
            paths.run_metadata,
            {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id,
                "workflow_id": workflow_id,
                "idempotency_key_sha256": _digest_text(idempotency_key),
            },
        )
        _atomic_write(paths.inputs / "start.json", raw)
        event = _make_event(
            None,
            run_id=run_id,
            kind="run_started",
            payload={
                "run_id": run_id,
                "workflow": workflow_id,
                "input_sha256": input_sha,
                "input_size": len(raw),
                "initial_node": "plan",
            },
            idempotency_key=idempotency_key,
            request_sha256=request_sha,
            artifact=None,
            exit_code=0,
        )
        _persist_event(paths, event)
        events, state = _load_ledger(paths)
        _write_projection(paths, state)
        _ = input_value
        return _result(state, exit_code=0, packet=_role_packet(state))


def _load_run(
    target: Path, run_id: str
) -> tuple[RunPaths, list[dict[str, Any]], dict[str, Any]]:
    target = _validate_workspace(target)
    paths = _paths(target, run_id)
    if not paths.run.is_dir():
        raise GraphError("run was not found", 2)
    events, state = _load_ledger(paths)
    return paths, events, state


def next_packet(target: Path, run_id: str) -> dict[str, Any]:
    _paths_checked, _events, state = _load_run(target, run_id)
    exit_code = 3 if state["status"] in {"blocked", "waiting_human"} else 0
    return _result(state, exit_code=exit_code, packet=_role_packet(state))


def status_run(target: Path, run_id: str) -> dict[str, Any]:
    _paths_checked, _events, state = _load_run(target, run_id)
    exit_code = 3 if state["status"] in {"blocked", "waiting_human"} else 0
    return _result(state, exit_code=exit_code)


def resume_run(target: Path, run_id: str) -> dict[str, Any]:
    paths, _events, state = _load_run(target, run_id)
    with _mutation_lock(paths):
        if not _projection_matches(paths, state):
            _write_projection(paths, state)
    exit_code = 3 if state["status"] in {"blocked", "waiting_human"} else 0
    return _result(state, exit_code=exit_code, packet=_role_packet(state))


def _validate_node_result(
    node: str, value: dict[str, Any], state: dict[str, Any]
) -> tuple[str, dict[str, Any]]:
    if value.get("schema_version") != SCHEMA_VERSION or value.get("node") != node:
        raise GraphError("result schema or node does not match the current packet", 2)
    decision = value.get("decision")
    if node in AGENT_NODES:
        if decision is not None:
            raise GraphError("agent node decision must be null", 2)
        result_status = value.get("status")
        if result_status not in {"accepted", "blocked"}:
            raise GraphError("agent result status must be accepted or blocked", 2)
        if result_status == "blocked" and not isinstance(value.get("blocker"), str):
            raise GraphError("blocked result requires a blocker label", 2)
        if result_status == "accepted":
            try:
                domain_data = growth_diagnosis.validate_node_artifact(node, value)
            except growth_diagnosis.GrowthContractError as exc:
                raise GraphError(
                    "accepted artifact does not satisfy the growth contract", 2
                ) from exc
            return cast(str, result_status), domain_data
        return cast(str, result_status), {}
    if node != "human_gate":
        raise GraphError("unsupported result node", 2)
    if decision not in {"approve", "revise"}:
        raise GraphError("human gate decision must be approve or revise", 2)
    provenance_value = value.get("approval_provenance")
    if not isinstance(provenance_value, dict):
        raise GraphError("human decision requires host interaction provenance", 2)
    provenance = cast(dict[str, Any], provenance_value)
    if provenance.get("channel") != "host_interaction":
        raise GraphError("human decision requires host interaction provenance", 2)
    if (
        not isinstance(provenance.get("actor_label"), str)
        or not provenance["actor_label"].strip()
    ):
        raise GraphError("human decision requires an actor label", 2)
    if (
        not isinstance(provenance.get("recorded_at"), str)
        or not provenance["recorded_at"].strip()
    ):
        raise GraphError("human decision requires a recorded timestamp", 2)
    if decision == "approve" and state.get("verification_verdict") != "pass":
        raise GraphError("approval is disabled after failed verification", 2)
    if decision == "revise" and state.get("revision") != 1:
        raise GraphError("E58 allows one revision only", 2)
    return cast(str, decision), {
        "approval_provenance": {
            "channel": "host_interaction",
            "actor_label": provenance["actor_label"],
            "recorded_at": provenance["recorded_at"],
        }
    }


def _ingest_artifact(
    paths: RunPaths, node: str, revision: int, raw: bytes
) -> dict[str, Any]:
    digest = sha256_bytes(raw)
    relative = Path("artifacts") / f"{node}-r{revision}-{digest}.json"
    destination = paths.run / relative
    if destination.exists():
        existing = destination.read_bytes()
        if existing != raw:
            raise GraphError("artifact digest collision", 4)
    else:
        _atomic_write(destination, raw)
    return {"path": relative.as_posix(), "sha256": digest, "size": len(raw)}


def submit_result(
    target: Path, run_id: str, result_file: Path, idempotency_key: str
) -> dict[str, Any]:
    paths, events, state = _load_run(target, run_id)
    with _mutation_lock(paths):
        events, state = _load_ledger(paths)
        if state["status"] in TERMINAL_STATUSES:
            raise GraphError("terminal runs cannot accept mutations", 2)
        raw, value = _read_candidate(result_file, paths.inbox, MAX_ARTIFACT_BYTES)
        request_sha = _request_sha(
            {"run_id": run_id, "result_sha256": sha256_bytes(raw)}
        )
        replay = _lookup_idempotency(events, idempotency_key, request_sha)
        if replay is not None:
            return _result(
                state,
                exit_code=replay["exit_code"],
                replayed=True,
                packet=_role_packet(state),
            )
        node = state["current_node"]
        if not isinstance(node, str):
            raise GraphError("run has no current node", 2)
        decision, extra = _validate_node_result(node, value, state)
        artifact: dict[str, Any] | None = None
        if node in AGENT_NODES or value.get("artifact") is not None:
            artifact = _ingest_artifact(paths, node, int(state["revision"]), raw)
        if node in AGENT_NODES and artifact is None:
            raise GraphError("agent result requires an artifact", 2)
        if node in AGENT_NODES and decision == "blocked":
            kind = "node_blocked"
            payload = {
                "node": node,
                "blocker": str(value.get("blocker")),
                "next_action": str(
                    value.get("next_action", "correct the blocker and resubmit")
                ),
                "artifact": artifact,
            }
            exit_code = 3
        elif node in AGENT_NODES:
            kind = "node_completed"
            verdict = extra.get("verdict", value.get("verification_verdict"))
            if node == "verify" and verdict not in {"pass", "fail"}:
                raise GraphError(
                    "verify result requires verification_verdict pass or fail", 2
                )
            payload = {
                "node": node,
                "result_status": "accepted",
                "verification_verdict": verdict,
                "artifact": artifact,
            }
            exit_code = 3 if node == "verify" else 0
        elif decision == "approve":
            kind = "human_approved"
            payload = {"node": node, "decision": decision, **extra}
            exit_code = 0
        else:
            kind = "revision_requested"
            payload = {"node": node, "decision": decision, **extra}
            exit_code = 0
        event = _make_event(
            state,
            run_id=run_id,
            kind=kind,
            payload=payload,
            idempotency_key=idempotency_key,
            request_sha256=request_sha,
            artifact=artifact,
            exit_code=exit_code,
        )
        _persist_event(paths, event)
        _events_after, new_state = _load_ledger(paths)
        _write_projection(paths, new_state)
        return _result(new_state, exit_code=exit_code, packet=_role_packet(new_state))


def close_run(
    target: Path, run_id: str, reason: str, idempotency_key: str
) -> dict[str, Any]:
    if not reason or len(reason) > 160:
        raise GraphError("abandon reason is required and must be short", 2)
    label = re.sub(r"[^A-Za-z0-9._-]+", "_", reason.strip()).strip("_")
    if not label:
        raise GraphError("abandon reason is empty", 2)
    paths, events, state = _load_run(target, run_id)
    with _mutation_lock(paths):
        events, state = _load_ledger(paths)
        request_sha = _request_sha({"run_id": run_id, "reason": label})
        replay = _lookup_idempotency(events, idempotency_key, request_sha)
        if replay is not None:
            return _result(state, exit_code=replay["exit_code"], replayed=True)
        if state["status"] in TERMINAL_STATUSES:
            raise GraphError("terminal runs cannot be abandoned", 2)
        event = _make_event(
            state,
            run_id=run_id,
            kind="run_abandoned",
            payload={"reason_label": label},
            idempotency_key=idempotency_key,
            request_sha256=request_sha,
            artifact=None,
            exit_code=0,
        )
        _persist_event(paths, event)
        _events_after, new_state = _load_ledger(paths)
        _write_projection(paths, new_state)
        return _result(new_state, exit_code=0)


def doctor_run(target: Path, run_id: str) -> dict[str, Any]:
    target = _validate_workspace(target)
    paths = _paths(target, run_id)
    if not paths.run.is_dir():
        raise GraphError("run was not found", 2)
    events, state = _load_ledger(paths)
    warnings: list[str] = []
    if not _projection_matches(paths, state):
        warnings.append("state.json is missing or stale; run resume will rebuild it")
    if any(
        path.name.startswith(".") and path.name.endswith(".tmp")
        for path in paths.events.iterdir()
    ):
        warnings.append("orphan temporary event files exist and were not promoted")
    return {
        "exit_code": 0,
        "run_id": run_id,
        "healthy": True,
        "event_count": len(events),
        "state": state,
        "warnings": warnings,
    }


def graph_operation(operation: str, **kwargs: Any) -> dict[str, Any]:
    """Dispatch the CLI operation without importing argparse here."""

    if operation == "start":
        return start_run(
            kwargs["target"],
            kwargs["workflow"],
            kwargs["input_file"],
            kwargs["idempotency_key"],
        )
    if operation == "next":
        return next_packet(kwargs["target"], kwargs["run_id"])
    if operation == "status":
        return status_run(kwargs["target"], kwargs["run_id"])
    if operation == "resume":
        return resume_run(kwargs["target"], kwargs["run_id"])
    if operation == "submit":
        return submit_result(
            kwargs["target"],
            kwargs["run_id"],
            kwargs["result_file"],
            kwargs["idempotency_key"],
        )
    if operation == "close":
        return close_run(
            kwargs["target"],
            kwargs["run_id"],
            kwargs["reason"],
            kwargs["idempotency_key"],
        )
    if operation == "doctor":
        return doctor_run(kwargs["target"], kwargs["run_id"])
    raise GraphError("unknown graph operation", 2)
