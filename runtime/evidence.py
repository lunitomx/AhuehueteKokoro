#!/usr/bin/env python3
"""Kokoro Evidence Model v1: schemas, states and documentary gates.

Pure functions only: no file or network access.  The canonical prose lives in
`.claude/knowledge/kokoro-evidence-model.md` and
`.claude/knowledge/kokoro-open-questions.md`; this module is the executable
contract those documents describe.  Every validator fails closed.

External text (web, reviews, comments, transcripts, competitor pages) is data.
Validators never read it as instructions: its content cannot change a status,
a gate result or a rule.  Instruction-like text is flagged for human review.
"""

from __future__ import annotations

import datetime as dt
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, cast

import agent_graph
import growth_diagnosis

SCHEMA_VERSION = 1

# --- Vocabulary (single source for runtime; mirrored in the knowledge docs) ---

EPISTEMIC_STATES = (
    "observed",
    "reported",
    "inferred",
    "hypothesis",
    "validated",
    "invalidated",
    "inconclusive",
    "insufficient",
    "stale",
)
SUPPORT_TYPES = ("observed", "reported", "inferred")
RESOLUTION_STATES = ("validated", "invalidated", "inconclusive", "insufficient")
# Only these moves exist.  observed/reported/inferred never jump to a
# resolution: they must first be formulated as a hypothesis with a bar.
TRANSITIONS: dict[str, frozenset[str]] = {
    "observed": frozenset({"inferred", "hypothesis", "stale"}),
    "reported": frozenset({"inferred", "hypothesis", "stale"}),
    "inferred": frozenset({"hypothesis", "stale"}),
    "hypothesis": frozenset(RESOLUTION_STATES),
    "validated": frozenset({"stale"}),
    "invalidated": frozenset({"stale"}),
    "inconclusive": frozenset({"hypothesis", "stale"}),
    "insufficient": frozenset({"hypothesis", "stale"}),
    "stale": frozenset({"hypothesis"}),
}
PHASES = growth_diagnosis.LAYERS
CONFIDENCE_LEVELS = growth_diagnosis.CONFIDENCE_LEVELS
TERRITORIES = (
    "invitado",
    "creacion_oferta",
    "mensaje",
    "canal_creativo",
    "conversion_seguimiento",
    "economia_medicion",
)
LOOP_STATUSES = ("captured", "ranked", "promoted", "hypothesis", "closed", "archived")
HYPOTHESIS_STATUSES = ("proposed", "approved", "resolved", "superseded")
PRIORITY_DIMENSIONS = ("impact", "uncertainty", "learnability", "urgency", "reversibility")
# Same tiers as Memory v2 visibility.  Only "team" may enter shared events.
PRIVACY_CLASSES = ("team", "personal", "sensitive", "secret")
SHAREABLE_PRIVACY_CLASSES = frozenset({"team"})
SOURCE_TYPES = (
    "platform_metric",
    "crm_record",
    "sales_record",
    "interview",
    "transcript",
    "survey",
    "document",
    "web_page",
    "review",
    "social_comment",
    "competitor_page",
    "experiment",
    "user_statement",
    "kokoro_inference",
)
# Content produced outside Kokoro and the people it serves: always DATA.
UNTRUSTED_SOURCE_TYPES = frozenset(
    {"web_page", "review", "social_comment", "competitor_page", "transcript", "document"}
)
VOICE_KINDS = ("verified_quote", "paraphrase", "illustrative")
# Knowledge updates a validation may PROPOSE.  System rules (skills, gates,
# identity, commands, knowledge files) are never targets: they change only
# through a reviewed pull request, never from evidence content.
KNOWLEDGE_UPDATE_TARGETS = ("guest_knowledge", "open_question")
GATE_STATUSES = ("Pass", "Partial", "Blocked", "Skipped")
# How fast a piece of knowledge ages.  The number is the longest allowed gap
# between generated_on and refresh_by; event_driven knowledge has no calendar
# and expires only when one of its invalidated_by events happens.
FRESHNESS_CLASSES = ("fast", "medium", "slow", "event_driven")
FRESHNESS_MAX_DAYS = {"fast": 30, "medium": 90, "slow": 365}

