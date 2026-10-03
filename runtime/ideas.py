#!/usr/bin/env python3
"""Idea bank: capture without judging, evaluate against evidence, brief, learn.

Lifecycle: raw → evaluated → selected → briefed → tested → learned, or
archived from any open state.  Selection is a human decision.  Third-party
material is kept as a reference plus a minimal excerpt and Kokoro's own
reading of it, never as a copied corpus.  External text stays DATA: an
instruction-like excerpt is flagged and changes nothing.
"""

from __future__ import annotations

import re
from typing import Any, cast

import evidence
from evidence import EvidenceError, GateResult

IDEA_STATUSES = ("raw", "evaluated", "selected", "briefed", "tested", "learned", "archived")
OPEN_IDEA_STATUSES = frozenset({"raw", "evaluated", "selected", "briefed", "tested"})
EXCERPT_TYPES = ("verified", "paraphrased", "none")
# Long enough for one sentence of context, short enough to never be a corpus.
MAX_EXCERPT_CHARS = 280
EVALUATION_DIMENSIONS = (
    "strategic_fit",
    "evidence_strength",
    "novelty",
    "production_cost",
    "speed_to_learn",
    "risk",
)
# Higher cost and risk lower the ordering score; the score never decides.
INVERTED_DIMENSIONS = frozenset({"production_cost", "risk"})
IDEA_FIELDS = frozenset(
    {
        "id",
        "guest",
        "concept",
        "source_type",
        "source_ref",
        "source_excerpt",
        "source_excerpt_type",
        "spark",
        "territory",
        "phase",
        "target_persona",
        "trigger_event",
        "desired_future",
        "tension",
        "evidence_refs",
        "privacy_class",
        "source_loop_id",
        "origin",
    }
)
BRIEF_FIELDS = frozenset(
    {"objective", "audience", "format", "learning_goal", "measurement", "hypothesis_id", "next_step"}
)
IDEA_ID = re.compile(r"^IDEA-[0-9A-Za-z_-]{1,64}$")


def _idea_id(value: Any, name: str) -> str:
    text = evidence._text(value, name)
    if not IDEA_ID.fullmatch(text):
        raise EvidenceError(f"{name} is not a valid idea id")
    return text


def validate_idea(raw: Any) -> dict[str, Any]:
    idea = evidence._object(raw, "idea")
    evidence._no_unknown(idea, IDEA_FIELDS, "idea")
    _idea_id(idea.get("id"), "idea.id")
    guest = evidence._text(idea.get("guest"), "guest")
    if not evidence.GUEST_REF_RE.fullmatch(guest):
        raise EvidenceError("guest must be a slug such as cliente_01, never a real name")
    evidence._text(idea.get("concept"), "concept")
    source_type = evidence._choice(idea.get("source_type"), evidence.SOURCE_TYPES, "source_type")
    ref = evidence._text(idea.get("source_ref"), "source_ref")
    if ref.startswith(("/", "~")):
        raise EvidenceError("source_ref must not be an absolute local path")
    excerpt_type = evidence._choice(
        idea.get("source_excerpt_type"), EXCERPT_TYPES, "source_excerpt_type"
    )
    excerpt = idea.get("source_excerpt")
    if excerpt_type == "none":
        if excerpt not in (None, ""):
            raise EvidenceError("source_excerpt_type none cannot carry an excerpt")
    else:
        text = evidence._text(excerpt, "source_excerpt")
        if len(text) > MAX_EXCERPT_CHARS:
            raise EvidenceError(
                f"keep a minimal excerpt (max {MAX_EXCERPT_CHARS} characters) plus the link"
            )
        if excerpt_type == "verified" and source_type == "kokoro_inference":
            raise EvidenceError("an AI-written phrase can never be a verified excerpt")
    evidence._text(idea.get("spark"), "spark")
    evidence._choice(idea.get("territory"), evidence.TERRITORIES, "territory")
    evidence._choice(idea.get("phase"), evidence.PHASES, "phase")
    for name in ("target_persona", "trigger_event", "desired_future", "tension"):
        evidence._optional_text(idea.get(name), name)
    evidence._text_list(idea.get("evidence_refs", []), "evidence_refs")
    privacy = evidence._choice(idea.get("privacy_class"), evidence.PRIVACY_CLASSES, "privacy_class")
    if privacy not in evidence.SHAREABLE_PRIVACY_CLASSES:
        raise EvidenceError(f"privacy_class {privacy} cannot enter the shared idea bank")
    if idea.get("source_loop_id") is not None:
        evidence._identifier(idea["source_loop_id"], "loop", "source_loop_id")
    if "origin" in idea:
        evidence.validate_origin(idea["origin"])
    if evidence.agent_graph._contains_secret_like(idea):
        raise EvidenceError("idea contains secret-like content")
    return idea


