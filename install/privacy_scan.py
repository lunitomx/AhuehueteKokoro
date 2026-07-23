#!/usr/bin/env python3
"""Scan a Kokoro release tree without ever printing detected secret values."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

GENERATED_DIRECTORIES = {
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
PRIVATE_DIRECTORIES = {
    ".kokoro",
    ".rai",
    ".raise",
    "clientes",
    "clients",
    "deliverables",
    "exports",
    "generated",
    "private",
    "reports",
}
SENSITIVE_SUFFIXES = {".csv", ".key", ".p12", ".pem", ".pfx", ".xls", ".xlsx"}
SENSITIVE_FILENAMES = {
    ".ds_store",
    "credentials.json",
    "service_account.json",
    "token.json",
}
HIGH_CONFIDENCE_PATTERNS = {
    "anthropic_" + "api_key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    "aws_" + "access_key": re.compile(r"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    "github_" + "token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,}"),
    "github_fine_grained_" + "token": re.compile(r"github_pat_[A-Za-z0-9_]{50,}"),
    "google_" + "api_key": re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    "google_oauth_" + "secret": re.compile(r"GOCSPX-[A-Za-z0-9_-]{20,}"),
    "meta_access_" + "token": re.compile(r"EAA[A-Za-z0-9]{40,}"),
    "openai_" + "api_key": re.compile(r"sk-(?:proj|svcacct)-[A-Za-z0-9_-]{20,}"),
    "private_" + "key": re.compile(r"-{5}BEGIN [A-Z0-9 ]*PRIVATE KEY-{5}"),
}
PRIVATE_PATH_PATTERNS = (
    re.compile(r"/" + r"Users/[A-Za-z0-9._-]+/"),
    re.compile(r"/" + r"home/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+\\", re.IGNORECASE),
)
PRIVATE_SOURCE_MARKERS = ("Raiz" + "Ancestral", "soya" + "huehuetedigital")
SECRET_ASSIGNMENT = re.compile(
    r"""
    ^\s*(?:export\s+)?[\"']?
    [A-Za-z][A-Za-z0-9_.-]*
    (?:token|secret|password|passwd|api[_-]?key|private[_-]?key)
    [A-Za-z0-9_.-]*[\"']?\s*[:=]\s*(?P<value>.*?)\s*,?\s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)
PLACEHOLDER_PATTERNS = (
    re.compile(r"<[^>\r\n]+>"),
    re.compile(r"\$[A-Z][A-Z0-9_]*"),
    re.compile(r"\$\{[^}\r\n]+\}"),
    re.compile(r"\$\{\{[^}\r\n]+\}\}"),
    re.compile(
        r"(?:your|tu|example|dummy|placeholder|redacted|replace_me|changeme|not_set|unset)(?:[-_].*)?",
        re.IGNORECASE,
    ),
)


@dataclass(frozen=True, order=True)
class Finding:
    """A finding that is safe to print because it contains no matched content."""

    relative_path: str
    line_number: int | None
    label: str

    def render(self) -> str:
        location = self.relative_path
        if self.line_number is not None:
            location = f"{location}:{self.line_number}"
        return f"{location}:{self.label}"


def is_sensitive_filename(path: Path) -> bool:
    """Return whether a release file name is forbidden regardless of content."""
    lowered = path.name.lower()
    return (
        lowered in SENSITIVE_FILENAMES
        or lowered == ".env"
        or lowered.endswith(".env")
        or (".env." in lowered and not lowered.endswith(".env.template"))
        or lowered.startswith("client_secret")
        or lowered.startswith("service-account")
        or path.suffix.lower() in SENSITIVE_SUFFIXES
    )


def is_placeholder(raw_value: str) -> bool:
    """Accept empty or unmistakably inert values, never realistic literals."""
    value = raw_value.strip().rstrip(",").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    if not value:
        return True
    if value in {"...", "***"}:
        return True
    return any(pattern.fullmatch(value) for pattern in PLACEHOLDER_PATTERNS)


def content_findings(relative_path: str, text: str) -> list[Finding]:
    """Find secret signatures and private paths while retaining only locations."""
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in HIGH_CONFIDENCE_PATTERNS.items():
            if pattern.search(line):
                findings.append(Finding(relative_path, line_number, label))
        if any(pattern.search(line) for pattern in PRIVATE_PATH_PATTERNS):
            findings.append(Finding(relative_path, line_number, "private_path"))
        if any(marker in line for marker in PRIVATE_SOURCE_MARKERS):
            findings.append(Finding(relative_path, line_number, "private_source"))

        assignment = SECRET_ASSIGNMENT.match(line)
        if assignment and not is_placeholder(assignment.group("value")):
            findings.append(Finding(relative_path, line_number, "secret_assignment"))
    return findings


def scan_tree(root: Path) -> list[Finding]:
    """Return stable, deduplicated release findings for a directory tree."""
    findings: set[Finding] = set()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        if any(part in GENERATED_DIRECTORIES for part in relative.parts):
            continue
        private_prefix = "rai" + "-"
        if any(
            part in PRIVATE_DIRECTORIES or part.startswith(private_prefix)
            for part in relative.parts
        ):
            findings.add(Finding(relative.as_posix(), None, "private_path_name"))
            continue
        if path.is_symlink():
            findings.add(Finding(relative.as_posix(), None, "symlink"))
            continue
        if not path.is_file():
            continue
        if is_sensitive_filename(path):
            findings.add(Finding(relative.as_posix(), None, "sensitive_filename"))
            continue
        try:
            text = path.read_bytes().decode("utf-8", errors="ignore")
        except OSError:
            findings.add(Finding(relative.as_posix(), None, "unreadable_file"))
            continue
        findings.update(content_findings(relative.as_posix(), text))
    return sorted(findings)


def main() -> None:
    """Run the release scan and use exit code 2 for a blocked release."""
    parser = argparse.ArgumentParser(prog="kokoro-privacy-scan")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print("Kokoro privacy scan error: root is not a directory", file=sys.stderr)
        raise SystemExit(2)

    findings = scan_tree(root)
    if findings:
        print("Kokoro privacy scan blocked release:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.render()}", file=sys.stderr)
        raise SystemExit(2)

    print("Kokoro privacy scan OK.")


if __name__ == "__main__":
    main()