ID_PATTERNS = {
    "loop": re.compile(r"^LOOP-[0-9A-Za-z_-]{1,64}$"),
    "hypothesis": re.compile(r"^(?:HYP|HIP)-[0-9A-Za-z_-]{1,64}$"),
    "experiment": re.compile(r"^EXP-[0-9A-Za-z_-]{1,64}$"),
    "validation": re.compile(r"^VAL-[0-9A-Za-z_-]{1,64}$"),
    # Anything freshness can depend on: loops, hypotheses, validations and
    # living artifacts such as FORCES-2026-08 or MESSAGE-2026-08.
    "dependency": re.compile(r"^[A-Z][A-Z0-9]{1,15}-[0-9A-Za-z_-]{1,64}$"),
}
GUEST_REF_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,79}$")
QUESTION_MIN_WORDS = 6
DUPLICATE_SIMILARITY = 0.8
VAGUE_QUESTION_STARTS = (
    "investigar",
    "explorar",
    "analizar",
    "revisar",
    "entender",
    "ver si",
    "research",
    "explore",
    "analyze",
    "look into",
    "understand",
)
HIDDEN_CONCLUSION_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"\bno es cierto que\b",
        r"\bverdad que\b",
        r"\bno crees que\b",
        r"\b(?:confirmar|demostrar|probar|comprobar) que\b",
        r"\bpor que\b.*\b(?:funciona|convierte|vende|es) mejor\b",
        r"\bya que\b",
        r"\bdado que\b",
        r"\bisn'?t it true\b",
        r"\b(?:confirm|prove|show) that\b",
        r"\bwhy does\b.*\bwork better\b",
    )
)
INSTRUCTION_LIKE_PATTERNS = tuple(
    re.compile(pattern)
    for pattern in (
        r"\bignor(?:e|a|ar)\b.{0,40}\b(?:instruc|rules|reglas|previous|anteriores)",
        r"\b(?:system prompt|prompt del sistema)\b",
        r"\b(?:reveal|revela|muestra|share|comparte)\b.{0,30}\b(?:secret|token|password|clave|contrasena)",
        r"\b(?:run|ejecuta|execute)\b.{0,20}\b(?:command|comando|shell|bash)\b",
        r"\b(?:mark|marca|set|pon)\b.{0,30}\b(?:validated|validado|approved|aprobad)",
        r"\b(?:you are now|ahora eres|act as|actua como)\b",
    )
)


class EvidenceError(ValueError):
    """Raised when evidence, a question or a hypothesis breaks the contract."""


@dataclass(frozen=True)
class GateResult:
    gate: str
    status: str
    reasons: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {"gate": self.gate, "status": self.status, "reasons": list(self.reasons)}


# --- Small typed readers ---------------------------------------------------


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvidenceError(f"{name} must be an object")
    return cast(dict[str, Any], value)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{name} must be a non-empty string")
    return value.strip()


def _optional_text(value: Any, name: str) -> str | None:
    return None if value is None else _text(value, name)


def _list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise EvidenceError(f"{name} must be a list")
    return cast(list[Any], value)


def _text_list(value: Any, name: str) -> list[str]:
    return [_text(item, name) for item in _list(value, name)]


def _choice(value: Any, choices: tuple[str, ...], name: str) -> str:
    if value not in choices:
        raise EvidenceError(f"{name} must be one of: {', '.join(choices)}")
    return cast(str, value)


def _identifier(value: Any, kind: str, name: str) -> str:
    text = _text(value, name)
    if not ID_PATTERNS[kind].fullmatch(text):
        raise EvidenceError(f"{name} is not a valid {kind} id")
    return text