def untrusted_excerpt(idea: dict[str, Any]) -> bool:
    excerpt = idea.get("source_excerpt") or ""
    return idea["source_type"] in evidence.UNTRUSTED_SOURCE_TYPES and evidence.instruction_like(excerpt)


def validate_evaluation(raw: Any) -> dict[str, int]:
    scores = evidence._object(raw, "evaluation")
    evidence._no_unknown(scores, frozenset(EVALUATION_DIMENSIONS), "evaluation")
    result: dict[str, int] = {}
    for name in EVALUATION_DIMENSIONS:
        value = scores.get(name)
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
            raise EvidenceError(f"evaluation.{name} must be an integer from 1 to 5")
        result[name] = value
    return result


def evaluation_score(scores: dict[str, int]) -> int:
    return sum(6 - scores[n] if n in INVERTED_DIMENSIONS else scores[n] for n in EVALUATION_DIMENSIONS)


def gate_idea_not_duplicate(idea: dict[str, Any], bank: list[dict[str, Any]]) -> GateResult:
    reasons = [
        f"duplicates {other['id']}"
        for other in bank
        if other["status"] in OPEN_IDEA_STATUSES
        and other["guest"] == idea["guest"]
        and evidence.question_similarity(other["concept"], idea["concept"])
        >= evidence.DUPLICATE_SIMILARITY
    ]
    return GateResult("GATE-NOT-DUPLICATE", "Blocked" if reasons else "Pass", tuple(reasons))


def validate_brief(raw: Any) -> dict[str, Any]:
    brief = evidence._object(raw, "brief")
    evidence._no_unknown(brief, BRIEF_FIELDS, "brief")
    for name in ("objective", "audience", "format", "learning_goal", "measurement", "next_step"):
        evidence._text(brief.get(name), f"brief.{name}")
    if brief.get("hypothesis_id") is not None:
        evidence._identifier(brief["hypothesis_id"], "hypothesis", "brief.hypothesis_id")
    return brief


# --- Reducers -------------------------------------------------------------------


def _idea(state: dict[str, Any], idea_id: Any) -> dict[str, Any]:
    record = state["ideas"].get(idea_id)
    if record is None:
        raise EvidenceError(f"unknown idea: {idea_id}")
    return cast(dict[str, Any], record)


def _move(record: dict[str, Any], allowed: set[str], target: str, ctx: dict[str, Any]) -> None:
    if record["status"] not in allowed:
        raise EvidenceError(f"{record['id']} is {record['status']}; {target} needs {sorted(allowed)}")
    record["status"] = target
    record["updated_at"] = ctx["occurred_at"]


def _fields(payload: Any, allowed: set[str]) -> dict[str, Any]:
    value = evidence._object(payload, "payload")
    evidence._no_unknown(value, frozenset(allowed), "payload")
    return value


def _on_idea_captured(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    idea = validate_idea(_fields(payload, {"idea"}).get("idea"))
    if idea["id"] in state["ideas"]:
        raise EvidenceError(f"idea already exists: {idea['id']}")
    gate = gate_idea_not_duplicate(idea, list(state["ideas"].values()))
    if gate.status == "Blocked":
        raise EvidenceError("gate blocked: GATE-NOT-DUPLICATE: " + ", ".join(gate.reasons))
    if idea.get("source_loop_id") is not None and idea["source_loop_id"] not in state["loops"]:
        raise EvidenceError(f"unknown loop: {idea['source_loop_id']}")
    state["ideas"][idea["id"]] = {
        **idea,
        "status": "raw",
        "evaluation": None,
        "score": None,
        "untrusted_excerpt": untrusted_excerpt(idea),
        "created_at": ctx["occurred_at"],
        "updated_at": ctx["occurred_at"],
    }


def _on_idea_evaluated(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"idea_id", "evaluation", "rationale"})
    record = _idea(state, value.get("idea_id"))
    scores = validate_evaluation(value.get("evaluation"))
    evidence._text(value.get("rationale"), "rationale")
    _move(record, {"raw", "evaluated"}, "evaluated", ctx)
    record.update(evaluation=scores, score=evaluation_score(scores), rationale=value["rationale"])


