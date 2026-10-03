#!/usr/bin/env python3
"""Creative iteration: change on purpose, read the signal honestly.

Three pieces:

* GATE-PERFORMANCE-SIGNAL reads results against the account's own declared
  baseline.  There are no universal thresholds: a minimum spend share or a
  minimum number of results means nothing until the account declares it.
  Downstream funnel quality outweighs cost per lead, and outcomes that have
  not matured yet give Partial, never a winner.
* The Iteration Brief names which families change and which must be
  preserved.  Signal Distance says how far the variant moved from its base:
  only levels 1-2 isolate a variable well enough to count as a controlled
  test.
* The Creative Learning Record mirrors the linked validation.  It cannot
  claim validated or invalidated without one, nor from an uncontrolled test.
"""

from __future__ import annotations

import datetime as dt
import math
import re
from typing import Any, cast

import evidence
from evidence import EvidenceError, GateResult

# B2B order: each stage is downstream of the ones before it.
FUNNEL_STAGES = (
    "impression",
    "click",
    "lead",
    "contacted",
    "qualified",
    "appointment",
    "show",
    "proposal",
    "sale",
    "collected",
)
ITERATION_FAMILIES = (
    "hook",
    "headline",
    "body_copy",
    "offer",
    "cta",
    "proof",
    "angle",
    "persona",
    "visual_subject",
    "visual_style",
    "format",
    "length",
    "audio",
    "placement",
    "audience",
    "landing",
)
CHANGE_SCOPES = ("element", "concept")
SIGNAL_LEVELS = {
    1: "one family, one element: clean read",
    2: "one family: controlled read",
    3: "two families: directional only",
    4: "three or more families or a new core idea: a new creative, not an iteration",
}
CONTROLLED_LEVELS = frozenset({1, 2})
REVIEW_DECISIONS = ("approved", "rejected", "needs_changes")
LEARNING_STATES = ("observed", "inferred", *evidence.RESOLUTION_STATES)
CLAIMING_STATES = frozenset({"validated", "invalidated"})
ITER_ID = re.compile(r"^ITER-[0-9A-Za-z_-]{1,64}$")
LEARN_ID = re.compile(r"^CLR-[0-9A-Za-z_-]{1,64}$")


def _pattern_id(value: Any, pattern: re.Pattern[str], name: str) -> str:
    text = evidence._text(value, name)
    if not pattern.fullmatch(text):
        raise EvidenceError(f"{name} is not a valid id")
    return text


