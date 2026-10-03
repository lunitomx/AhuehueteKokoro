#!/usr/bin/env python3
"""Learning traces: corrections and lessons that stay local until a human
promotes them.

A single correction changes one output, not the method.  Team, skill and
system scope need an explicit rule from the person; skill and system scope
come only from user feedback.  Promotion is a human event with a declared
basis.  Applying a promoted trace needs a reviewed change reference: this
module never edits a skill, a prompt or a rule file.
"""

from __future__ import annotations

import re
from typing import Any, cast

import evidence
from evidence import EvidenceError

TRACE_SCOPES = ("output", "guest", "team", "skill", "system")
WIDE_SCOPES = frozenset({"team", "skill", "system"})
METHOD_SCOPES = frozenset({"skill", "system"})
FEEDBACK_SOURCES = ("user", "guest_result", "performance", "review", "kokoro_reflection")
TRACE_STATUSES = ("captured", "promoted", "rejected", "applied", "superseded")
PROMOTION_BASES = ("explicit_rule", "repetition", "performance", "confirmed")
# Three consistent traces is the smallest repetition that is not a coincidence.
MIN_REPETITION = 3
TRACE_FIELDS = frozenset(
    {
        "id",
        "guest",
        "scope",
        "feedback_source",
        "observation",
        "correction",
        "explicit_rule",
        "skill_ref",
        "evidence_refs",
        "supersedes",
        "privacy_class",
        "origin",
    }
)
TRACE_ID = re.compile(r"^TRACE-[0-9A-Za-z_-]{1,64}$")


def _trace_id(value: Any, name: str) -> str:
    text = evidence._text(value, name)
    if not TRACE_ID.fullmatch(text):
        raise EvidenceError(f"{name} is not a valid trace id")
    return text


def validate_trace(raw: Any) -> dict[str, Any]:
    trace = evidence._object(raw, "trace")
    evidence._no_unknown(trace, TRACE_FIELDS, "trace")
    _trace_id(trace.get("id"), "trace.id")
    scope = evidence._choice(trace.get("scope"), TRACE_SCOPES, "scope")
    source = evidence._choice(trace.get("feedback_source"), FEEDBACK_SOURCES, "feedback_source")
    guest = trace.get("guest")
    if scope in ("output", "guest"):
        guest = evidence._text(guest, "guest")
    if guest is not None and not evidence.GUEST_REF_RE.fullmatch(str(guest)):
        raise EvidenceError("guest must be a slug such as cliente_01, never a real name")
    evidence._text(trace.get("observation"), "observation")
    evidence._optional_text(trace.get("correction"), "correction")
    rule = evidence._optional_text(trace.get("explicit_rule"), "explicit_rule")
    if scope in WIDE_SCOPES and not rule:
        raise EvidenceError(
            f"scope {scope} needs an explicit_rule from the person; one correction stays local"
        )
    if scope in METHOD_SCOPES and source != "user":
        raise EvidenceError(f"scope {scope} can only come from user feedback")
    if scope in METHOD_SCOPES:
        skill = evidence._text(trace.get("skill_ref"), "skill_ref")
        if not evidence.SKILL_RE.fullmatch(skill):
            raise EvidenceError("skill_ref must look like /kokoro-name")
    evidence._text_list(trace.get("evidence_refs", []), "evidence_refs")
    if trace.get("supersedes") is not None:
        _trace_id(trace["supersedes"], "supersedes")
    privacy = evidence._choice(trace.get("privacy_class"), evidence.PRIVACY_CLASSES, "privacy_class")
    if privacy not in evidence.SHAREABLE_PRIVACY_CLASSES:
        raise EvidenceError(f"privacy_class {privacy} cannot enter shared learning")
    if "origin" in trace:
        evidence.validate_origin(trace["origin"])
    if evidence.instruction_like(" ".join(str(trace.get(k) or "") for k in ("observation", "correction", "explicit_rule"))) and source != "user":
        raise EvidenceError("instruction-like text from a non-user source cannot become a trace")
    if evidence.agent_graph._contains_secret_like(trace):
        raise EvidenceError("trace contains secret-like content")
    return trace


def _fields(payload: Any, allowed: set[str]) -> dict[str, Any]:
    value = evidence._object(payload, "payload")
    evidence._no_unknown(value, frozenset(allowed), "payload")
    return value


def _trace(state: dict[str, Any], trace_id: Any) -> dict[str, Any]:
    record = state["traces"].get(trace_id)
    if record is None:
        raise EvidenceError(f"unknown trace: {trace_id}")
    return cast(dict[str, Any], record)


