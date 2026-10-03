#!/usr/bin/env python3
"""Shared, append-only evidence ledger and its rebuildable views.

Canonical history: `.kokoro/shared/events/evidence/NNNNNN-<type>-evt-<hex>.json`.
Views (`.kokoro/shared/views/evidence/*.yaml`) are projections written as JSON,
which is valid YAML 1.2; deleting them loses nothing because `rebuild_views`
replays the ledger.  The subdirectories keep this ledger apart from Memory v2,
which owns the `*.yaml` events and `views/open-loops.yaml` one level up.

Mechanics reuse E58 (`agent_graph`): canonical JSON, SHA-256 hash chain,
idempotency keys, atomic writes, advisory lock and fail-closed errors
(code 2 = rejected input, code 4 = integrity failure).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, cast

import agent_graph
import evidence
from agent_graph import GraphError

LEDGER_SCHEMA_VERSION = 1
EVENTS_RELATIVE = Path(".kokoro") / "shared" / "events" / "evidence"
VIEWS_RELATIVE = Path(".kokoro") / "shared" / "views" / "evidence"
LOCK_RELATIVE = Path(".kokoro") / "local"
LOCK_NAME = "evidence-ledger.lock"
EVENT_FILE_RE = re.compile(
    r"^(?P<sequence>[0-9]{6})-(?P<type>[a-z_]+)-(?P<event_id>evt-[0-9a-f]{32})\.json$"
)
ACTIVE_LOOP_STATUSES = frozenset({"captured", "ranked", "promoted", "hypothesis"})
VIEW_NAMES = ("open-loops", "hypotheses", "validations")


@dataclass(frozen=True)
class LedgerPaths:
    workspace: Path
    events: Path
    views: Path
    lock_root: Path


# --- Paths and file reading ----------------------------------------------------


def ledger_paths(target: Path) -> LedgerPaths:
    workspace = agent_graph._validate_workspace(target)
    paths = LedgerPaths(
        workspace=workspace,
        events=workspace / EVENTS_RELATIVE,
        views=workspace / VIEWS_RELATIVE,
        lock_root=workspace / LOCK_RELATIVE,
    )
    _reject_redirected_paths(paths)
    return paths


def _reject_redirected_paths(paths: LedgerPaths) -> None:
    """A symlink anywhere under the workspace could send writes outside it."""

    for path in (paths.events, paths.views, paths.lock_root / LOCK_NAME):
        try:
            agent_graph._reject_symlink_components(path, paths.workspace)
        except GraphError as exc:
            raise GraphError("evidence ledger paths must not be symlinks", 4) from exc
    for name in render_views(empty_state()):
        if (paths.views / f"{name}.yaml").is_symlink():
            raise GraphError("evidence ledger paths must not be symlinks", 4)


def _event_files(paths: LedgerPaths) -> list[Path]:
    if not paths.events.exists():
        return []
    if paths.events.is_symlink() or not paths.events.is_dir():
        raise GraphError("evidence ledger directory is invalid", 4)
    found: list[tuple[int, Path]] = []
    for path in paths.events.iterdir():
        if path.name.startswith(".") and path.name.endswith(".tmp"):
            continue
        match = EVENT_FILE_RE.fullmatch(path.name)
        if not match or path.is_symlink() or not path.is_file():
            raise GraphError("evidence ledger contains an invalid file", 4)
        found.append((int(match.group("sequence")), path))
    return [path for _sequence, path in sorted(found)]


# --- Projection state -----------------------------------------------------------


def empty_state() -> dict[str, Any]:
    return {
        "loops": {},
        "hypotheses": {},
        "validations": {},
        "last_sequence": 0,
        "last_event_sha256": None,
    }


def _payload(event_payload: Any, allowed: frozenset[str]) -> dict[str, Any]:
    payload = evidence._object(event_payload, "payload")
    evidence._no_unknown(payload, allowed, "payload")
    return payload


def _loop(state: dict[str, Any], loop_id: Any) -> dict[str, Any]:
    loop = state["loops"].get(loop_id)
    if loop is None:
        raise evidence.EvidenceError(f"unknown loop: {loop_id}")
    return cast(dict[str, Any], loop)


def _hypothesis(state: dict[str, Any], hypothesis_id: Any) -> dict[str, Any]:
    hypothesis = state["hypotheses"].get(hypothesis_id)
    if hypothesis is None:
        raise evidence.EvidenceError(f"unknown hypothesis: {hypothesis_id}")
    return cast(dict[str, Any], hypothesis)


def _require_status(record: dict[str, Any], allowed: set[str], action: str) -> None:
    if record["status"] not in allowed:
        raise evidence.EvidenceError(
            f"{record['id']} is {record['status']}; {action} needs {sorted(allowed)}"
        )


def _active_loops(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        loop for loop in state["loops"].values() if loop["status"] in ACTIVE_LOOP_STATUSES
    ]


def _on_loop_captured(state: dict[str, Any], payload: dict[str, Any]) -> None:
    loop = evidence.validate_loop(
        _payload(payload, frozenset({"loop"}))["loop"], _active_loops(state)
    )
    if loop["id"] in state["loops"]:
        raise evidence.EvidenceError(f"loop already exists: {loop['id']}")
    state["loops"][loop["id"]] = {
        **loop,
        "status": "captured",
        "priority": None,
        "priority_total": None,
        "hypothesis_ids": [],
        "untrusted_flags": evidence.untrusted_flags(loop["provenance"]),
    }


def _on_loop_ranked(state: dict[str, Any], payload: dict[str, Any]) -> None:
    value = _payload(payload, frozenset({"loop_id", "priority", "rationale"}))
    loop = _loop(state, value.get("loop_id"))
    _require_status(loop, {"captured", "ranked"}, "ranking")
    scores = evidence.validate_priority(value.get("priority"))
    evidence._text(value.get("rationale"), "rationale")
    loop.update(
        status="ranked", priority=scores, priority_total=evidence.priority_total(scores)
    )


def _on_loop_promoted(state: dict[str, Any], payload: dict[str, Any]) -> None:
    value = _payload(payload, frozenset({"loop_id", "reason"}))
    loop = _loop(state, value.get("loop_id"))
    _require_status(loop, {"ranked"}, "promotion")
    evidence._text(value.get("reason"), "reason")
    loop["status"] = "promoted"


def _on_loop_archived(state: dict[str, Any], payload: dict[str, Any]) -> None:
    value = _payload(payload, frozenset({"loop_id", "reason"}))
    loop = _loop(state, value.get("loop_id"))
    _require_status(loop, set(ACTIVE_LOOP_STATUSES), "archiving")
    evidence._text(value.get("reason"), "reason")
    loop["status"] = "archived"


def _attach_to_loop(state: dict[str, Any], hypothesis: dict[str, Any]) -> None:
    loop_id = hypothesis.get("source_loop_id")
    if loop_id is None:
        return
    loop = _loop(state, loop_id)
    redesign = hypothesis.get("supersedes") in loop["hypothesis_ids"]
    if not (loop["status"] == "promoted" or (loop["status"] == "hypothesis" and redesign)):
        raise evidence.EvidenceError(
            f"{loop_id} must be promoted before it becomes a hypothesis"
        )
    loop["status"] = "hypothesis"
    loop["hypothesis_ids"].append(hypothesis["id"])


def _on_hypothesis_created(state: dict[str, Any], payload: dict[str, Any]) -> None:
    hypothesis = evidence.validate_hypothesis(
        _payload(payload, frozenset({"hypothesis"}))["hypothesis"]
    )
    if hypothesis["id"] in state["hypotheses"]:
        raise evidence.EvidenceError(f"hypothesis already exists: {hypothesis['id']}")
    previous_id = hypothesis.get("supersedes")
    if previous_id is not None:
        previous = _hypothesis(state, previous_id)
        _require_status(previous, {"proposed", "approved"}, "redesign")
        previous["status"] = "superseded"
        previous["superseded_by"] = hypothesis["id"]
    _attach_to_loop(state, hypothesis)
    state["hypotheses"][hypothesis["id"]] = {
        **hypothesis,
        "status": "proposed",
        "bar_sha256": evidence.bar_digest(hypothesis["precommitted_bar"]),
        "approved_by": None,
        "approver_ref": None,
        "validation_ids": [],
    }


def _on_hypothesis_approved(state: dict[str, Any], payload: dict[str, Any]) -> None:
    value = _payload(
        payload, frozenset({"hypothesis_id", "approved_by", "approver_ref", "bar_sha256"})
    )
    hypothesis = _hypothesis(state, value.get("hypothesis_id"))
    _require_status(hypothesis, {"proposed"}, "approval")
    if value.get("approved_by") != "human":
        raise evidence.EvidenceError("only a human can approve a hypothesis")
    approver = evidence._text(value.get("approver_ref"), "approver_ref")
    if not evidence.GUEST_REF_RE.fullmatch(approver):
        raise evidence.EvidenceError("approver_ref must be a slug, not a real name")
    if value.get("bar_sha256") != hypothesis["bar_sha256"]:
        raise evidence.EvidenceError("approval must confirm the exact precommitted bar")
    hypothesis.update(status="approved", approved_by="human", approver_ref=approver)


def _check_revalidation(
    state: dict[str, Any], hypothesis: dict[str, Any], record: dict[str, Any]
) -> None:
    previous_id = record.get("revalidates")
    if hypothesis["status"] == "approved" and previous_id is None:
        return
    if hypothesis["status"] != "resolved" or previous_id is None:
        raise evidence.EvidenceError(
            f"{hypothesis['id']} must be approved (or resolved and stale) to validate"
        )
    previous = state["validations"].get(previous_id)
    if previous is None or previous["hypothesis_id"] != hypothesis["id"]:
        raise evidence.EvidenceError("revalidates must name this hypothesis' validation")
    if previous["current_state"] != "stale":
        raise evidence.EvidenceError("only a stale validation can be revalidated")


def _on_validation_recorded(state: dict[str, Any], payload: dict[str, Any]) -> None:
    record = evidence.validate_validation(
        _payload(payload, frozenset({"validation"}))["validation"]
    )
    if record["id"] in state["validations"]:
        raise evidence.EvidenceError(f"validation already exists: {record['id']}")
    hypothesis = _hypothesis(state, record["hypothesis_id"])
    _check_revalidation(state, hypothesis, record)
    if record["bar_sha256"] != hypothesis["bar_sha256"]:
        raise evidence.EvidenceError(
            "evidence bar changed after commitment; record a redesign first"
        )
    linked = hypothesis.get("experiment_id")
    if linked and record.get("experiment_id") not in (None, linked):
        raise evidence.EvidenceError("experiment_id does not match the hypothesis")
    evidence.check_transition("hypothesis", record["state"])
    state["validations"][record["id"]] = {**record, "current_state": record["state"]}
    hypothesis["status"] = "resolved"
    hypothesis["validation_ids"].append(record["id"])
    loop_id = hypothesis.get("source_loop_id")
    if loop_id is not None:
        _loop(state, loop_id)["status"] = "closed"


def _on_validation_expired(state: dict[str, Any], payload: dict[str, Any]) -> None:
    value = _payload(payload, frozenset({"validation_id", "reason"}))
    record = state["validations"].get(value.get("validation_id"))
    if record is None:
        raise evidence.EvidenceError(f"unknown validation: {value.get('validation_id')}")
    evidence._text(value.get("reason"), "reason")
    evidence.check_transition(record["current_state"], "stale")
    record["current_state"] = "stale"


REDUCERS: dict[str, Callable[[dict[str, Any], dict[str, Any]], None]] = {
    "loop_captured": _on_loop_captured,
    "loop_ranked": _on_loop_ranked,
    "loop_promoted": _on_loop_promoted,
    "loop_archived": _on_loop_archived,
    "hypothesis_created": _on_hypothesis_created,
    "hypothesis_approved": _on_hypothesis_approved,
    "validation_recorded": _on_validation_recorded,
    "validation_expired": _on_validation_expired,
}
EVENT_TYPES = tuple(REDUCERS)


def apply_event(state: dict[str, Any], event_type: str, payload: Any) -> dict[str, Any]:
    """Return the next state, or raise EvidenceError without touching `state`."""

    reducer = REDUCERS.get(event_type)
    if reducer is None:
        raise evidence.EvidenceError(f"unknown evidence event type: {event_type}")
    if agent_graph._contains_secret_like(payload):
        raise evidence.EvidenceError("payload contains secret-like content")
    next_state = cast(dict[str, Any], _deep_copy(state))
    reducer(next_state, cast(dict[str, Any], _deep_copy(payload)))
    return next_state


def _deep_copy(value: Any) -> Any:
    return json.loads(agent_graph.canonical_bytes(value))


# --- Ledger load, verify and append -------------------------------------------------


def _check_envelope(event: dict[str, Any], path: Path, sequence: int, prev: Any) -> None:
    match = EVENT_FILE_RE.fullmatch(path.name)
    if match is None or int(match.group("sequence")) != sequence:
        raise GraphError("evidence event sequence is missing or out of order", 4)
    if event.get("sequence") != sequence or event.get("type") != match.group("type"):
        raise GraphError("evidence event does not match its filename", 4)
    if event.get("event_id") != match.group("event_id"):
        raise GraphError("evidence event id does not match its filename", 4)
    if event.get("previous_event_sha256") != prev:
        raise GraphError("evidence hash chain is broken", 4)
    if event.get("event_sha256") != agent_graph._event_hash(event):
        raise GraphError("evidence event hash is invalid", 4)


def load_ledger(paths: LedgerPaths) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Replay and verify every event; any tampering is an integrity error."""

    state = empty_state()
    events: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    for sequence, path in enumerate(_event_files(paths), start=1):
        event = agent_graph._read_json(path)
        _check_envelope(event, path, sequence, state["last_event_sha256"])
        key = event.get("idempotency_key_sha256")
        if not isinstance(key, str) or key in seen_keys:
            raise GraphError("evidence idempotency key is duplicated or malformed", 4)
        seen_keys.add(key)
        try:
            state = apply_event(state, str(event["type"]), event.get("payload"))
        except evidence.EvidenceError as exc:
            raise GraphError(f"evidence ledger replay failed: {exc}", 4) from exc
        state["last_sequence"] = sequence
        state["last_event_sha256"] = event["event_sha256"]
        events.append(event)
    return events, state


