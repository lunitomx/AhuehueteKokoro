#!/usr/bin/env python3
"""Freshness graph: which knowledge is current, expired or stale by dependency.

Nodes are living artifacts (Forces, message, landing, finance...) registered
with `context_refreshed`, plus recorded validations.  Edges come from each
node's `freshness.depends_on`.  A node is:

- `stale`: someone marked it stale, or (validations) it was expired;
- `stale_by_dependency`: a direct upstream changed materially after this node
  was last verified;
- `potentially_stale`: a direct upstream is itself stale in any way;
- `superseded`: a newer artifact replaced it;
- `current`: none of the above.

Calendar expiry (`refresh_by`) is separate because it depends on today's date;
views stay deterministic and reports take `today` as an argument.  Nothing here
refreshes anything: the graph only says what should be reviewed.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Any, cast

import evidence
from evidence import EvidenceError, GateResult

ARTIFACT_FIELDS = frozenset(
    {"id", "guest", "kind", "title", "source_ref", "freshness", "supersedes"}
)
KIND_RE = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
NODE_STATUSES = ("current", "potentially_stale", "stale_by_dependency", "stale", "superseded")
# What a recommendation may do with a node in each status.
GATE_USES = ("explore", "decide")
BLOCKING_STATUSES = frozenset({"stale", "stale_by_dependency", "superseded"})


# --- Contracts ----------------------------------------------------------------


def validate_artifact(raw: Any) -> dict[str, Any]:
    artifact = evidence._object(raw, "artifact")
    evidence._no_unknown(artifact, ARTIFACT_FIELDS, "artifact")
    evidence._identifier(artifact.get("id"), "dependency", "artifact.id")
    guest = evidence._text(artifact.get("guest"), "artifact.guest")
    if not evidence.GUEST_REF_RE.fullmatch(guest):
        raise EvidenceError("artifact.guest must be a slug such as cliente_01")
    if not KIND_RE.fullmatch(evidence._text(artifact.get("kind"), "artifact.kind")):
        raise EvidenceError("artifact.kind must be a short slug such as forces or landing")
    evidence._text(artifact.get("title"), "artifact.title")
    ref = evidence._text(artifact.get("source_ref"), "artifact.source_ref")
    if ref.startswith(("/", "~")) or re.match(r"^[A-Za-z]:\\", ref):
        raise EvidenceError("artifact.source_ref must be relative to the workspace")
    evidence.validate_freshness(artifact.get("freshness"))
    if artifact.get("supersedes") is not None:
        evidence._identifier(artifact["supersedes"], "dependency", "artifact.supersedes")
        if artifact["supersedes"] == artifact["id"]:
            raise EvidenceError("an artifact cannot supersede itself")
    return artifact


# --- Graph --------------------------------------------------------------------


def nodes(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Every freshness-bearing record keyed by id, in one shape."""

    found: dict[str, dict[str, Any]] = {}
    for record in state["artifacts"].values():
        found[record["id"]] = {
            "id": record["id"],
            "node_type": "artifact",
            "guest": record["guest"],
            "kind": record["kind"],
            "title": record["title"],
            "freshness": record["freshness"],
            "verified_sequence": record["verified_sequence"],
            "changed_sequence": record["changed_sequence"],
            "own_status": record["status"],
        }
    for record in state["validations"].values():
        hypothesis = state["hypotheses"].get(record["hypothesis_id"], {})
        found[record["id"]] = {
            "id": record["id"],
            "node_type": "validation",
            "guest": hypothesis.get("guest"),
            "kind": "validation",
            "title": record["finding"],
            "freshness": record["freshness"],
            "verified_sequence": record["recorded_sequence"],
            "changed_sequence": record["changed_sequence"],
            "own_status": "stale" if record["current_state"] == "stale" else "current",
        }
    return found


def _depends_on(node: dict[str, Any]) -> list[str]:
    return list(node["freshness"].get("depends_on", []))


def check_dependencies(state: dict[str, Any], node_id: str, block: dict[str, Any]) -> None:
    """Refuse an edge set that would close a cycle through `node_id`."""

    graph = nodes(state)
    pending = list(block.get("depends_on", []))
    seen: set[str] = set()
    while pending:
        current = pending.pop()
        if current == node_id:
            raise EvidenceError(f"freshness dependencies form a cycle through {node_id}")
        if current in seen or current not in graph:
            continue
        seen.add(current)
        pending.extend(_depends_on(graph[current]))


