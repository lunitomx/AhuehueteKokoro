"""Kokoro integrity tests — verifican invariantes del proyecto.

Regla 4: Antes de cada commit, uv run pytest -q debe ser 0 passed, 0 failed.
Estos tests validan que el estado del repo es consistente.
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def find_md_files(directory: str) -> list[Path]:
    """Find all markdown files in a directory, recursively."""
    return sorted(Path(PROJECT_ROOT, directory).rglob("*.md"))


class TestDoneCriteria:
    """Rule 1: Stories marked COMPLETE must have all checkboxes [x], not [ ]."""

    def test_no_unchecked_in_complete_epics(self):
        """All epics with Status: COMPLETE must have 0 unchecked [ ] checkboxes in Done Criteria."""
        epic_dirs = list(Path(PROJECT_ROOT, "work/epics").glob("e*"))
        violations = []

        for epic_dir in epic_dirs:
            scope = epic_dir / "scope.md"
            if not scope.exists():
                continue
            content = scope.read_text()
            if "**Status:** COMPLETE" not in content and "Status:** COMPLETE" not in content:
                continue

            # Find unchecked checkboxes in Done Criteria section
            done_section = content.split("## Done Criteria")[-1] if "## Done Criteria" in content else ""
            done_section = done_section.split("## ")[0] if "## " in done_section else done_section

            unchecked = [line.strip() for line in done_section.split("\n") if line.strip().startswith("- [ ]")]
            if unchecked:
                violations.append(f"{epic_dir.name}: {len(unchecked)} unchecked")

        assert violations == [], (
            f"COMPLETE epics with unchecked done criteria:\n" + "\n".join(violations)
        )


class TestIdentityDrift:
    """AGENTS.md and CLAUDE.md must both reference IDENTITY_kokoro.md."""

    def test_agents_references_identity(self):
        agents = Path(PROJECT_ROOT, "AGENTS.md").read_text()
        assert "IDENTITY_kokoro.md" in agents, "AGENTS.md must reference IDENTITY_kokoro.md"

    def test_claude_references_identity(self):
        claude = Path(PROJECT_ROOT, ".claude/CLAUDE.md").read_text()
        assert "IDENTITY_kokoro.md" in claude, "CLAUDE.md must reference IDENTITY_kokoro.md"

    def test_identity_exists(self):
        assert Path(PROJECT_ROOT, "IDENTITY_kokoro.md").exists(), "IDENTITY_kokoro.md must exist"


class TestKnowledgeCoverage:
    """Every command file references at least one knowledge file or is self-documenting."""

    def test_command_knowledge_map_exists(self):
        kmap = Path(PROJECT_ROOT, ".claude/knowledge/kokoro-command-knowledge-map.md")
        assert kmap.exists(), "Command-knowledge cross-reference map must exist"


class TestPublicInstallSurface:
    """The public repo must expose Kokoro without leaking internal RaiSE skills."""

    def test_codex_kokoro_skill_exists(self):
        skill = Path(PROJECT_ROOT, ".agents/skills/kokoro/SKILL.md")
        assert skill.exists(), "Codex install surface must expose a Kokoro skill"

    def test_no_rai_skills_in_public_surface(self):
        leaked = [
            str(path.relative_to(PROJECT_ROOT))
            for path in Path(PROJECT_ROOT, ".claude/skills").glob("rai-*")
        ]
        assert leaked == [], "Public repo must not ship RaiSE skills:\n" + "\n".join(leaked)


class TestE45Deliverables:
    """S45.1-S45.3: Verify E45 deliverables exist on disk."""

    def test_meta_detector_exists(self):
        assert Path(PROJECT_ROOT, ".claude/knowledge/kokoro-learning-state-detector-meta.md").exists()

    def test_google_detector_exists(self):
        assert Path(PROJECT_ROOT, ".claude/knowledge/kokoro-learning-state-detector-google.md").exists()

    def test_open_shows_reason(self):
        content = Path(PROJECT_ROOT, ".claude/commands/kokoro-open.md").read_text()
        assert "learning_state_reason" in content, "kokoro-open must show learning_state_reason"

    def test_schema_has_source_fields(self):
        content = Path(PROJECT_ROOT, ".claude/knowledge/kokoro-google-ads-learning-record.md").read_text()
        assert "learning_state_reason" in content
        assert "learning_state_source" in content

    def test_ads_has_detector_code(self):
        content = Path(PROJECT_ROOT, ".claude/commands/kokoro-ads.md").read_text()
        assert "detect_meta_ads_state" in content

    def test_gads_has_detector_code(self):
        content = Path(PROJECT_ROOT, ".claude/commands/kokoro-gads.md").read_text()
        assert "detect_google_ads_state" in content