def _make_event(
    state: dict[str, Any], event_type: str, payload: Any, key: str, request_sha: str
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "sequence": state["last_sequence"] + 1,
        "event_id": agent_graph._event_id(),
        "type": event_type,
        "occurred_at": agent_graph._utc_now(),
        "idempotency_key_sha256": agent_graph._digest_text(key),
        "request_sha256": request_sha,
        "previous_event_sha256": state["last_event_sha256"],
        "payload": payload,
    }
    event["event_sha256"] = agent_graph._event_hash(event)
    return event


def _replay(events: list[dict[str, Any]], key: str, request_sha: str) -> dict[str, Any] | None:
    key_sha = agent_graph._digest_text(key)
    for event in events:
        if event["idempotency_key_sha256"] == key_sha:
            if event["request_sha256"] != request_sha:
                raise GraphError("idempotency key conflict", 4)
            return event
    return None


def append_event(
    target: Path, event_type: str, payload: Any, idempotency_key: str
) -> dict[str, Any]:
    """Validate, append and project one event.  Identical retries replay."""

    if not idempotency_key or len(idempotency_key) > 256:
        raise GraphError("idempotency key is required (max 256 characters)", 2)
    paths = ledger_paths(target)
    request_sha = agent_graph._request_sha({"type": event_type, "payload": payload})
    with agent_graph.directory_lock(paths.lock_root, LOCK_NAME):
        _reject_redirected_paths(paths)
        events, state = load_ledger(paths)
        replayed = _replay(events, idempotency_key, request_sha)
        if replayed is not None:
            return {"exit_code": 0, "replayed": True, "event": replayed}
        try:
            next_state = apply_event(state, event_type, payload)
        except evidence.EvidenceError as exc:
            raise GraphError(str(exc), 2) from exc
        event = _make_event(state, event_type, payload, idempotency_key, request_sha)
        name = f"{event['sequence']:06d}-{event_type}-{event['event_id']}.json"
        if (paths.events / name).exists():
            raise GraphError("evidence event filename already exists", 4)
        agent_graph._atomic_write(paths.events / name, agent_graph.canonical_bytes(event) + b"\n")
        next_state.update(last_sequence=event["sequence"], last_event_sha256=event["event_sha256"])
        _write_views(paths, next_state)
    return {"exit_code": 0, "replayed": False, "event": event}


