"""Secret-safe readiness diagnostics for the Meta Ads connector."""

from __future__ import annotations

import argparse
import json
import os
import stat
from collections.abc import Mapping
from pathlib import Path
from typing import Literal, TypedDict

REQUIRED_ENVIRONMENT = (
    "FACEBOOK_ACCESS_TOKEN",
    "FACEBOOK_APP_ID",
    "FACEBOOK_APP_SECRET",
)


class DiagnosticResult(TypedDict):
    """Stable, secret-free connector readiness result."""

    missing: list[str]
    status: Literal["ready", "unconfigured"]


def load_environment_file(path: Path) -> dict[str, str]:
    """Parse an allowlisted environment file without executing shell syntax."""
    if not path.exists():
        return {}
    if path.is_symlink():
        raise ValueError("credential file must not be a symlink")
    if not path.is_file():
        raise ValueError(f"credential path is not a regular file: {path}")
    if os.name == "posix" and stat.S_IMODE(path.stat().st_mode) & 0o077:
        raise ValueError("credential file permissions must be 0600")

    allowed = set(REQUIRED_ENVIRONMENT)
    parsed: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"invalid credential line: {line_number}")
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in allowed:
            raise ValueError(f"unsupported credential name on line {line_number}")
        if key in parsed:
            raise ValueError(f"duplicate credential name on line {line_number}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        parsed[key] = value
    return parsed


def merged_environment(
    environment: Mapping[str, str],
    credential_file: Path | None,
) -> dict[str, str]:
    """Merge local credentials without overriding explicit process values."""
    merged = dict(environment)
    if credential_file is not None:
        for key, value in load_environment_file(credential_file).items():
            merged.setdefault(key, value)
    return merged


def diagnose(environment: Mapping[str, str] | None = None) -> DiagnosticResult:
    """Return readiness without reading or revealing credential values."""
    source = os.environ if environment is None else environment
    missing = [
        name for name in REQUIRED_ENVIRONMENT if not source.get(name, "").strip()
    ]
    return {
        "missing": missing,
        "status": "unconfigured" if missing else "ready",
    }


def main() -> None:
    """Print a human or JSON readiness result; unconfigured is not an error."""
    parser = argparse.ArgumentParser(prog="kokoro-meta-ads-doctor")
    parser.add_argument("--json", action="store_true", help="Emit compact JSON")
    parser.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="Read credentials from a local 0600 file",
    )
    args = parser.parse_args()
    try:
        environment = merged_environment(os.environ, args.env_file)
    except ValueError as error:
        if args.json:
            print(json.dumps({"error": str(error), "status": "unsafe_configuration"}))
        else:
            print(f"Meta Ads connector: unsafe configuration ({error})")
        raise SystemExit(2) from error
    result = diagnose(environment)

    if args.json:
        print(json.dumps(result, sort_keys=True))
        return

    if result["status"] == "ready":
        print("Meta Ads connector: ready")
        return

    missing = ", ".join(str(name) for name in result["missing"])
    print(f"Meta Ads connector: unconfigured (missing: {missing})")


if __name__ == "__main__":
    main()
