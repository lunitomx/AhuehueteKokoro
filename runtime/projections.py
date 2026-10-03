#!/usr/bin/env python3
"""Domain registry for the evidence ledger.

The ledger knows the hash chain and the core evidence events.  Each domain
module (freshness, ideas, learning, creative) owns its contract: its state,
its reducers and its views.  This module only joins them, so neither the
ledger nor agent_graph grows into a monolith.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

import creative
import freshness
import ideas
import learning

DOMAINS = (freshness, ideas, learning, creative)


def _join_reducers() -> dict[str, Any]:
    joined: dict[str, Any] = {}
    for module in DOMAINS:
        overlap = set(joined) & set(module.REDUCERS)
        if overlap:
            raise RuntimeError(f"event types claimed twice: {sorted(overlap)}")
        joined.update(module.REDUCERS)
    return joined


REDUCERS = _join_reducers()


def empty_state() -> dict[str, Any]:
    state: dict[str, Any] = {}
    for module in DOMAINS:
        state.update(module.empty_state())
    return state


def render(state: dict[str, Any]) -> dict[str, Any]:
    views: dict[str, Any] = {}
    for module in DOMAINS:
        views.update(module.render(state))
    return views


def check_dependencies(state: dict[str, Any], node_id: str, block: dict[str, Any]) -> None:
    freshness.check_dependencies(state, node_id, block)


def _share(part: int, whole: int) -> float | None:
    return round(part / whole, 3) if whole else None


def summary(state: dict[str, Any], today: dt.date) -> dict[str, Any]:
    """System health in numbers.  Read-only: it never changes a record."""

    loops = list(state["loops"].values())
    validations = list(state["validations"].values())
    resolved = [v for v in validations if v["current_state"] != "stale"]
    fresh = freshness.report(state, today)
    attention = fresh["needs_attention"]
    idea_counts: dict[str, int] = {status: 0 for status in ideas.IDEA_STATUSES}
    for idea in state["ideas"].values():
        idea_counts[idea["status"]] += 1
    iterations = list(state["iterations"].values())
    return {
        "today": today.isoformat(),
        "mutates": False,
        "loops": {
            "open": sum(1 for loop in loops if loop["status"] not in ("closed", "archived")),
            "closed": sum(1 for loop in loops if loop["status"] == "closed"),
        },
        "validations": {
            "total": len(validations),
            "invalidated_share": _share(sum(1 for v in resolved if v["current_state"] == "invalidated"), len(resolved)),
            "inconclusive_share": _share(sum(1 for v in resolved if v["current_state"] == "inconclusive"), len(resolved)),
            "overdue_revalidations": sorted(
                n["id"] for n in attention if n["node_type"] == "validation" and n["calendar"] == "expired"
            ),
        },
        "artifacts": {
            "total": len(state["artifacts"]),
            "needing_attention": sorted(n["id"] for n in attention if n["node_type"] == "artifact"),
        },
        "ideas": idea_counts,
        "learning": {
            "pending_traces": sum(1 for t in state["traces"].values() if t["status"] == "captured"),
            "promoted_traces": sum(1 for t in state["traces"].values() if t["status"] == "promoted"),
        },
        "creative": {
            "iterations": len(iterations),
            "single_variable_share": _share(sum(1 for i in iterations if i["controlled_test"]), len(iterations)),
        },
    }
