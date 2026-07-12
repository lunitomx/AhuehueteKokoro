---
allowed-tools:
- Read
- Edit
- Write
- Grep
- Glob
- Bash
description: Execute fix tasks with TDD and all validation gates. Phase 5 of bugfix
  pipeline.
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '5'
  raise.frequency: per-bug
  raise.gate: gate-code
  raise.inputs: '- bug_id: string, required, argument

    - plan_md: file_path, required, from_previous

    '
  raise.next: bugfix-review
  raise.outputs: '- code_commits: list, git

    '
  raise.prerequisites: bugfix-plan
  raise.skillset: raise-maintainability
  raise.version: 2.4.0
  raise.visibility: public
  raise.work_cycle: bugfix
name: rai-bugfix-fix
---

# Bugfix Fix

## Purpose

Execute the planned fix tasks in strict TDD order: RED (failing regression test) → GREEN (minimal fix) → REFACTOR. Each task verified and committed independently.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow plan tasks exactly, RED-GREEN-REFACTOR, run all 4 gates
- **Ha**: Combine related tasks when gates are stable
- **Ri**: Adaptive TDD (property tests, mutation testing)

## Context

**When to use:** After `/rai-bugfix-plan` has decomposed the fix into atomic tasks.

**When to skip:** Never — even if the fix seems trivial, follow the plan.

**Inputs:** Bug ID, `work/bugs/{issue_key}/plan.md` with atomic tasks.

**Expected state:** On bug branch. Plan artifact exists. All current gates pass.

## Steps

### Step 0: Instrument

```bash
rai signal emit-work bugfix "{bug_id}" --event start --phase fix 2>/dev/null || true
```

### Step 1: Execute Tasks in Order

Per task from `plan.md`:

1. **RED** — Write a failing test that defines expected behavior
2. **GREEN** — Write minimal code to make the test pass
3. **REFACTOR** — Clean up while keeping tests green

**Run ALL four gates** (test + lint + format + type check) after each task via the CLI — **NEVER run the test command directly** (keeps context clean):

```bash
rai gate check gate-tests --scope {changed_test_path}   # fast check, scoped
rai gate check gate-lint
rai gate check gate-format
rai gate check gate-types
```

Fall back to `rai gate check gate-tests` (unscoped) only when the scope path is ambiguous.

If verification fails: fix and re-verify (max 3 attempts before escalating).

### Step 2: Commit & Present

Per completed task:

1. Commit with the message from the plan
2. Present to the human: what was completed, files changed, verification results
3. Wait for acknowledgment before continuing

### Step 3: Iterate or Finalize

| Condition | Action |
|-----------|--------|
| More tasks remain | Return to Step 1 |
| All tasks complete | Run `rai gate check --all`, present summary |
| Task blocked | Document blocker, escalate to human |

<verification>
All tasks committed. All four gates pass. Bug no longer reproduces.
</verification>

<if-blocked>
3 attempts without fix → document partial state, create follow-up issue.
</if-blocked>

## Output

| Item | Destination |
|------|-------------|
| Code + commits | On bug branch |

Transition bug to review status before signaling completion (non-blocking):
```bash
rai backlog statuses list --issue-type Bug
```
Infer review status: `category=indeterminate` + name contains Review, Revision, Code Review.
Single candidate → transition silently. Multiple or ambiguous → ask developer. None → skip silently.
```bash
rai backlog transition {bug_key} {review_slug}
```

```bash
rai signal emit-work bugfix "{bug_id}" --event complete --phase fix 2>/dev/null || true
```

**STOP HERE.** Return your summary to the orchestrator. Do NOT invoke any further skill.

## Quality Checklist

- [ ] TDD cycle followed per Step 1 — RED proves bug, GREEN minimal fix, REFACTOR cleans up while keeping tests green
- [ ] Regression test not skipped; root cause addressed (not symptoms)
- [ ] All four gates pass after each task (test, lint, type check, format)
- [ ] Each task committed independently
- [ ] Human acknowledged each task before proceeding
- [ ] Bug no longer reproduces after fix

## References

- Gate: `gates/gate-code.md`
- Previous: `/rai-bugfix-plan`
- Next: `/rai-bugfix-review`
