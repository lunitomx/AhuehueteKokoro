"""Deterministic domain contract for the E58 growth-diagnosis workflow."""

from __future__ import annotations

from typing import Any, cast

SCHEMA_VERSION = 1
LAYERS = ("suelo", "semilla", "germinacion", "cosecha")
ALLOWED_ROUTES = frozenset(
    {
        "/kokoro-diagnose",
        "/kokoro-canvas",
        "/kokoro-forces",
        "/kokoro-validate",
        "/kokoro-campaign-lab-run",
        "/kokoro-ads",
        "/kokoro-gads",
        "/kokoro-factory",
        "/kokoro-funnel",
        "/kokoro-rhythm",
        "/kokoro-tracking-check",
    }
)
SEVERITIES = frozenset({"low", "medium", "high", "critical"})
LAYER_STATUSES = frozenset({"known", "partial", "unknown"})


class GrowthContractError(ValueError):
    """A deterministic domain-contract failure safe to show without payloads."""


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GrowthContractError(f"{label} must be an object")
    return cast(dict[str, Any], value)


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GrowthContractError(f"{label} must be a non-empty string")
    return value


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise GrowthContractError(f"{label} must be a list of strings")
    items = cast(list[Any], value)
    if any(not isinstance(item, str) for item in items):
        raise GrowthContractError(f"{label} must be a list of strings")
    return cast(list[str], items)


def _layers(value: Any) -> dict[str, dict[str, Any]]:
    layers = _object(value, "system_read")
    if set(layers) != set(LAYERS):
        raise GrowthContractError(
            "system_read must contain exactly the four Kokoro layers"
        )
    normalized: dict[str, dict[str, Any]] = {}
    for layer in LAYERS:
        item = _object(layers[layer], layer)
        if item.get("status") not in LAYER_STATUSES:
            raise GrowthContractError(f"{layer}.status is invalid")
        normalized[layer] = {
            "status": item["status"],
            "source_refs": _string_list(
                item.get("source_refs", []), f"{layer}.source_refs"
            ),
            "unknowns": _string_list(item.get("unknowns", []), f"{layer}.unknowns"),
        }
    return normalized


def _common(value: dict[str, Any], node: str) -> None:
    if value.get("schema_version") != SCHEMA_VERSION or value.get("node") != node:
        raise GrowthContractError("domain artifact schema or node is invalid")
    if value.get("status") != "accepted":
        raise GrowthContractError("domain artifact must be an accepted NodeResult")
    if value.get("external_actions") not in (None, []):
        raise GrowthContractError(
            "E58 domain artifacts cannot contain external actions"
        )


def validate_plan(value: dict[str, Any]) -> dict[str, Any]:
    _common(value, "plan")
    layers = _layers(value.get("system_read"))
    missing = _string_list(value.get("missing_inputs", []), "missing_inputs")
    next_input = value.get("next_critical_input")
    if next_input is not None:
        _string(next_input, "next_critical_input")
    return {"system_read": layers, "missing_inputs": missing}


def validate_execute(value: dict[str, Any]) -> dict[str, Any]:
    _common(value, "execute")
    layers = _layers(value.get("system_read"))
    bottleneck = _object(value.get("primary_bottleneck"), "primary_bottleneck")
    _string(bottleneck.get("name"), "primary_bottleneck.name")
    _string(bottleneck.get("reason"), "primary_bottleneck.reason")
    refs = _string_list(
        bottleneck.get("source_refs", []), "primary_bottleneck.source_refs"
    )
    confidence = bottleneck.get("confidence")
    if confidence not in {"low", "medium", "high"}:
        raise GrowthContractError("primary_bottleneck.confidence is invalid")
    route = _object(value.get("recommended_route"), "recommended_route")
    command = _string(route.get("command"), "recommended_route.command")
    if command not in ALLOWED_ROUTES:
        raise GrowthContractError("recommended_route.command is not allowed")
    _string(route.get("reason"), "recommended_route.reason")
    days_value = value.get("seven_day_plan")
    if not isinstance(days_value, list):
        raise GrowthContractError("seven_day_plan must contain exactly seven items")
    days = cast(list[Any], days_value)
    if len(days) != 7:
        raise GrowthContractError("seven_day_plan must contain exactly seven items")
    seen_days: set[int] = set()
    for item in days:
        day = _object(item, "seven_day_plan item")
        day_number = day.get("day")
        if (
            not isinstance(day_number, int)
            or isinstance(day_number, bool)
            or day_number not in range(1, 8)
        ):
            raise GrowthContractError(
                "seven_day_plan days must be unique integers 1 through 7"
            )
        if day_number in seen_days:
            raise GrowthContractError("seven_day_plan days must be unique")
        seen_days.add(day_number)
        _string(day.get("action"), "seven_day_plan.action")
        _string(day.get("metric"), "seven_day_plan.metric")
        _string(day.get("owner"), "seven_day_plan.owner")
    if seen_days != set(range(1, 8)):
        raise GrowthContractError("seven_day_plan must cover days 1 through 7")
    gate = _object(value.get("open_gate"), "open_gate")
    _string(gate.get("name"), "open_gate.name")
    _string(gate.get("reason"), "open_gate.reason")
    return {"system_read": layers, "source_refs": refs}


