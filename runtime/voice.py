#!/usr/bin/env python3
"""Voice lint: Kokoro vocabulary, generic AI phrasing, testimony that may be invented.

Advisory and read-only.  It never rewrites copy: it points at a phrase and
suggests the Kokoro word, and a person decides.  The vocabulary table mirrors
the one in CLAUDE.md; a word used inside a quote from a real source is the
guest's voice and is not flagged.
"""

from __future__ import annotations

import re
from typing import Any

import evidence
from grounding import ILLUSTRATIVE_MARKERS, QUOTE_RE

# (pattern on normalized text, suggestion).  Spanish and English.
VOCABULARY = (
    (r"\bprecios?\b", "inversion"),
    (r"\bproductos?\b", "creacion"),
    (r"\bgratis\b", "cortesia / de regalo"),
    (r"\bdescuentos?\b", "condiciones especiales"),
    (r"\bclientes?\b", "invitado / persona"),
    (r"\bcomprar?\b", "adquirir / elegir"),
    (r"\bbarat[oa]s?\b", "accesible"),
    (r"\bvender\b", "compartir / invitar"),
    (r"\bproblemas?\b", "oportunidad / reto"),
    (r"\bgastar\b", "invertir"),
    (r"\bprice\b", "investment"),
    (r"\bfree\b", "complimentary"),
    (r"\bdiscount\b", "special conditions"),
    (r"\bcheap\b", "accessible"),
)
GENERIC_PHRASES = (
    r"\bhacks?\b",
    r"\bgrowth hacking\b",
    r"\bmonetizar\b",
    r"\bescalar rapido\b",
    r"\b\d+ tips\b",
    r"\bduplica tus ventas\b",
    r"\bresultados garantizados\b",
    r"\ben el mundo actual\b",
    r"\bno es solo .{1,40}, es\b",
    r"\bdesbloquea\b",
    r"\bpotencia tu\b",
    r"\bllev(?:a|ar) tu negocio al siguiente nivel\b",
    r"\bin today'?s (?:fast-paced|digital) world\b",
    r"\bunlock\b",
    r"\bgame[- ]changer\b",
    r"\btake your business to the next level\b",
)


def lint(copy: str) -> dict[str, Any]:
    text = evidence._text(copy, "copy")
    quoted = " ".join(m.group(1) for m in QUOTE_RE.finditer(text))
    outside = evidence.normalize(QUOTE_RE.sub(" ", text))
    findings: list[dict[str, str]] = []
    for pattern, suggestion in VOCABULARY:
        for match in re.finditer(pattern, outside):
            findings.append({"kind": "vocabulary", "found": match.group(0), "suggest": suggestion})
    for pattern in GENERIC_PHRASES:
        for match in re.finditer(pattern, outside):
            findings.append({"kind": "generic_ai", "found": match.group(0), "suggest": "say what this person gains, concretely"})
    plain = evidence.normalize(text)
    if quoted and not any(marker in plain for marker in ILLUSTRATIVE_MARKERS):
        findings.append(
            {
                "kind": "possible_testimony",
                "found": quoted[:80],
                "suggest": "run grounding check with the source, or label it as illustrative",
            }
        )
    return {
        "status": "Partial" if findings else "Pass",
        "findings": findings,
        "mutates": False,
    }
