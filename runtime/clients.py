#!/usr/bin/env python3
"""Guest registry (`.kokoro/clients.json`) for the public Kokoro package.

Standard library only.  The registry lives in the private project workspace,
never in the package.  Every write validates the whole registry first, rejects
secret-like values and replaces the file atomically.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, cast

import agent_graph

REGISTRY_VERSION = 1
REGISTRY_RELATIVE = Path(".kokoro") / "clients.json"
SESSION_LOG_KEY = "session_log"
SESSION_LOG_LIMIT = 20
CLIENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,79}$")
METADATA_KEY_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
STRING_FIELDS = ("name", "group", "description", "campaign_folder", "industry")
OPTIONAL_STRING_FIELDS = ("context_file", "coaching_state_path")
LIST_FIELDS = ("repos", "segments")
TIMESTAMP_FIELDS = ("created", "updated")
PROFILE_FIELDS = frozenset(
    ("id", "metadata")
    + STRING_FIELDS
    + OPTIONAL_STRING_FIELDS
    + LIST_FIELDS
    + TIMESTAMP_FIELDS
)
INPUT_FIELDS = PROFILE_FIELDS - frozenset(TIMESTAMP_FIELDS)


class ClientError(ValueError):
    """Raised when a guest registry operation would be unsafe or malformed."""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slugify(name: str) -> str:
    """Derive a stable guest id from a display name."""

    slug = re.sub(r"[^a-z0-9_-]+", "-", name.strip().lower()).strip("-")
    if not CLIENT_ID_RE.fullmatch(slug):
        raise ClientError("name cannot be converted into a valid guest id")
    return slug


def _string(value: Any, field: str, *, allow_empty: bool = True) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ClientError(f"{field} must be a non-empty string")
    return value


def _relative_path(value: Any, field: str) -> str:
    text = _string(value, field)
    if text and (Path(text).is_absolute() or text.startswith("~")):
        raise ClientError(f"{field} must be a project-relative path")
    return text


def _string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list):
        raise ClientError(f"{field} must be a list of strings")
    items = cast(list[Any], value)
    return [_relative_path(item, field) if field == "repos" else _string(item, field) for item in items]


def _timestamp(value: Any, field: str) -> str:
    text = _string(value, field, allow_empty=False)
    try:
        dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ClientError(f"{field} must be an ISO 8601 timestamp") from exc
    return text


def validate_profile(raw: Any) -> dict[str, Any]:
    """Return a normalized profile or fail closed on any unknown or bad field."""

    if not isinstance(raw, dict):
        raise ClientError("guest profile must be an object")
    value = cast(dict[str, Any], raw)
    unknown = sorted(set(value) - PROFILE_FIELDS)
    if unknown:
        raise ClientError("unknown guest fields: " + ", ".join(unknown))
    client_id = _string(value.get("id"), "id", allow_empty=False)
    if not CLIENT_ID_RE.fullmatch(client_id):
        raise ClientError("id must be a lowercase slug")
    profile: dict[str, Any] = {"id": client_id}
    for field in STRING_FIELDS:
        allow_empty = field not in {"name", "group"}
        profile[field] = _string(value.get(field, ""), field, allow_empty=allow_empty)
    for field in OPTIONAL_STRING_FIELDS:
        item = value.get(field)
        profile[field] = None if item is None else _relative_path(item, field)
    profile["campaign_folder"] = _relative_path(profile["campaign_folder"], "campaign_folder")
    for field in LIST_FIELDS:
        profile[field] = _string_list(value.get(field, []), field)
    for field in TIMESTAMP_FIELDS:
        profile[field] = _timestamp(value.get(field), field)
    metadata = value.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ClientError("metadata must be an object")
    profile["metadata"] = metadata
    if agent_graph._contains_secret_like(profile):
        raise ClientError("guest profile contains secret-like content")
    return profile


def validate_registry(raw: Any) -> dict[str, Any]:
    """Validate the full registry, including unique guest ids."""

    if not isinstance(raw, dict):
        raise ClientError("registry must be an object")
    value = cast(dict[str, Any], raw)
    if value.get("version") != REGISTRY_VERSION:
        raise ClientError("unsupported registry version")
    clients_raw = value.get("clients")
    if not isinstance(clients_raw, list):
        raise ClientError("registry.clients must be a list")
    clients = [validate_profile(item) for item in cast(list[Any], clients_raw)]
    ids = [client["id"] for client in clients]
    if len(ids) != len(set(ids)):
        raise ClientError("registry contains duplicated guest ids")
    return {
        "version": REGISTRY_VERSION,
        "clients": clients,
        "created": _timestamp(value.get("created"), "created"),
        "updated": _timestamp(value.get("updated"), "updated"),
    }


def create_empty_registry() -> dict[str, Any]:
    now = _now()
    return {"version": REGISTRY_VERSION, "clients": [], "created": now, "updated": now}


def registry_path(project: Path) -> Path:
    return project / REGISTRY_RELATIVE


def load_registry(project: Path) -> dict[str, Any] | None:
    """Return the validated registry, or None when the project has none yet."""

    path = registry_path(project)
    if path.is_symlink():
        raise ClientError("registry path must not be a symlink")
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ClientError("registry is not readable JSON") from exc
    return validate_registry(raw)


def save_registry(project: Path, registry: dict[str, Any]) -> Path:
    """Validate and atomically persist the registry in a private workspace."""

    workspace = agent_graph._validate_workspace(project)
    validated = validate_registry(registry)
    path = registry_path(workspace)
    # A symlinked `.kokoro` would send the registry outside the workspace.
    agent_graph._reject_symlink_components(path, workspace)
    data = json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True)
    agent_graph._atomic_write(path, data.encode("utf-8") + b"\n")
    return path


def find_by_id(registry: dict[str, Any], client_id: str) -> dict[str, Any] | None:
    return next((c for c in registry["clients"] if c["id"] == client_id), None)


def find_by_name(registry: dict[str, Any], query: str) -> dict[str, Any] | None:
    """Return the first guest whose name contains query, ignoring case."""

    needle = query.strip().lower()
    if not needle:
        raise ClientError("name query must not be empty")
    return next((c for c in registry["clients"] if needle in c["name"].lower()), None)


def find_by_segment(registry: dict[str, Any], segment: str) -> list[dict[str, Any]]:
    needle = segment.strip().lower()
    return [
        c for c in registry["clients"] if needle in (s.lower() for s in c["segments"])
    ]


def list_groups(registry: dict[str, Any]) -> list[str]:
    return sorted({c["group"] for c in registry["clients"]})


def _load_or_empty(project: Path) -> dict[str, Any]:
    return load_registry(project) or create_empty_registry()


def _require(registry: dict[str, Any], client_id: str) -> dict[str, Any]:
    client = find_by_id(registry, client_id)
    if client is None:
        raise ClientError(f"guest not found: {client_id}")
    return client


def create_client(project: Path, raw: Any) -> dict[str, Any]:
    """Register one guest; the id is derived from the name when absent."""

    if not isinstance(raw, dict):
        raise ClientError("guest input must be an object")
    value = dict(cast(dict[str, Any], raw))
    unknown = sorted(set(value) - INPUT_FIELDS)
    if unknown:
        raise ClientError("unknown or automatic guest fields: " + ", ".join(unknown))
    value.setdefault("id", slugify(_string(value.get("name"), "name", allow_empty=False)))
    now = _now()
    profile = validate_profile({**value, "created": now, "updated": now})
    registry = _load_or_empty(project)
    if find_by_id(registry, profile["id"]) is not None:
        raise ClientError(f"guest already exists: {profile['id']}")
    registry["clients"].append(profile)
    registry["updated"] = now
    save_registry(project, registry)
    return profile


def set_metadata(project: Path, client_id: str, key: str, value: Any) -> dict[str, Any]:
    """Replace one metadata key; session_log has its own append operation."""

    if not METADATA_KEY_RE.fullmatch(key) or key == SESSION_LOG_KEY:
        raise ClientError("metadata key is invalid or reserved")
    registry = _load_or_empty(project)
    client = _require(registry, client_id)
    client["metadata"][key] = value
    return _touch_and_save(project, registry, client)


def append_session_log(project: Path, client_id: str, entry: Any) -> dict[str, Any]:
    """Insert the newest entry first and keep the latest SESSION_LOG_LIMIT."""

    if not isinstance(entry, dict):
        raise ClientError("session log entry must be an object")
    entry_value = cast(dict[str, Any], entry)
    for field in ("date", "type", "skill", "summary"):
        _string(entry_value.get(field), f"entry.{field}", allow_empty=False)
    registry = _load_or_empty(project)
    client = _require(registry, client_id)
    entry_value["client_id"] = client_id
    log = client["metadata"].get(SESSION_LOG_KEY, [])
    if not isinstance(log, list):
        raise ClientError("existing session_log is malformed")
    client["metadata"][SESSION_LOG_KEY] = ([entry_value] + log)[:SESSION_LOG_LIMIT]
    return _touch_and_save(project, registry, client)


def _touch_and_save(
    project: Path, registry: dict[str, Any], client: dict[str, Any]
) -> dict[str, Any]:
    now = _now()
    client["updated"] = now
    registry["updated"] = now
    save_registry(project, registry)
    return client