def _date(value: Any, name: str) -> dt.date:
    text = _text(value, name)
    try:
        return dt.datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError as exc:
        raise EvidenceError(f"{name} must be an ISO 8601 date") from exc


def _no_unknown(value: dict[str, Any], allowed: frozenset[str], name: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise EvidenceError(f"{name} has unknown fields: {', '.join(unknown)}")


def normalize(text: str) -> str:
    """Lowercase, strip accents and punctuation for heuristic comparisons."""

    decomposed = unicodedata.normalize("NFKD", text.lower())
    plain = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9' ]+", " ", plain).strip()


def instruction_like(text: str) -> bool:
    """Flag text that tries to instruct the system.  Flagging never obeys."""

    plain = normalize(text)
    return any(pattern.search(plain) for pattern in INSTRUCTION_LIKE_PATTERNS)


# --- States ---------------------------------------------------------------


def check_transition(current: str, target: str) -> None:
    """Allow only documented state moves; nothing is promoted implicitly."""

    _choice(current, EPISTEMIC_STATES, "current state")
    _choice(target, EPISTEMIC_STATES, "target state")
    if target not in TRANSITIONS[current]:
        raise EvidenceError(f"transition {current} -> {target} is not allowed")


# --- Freshness v1 -------------------------------------------------------------

FRESHNESS_FIELDS = frozenset(
    {
        "generated_on",
        "refresh_by",
        "freshness_class",
        "depends_on",
        "invalidated_by",
        "last_material_change",
    }
)


def validate_freshness(raw: Any) -> dict[str, Any]:
    """When knowledge was produced, when it must be reviewed, and what it rests on."""

    block = _object(raw, "freshness")
    _no_unknown(block, FRESHNESS_FIELDS, "freshness")
    kind = _choice(block.get("freshness_class"), FRESHNESS_CLASSES, "freshness_class")
    generated = _date(block.get("generated_on"), "freshness.generated_on")
    triggers = _text_list(block.get("invalidated_by", []), "freshness.invalidated_by")
    if kind == "event_driven":
        if not triggers:
            raise EvidenceError("event_driven freshness needs at least one invalidated_by event")
        if block.get("refresh_by") is not None:
            _date(block["refresh_by"], "freshness.refresh_by")
    else:
        refresh = _date(block.get("refresh_by"), "freshness.refresh_by")
        if refresh < generated:
            raise EvidenceError("refresh_by cannot be earlier than generated_on")
        if (refresh - generated).days > FRESHNESS_MAX_DAYS[kind]:
            raise EvidenceError(
                f"{kind} knowledge must be reviewed within {FRESHNESS_MAX_DAYS[kind]} days"
            )
    for ref in _list(block.get("depends_on", []), "freshness.depends_on"):
        _identifier(ref, "dependency", "freshness.depends_on")
    if block.get("last_material_change") is not None:
        if _date(block["last_material_change"], "freshness.last_material_change") < generated:
            raise EvidenceError("last_material_change cannot be earlier than generated_on")
    return block


def freshness_status(block: dict[str, Any], today: dt.date) -> str:
    """'fresh' or 'expired' by calendar; 'event_driven' when only events expire it.

    Expiry by dependency (an upstream artifact changed) is resolved by the
    freshness graph, not here: this function only reads one block.
    """

    if block.get("refresh_by") is None:
        return "event_driven"
    return "expired" if today > _date(block["refresh_by"], "freshness.refresh_by") else "fresh"


# --- Provenance v1 ----------------------------------------------------------

PROVENANCE_FIELDS = frozenset(
    {
        "source_type",
        "source_ref",
        "observed_at",
        "retrieved_at",
        "scope",
        "claim",
        "support_type",
        "confidence",
        "privacy_class",
        "metric",
        "voice",
        "freshness",
    }
)
METRIC_FIELDS = frozenset(
    {"numerator", "denominator", "window", "unit", "platform", "attribution"}
)
VOICE_FIELDS = frozenset({"kind", "speaker_ref", "text"})


def _validate_metric(raw: Any) -> dict[str, Any]:
    metric = _object(raw, "metric")
    _no_unknown(metric, METRIC_FIELDS, "metric")
    missing = sorted(METRIC_FIELDS - set(metric))
    if missing:
        raise EvidenceError("metric is missing: " + ", ".join(missing))
    for name in ("numerator", "denominator"):
        value = metric[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise EvidenceError(f"metric.{name} must be a non-negative number")
    if metric["denominator"] == 0:
        raise EvidenceError("metric.denominator must be greater than zero")
    window = _object(metric["window"], "metric.window")
    if _date(window.get("start"), "metric.window.start") > _date(
        window.get("end"), "metric.window.end"
    ):
        raise EvidenceError("metric.window.start must not be after its end")
    for name in ("unit", "platform", "attribution"):
        _text(metric[name], f"metric.{name}")
    return metric


def _validate_voice(raw: Any, source_type: str, support_type: str) -> dict[str, Any]:
    voice = _object(raw, "voice")
    _no_unknown(voice, VOICE_FIELDS, "voice")
    kind = _choice(voice.get("kind"), VOICE_KINDS, "voice.kind")
    _text(voice.get("text"), "voice.text")
    if kind == "verified_quote":
        if source_type == "kokoro_inference":
            raise EvidenceError("an AI-generated phrase can never be a verified quote")
        speaker = _text(voice.get("speaker_ref"), "voice.speaker_ref")
        if not GUEST_REF_RE.fullmatch(speaker):
            raise EvidenceError("voice.speaker_ref must be a slug, not a real name")
    if kind == "illustrative" and support_type != "inferred":
        raise EvidenceError("illustrative language can only carry support_type inferred")
    return voice


def validate_provenance(raw: Any, *, shared: bool = True) -> dict[str, Any]:
    """Validate one evidence item.  The claim is stored as opaque data."""

    item = _object(raw, "provenance")
    _no_unknown(item, PROVENANCE_FIELDS, "provenance")
    source_type = _choice(item.get("source_type"), SOURCE_TYPES, "source_type")
    source_ref = _text(item.get("source_ref"), "source_ref")
    if source_ref.startswith(("/", "~")) or re.match(r"^[A-Za-z]:\\", source_ref):
        raise EvidenceError("source_ref must not be an absolute local path")
    observed = _date(item.get("observed_at"), "observed_at")
    retrieved = _date(item.get("retrieved_at"), "retrieved_at")
    if retrieved < observed:
        raise EvidenceError("retrieved_at cannot be earlier than observed_at")
    _text(item.get("scope"), "scope")
    _text(item.get("claim"), "claim")
    support_type = _choice(item.get("support_type"), SUPPORT_TYPES, "support_type")
    if source_type == "kokoro_inference" and support_type != "inferred":
        raise EvidenceError("kokoro_inference evidence can only be inferred")
    _choice(item.get("confidence"), CONFIDENCE_LEVELS, "confidence")
    privacy = _choice(item.get("privacy_class"), PRIVACY_CLASSES, "privacy_class")
    if shared and privacy not in SHAREABLE_PRIVACY_CLASSES:
        raise EvidenceError(f"privacy_class {privacy} cannot enter shared evidence")
    if source_type == "platform_metric" and "metric" not in item:
        raise EvidenceError("platform_metric evidence requires metric details")
    if "metric" in item:
        _validate_metric(item["metric"])
    if "voice" in item:
        _validate_voice(item["voice"], source_type, support_type)
    if "freshness" in item:
        validate_freshness(item["freshness"])
    if agent_graph._contains_secret_like(item):
        raise EvidenceError("provenance contains secret-like content")
    return item


def is_untrusted(item: dict[str, Any]) -> bool:
    return item.get("source_type") in UNTRUSTED_SOURCE_TYPES


def untrusted_flags(items: list[dict[str, Any]]) -> list[str]:
    """Return source refs whose external text looks like an instruction."""

    flagged: list[str] = []
    for item in items:
        texts = [str(item.get("claim", ""))]
        voice = item.get("voice")
        if isinstance(voice, dict):
            texts.append(str(cast(dict[str, Any], voice).get("text", "")))
        if is_untrusted(item) and any(instruction_like(t) for t in texts):
            flagged.append(str(item.get("source_ref")))
    return flagged


def _provenance_list(value: Any, name: str, *, required: bool) -> list[dict[str, Any]]:
    items = [validate_provenance(item) for item in _list(value, name)]
    if required and not items:
        raise EvidenceError(f"{name} requires at least one provenance item")
    return items


# --- Gates ------------------------------------------------------------------


def _gate(name: str, reasons: list[str], *, partial: bool = False) -> GateResult:
    if not reasons:
        return GateResult(name, "Pass")
    return GateResult(name, "Partial" if partial else "Blocked", tuple(reasons))


def gate_question_exact(question: str) -> GateResult:
    """Concrete, closable question with no conclusion hidden inside."""

    reasons: list[str] = []
    text = question.strip()
    plain = normalize(text)
    if not text.endswith("?"):
        reasons.append("question must be written as a question ending in '?'")
    if len(plain.split()) < QUESTION_MIN_WORDS:
        reasons.append(f"question needs at least {QUESTION_MIN_WORDS} words")
    if plain.startswith(VAGUE_QUESTION_STARTS):
        reasons.append("question is a task ('investigar X'), not a question")
    if any(pattern.search(plain) for pattern in HIDDEN_CONCLUSION_PATTERNS):
        reasons.append("question carries its expected answer (hidden conclusion)")
    return _gate("GATE-QUESTION-EXACT", reasons)


def gate_decision_linked(decision: Any) -> GateResult:
    reasons = [] if isinstance(decision, str) and decision.strip() else [
        "name the decision that would change with the answer"
    ]
    return _gate("GATE-DECISION-LINKED", reasons)


def gate_source_possible(routes: Any) -> GateResult:
    valid = isinstance(routes, list) and any(
        isinstance(item, str) and item.strip() for item in cast(list[Any], routes)
    )
    reasons = [] if valid else ["declare at least one plausible evidence route"]
    return _gate("GATE-SOURCE-POSSIBLE", reasons)


def question_similarity(left: str, right: str) -> float:
    a, b = set(normalize(left).split()), set(normalize(right).split())
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def gate_not_duplicate(loop: dict[str, Any], active: list[dict[str, Any]]) -> GateResult:
    """Block when an active loop for the same guest asks the same thing."""

    reasons = [
        f"duplicates {other['id']}"
        for other in active
        if other.get("id") != loop.get("id")
        and other.get("guest") == loop.get("guest")
        and question_similarity(str(other.get("question", "")), str(loop.get("question", "")))
        >= DUPLICATE_SIMILARITY
    ]
    return _gate("GATE-NOT-DUPLICATE", reasons)


def gate_hypothesis_falsifiable(hypothesis: dict[str, Any]) -> GateResult:
    reasons: list[str] = []
    plan = hypothesis.get("evidence_plan")
    disconfirming = plan.get("disconfirming_read") if isinstance(plan, dict) else None
    if not isinstance(disconfirming, str) or not disconfirming.strip():
        reasons.append("declare which observable result would prove it wrong")
    bar = hypothesis.get("precommitted_bar")
    invalidated = bar.get("invalidated") if isinstance(bar, dict) else None
    validated = bar.get("validated") if isinstance(bar, dict) else None
    if not isinstance(invalidated, str) or not invalidated.strip():
        reasons.append("precommitted_bar.invalidated is required")
    elif isinstance(validated, str) and normalize(invalidated) == normalize(validated):
        reasons.append("validated and invalidated criteria cannot be the same")
    return _gate("GATE-HYPOTHESIS-FALSIFIABLE", reasons)


def gate_evidence_bar_precommitted(hypothesis: dict[str, Any]) -> GateResult:
    bar = hypothesis.get("precommitted_bar")
    if not isinstance(bar, dict):
        return _gate("GATE-EVIDENCE-BAR-PRECOMMITTED", ["precommitted_bar is required"])
    bar_value = cast(dict[str, Any], bar)
    reasons = [
        f"precommitted_bar.{state} is required"
        for state in RESOLUTION_STATES
        if not isinstance(bar_value.get(state), str) or not bar_value[state].strip()
    ]
    return _gate("GATE-EVIDENCE-BAR-PRECOMMITTED", reasons)


def gate_untrusted_content_isolated(items: list[dict[str, Any]]) -> GateResult:
    """Partial when external text looks like an instruction: kept as data only."""

    flagged = untrusted_flags(items)
    reasons = [f"instruction-like external text kept as data: {ref}" for ref in flagged]
    return _gate("GATE-UNTRUSTED-CONTENT-ISOLATED", reasons, partial=True)


def _require_pass(results: list[GateResult]) -> None:
    blocked = [r for r in results if r.status == "Blocked"]
    if blocked:
        details = "; ".join(f"{r.gate}: {', '.join(r.reasons)}" for r in blocked)
        raise EvidenceError(f"gate blocked: {details}")


# --- Open Questions ----------------------------------------------------------

LOOP_FIELDS = frozenset(
    {
        "id",
        "guest",
        "phase",
        "territory",
        "observation",
        "question",
        "why_it_matters",
        "evidence_routes",
        "provenance",
        "links",
        "freshness",
        "origin",
    }
)
ORIGIN_FIELDS = frozenset({"source_skill", "source_run_id", "source_event_ids"})
SKILL_RE = re.compile(r"^/kokoro(?:-[a-z0-9]+)*$")


def validate_origin(raw: Any) -> dict[str, Any]:
    """Which skill, run and ledger events produced a record (all optional ids)."""

    origin = _object(raw, "origin")
    _no_unknown(origin, ORIGIN_FIELDS, "origin")
    skill = _text(origin.get("source_skill"), "origin.source_skill")
    if not SKILL_RE.fullmatch(skill):
        raise EvidenceError("origin.source_skill must be a Kokoro command such as /kokoro-open")
    if origin.get("source_run_id") is not None:
        if not re.fullmatch(r"run-[0-9a-f]{24}", _text(origin["source_run_id"], "source_run_id")):
            raise EvidenceError("origin.source_run_id must be a graph run id")
    for event_id in _list(origin.get("source_event_ids", []), "origin.source_event_ids"):
        if not isinstance(event_id, str) or not re.fullmatch(r"evt-[0-9a-f]{32}", event_id):
            raise EvidenceError("origin.source_event_ids must be ledger event ids")
    return origin


def loop_gates(loop: dict[str, Any], active: list[dict[str, Any]]) -> list[GateResult]:
    why = loop.get("why_it_matters")
    decision = why.get("decision") if isinstance(why, dict) else None
    return [
        gate_question_exact(str(loop.get("question", ""))),
        gate_decision_linked(decision),
        gate_source_possible(loop.get("evidence_routes")),
        gate_not_duplicate(loop, active),
        gate_untrusted_content_isolated(
            [p for p in loop.get("provenance", []) if isinstance(p, dict)]
        ),
    ]


def validate_loop(raw: Any, active: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Validate a captured open question.  It always starts as 'captured'."""

    loop = _object(raw, "loop")
    _no_unknown(loop, LOOP_FIELDS, "loop")
    _identifier(loop.get("id"), "loop", "loop.id")
    guest = _text(loop.get("guest"), "guest")
    if not GUEST_REF_RE.fullmatch(guest):
        raise EvidenceError("guest must be a slug such as cliente_01, never a real name")
    _choice(loop.get("phase"), PHASES, "phase")
    _choice(loop.get("territory"), TERRITORIES, "territory")
    _text(loop.get("observation"), "observation")
    _text(loop.get("question"), "question")
    why = _object(loop.get("why_it_matters"), "why_it_matters")
    _no_unknown(why, frozenset({"decision", "impact"}), "why_it_matters")
    _optional_text(why.get("impact"), "why_it_matters.impact")
    _text_list(loop.get("evidence_routes", []), "evidence_routes")
    _provenance_list(loop.get("provenance"), "provenance", required=True)
    _text_list(loop.get("links", []), "links")
    if "freshness" in loop:
        validate_freshness(loop["freshness"])
    if "origin" in loop:
        validate_origin(loop["origin"])
    _require_pass(loop_gates(loop, active or []))
    return loop


def validate_priority(raw: Any) -> dict[str, int]:
    """Five 1-5 scores.  The total orders the conversation; it decides nothing."""

    priority = _object(raw, "priority")
    _no_unknown(priority, frozenset(PRIORITY_DIMENSIONS), "priority")
    scores: dict[str, int] = {}
    for name in PRIORITY_DIMENSIONS:
        value = priority.get(name)
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
            raise EvidenceError(f"priority.{name} must be an integer from 1 to 5")
        scores[name] = value
    return scores


def priority_total(scores: dict[str, int]) -> int:
    return sum(scores[name] for name in PRIORITY_DIMENSIONS)


# --- Hypothesis --------------------------------------------------------------

HYPOTHESIS_FIELDS = frozenset(
    {
        "id",
        "source_loop_id",
        "origin",
        "guest",
        "prediction",
        "decision_at_stake",
        "evidence_plan",
        "precommitted_bar",
        "experiment_id",
        "supersedes",
        "redesign_reason",
    }
)


def bar_digest(bar: dict[str, Any]) -> str:
    """Fingerprint of the precommitted bar; a later change breaks the match."""

    subset = {state: bar.get(state) for state in RESOLUTION_STATES}
    return agent_graph.sha256_bytes(agent_graph.canonical_bytes(subset))


def validate_hypothesis(raw: Any) -> dict[str, Any]:
    hypothesis = _object(raw, "hypothesis")
    _no_unknown(hypothesis, HYPOTHESIS_FIELDS, "hypothesis")
    _identifier(hypothesis.get("id"), "hypothesis", "hypothesis.id")
    if hypothesis.get("source_loop_id") is not None:
        _identifier(hypothesis["source_loop_id"], "loop", "source_loop_id")
    else:
        _text(hypothesis.get("origin"), "origin (skill that created it, when no loop)")
    guest = _text(hypothesis.get("guest"), "guest")
    if not GUEST_REF_RE.fullmatch(guest):
        raise EvidenceError("guest must be a slug such as cliente_01")
    _text(hypothesis.get("prediction"), "prediction")
    _text(hypothesis.get("decision_at_stake"), "decision_at_stake")
    plan = _object(hypothesis.get("evidence_plan"), "evidence_plan")
    _no_unknown(
        plan,
        frozenset({"sources", "disconfirming_read", "unavailable_sources"}),
        "evidence_plan",
    )
    if not _text_list(plan.get("sources"), "evidence_plan.sources"):
        raise EvidenceError("evidence_plan.sources needs at least one source")
    _text_list(plan.get("unavailable_sources", []), "evidence_plan.unavailable_sources")
    _object(hypothesis.get("precommitted_bar"), "precommitted_bar")
    _no_unknown(
        hypothesis["precommitted_bar"], frozenset(RESOLUTION_STATES), "precommitted_bar"
    )
    if hypothesis.get("experiment_id") is not None:
        _identifier(hypothesis["experiment_id"], "experiment", "experiment_id")
    if hypothesis.get("supersedes") is not None:
        _identifier(hypothesis["supersedes"], "hypothesis", "supersedes")
        _text(hypothesis.get("redesign_reason"), "redesign_reason")
    _require_pass(
        [gate_hypothesis_falsifiable(hypothesis), gate_evidence_bar_precommitted(hypothesis)]
    )
    if agent_graph._contains_secret_like(hypothesis):
        raise EvidenceError("hypothesis contains secret-like content")
    return hypothesis


# --- Validation ----------------------------------------------------------------

VALIDATION_FIELDS = frozenset(
    {
        "id",
        "hypothesis_id",
        "experiment_id",
        "state",
        "bar_sha256",
        "evidence_for",
        "evidence_against",
        "missing_evidence",
        "finding",
        "decision_impact",
        "knowledge_updates_proposed",
        "new_loops",
        "freshness",
        "revalidates",
    }
)


def _validate_update(raw: Any) -> dict[str, Any]:
    update = _object(raw, "knowledge update")
    _no_unknown(update, frozenset({"target", "summary"}), "knowledge update")
    target = update.get("target")
    if target not in KNOWLEDGE_UPDATE_TARGETS:
        raise EvidenceError(
            "evidence can only propose guest knowledge or open questions; "
            "system rules change only through a reviewed pull request"
        )
    _text(update.get("summary"), "knowledge update summary")
    return update


def _require_resolution_evidence(
    state: str,
    support: list[dict[str, Any]],
    against: list[dict[str, Any]],
    missing: list[str],
) -> None:
    if state == "validated":
        if not support:
            raise EvidenceError("validated requires evidence_for")
        if all(item["support_type"] == "inferred" for item in support):
            raise EvidenceError("validated cannot rest only on inferred evidence")
        if any(item.get("voice", {}).get("kind") == "illustrative" for item in support):
            raise EvidenceError("illustrative language is never evidence for a claim")
    elif state == "invalidated" and not against:
        raise EvidenceError("invalidated requires evidence_against")
    elif state == "inconclusive" and not (support and against):
        raise EvidenceError("inconclusive requires evidence pointing both ways")
    elif state == "insufficient" and not missing:
        raise EvidenceError("insufficient requires missing_evidence")


def validate_validation(raw: Any) -> dict[str, Any]:
    """Validate a resolution.  The bar fingerprint is checked by the ledger."""

    record = _object(raw, "validation")
    _no_unknown(record, VALIDATION_FIELDS, "validation")
    _identifier(record.get("id"), "validation", "validation.id")
    _identifier(record.get("hypothesis_id"), "hypothesis", "hypothesis_id")
    if record.get("experiment_id") is not None:
        _identifier(record["experiment_id"], "experiment", "experiment_id")
    if record.get("revalidates") is not None:
        _identifier(record["revalidates"], "validation", "revalidates")
    state = _choice(record.get("state"), RESOLUTION_STATES, "state")
    _text(record.get("bar_sha256"), "bar_sha256")
    support = _provenance_list(record.get("evidence_for", []), "evidence_for", required=False)
    against = _provenance_list(
        record.get("evidence_against", []), "evidence_against", required=False
    )
    missing = _text_list(record.get("missing_evidence", []), "missing_evidence")
    _require_resolution_evidence(state, support, against, missing)
    _text(record.get("finding"), "finding")
    _text(record.get("decision_impact"), "decision_impact")
    for update in _list(record.get("knowledge_updates_proposed", []), "updates"):
        _validate_update(update)
    for loop_id in _list(record.get("new_loops", []), "new_loops"):
        _identifier(loop_id, "loop", "new_loops")
    # A resolution always ages: generated_on is the day it was resolved and
    # refresh_by (or an invalidated_by event) is when it must be revalidated.
    validate_freshness(record.get("freshness"))
    if agent_graph._contains_secret_like(record):
        raise EvidenceError("validation contains secret-like content")
    return record