def statuses(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Dependency status of every node.  Deterministic: no calendar here."""

    graph = nodes(state)
    result: dict[str, dict[str, Any]] = {}

    def resolve(node_id: str, visiting: frozenset[str]) -> str:
        if node_id in result:
            return cast(str, result[node_id]["status"])
        if node_id in visiting:
            raise EvidenceError(f"freshness dependencies form a cycle through {node_id}")
        node = graph[node_id]
        reasons: list[str] = []
        untracked: list[str] = []
        status = node["own_status"]
        if status in ("stale", "superseded"):
            reasons.append(f"{node_id} is {status}")
        for dep in _depends_on(node):
            upstream = graph.get(dep)
            if upstream is None:
                untracked.append(dep)
                continue
            upstream_status = resolve(dep, visiting | {node_id})
            if upstream["changed_sequence"] > node["verified_sequence"]:
                reasons.append(f"{dep} changed after {node_id} was last verified")
                if status not in ("stale", "superseded"):
                    status = "stale_by_dependency"
            elif upstream_status != "current":
                reasons.append(f"{dep} is {upstream_status}")
                if status == "current":
                    status = "potentially_stale"
        result[node_id] = {"status": status, "reasons": reasons, "untracked": untracked}
        return status

    for node_id in sorted(graph):
        resolve(node_id, frozenset())
    return result


def calendar_status(block: dict[str, Any], today: dt.date) -> dict[str, Any]:
    kind = evidence.freshness_status(block, today)
    due = block.get("refresh_by")
    days = None if due is None else (evidence._date(due, "refresh_by") - today).days
    return {"calendar": kind, "days_to_refresh": days}


RECOMMENDATIONS = {
    ("artifact", "stale"): "refresh",
    ("artifact", "stale_by_dependency"): "review_against_upstream",
    ("artifact", "potentially_stale"): "check_upstream_first",
    ("artifact", "superseded"): "repoint_dependents",
    ("artifact", "expired"): "refresh",
    ("validation", "stale"): "revalidate",
    ("validation", "stale_by_dependency"): "expire_then_revalidate",
    ("validation", "potentially_stale"): "check_upstream_first",
    ("validation", "expired"): "expire_then_revalidate",
}


def report(state: dict[str, Any], today: dt.date, guest: str | None = None) -> dict[str, Any]:
    """Steps 1-4 of /kokoro-refresh: read, detect, walk dependencies, recommend."""

    graph = nodes(state)
    by_status = statuses(state)
    attention: list[dict[str, Any]] = []
    for node_id in sorted(graph):
        node = graph[node_id]
        if guest is not None and node["guest"] != guest:
            continue
        calendar = calendar_status(node["freshness"], today)
        status = by_status[node_id]["status"]
        key = status if status != "current" else (
            "expired" if calendar["calendar"] == "expired" else None
        )
        if key is None:
            continue
        attention.append(
            {
                "id": node_id,
                "node_type": node["node_type"],
                "kind": node["kind"],
                "title": node["title"],
                "status": status,
                **calendar,
                "reasons": by_status[node_id]["reasons"],
                "recommendation": RECOMMENDATIONS[(node["node_type"], key)],
            }
        )
    order = {"stale": 0, "stale_by_dependency": 1, "superseded": 2, "potentially_stale": 3, "current": 4}
    attention.sort(key=lambda item: (order[item["status"]], item["id"]))
    return {
        "exit_code": 0,
        "today": today.isoformat(),
        "nodes": len([n for n in graph.values() if guest is None or n["guest"] == guest]),
        "needs_attention": attention,
        "mutates": False,
    }


def gate_context_fresh(
    state: dict[str, Any], ids: list[str], today: dt.date, use: str
) -> GateResult:
    """GATE-CONTEXT-FRESH for the persisted context a recommendation rests on.

    `explore`: anything not current is Partial (say so, keep going).
    `decide`: stale, stale by dependency, superseded, expired or unknown context
    is Blocked; potentially stale context is Partial.
    """

    evidence._choice(use, GATE_USES, "use")
    if not ids:
        return GateResult("GATE-CONTEXT-FRESH", "Skipped", ("no persisted context used",))
    graph = nodes(state)
    by_status = statuses(state)
    blocked: list[str] = []
    partial: list[str] = []
    for node_id in ids:
        if node_id not in graph:
            (blocked if use == "decide" else partial).append(f"{node_id}: no freshness metadata")
            continue
        status = by_status[node_id]["status"]
        calendar = calendar_status(graph[node_id]["freshness"], today)["calendar"]
        if status in BLOCKING_STATUSES or calendar == "expired":
            label = status if status != "current" else "expired"
            (blocked if use == "decide" else partial).append(f"{node_id}: {label}")
        elif status == "potentially_stale":
            partial.append(f"{node_id}: potentially_stale")
    if blocked:
        return GateResult("GATE-CONTEXT-FRESH", "Blocked", tuple(blocked + partial))
    if partial:
        return GateResult("GATE-CONTEXT-FRESH", "Partial", tuple(partial))
    return GateResult("GATE-CONTEXT-FRESH", "Pass")


# --- Reducers -------------------------------------------------------------------


def _on_context_refreshed(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = evidence._object(payload, "payload")
    evidence._no_unknown(value, frozenset({"artifact", "material_change", "summary"}), "payload")
    artifact = validate_artifact(value.get("artifact"))
    material = value.get("material_change")
    if not isinstance(material, bool):
        raise EvidenceError("material_change must be true or false")
    evidence._text(value.get("summary"), "summary")
    artifact_id = artifact["id"]
    if artifact_id in state["validations"]:
        raise EvidenceError(f"{artifact_id} is a validation; use /kokoro-revalidate")
    check_dependencies(state, artifact_id, artifact["freshness"])
    previous = state["artifacts"].get(artifact_id)
    block = artifact["freshness"]
    if previous is not None:
        if previous["status"] == "superseded":
            raise EvidenceError(f"{artifact_id} was superseded by {previous['superseded_by']}")
        if previous["guest"] != artifact["guest"]:
            raise EvidenceError("an artifact cannot move to another guest")
        if evidence._date(block["generated_on"], "generated_on") < evidence._date(
            previous["freshness"]["generated_on"], "generated_on"
        ):
            raise EvidenceError("generated_on cannot go back in time")
    if material and block.get("last_material_change") is None:
        block["last_material_change"] = block["generated_on"]
    record = {
        **artifact,
        "status": "current",
        "material_change": material,
        "last_summary": value["summary"],
        "verified_sequence": ctx["sequence"],
        # A first registration is not a change: nobody verified against it yet.
        "changed_sequence": (
            ctx["sequence"] if material and previous is not None
            else (previous or {}).get("changed_sequence", 0)
        ),
        "refresh_count": (previous or {}).get("refresh_count", 0) + 1,
        "material_refresh_count": (previous or {}).get("material_refresh_count", 0)
        + (1 if material and previous is not None else 0),
        "created_at": (previous or {}).get("created_at", ctx["occurred_at"]),
        "updated_at": ctx["occurred_at"],
    }
    old_id = artifact.get("supersedes")
    if old_id is not None:
        if previous is not None:
            raise EvidenceError("only a new artifact id can supersede another")
        old = state["artifacts"].get(old_id)
        if old is None or old["status"] == "superseded":
            raise EvidenceError(f"{old_id} is not a current artifact")
        if old["guest"] != artifact["guest"]:
            raise EvidenceError("an artifact can only supersede one of the same guest")
        old.update(
            status="superseded",
            superseded_by=artifact_id,
            changed_sequence=ctx["sequence"],
            updated_at=ctx["occurred_at"],
        )
    state["artifacts"][artifact_id] = record


def _on_context_marked_stale(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = evidence._object(payload, "payload")
    evidence._no_unknown(value, frozenset({"artifact_id", "reason", "trigger"}), "payload")
    artifact_id = value.get("artifact_id")
    record = state["artifacts"].get(artifact_id)
    if record is None:
        raise EvidenceError(f"unknown artifact: {artifact_id}")
    if record["status"] != "current":
        raise EvidenceError(f"{artifact_id} is already {record['status']}")
    evidence._text(value.get("reason"), "reason")
    trigger = evidence._text(value.get("trigger"), "trigger")
    if trigger != "manual" and trigger not in record["freshness"].get("invalidated_by", []):
        raise EvidenceError("trigger must be 'manual' or one of the artifact's invalidated_by events")
    record.update(
        status="stale",
        stale_reason=value["reason"],
        stale_trigger=trigger,
        changed_sequence=ctx["sequence"],
        updated_at=ctx["occurred_at"],
    )


REDUCERS = {
    "context_refreshed": _on_context_refreshed,
    "context_marked_stale": _on_context_marked_stale,
}


def empty_state() -> dict[str, Any]:
    return {"artifacts": {}}


def render(state: dict[str, Any]) -> dict[str, Any]:
    by_status = statuses(state)
    graph = nodes(state)
    dependents: dict[str, list[str]] = {node_id: [] for node_id in graph}
    for node_id, node in graph.items():
        for dep in _depends_on(node):
            dependents.setdefault(dep, []).append(node_id)
    return {
        "freshness": {
            "nodes": [
                {
                    "id": node_id,
                    "node_type": graph[node_id]["node_type"],
                    "guest": graph[node_id]["guest"],
                    "kind": graph[node_id]["kind"],
                    "title": graph[node_id]["title"],
                    **graph[node_id]["freshness"],
                    "status": by_status[node_id]["status"],
                    "reasons": by_status[node_id]["reasons"],
                    "untracked_dependencies": by_status[node_id]["untracked"],
                    "dependents": sorted(dependents.get(node_id, [])),
                }
                for node_id in sorted(graph)
            ]
        }
    }