def _number(value: Any, name: str, *, minimum: float = 0.0, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise EvidenceError(f"{name} must be a number")
    if value < minimum or (maximum is not None and value > maximum):
        raise EvidenceError(f"{name} is out of range")
    return float(value)


# --- GATE-PERFORMANCE-SIGNAL ------------------------------------------------

BASELINE_FIELDS = frozenset(
    {"source_ref", "min_spend_share", "min_results", "result_stage", "fatigue_frequency", "outcome_lag_days"}
)
VARIANT_FIELDS = frozenset({"id", "spend", "spend_share", "frequency", "funnel", "margin"})
SIGNAL_FIELDS = frozenset({"baseline", "variants", "window_end", "as_of"})


def validate_baseline(raw: Any) -> dict[str, Any]:
    base = evidence._object(raw, "baseline")
    evidence._no_unknown(base, BASELINE_FIELDS, "baseline")
    evidence._text(base.get("source_ref"), "baseline.source_ref")
    _number(base.get("min_spend_share"), "baseline.min_spend_share", maximum=1.0)
    _number(base.get("min_results"), "baseline.min_results", minimum=1.0)
    evidence._choice(base.get("result_stage"), FUNNEL_STAGES, "baseline.result_stage")
    if base.get("fatigue_frequency") is not None:
        _number(base["fatigue_frequency"], "baseline.fatigue_frequency", minimum=1.0)
    if base.get("outcome_lag_days") is not None:
        _number(base["outcome_lag_days"], "baseline.outcome_lag_days")
    return base


def _validate_variant(raw: Any) -> dict[str, Any]:
    variant = evidence._object(raw, "variant")
    evidence._no_unknown(variant, VARIANT_FIELDS, "variant")
    evidence._text(variant.get("id"), "variant.id")
    _number(variant.get("spend"), "variant.spend")
    _number(variant.get("spend_share"), "variant.spend_share", maximum=1.0)
    if variant.get("frequency") is not None:
        _number(variant["frequency"], "variant.frequency")
    funnel = evidence._object(variant.get("funnel"), "variant.funnel")
    evidence._no_unknown(funnel, frozenset(FUNNEL_STAGES), "variant.funnel")
    previous = math.inf
    for stage in FUNNEL_STAGES:
        if stage in funnel:
            count = _number(funnel[stage], f"funnel.{stage}")
            if count > previous:
                raise EvidenceError(f"funnel.{stage} cannot exceed an upstream stage")
            previous = count
    if variant.get("margin") is not None:
        _number(variant["margin"], "variant.margin", minimum=-math.inf)
    return variant


def _cost(variant: dict[str, Any], stage: str) -> float:
    count = variant["funnel"].get(stage, 0)
    return variant["spend"] / count if count else math.inf


def read_signal(raw: Any) -> dict[str, Any]:
    """Read a test result without deciding anything.  Returns the gate result,
    the cost-per-lead leader and the downstream leader with the stage used."""

    signal = evidence._object(raw, "signal")
    evidence._no_unknown(signal, SIGNAL_FIELDS, "signal")
    if signal.get("baseline") is None:
        gate = GateResult(
            "GATE-PERFORMANCE-SIGNAL",
            "Blocked",
            ("declare this account's baseline first; Kokoro has no universal thresholds",),
        )
        return {"gate": gate.as_dict(), "cpl_leader": None, "downstream_leader": None, "decisive_stage": None}
    base = validate_baseline(signal["baseline"])
    variants = [_validate_variant(v) for v in evidence._list(signal.get("variants"), "variants")]
    if not variants:
        raise EvidenceError("variants requires at least one variant")
    if len({v["id"] for v in variants}) != len(variants):
        raise EvidenceError("variant ids must be unique")

    blocked: list[str] = []
    partial: list[str] = []
    for variant in variants:
        if variant["spend_share"] < base["min_spend_share"]:
            blocked.append(f"{variant['id']}: spend share below the account baseline")
        if variant["funnel"].get(base["result_stage"], 0) < base["min_results"]:
            blocked.append(f"{variant['id']}: fewer {base['result_stage']} results than the baseline minimum")
        fatigue = base.get("fatigue_frequency")
        if fatigue is not None and variant.get("frequency") is not None and variant["frequency"] > fatigue:
            partial.append(f"{variant['id']}: frequency above the fatigue line; results may be fatigue")
    lag = base.get("outcome_lag_days")
    if lag:
        window_end = evidence._date(signal.get("window_end"), "window_end")
        as_of = evidence._date(signal.get("as_of"), "as_of")
        if (as_of - window_end) < dt.timedelta(days=lag):
            partial.append("downstream outcomes have not matured; read again after the lag")

    cpl_leader = min(variants, key=lambda v: (_cost(v, "lead"), v["id"]))["id"] if all("lead" in v["funnel"] for v in variants) else None
    decisive = None
    for stage in reversed(FUNNEL_STAGES[FUNNEL_STAGES.index("lead") :]):
        if all(stage in v["funnel"] for v in variants):
            decisive = stage
            break
    if all(v.get("margin") is not None for v in variants):
        leader = max(variants, key=lambda v: (v["margin"], v["id"]))["id"]
        decisive = "margin"
    elif decisive is not None:
        leader = min(variants, key=lambda v: (_cost(v, decisive), v["id"]))["id"]
    else:
        leader = None
    if cpl_leader and leader and cpl_leader != leader and decisive != "lead":
        partial.append(f"{cpl_leader} has the lowest cost per lead but {leader} wins at {decisive}; downstream wins")

    status = "Blocked" if blocked else "Partial" if partial else "Pass"
    gate = GateResult("GATE-PERFORMANCE-SIGNAL", status, tuple(blocked + partial))
    return {
        "gate": gate.as_dict(),
        "cpl_leader": cpl_leader,
        "downstream_leader": leader if not blocked else None,
        "decisive_stage": decisive,
    }


def gate_performance_signal(raw: Any) -> GateResult:
    result = read_signal(raw)["gate"]
    return GateResult(result["gate"], result["status"], tuple(result["reasons"]))


# --- Iteration Brief and Signal Distance ------------------------------------

CHANGE_FIELDS = frozenset({"family", "scope", "description"})
ITERATION_FIELDS = frozenset(
    {
        "id",
        "guest",
        "base_creative_ref",
        "hypothesis_id",
        "changes",
        "preserve",
        "core_idea_changed",
        "learning_goal",
        "success_metric",
        "privacy_class",
        "origin",
    }
)


def signal_distance(changes: list[dict[str, Any]], core_idea_changed: bool) -> int:
    families = {c["family"] for c in changes}
    if core_idea_changed or len(families) >= 3:
        return 4
    if len(families) == 2:
        return 3
    return 1 if all(c["scope"] == "element" for c in changes) and len(changes) == 1 else 2


def validate_iteration(raw: Any) -> dict[str, Any]:
    brief = evidence._object(raw, "iteration")
    evidence._no_unknown(brief, ITERATION_FIELDS, "iteration")
    _pattern_id(brief.get("id"), ITER_ID, "iteration.id")
    guest = evidence._text(brief.get("guest"), "guest")
    if not evidence.GUEST_REF_RE.fullmatch(guest):
        raise EvidenceError("guest must be a slug such as cliente_01, never a real name")
    evidence._text(brief.get("base_creative_ref"), "base_creative_ref")
    if brief.get("hypothesis_id") is not None:
        evidence._identifier(brief["hypothesis_id"], "hypothesis", "hypothesis_id")
    changes = evidence._list(brief.get("changes"), "changes")
    if not changes:
        raise EvidenceError("an iteration changes at least one family")
    for change in changes:
        item = evidence._object(change, "change")
        evidence._no_unknown(item, CHANGE_FIELDS, "change")
        evidence._choice(item.get("family"), ITERATION_FAMILIES, "change.family")
        evidence._choice(item.get("scope"), CHANGE_SCOPES, "change.scope")
        evidence._text(item.get("description"), "change.description")
    preserve = [evidence._choice(f, ITERATION_FAMILIES, "preserve") for f in evidence._list(brief.get("preserve", []), "preserve")]
    conflicts = sorted({c["family"] for c in changes} & set(preserve))
    if conflicts:
        raise EvidenceError("preservation contract conflict: changes touch preserved " + ", ".join(conflicts))
    if not isinstance(brief.get("core_idea_changed"), bool):
        raise EvidenceError("core_idea_changed must be true or false")
    evidence._text(brief.get("learning_goal"), "learning_goal")
    evidence._text(brief.get("success_metric"), "success_metric")
    privacy = evidence._choice(brief.get("privacy_class"), evidence.PRIVACY_CLASSES, "privacy_class")
    if privacy not in evidence.SHAREABLE_PRIVACY_CLASSES:
        raise EvidenceError(f"privacy_class {privacy} cannot enter shared evidence")
    if "origin" in brief:
        evidence.validate_origin(brief["origin"])
    if evidence.agent_graph._contains_secret_like(brief):
        raise EvidenceError("iteration contains secret-like content")
    return brief


# --- Creative Learning Record -----------------------------------------------

LEARNING_FIELDS = frozenset(
    {"id", "guest", "iteration_id", "epistemic_state", "validation_id", "lesson", "evidence_refs", "privacy_class"}
)


def validate_learning_record(raw: Any) -> dict[str, Any]:
    record = evidence._object(raw, "learning_record")
    evidence._no_unknown(record, LEARNING_FIELDS, "learning_record")
    _pattern_id(record.get("id"), LEARN_ID, "learning_record.id")
    guest = evidence._text(record.get("guest"), "guest")
    if not evidence.GUEST_REF_RE.fullmatch(guest):
        raise EvidenceError("guest must be a slug")
    _pattern_id(record.get("iteration_id"), ITER_ID, "iteration_id")
    state = evidence._choice(record.get("epistemic_state"), LEARNING_STATES, "epistemic_state")
    if record.get("validation_id") is not None:
        evidence._identifier(record["validation_id"], "validation", "validation_id")
    elif state in evidence.RESOLUTION_STATES:
        raise EvidenceError(f"epistemic_state {state} needs a recorded validation_id")
    evidence._text(record.get("lesson"), "lesson")
    evidence._text_list(record.get("evidence_refs", []), "evidence_refs")
    privacy = evidence._choice(record.get("privacy_class"), evidence.PRIVACY_CLASSES, "privacy_class")
    if privacy not in evidence.SHAREABLE_PRIVACY_CLASSES:
        raise EvidenceError(f"privacy_class {privacy} cannot enter shared evidence")
    if evidence.agent_graph._contains_secret_like(record):
        raise EvidenceError("learning record contains secret-like content")
    return record


# --- Reducers -------------------------------------------------------------------


def _fields(payload: Any, allowed: set[str]) -> dict[str, Any]:
    value = evidence._object(payload, "payload")
    evidence._no_unknown(value, frozenset(allowed), "payload")
    return value


def _iteration(state: dict[str, Any], iteration_id: Any) -> dict[str, Any]:
    record = state["iterations"].get(iteration_id)
    if record is None:
        raise EvidenceError(f"unknown iteration: {iteration_id}")
    return cast(dict[str, Any], record)


def _on_iteration_planned(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    brief = validate_iteration(_fields(payload, {"iteration"}).get("iteration"))
    if brief["id"] in state["iterations"]:
        raise EvidenceError(f"iteration already exists: {brief['id']}")
    if brief.get("hypothesis_id") is not None and brief["hypothesis_id"] not in state["hypotheses"]:
        raise EvidenceError(f"unknown hypothesis: {brief['hypothesis_id']}")
    level = signal_distance(brief["changes"], brief["core_idea_changed"])
    state["iterations"][brief["id"]] = {
        **brief,
        "signal_distance": level,
        "signal_reading": SIGNAL_LEVELS[level],
        "controlled_test": level in CONTROLLED_LEVELS,
        "status": "planned",
        "created_at": ctx["occurred_at"],
        "updated_at": ctx["occurred_at"],
    }


def _on_iteration_reviewed(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"iteration_id", "reviewed_by", "reviewer_ref", "decision", "notes"})
    record = _iteration(state, value.get("iteration_id"))
    if value.get("reviewed_by") != "human":
        raise EvidenceError("only a human can review an iteration")
    reviewer = evidence._text(value.get("reviewer_ref"), "reviewer_ref")
    if not evidence.GUEST_REF_RE.fullmatch(reviewer):
        raise EvidenceError("reviewer_ref must be a slug, not a real name")
    decision = evidence._choice(value.get("decision"), REVIEW_DECISIONS, "decision")
    evidence._optional_text(value.get("notes"), "notes")
    if record["status"] not in ("planned", "needs_changes"):
        raise EvidenceError(f"{record['id']} is already {record['status']}")
    record.update(status=decision, reviewer_ref=reviewer, review_notes=value.get("notes"), updated_at=ctx["occurred_at"])


def _on_learning_recorded(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    record = validate_learning_record(_fields(payload, {"learning_record"}).get("learning_record"))
    if record["id"] in state["creative_learnings"]:
        raise EvidenceError(f"learning record already exists: {record['id']}")
    iteration = _iteration(state, record["iteration_id"])
    if iteration["status"] != "approved":
        raise EvidenceError("a learning record needs an iteration a human approved")
    if iteration["guest"] != record["guest"]:
        raise EvidenceError("learning record and iteration belong to different guests")
    if record.get("validation_id") is not None:
        validation = state["validations"].get(record["validation_id"])
        if validation is None:
            raise EvidenceError(f"unknown validation: {record['validation_id']}")
        if validation["current_state"] != record["epistemic_state"]:
            raise EvidenceError(
                f"learning record says {record['epistemic_state']} but the validation is {validation['current_state']}"
            )
    if record["epistemic_state"] in CLAIMING_STATES and not iteration["controlled_test"]:
        raise EvidenceError(
            f"signal distance {iteration['signal_distance']} is not a controlled test; it cannot claim {record['epistemic_state']}"
        )
    state["creative_learnings"][record["id"]] = {
        **record,
        "signal_distance": iteration["signal_distance"],
        "created_at": ctx["occurred_at"],
    }
    iteration.update(status="learned", updated_at=ctx["occurred_at"])


REDUCERS = {
    "creative_iteration_planned": _on_iteration_planned,
    "creative_iteration_reviewed": _on_iteration_reviewed,
    "creative_learning_recorded": _on_learning_recorded,
}


def empty_state() -> dict[str, Any]:
    return {"iterations": {}, "creative_learnings": {}}


def render(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "creative": {
            "iterations": [state["iterations"][k] for k in sorted(state["iterations"])],
            "learning_records": [state["creative_learnings"][k] for k in sorted(state["creative_learnings"])],
        }
    }
