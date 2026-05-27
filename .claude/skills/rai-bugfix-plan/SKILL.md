---
allowed-tools:
- Read
- Grep
- Glob
- Bash(rai:*)
description: Decompose fix into atomic TDD tasks. Phase 4 of bugfix pipeline.
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '4'
  raise.frequency: per-bug
  raise.gate: ''
  raise.inputs: '- bug_id: string, required, argument

    - analysis_md: file_path, required, from_previous

    '
  raise.next: bugfix-fix
  raise.outputs: '- plan_md: file_path, next_skill

    '
  raise.prerequisites: bugfix-analyse
  raise.skillset: raise-maintainability
  raise.version: 2.4.0
  raise.visibility: public
  raise.work_cycle: bugfix
name: rai-bugfix-plan
---

# Bugfix Plan

## Purpose

Decompose the fix into atomic, independently committable tasks in TDD order. The regression test task comes first — proving the bug exists before fixing it.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow template, regression test first, explicit verification per task
- **Ha**: Collapse plan for XS bugs (2 tasks: test + fix)
- **Ri**: Adaptive task granularity based on complexity signals

## Context

**When to use:** After `/rai-bugfix-analyse` has confirmed root cause and fix approach.

**When to skip:** Never — even a 1-task fix benefits from explicit planning (regression test + fix = 2 tasks minimum).

**Inputs:** Bug ID, `work/bugs/{issue_key}/analysis.md` with root cause and fix approach.

**Expected state:** On bug branch. Analysis artifact exists.

## Steps

### Step 0: Instrument

```bash
rai signal emit-work bugfix "{bug_id}" --event start --phase plan 2>/dev/null || true
```

### Step 1: Decompose into Tasks

Publish `work/bugs/{issue_key}/plan.md` via CLI: atomic tasks in TDD order.

Each task must have:
- **Description:** What to do
- **Verification:** Command from `.raise/manifest.yaml` (test, lint, type check)
- **Commit message:** Following `fix({issue_key}): {description}` convention

The regression test task MUST be first:

```bash
rai docs write bugfix-plan \
  --title "{issue_key}: plan" \
  --stdin \
  --output-path work/bugs/{issue_key}/plan.md << 'EOF'
## Tasks

### T1: Write regression test (RED)
- Write test that reproduces the bug
- Verify: `{test_command}` — test FAILS (proves bug exists)
- Commit: `test({issue_key}): add regression test for {description}`

### T2: Fix {description} (GREEN)
- {specific change}
- Verify: `{test_command}` — test PASSES
- Commit: `fix({issue_key}): {description}`

### T3: Refactor (if needed)
- {cleanup}
- Verify: all gates pass
- Commit: `refactor({issue_key}): {description}`
EOF
```

<verification>
Regression test task listed first. Each task independently committable.
</verification>

<if-blocked>
Fix approach unclear → return to `/rai-bugfix-analyse` for deeper investigation.
</if-blocked>

### Step 2: Commit Plan

```bash
git add work/bugs/{issue_key}/plan.md
git commit -m "bug({issue_key}): plan — {N} tasks, TDD order

Co-Authored-By: Rai <rai@humansys.ai>"
```

## Output

| Item | Destination |
|------|-------------|
| Plan | `work/bugs/{issue_key}/plan.md` |

```bash
rai signal emit-work bugfix "{bug_id}" --event complete --phase plan 2>/dev/null || true
```

**STOP HERE.** Return your summary to the orchestrator. Do NOT invoke any further skill.

## Quality Checklist

- [ ] Regression test is task #1
- [ ] Each task independently committable
- [ ] Verification command specified per task
- [ ] Commit message specified per task
- [ ] NEVER start fixing without a plan

## References

- Previous: `/rai-bugfix-analyse`
- Next: `/rai-bugfix-fix`