def validate_critique(value: dict[str, Any]) -> dict[str, Any]:
    _common(value, "critique")
    _layers(value.get("system_read"))
    findings_value = value.get("findings")
    if not isinstance(findings_value, list):
        raise GrowthContractError("critique.findings must be a list")
    findings = cast(list[Any], findings_value)
    for finding in findings:
        item = _object(finding, "critique finding")
        if item.get("severity") not in SEVERITIES:
            raise GrowthContractError("critique finding severity is invalid")
        _string(item.get("claim"), "critique finding.claim")
        refs = item.get("source_refs", item.get("evidence_refs", []))
        _string_list(refs, "critique finding.source_refs")
    _string(value.get("summary"), "critique.summary")
    return {"finding_count": len(findings)}


def validate_verify(value: dict[str, Any]) -> dict[str, Any]:
    _common(value, "verify")
    verdict = value.get("verdict", value.get("verification_verdict"))
    if verdict not in {"pass", "fail"}:
        raise GrowthContractError("verify verdict must be pass or fail")
    checks = _object(value.get("deterministic_checks"), "deterministic_checks")
    required = ("required_sections", "evidence", "privacy", "external_actions")
    if any(key not in checks for key in required):
        raise GrowthContractError("verify deterministic_checks is incomplete")
    if any(not isinstance(checks[key], bool) for key in required):
        raise GrowthContractError("verify deterministic_checks values must be booleans")
    if verdict == "pass" and not all(checks[key] for key in required):
        raise GrowthContractError("verify pass requires every deterministic check")
    _string(value.get("summary"), "verify.summary")
    return {"verdict": verdict, "checks": checks}


def validate_node_artifact(node: str, value: dict[str, Any]) -> dict[str, Any]:
    """Validate one accepted domain artifact and return normalized gate data."""

    if node == "plan":
        return validate_plan(value)
    if node == "execute":
        return validate_execute(value)
    if node == "critique":
        return validate_critique(value)
    if node == "verify":
        return validate_verify(value)
    if node == "human_gate":
        return {}
    raise GrowthContractError("unsupported growth-diagnosis node")


def render_execute_markdown(value: dict[str, Any]) -> str:
    """Render canonical execute JSON into the existing Spanish output contract."""

    normalized = validate_execute(value)
    layers = value["system_read"]
    lines = [
        "## Diagnostico de Crecimiento",
        "",
        "### Lectura del Sistema",
        "| Capa | Estado | Evidencia |",
        "|------|--------|-----------|",
    ]
    for layer in LAYERS:
        item = layers[layer]
        evidence = ", ".join(item["source_refs"]) or "No detectado"
        lines.append(f"| {layer.title()} | {item['status']} | {evidence} |")
    bottleneck = value["primary_bottleneck"]
    route = value["recommended_route"]
    lines.extend(
        [
            "",
            "### Cuello de Botella Principal",
            str(bottleneck["name"]),
            "",
            "### Ruta Recomendada",
            f"{route['command']} porque {route['reason']}.",
            "",
            "### Plan de 7 Dias",
            "| Dia | Accion | Metrica | Owner |",
            "|-----|--------|---------|-------|",
        ]
    )
    for item in sorted(value["seven_day_plan"], key=lambda day: day["day"]):
        lines.append(
            f"| {item['day']} | {item['action']} | {item['metric']} | {item['owner']} |"
        )
    gate = value["open_gate"]
    lines.extend(["", "### Gate Abierto", f"{gate['name']}: {gate['reason']}", ""])
    _ = normalized
    return "\n".join(lines)


def render_mode_message(graph_available: bool, reason: str = "") -> str:
    if graph_available:
        return "Modo: grafo gobernado"
    suffix = f" Razón: {reason}." if reason else ""
    return f"Modo: directo compatible.{suffix}"