def _on_idea_selected(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"idea_id", "selected_by", "selector_ref", "reason"})
    record = _idea(state, value.get("idea_id"))
    if value.get("selected_by") != "human":
        raise EvidenceError("only a human can select an idea")
    selector = evidence._text(value.get("selector_ref"), "selector_ref")
    if not evidence.GUEST_REF_RE.fullmatch(selector):
        raise EvidenceError("selector_ref must be a slug, not a real name")
    evidence._text(value.get("reason"), "reason")
    _move(record, {"evaluated"}, "selected", ctx)
    record.update(selected_by="human", selector_ref=selector, selection_reason=value["reason"])


def _on_idea_briefed(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"idea_id", "brief"})
    record = _idea(state, value.get("idea_id"))
    brief = validate_brief(value.get("brief"))
    if brief.get("hypothesis_id") is not None and brief["hypothesis_id"] not in state["hypotheses"]:
        raise EvidenceError(f"unknown hypothesis: {brief['hypothesis_id']}")
    _move(record, {"selected"}, "briefed", ctx)
    record["brief"] = brief


def _on_idea_tested(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    """A test ran.  It becomes `learned` only when a recorded validation or
    creative learning record backs the lesson; an anecdote stays `tested`."""

    value = _fields(payload, {"idea_id", "test_ref", "outcome", "validation_id", "learning_record_id"})
    record = _idea(state, value.get("idea_id"))
    evidence._text(value.get("test_ref"), "test_ref")
    evidence._text(value.get("outcome"), "outcome")
    backing = None
    if value.get("validation_id") is not None:
        validation = state["validations"].get(value["validation_id"])
        if validation is None:
            raise EvidenceError(f"unknown validation: {value['validation_id']}")
        backing = {"validation_id": validation["id"], "state": validation["current_state"]}
    if value.get("learning_record_id") is not None:
        learning = state["creative_learnings"].get(value["learning_record_id"])
        if learning is None:
            raise EvidenceError(f"unknown creative learning record: {value['learning_record_id']}")
        backing = {"learning_record_id": learning["id"], "state": learning["epistemic_state"]}
    _move(record, {"briefed", "tested"}, "learned" if backing else "tested", ctx)
    record.update(test_ref=value["test_ref"], outcome=value["outcome"], backed_by=backing)


def _on_idea_archived(state: dict[str, Any], payload: dict[str, Any], ctx: dict[str, Any]) -> None:
    value = _fields(payload, {"idea_id", "reason"})
    record = _idea(state, value.get("idea_id"))
    evidence._text(value.get("reason"), "reason")
    _move(record, set(OPEN_IDEA_STATUSES), "archived", ctx)
    record["archive_reason"] = value["reason"]


REDUCERS = {
    "idea_captured": _on_idea_captured,
    "idea_evaluated": _on_idea_evaluated,
    "idea_selected": _on_idea_selected,
    "idea_briefed": _on_idea_briefed,
    "idea_tested": _on_idea_tested,
    "idea_archived": _on_idea_archived,
}


def empty_state() -> dict[str, Any]:
    return {"ideas": {}}


def render(state: dict[str, Any]) -> dict[str, Any]:
    ideas = [state["ideas"][key] for key in sorted(state["ideas"])]
    open_ideas = [i for i in ideas if i["status"] in OPEN_IDEA_STATUSES]
    open_ideas.sort(key=lambda i: (-(i["score"] or 0), i["id"]))
    return {
        "idea-bank": {
            "open_ideas": open_ideas,
            "closed_ideas": [i for i in ideas if i["status"] not in OPEN_IDEA_STATUSES],
        }
    }
