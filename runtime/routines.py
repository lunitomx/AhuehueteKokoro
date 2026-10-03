#!/usr/bin/env python3
"""Routine recipes: declarative, never scheduled.

A recipe says what a routine reads, what it may write, and what it needs.
Kokoro does not install cron jobs, hooks or background agents: a person runs
a routine when they choose, and `cadence_suggestion` is only a suggestion.
Any recipe that writes needs `requires_action_permission: true`, so the run
asks before it changes anything.
"""

from __future__ import annotations

import re
from typing import Any

import evidence
from evidence import EvidenceError

RECIPE_FIELDS = frozenset(
    {
        "name",
        "purpose",
        "cadence_suggestion",
        "reads",
        "writes",
        "requires_action_permission",
        "required_connectors",
        "privacy_scope",
        "command",
    }
)
CADENCES = ("daily", "weekly", "biweekly", "monthly", "on_demand", "event_driven")
PRIVACY_SCOPES = ("team", "personal")
CONNECTORS = ("meta_ads", "google_ads", "ga4", "search_console", "crm")
NAME_RE = re.compile(r"^[a-z][a-z0-9-]{2,40}$")
# Only workspace paths under .kokoro/shared or .kokoro/private, never the package.
PATH_RE = re.compile(r"^\.kokoro/(?:shared|private)/[A-Za-z0-9_./*-]+$")
FORBIDDEN_WRITES = re.compile(r"(?:^|/)(?:skills|commands|agents|knowledge)(?:/|$)|\.claude/|CLAUDE\.md")


def validate_recipe(raw: Any) -> dict[str, Any]:
    recipe = evidence._object(raw, "recipe")
    evidence._no_unknown(recipe, RECIPE_FIELDS, "recipe")
    name = evidence._text(recipe.get("name"), "name")
    if not NAME_RE.fullmatch(name):
        raise EvidenceError("name must be a short kebab-case slug")
    evidence._text(recipe.get("purpose"), "purpose")
    evidence._choice(recipe.get("cadence_suggestion"), CADENCES, "cadence_suggestion")
    reads = evidence._text_list(recipe.get("reads"), "reads")
    writes = evidence._text_list(recipe.get("writes", []), "writes")
    for path in reads + writes:
        if not PATH_RE.fullmatch(path) or ".." in path:
            raise EvidenceError(f"{path} must be a workspace path under .kokoro/shared or .kokoro/private")
    for path in writes:
        if FORBIDDEN_WRITES.search(path):
            raise EvidenceError(f"a routine never writes skills, commands or rules: {path}")
    permission = recipe.get("requires_action_permission")
    if not isinstance(permission, bool):
        raise EvidenceError("requires_action_permission must be true or false")
    if writes and not permission:
        raise EvidenceError("a routine that writes must require action permission")
    for connector in evidence._list(recipe.get("required_connectors", []), "required_connectors"):
        evidence._choice(connector, CONNECTORS, "required_connectors")
    scope = evidence._choice(recipe.get("privacy_scope"), PRIVACY_SCOPES, "privacy_scope")
    if scope == "team" and any(p.startswith(".kokoro/private/") for p in writes):
        raise EvidenceError("a team-scope routine cannot write private paths")
    command = evidence._text(recipe.get("command"), "command")
    if not evidence.SKILL_RE.fullmatch(command):
        raise EvidenceError("command must be a Kokoro slash command such as /kokoro-refresh")
    return recipe


EVIDENCE_VIEWS = ".kokoro/shared/views/evidence/*.yaml"
EVIDENCE_EVENTS = ".kokoro/shared/events/evidence/*.json"

BUILTIN_RECIPES: tuple[dict[str, Any], ...] = (
    {
        "name": "freshness-review",
        "purpose": "List artifacts and validations that expired or lost an upstream; recommend, never refresh.",
        "cadence_suggestion": "weekly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [],
        "requires_action_permission": False,
        "required_connectors": [],
        "privacy_scope": "team",
        "command": "/kokoro-refresh",
    },
    {
        "name": "loop-rollup",
        "purpose": "Group open questions by guest and territory and propose merges for a person to approve.",
        "cadence_suggestion": "weekly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [EVIDENCE_EVENTS],
        "requires_action_permission": True,
        "required_connectors": [],
        "privacy_scope": "team",
        "command": "/kokoro-loop-rollup",
    },
    {
        "name": "revalidation-queue",
        "purpose": "Show validations past their refresh date and draft the revalidation plan.",
        "cadence_suggestion": "monthly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [],
        "requires_action_permission": False,
        "required_connectors": [],
        "privacy_scope": "team",
        "command": "/kokoro-revalidate",
    },
    {
        "name": "idea-harvest",
        "purpose": "Capture raw ideas from sessions and sources into the idea bank, without judging them.",
        "cadence_suggestion": "weekly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [EVIDENCE_EVENTS],
        "requires_action_permission": True,
        "required_connectors": [],
        "privacy_scope": "team",
        "command": "/kokoro-idea-harvest",
    },
    {
        "name": "creative-signal-read",
        "purpose": "Read live campaign results against the account baseline and draft the next iteration brief.",
        "cadence_suggestion": "weekly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [],
        "requires_action_permission": False,
        "required_connectors": ["meta_ads"],
        "privacy_scope": "team",
        "command": "/kokoro-iterate",
    },
    {
        "name": "learning-review",
        "purpose": "Show pending learning traces so a person promotes, rejects or leaves them local.",
        "cadence_suggestion": "biweekly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [EVIDENCE_EVENTS],
        "requires_action_permission": True,
        "required_connectors": [],
        "privacy_scope": "team",
        "command": "/kokoro-learn",
    },
    {
        "name": "weekly-scorecard",
        "purpose": "Join the evidence summary with the 90-minute weekly rhythm.",
        "cadence_suggestion": "weekly",
        "reads": [EVIDENCE_VIEWS],
        "writes": [],
        "requires_action_permission": False,
        "required_connectors": [],
        "privacy_scope": "team",
        "command": "/kokoro-rhythm",
    },
)


def recipes() -> list[dict[str, Any]]:
    return [validate_recipe(dict(r)) for r in BUILTIN_RECIPES]


def find(name: str) -> dict[str, Any]:
    for recipe in recipes():
        if recipe["name"] == name:
            return recipe
    raise EvidenceError(f"unknown routine: {name}")