def _on_trace_captured(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    trace = validate_trace(_fields(payload, {"trace"}).get("trace"))
    if trace["id"] in state["traces"]:
        raise EvidenceError(f"trace already exists: {trace['id']}")
    old_id = trace.get("supersedes")
    if old_id is not None:
        old = _trace(state, old_id)
        if old["status"] == "superseded":
            raise EvidenceError(f"{old_id} is already superseded")
        old.update(status="superseded", superseded_by=trace["id"], updated_at=ctx["occurred_at"])
    state["traces"][trace["id"]] = {
        **trace,
        "status": "captured",
        "created_at": ctx["occurred_at"],
        "updated_at": ctx["occurred_at"],
    }


def _check_basis(state: dict[str, Any], record: dict[str, Any], value: dict[str, Any]) -> dict[str, Any]:
    basis = evidence._choice(value.get("basis"), PROMOTION_BASES, "basis")
    refs = evidence._text_list(value.get("basis_refs", []), "basis_refs")
    if basis == "explicit_rule" and not record.get("explicit_rule"):
        raise EvidenceError("basis explicit_rule needs a trace that carries one")
    if basis == "repetition":
        if len(set(refs)) < MIN_REPETITION - 1:
            raise EvidenceError(f"repetition needs {MIN_REPETITION} consistent traces in total")
        for ref in refs:
            other = _trace(state, ref)
            if other["id"] == record["id"] or other["status"] in ("rejected", "superseded"):
                raise EvidenceError(f"{ref} cannot count as a repetition")
    if basis == "performance":
        if len(refs) != 1 or refs[0] not in state["validations"]:
            raise EvidenceError("basis performance needs one recorded validation id")
        if state["validations"][refs[0]]["current_state"] != "validated":
            raise EvidenceError("basis performance needs a validated validation")
    return {"basis": basis, "basis_refs": refs}


def _on_trace_promoted(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"trace_id", "promoted_by", "approver_ref", "to_scope", "basis", "basis_refs", "reason"})
    record = _trace(state, value.get("trace_id"))
    if value.get("promoted_by") != "human":
        raise EvidenceError("only a human can promote a learning trace")
    approver = evidence._text(value.get("approver_ref"), "approver_ref")
    if not evidence.GUEST_REF_RE.fullmatch(approver):
        raise EvidenceError("approver_ref must be a slug, not a real name")
    if record["status"] != "captured":
        raise EvidenceError(f"{record['id']} is {record['status']}; only captured traces can be promoted")
    to_scope = evidence._choice(value.get("to_scope"), TRACE_SCOPES, "to_scope")
    if TRACE_SCOPES.index(to_scope) < TRACE_SCOPES.index(record["scope"]):
        raise EvidenceError("promotion cannot narrow a trace's scope")
    if to_scope in WIDE_SCOPES and not record.get("explicit_rule"):
        raise EvidenceError(f"scope {to_scope} needs an explicit_rule on the trace")
    if to_scope in METHOD_SCOPES and record["feedback_source"] != "user":
        raise EvidenceError(f"scope {to_scope} can only come from user feedback")
    if to_scope in METHOD_SCOPES and not record.get("skill_ref"):
        raise EvidenceError(f"scope {to_scope} needs a skill_ref on the trace")
    basis = _check_basis(state, record, value)
    evidence._text(value.get("reason"), "reason")
    record.update(
        status="promoted",
        promoted_scope=to_scope,
        promotion={**basis, "approver_ref": approver, "reason": value["reason"]},
        updated_at=ctx["occurred_at"],
    )


def _on_trace_rejected(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"trace_id", "reason"})
    record = _trace(state, value.get("trace_id"))
    evidence._text(value.get("reason"), "reason")
    if record["status"] not in ("captured", "promoted"):
        raise EvidenceError(f"{record['id']} is {record['status']}; it cannot be rejected")
    record.update(status="rejected", reject_reason=value["reason"], updated_at=ctx["occurred_at"])


def _on_trace_applied(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    """Record that a reviewed change carried the lesson.  Nothing is edited here."""

    value = _fields(payload, {"trace_id", "change_ref", "reviewed_by"})
    record = _trace(state, value.get("trace_id"))
    if record["status"] != "promoted":
        raise EvidenceError("only a promoted trace can be applied")
    change = evidence._text(value.get("change_ref"), "change_ref")
    if change.startswith(("/", "~")):
        raise EvidenceError("change_ref must be a commit, PR or relative path, not a local path")
    if value.get("reviewed_by") != "human":
        raise EvidenceError("a learning change must be reviewed by a human")
    record.update(status="applied", change_ref=change, updated_at=ctx["occurred_at"])


REDUCERS = {
    "learning_trace_captured": _on_trace_captured,
    "learning_trace_promoted": _on_trace_promoted,
    "learning_trace_rejected": _on_trace_rejected,
    "learning_trace_applied": _on_trace_applied,
}


def empty_state() -> dict[str, Any]:
    return {"traces": {}}


def render(state: dict[str, Any]) -> dict[str, Any]:
    traces = [state["traces"][key] for key in sorted(state["traces"])]
    return {
        "learning": {
            "pending_traces": [t for t in traces if t["status"] == "captured"],
            "promoted_traces": [t for t in traces if t["status"] == "promoted"],
            "applied_traces": [t for t in traces if t["status"] == "applied"],
            "closed_traces": [t for t in traces if t["status"] in ("rejected", "superseded")],
        }
    }
