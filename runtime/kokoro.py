#!/usr/bin/env python3
"""Portable Kokoro runtime entry point shipped by the public package."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

START = "<!-- KOKORO START -->"
END = "<!-- KOKORO END -->"
SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|secret|token|password|private[_-]?key)\s*[:=]"
)


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def merge_marked(existing: str, content: str) -> str:
    existing = existing.replace("\r\n", "\n").replace("\r", "\n")
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    section = f"{START}\n{content.rstrip()}\n{END}\n"
    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
    if START in existing:
        return pattern.sub(lambda _match: section.rstrip(), existing)
    separator = "" if not existing or existing.endswith("\n\n") else "\n"
    return f"{existing}{separator}\n{section}"


def copy_owned(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        if item.is_dir() or item.name == ".gitkeep":
            continue
        relative = item.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or item.name.startswith("kokoro"):
            shutil.copy2(item, destination)


def init(target: Path) -> None:
    root = package_root()
    claude_source = root / "CLAUDE.md"
    if not claude_source.is_file():
        raise RuntimeError("Kokoro package is incomplete; run install/verify.sh")
    claude_dir = target / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    claude_target = claude_dir / "CLAUDE.md"
    existing = (
        claude_target.read_text(encoding="utf-8") if claude_target.exists() else ""
    )
    claude_target.write_text(
        merge_marked(existing, claude_source.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    copy_owned(root / "commands", claude_dir / "commands")
    copy_owned(root / "knowledge", claude_dir / "knowledge")
    agents_source = root / "AGENTS.md"
    agents_target = target / "AGENTS.md"
    agents_content = agents_source.read_text(encoding="utf-8")
    agents_existing = (
        agents_target.read_text(encoding="utf-8") if agents_target.exists() else ""
    )
    agents_target.write_text(
        merge_marked(agents_existing, agents_content), encoding="utf-8"
    )
    print(f"Kokoro initialized in {target}")


def doctor() -> None:
    root = package_root()
    required = (
        root / "AGENTS.md",
        root / "CLAUDE.md",
        root / "commands" / "kokoro.md",
        root / "knowledge",
    )
    missing = [str(path.relative_to(root)) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("Kokoro package is incomplete: " + ", ".join(missing))
    print("Kokoro runtime OK.")


def workspace_init(target: Path, private_remote: str) -> None:
    """Create memory tiers only in an explicitly verified private workspace."""

    target = target.resolve()
    if target == package_root():
        raise RuntimeError("never create entrepreneur memory in the public package")
    remote = _origin(target)
    if remote is None:
        raise RuntimeError(
            "workspace needs a Git origin with verified private visibility"
        )
    if "ahuehuetekokoro" in remote.lower() or remote != private_remote:
        raise RuntimeError("workspace origin is not explicitly verified as private")
    for relative in (
        ".kokoro/shared/events",
        ".kokoro/shared/views",
        ".kokoro/local",
        ".kokoro/secrets",
        ".kokoro/cache",
        ".kokoro/raw",
    ):
        (target / relative).mkdir(parents=True, exist_ok=True)
    gitignore = target / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    owned = (
        "\n# Kokoro private memory\n.kokoro/local/\n.kokoro/secrets/\n"
        ".kokoro/cache/\n.kokoro/raw/\n"
    )
    if "# Kokoro private memory" not in existing:
        gitignore.write_text(existing.rstrip() + owned, encoding="utf-8")
    print(f"Kokoro private workspace initialized in {target}")


def _origin(target: Path) -> str | None:
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or None


def privacy_check(target: Path, private_remote: str) -> None:
    """Fail closed when staged sharing data lacks repository or secret proof."""

    target = target.resolve()
    remote = _origin(target)
    if (
        remote is None
        or remote != private_remote
        or "ahuehuetekokoro" in remote.lower()
    ):
        raise RuntimeError(
            "privacy check requires an explicitly verified private origin"
        )
    paths = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    staged = [item for item in paths.stdout.splitlines() if item]
    forbidden = [
        item
        for item in staged
        if item.startswith(".kokoro/local/")
        or item.startswith(".kokoro/secrets/")
        or item.startswith(".kokoro/raw/")
    ]
    if forbidden:
        raise RuntimeError(
            "privacy check rejected private staged paths: " + ", ".join(forbidden)
        )
    diff = subprocess.run(
        ["git", "diff", "--cached", "--no-ext-diff"],
        cwd=target,
        check=False,
        capture_output=True,
        text=True,
    )
    if SECRET_PATTERN.search(diff.stdout):
        raise RuntimeError("privacy check rejected secret-like staged content")
    print("Kokoro privacy check OK.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="kokoro")
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init", help="Initialize a project safely")
    init_parser.add_argument("--target", type=Path, default=Path.cwd())
    workspace_parser = commands.add_parser(
        "workspace-init", help="Create private memory tiers"
    )
    workspace_parser.add_argument("--target", type=Path, required=True)
    workspace_parser.add_argument("--private-remote", required=True)
    privacy_parser = commands.add_parser(
        "privacy-check", help="Validate staged shared data"
    )
    privacy_parser.add_argument("--target", type=Path, required=True)
    privacy_parser.add_argument("--private-remote", required=True)
    commands.add_parser("doctor", help="Verify the installed runtime")
    args = parser.parse_args()
    try:
        if args.command == "init":
            init(args.target.resolve())
        elif args.command == "workspace-init":
            workspace_init(args.target, args.private_remote)
        elif args.command == "privacy-check":
            privacy_check(args.target, args.private_remote)
        else:
            doctor()
    except RuntimeError as exc:
        print(f"Kokoro error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