# --- Views ----------------------------------------------------------------------


def render_views(state: dict[str, Any]) -> dict[str, bytes]:
    """Deterministic projections; JSON text is also valid YAML 1.2."""

    def ordered(records: dict[str, Any]) -> list[Any]:
        return [records[key] for key in sorted(records)]

    loops = ordered(state["loops"])
    active = [loop for loop in loops if loop["status"] in ACTIVE_LOOP_STATUSES]
    active.sort(key=lambda loop: (-(loop["priority_total"] or 0), loop["id"]))
    common = {
        "version": LEDGER_SCHEMA_VERSION,
        "generated_from": EVENTS_RELATIVE.as_posix(),
        "last_sequence": state["last_sequence"],
        "last_event_sha256": state["last_event_sha256"],
    }
    views = {
        "open-loops": {
            **common,
            "open_loops": active,
            "closed_loops": [l for l in loops if l["status"] not in ACTIVE_LOOP_STATUSES],
        },
        "hypotheses": {**common, "hypotheses": ordered(state["hypotheses"])},
        "validations": {**common, "validations": ordered(state["validations"])},
    }
    return {
        name: agent_graph.canonical_bytes(value) + b"\n" for name, value in views.items()
    }


def _write_views(paths: LedgerPaths, state: dict[str, Any]) -> dict[str, Path]:
    written: dict[str, Path] = {}
    for name, data in render_views(state).items():
        path = paths.views / f"{name}.yaml"
        agent_graph._atomic_write(path, data)
        written[name] = path
    return written


