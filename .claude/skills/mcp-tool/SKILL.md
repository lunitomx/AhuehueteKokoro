---
name: mcp-tool
description: Scaffold a new Kokoro MCP tool — either a skill-loader (reads a .md file) or a utility tool (custom Python logic)
---

# New Kokoro MCP Tool

Scaffold a new tool in the Kokoro MCP server. There are two types — identify which before starting.

## Tool Types

### Type A — Skill Loader
Loads a `.md` file from `extension/.claude/commands/` and returns its content.
Use for: all Kokoro coaching skills (diagnose, canvas, forces, etc.)

**What to do:**
1. Add entry to `SKILLS` dict in `src/kokoro/mcp_server.py`:
   ```python
   "kokoro_{name}": (
       "kokoro-{name}.md",
       "{One-line description in Spanish — what the tool does}",
   ),
   ```
2. Verify the `.md` file exists at `extension/.claude/commands/kokoro-{name}.md`
3. Update the skill count assertion in `tests/test_mcp_server.py`:
   - Find `test_has_16_skills` (or current count) → increment by 1
   - Add the skill name to the correct phase list in the same file

### Type B — Utility Tool
Has actual Python logic (reads/writes state, transforms data, etc.)
Use for: tools like `kokoro_init`, `kokoro_progress`

**What to do:**
1. Add a `@mcp.tool()` function to `src/kokoro/mcp_server.py` **after** the dynamic skill registration block:
   ```python
   @mcp.tool(
       name="kokoro_{name}",
       description="{One-line description in Spanish}",
   )
   def kokoro_{name}(param: str) -> str:
       """Docstring."""
       state = load_state(_PROJECT_DIR)
       if state is None:
           return "No hay estado de coaching. Usa kokoro_init para comenzar."
       # ... logic ...
       return result
   ```
2. Create `tests/test_{name}.py` following the pattern in `tests/test_mcp_server.py`:
   - Use `tmp_path` + `monkeypatch` to mock `_PROJECT_DIR`
   - Use `create_empty_state` + `save_state` from `kokoro.ontology.store`
   - Test: empty state path, happy path, edge cases

## Invariants (never break these)

- All functions need full type annotations — Pyright strict will fail otherwise
- All imports at top of file with `from __future__ import annotations`
- No bare `except:` — always catch specific exceptions
- `load_state` returns `None` when no state exists — always guard against it
- Skill tool names: `kokoro_{snake_case}` — no camelCase, no dashes
- File names in SKILLS dict: `kokoro-{kebab-case}.md` — dashes, not underscores

## Key paths

```
src/kokoro/mcp_server.py          ← server file, SKILLS dict + tool functions
extension/.claude/commands/       ← .md files for skill-loader tools
tests/test_mcp_server.py          ← registry tests, update skill count here
tests/test_{name}.py              ← new test file for utility tools
```

## Validation after scaffolding

Run in order — all must pass before considering done:

```bash
uv run ruff check src/kokoro/mcp_server.py
uv run pyright src/kokoro/mcp_server.py
uv run pytest tests/test_mcp_server.py -v
```

For utility tools also run:
```bash
uv run pytest tests/test_{name}.py -v
```
