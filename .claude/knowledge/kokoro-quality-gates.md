# Quality Gates Library

> Reusable verification gates for skill orchestration. Each gate is a named
> check that an orchestrator skill can invoke after a sub-skill completes.

## How to Use

In an orchestrator skill, after delegating to a sub-skill, apply the relevant
gate(s) before proceeding to the next phase. Example:

```
### After sub-skill completes:
Apply: GATE-ARTIFACT-EXISTS, GATE-CONTENT-COMPLETE
If any gate fails → STOP, report which gate failed and why.
```

## Gates

### GATE-ARTIFACT-EXISTS

**Purpose:** Verify a file was created at the expected path.
**Check:** `ls {expected_path}` or `test -f {expected_path}`
**Pass:** File exists and is non-empty (size > 0 bytes).
**Fail action:** Stop orchestration. Report missing artifact and which sub-skill
should have produced it.
**Example:** After /kokoro-diagnose, verify `.kokoro/diagnostics/speedboat.md` exists.

### GATE-FORMAT-VALID

**Purpose:** Verify file follows expected structure.
**Check:** Inspect file for required sections (headings, frontmatter, tables).
**Pass:** All required structural elements present in correct order.
**Fail action:** Stop. Report which structural elements are missing or malformed.
**Example:** After ADR creation, verify Status/Context/Decision/Rationale/Consequences
sections exist.

### GATE-CONTENT-COMPLETE

**Purpose:** Verify all required fields/sections have substantive content (not
empty or placeholder).
**Check:** Read file, verify each required section has ≥1 sentence of real content.
**Pass:** No section is empty, no placeholder text (TODO, TBD, FIXME, [fill in]).
**Fail action:** Stop. Report which sections need content.
**Example:** After canvas sub-skill, verify all 9 Lean Canvas blocks have content.

### GATE-MIRROR-IDENTICAL

**Purpose:** Verify two files are byte-identical.
**Check:** `diff {source} {mirror}` (empty output = identical).
**Pass:** diff produces no output.
**Fail action:** Stop. Show diff. Re-copy source to mirror.
**Example:** After knowledge file creation, verify `.claude/knowledge/` and
`extension/.claude/knowledge/` copies match.

### GATE-LINE-THRESHOLD

**Purpose:** Prevent monolith drift — verify a skill or artifact stays under
line limit.
**Check:** `wc -l < {file}` and compare to threshold (default: 200 for skills).
**Pass:** Line count ≤ threshold.
**Fail action:** Warning (not hard stop). Flag for review — skill may need splitting.
**Example:** After skill modification, verify it hasn't grown past 200-line
guidance threshold.

### GATE-NO-PLACEHOLDERS

**Purpose:** Verify no incomplete markers remain in output.
**Check:** `grep -inE '(TODO|FIXME|TBD|\[fill|PLACEHOLDER|XXX)' {file}`
**Pass:** grep returns no matches (exit code 1).
**Fail action:** Stop. List placeholder locations. Sub-skill must complete all
sections.
**Example:** After any content-producing sub-skill, scan output for residual
placeholders.

### GATE-REFERENCES-VALID

**Purpose:** Verify that paths, links, or references in the artifact point to
real files.
**Check:** Extract file paths from content, verify each with `test -f`.
**Pass:** All referenced paths exist.
**Fail action:** Warning. List broken references. May indicate stale content or
ordering issue.
**Example:** After design doc creation, verify referenced modules/files exist
on disk.

## Composing Gates

Orchestrators typically apply gates in this order:

1. GATE-ARTIFACT-EXISTS (did it produce anything?)
2. GATE-FORMAT-VALID (is it structured correctly?)
3. GATE-CONTENT-COMPLETE (is it actually filled in?)
4. GATE-NO-PLACEHOLDERS (is it truly done?)

Additional gates for specific scenarios:

- After mirror operations: + GATE-MIRROR-IDENTICAL
- After skill modifications: + GATE-LINE-THRESHOLD
- After docs with cross-references: + GATE-REFERENCES-VALID

## Gate Failure Protocol

When a gate fails:

1. **Stop** — do not proceed to next sub-skill
2. **Report** — which gate, which file, what specifically failed
3. **Retry once** — if the sub-skill can be re-run, try once
4. **Escalate** — if retry fails, stop orchestration and report to human