def rebuild_views(target: Path) -> dict[str, Path]:
    """Recreate every view from the ledger alone."""

    paths = ledger_paths(target)
    with agent_graph.directory_lock(paths.lock_root, LOCK_NAME):
        _reject_redirected_paths(paths)
        _events, state = load_ledger(paths)
        return _write_views(paths, state)


def verify(target: Path) -> dict[str, Any]:
    """Verify the hash chain and report whether views match a fresh replay."""

    paths = ledger_paths(target)
    events, state = load_ledger(paths)
    stale_views = []
    for name, data in render_views(state).items():
        path = paths.views / f"{name}.yaml"
        if not path.is_file() or path.read_bytes() != data:
            stale_views.append(name)
    return {
        "exit_code": 0,
        "events": len(events),
        "last_event_sha256": state["last_event_sha256"],
        "views_match": not stale_views,
        "stale_views": stale_views,
    }


# --- Dry-run gate check for skills ---------------------------------------------------

CHECKERS: dict[str, Callable[[Any], Any]] = {
    "provenance": evidence.validate_provenance,
    "hypothesis": evidence.validate_hypothesis,
    "validation": evidence.validate_validation,
    "freshness": evidence.validate_freshness,
}


def check(kind: str, value: Any, target: Path | None = None) -> dict[str, Any]:
    """Validate a record without writing.  Loops also run the duplicate gate."""

    try:
        if kind == "loop":
            active = _active_loops(load_ledger(ledger_paths(target))[1]) if target else []
            evidence.validate_loop(value, active)
        elif kind in CHECKERS:
            CHECKERS[kind](value)
        else:
            raise evidence.EvidenceError(f"unknown record kind: {kind}")
    except evidence.EvidenceError as exc:
        return {"exit_code": 2, "ok": False, "error": str(exc)}
    if kind == "hypothesis":
        # The digest a human approval and every validation must repeat.
        return {"exit_code": 0, "ok": True, "bar_sha256": evidence.bar_digest(value["precommitted_bar"])}
    return {"exit_code": 0, "ok": True}
