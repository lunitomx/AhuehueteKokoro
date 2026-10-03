#!/usr/bin/env python3
"""GATE-GROUNDED: every claim in a piece of copy traces back to a source.

Seven checks, all read-only:

1. sources_present         copy with claims needs at least one source
2. numbers_sourced         every number in the copy appears in a source
3. testimonial_labeled     a quote that no verified source contains must be
                           visibly labeled as illustrative
4. no_ai_testimony         a Kokoro inference can never back a quote
5. untrusted_isolated      instruction-like text in a source stays data
6. inference_not_fact      claims backed only by inference read as Partial
7. sources_fresh           an expired source makes the copy Partial

Blocked means the copy cannot ship as is.  Partial means a person decides.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Any

import evidence
from evidence import EvidenceError, GateResult

SOURCE_FIELDS = frozenset({"source_ref", "source_type", "support_type", "text", "freshness"})
INPUT_FIELDS = frozenset({"copy", "sources"})
# Numbers with optional decimals, thousands separators and percent.
NUMBER_RE = re.compile(r"\d[\d.,]*%?")
QUOTE_RE = re.compile(r"[\"“«]([^\"”»]{12,})[\"”»]")
ILLUSTRATIVE_MARKERS = (
    "ilustrativo",
    "ilustrativa",
    "ejemplo ilustrativo",
    "dramatizacion",
    "illustrative",
    "dramatization",
    "not a real testimonial",
    "no es un testimonio real",
)
QUOTE_SOURCE_TYPES = frozenset({"interview", "transcript", "survey", "review", "social_comment", "user_statement"})
CHECKS = (
    "sources_present",
    "numbers_sourced",
    "testimonial_labeled",
    "no_ai_testimony",
    "untrusted_isolated",
    "inference_not_fact",
    "sources_fresh",
)


def _numbers(text: str) -> set[str]:
    return {m.group(0).rstrip(".,").replace(",", "") for m in NUMBER_RE.finditer(text)}


def validate_input(raw: Any) -> dict[str, Any]:
    value = evidence._object(raw, "grounding")
    evidence._no_unknown(value, INPUT_FIELDS, "grounding")
    evidence._text(value.get("copy"), "copy")
    for item in evidence._list(value.get("sources", []), "sources"):
        source = evidence._object(item, "source")
        evidence._no_unknown(source, SOURCE_FIELDS, "source")
        evidence._text(source.get("source_ref"), "source.source_ref")
        evidence._choice(source.get("source_type"), evidence.SOURCE_TYPES, "source.source_type")
        evidence._choice(source.get("support_type", "observed"), evidence.SUPPORT_TYPES, "source.support_type")
        evidence._text(source.get("text"), "source.text")
        if source.get("freshness") is not None:
            evidence.validate_freshness(source["freshness"])
    return value


def check(raw: Any, today: dt.date) -> dict[str, Any]:
    value = validate_input(raw)
    copy = value["copy"]
    sources: list[dict[str, Any]] = value.get("sources", [])
    plain_copy = evidence.normalize(copy)
    results: dict[str, GateResult] = {}

    def put(name: str, reasons: list[str], *, partial: bool = False) -> None:
        results[name] = evidence._gate(name, reasons, partial=partial)

    numbers = _numbers(copy)
    quotes = [m.group(1).strip() for m in QUOTE_RE.finditer(copy)]
    has_claims = bool(numbers or quotes)
    put("sources_present", ["copy makes claims but cites no source"] if has_claims and not sources else [])

    source_numbers: set[str] = set()
    for source in sources:
        source_numbers |= _numbers(source["text"])
    put("numbers_sourced", [f"number {n} is not in any source" for n in sorted(numbers - source_numbers)])

    labeled = any(marker in plain_copy for marker in ILLUSTRATIVE_MARKERS)
    unverified: list[str] = []
    ai_backed: list[str] = []
    for quote in quotes:
        needle = evidence.normalize(quote)
        backers = [s for s in sources if needle and needle in evidence.normalize(s["text"])]
        real = [s for s in backers if s["source_type"] in QUOTE_SOURCE_TYPES and s.get("support_type", "observed") != "inferred"]
        if any(s["source_type"] == "kokoro_inference" for s in backers) and not real:
            ai_backed.append(quote)
        if not real and not labeled:
            unverified.append(quote)
    put("testimonial_labeled", [f"quote reads as a testimonial but no verified source says it: {q[:60]}" for q in unverified])
    put("no_ai_testimony", [f"an AI-written phrase cannot be presented as testimony: {q[:60]}" for q in ai_backed if not labeled])

    flagged = [s["source_ref"] for s in sources if s["source_type"] in evidence.UNTRUSTED_SOURCE_TYPES and evidence.instruction_like(s["text"])]
    put("untrusted_isolated", [f"{ref} contains instruction-like text; kept as data, not obeyed" for ref in flagged], partial=True)

    trusted = [s for s in sources if s.get("support_type", "observed") != "inferred" and s["source_type"] != "kokoro_inference"]
    put("inference_not_fact", ["every source is an inference; present the claim as a hypothesis"] if sources and not trusted else [], partial=True)

    expired = [s["source_ref"] for s in sources if s.get("freshness") and evidence.freshness_status(s["freshness"], today) == "expired"]
    put("sources_fresh", [f"{ref} is past its refresh date" for ref in expired], partial=True)

    ordered = [results[name] for name in CHECKS]
    if any(r.status == "Blocked" for r in ordered):
        status = "Blocked"
    elif any(r.status == "Partial" for r in ordered):
        status = "Partial"
    else:
        status = "Pass"
    reasons = tuple(reason for r in ordered for reason in r.reasons)
    return {
        "gate": GateResult("GATE-GROUNDED", status, reasons).as_dict(),
        "checks": [r.as_dict() for r in ordered],
        "mutates": False,
    }


def gate_grounded(raw: Any, today: dt.date) -> GateResult:
    gate = check(raw, today)["gate"]
    return GateResult(gate["gate"], gate["status"], tuple(gate["reasons"]))


__all__ = ["CHECKS", "EvidenceError", "check", "gate_grounded", "validate_input"]
