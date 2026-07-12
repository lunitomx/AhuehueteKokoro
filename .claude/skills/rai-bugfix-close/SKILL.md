---
allowed-tools:
- Read
- Bash(git:*)
- Bash(glab:*)
- Bash(rai:*)
description: Push branch, create MR, verify artifacts complete. Phase 7 of bugfix
  pipeline.
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '7'
  raise.frequency: per-bug
  raise.gate: ''
  raise.inputs: '- bug_id: string, required, argument

    - dev_branch: string, required, config

    '
  raise.next: ''
  raise.outputs: '- mr_url: string, terminal

    '
  raise.prerequisites: bugfix-review
  raise.skillset: raise-maintainability
  raise.version: 2.4.0
  raise.visibility: public
  raise.work_cycle: bugfix
name: rai-bugfix-close
---

# Bugfix Close

## Purpose

Push the bug branch, create a merge request targeting the development branch, and clean up the local branch. All artifacts must exist before closing.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow all steps, verify all 4 artifacts, create MR
- **Ha**: Streamline for batch closures
- **Ri**: Automated close with CI/CD integration

## Context

**When to use:** After `/rai-bugfix-review` has produced the retrospective artifact.

**When to skip:** Never — closing is how bug work becomes visible to the team.

**Inputs:** Bug ID, `{dev_branch}` from `.raise/manifest.yaml`.

**Expected state:** On bug branch. All artifacts exist (scope.md, analysis.md, plan.md, retro.md). Gates passed in fix phase.

## Steps

### Step 0: Instrument

```bash
rai signal emit-work bugfix "{bug_id}" --event start --phase close 2>/dev/null || true
```

### Step 1: Verify Completeness & Clean Tree

Check all required artifacts exist and working tree is clean:

```bash
for f in scope.md analysis.md plan.md retro.md; do
  [ -f "work/bugs/{issue_key}/$f" ] && echo "✓ $f" || echo "ERROR: Missing $f"
done
git status --short
```

| Condition | Action |
|-----------|--------|
| All 4 artifacts + clean tree | Continue |
| Any artifact missing | **STOP** — run the missing phase skill first |
| Uncommitted changes | Commit them before push |

<verification>
All 4 artifacts verified. Working tree clean.
</verification>

### Step 1b: Architecture Review Gate

Run the AR checklist before pushing. This gate is mandatory — use the escape hatch only for XS/docs/tooling fixes with no production code changes.

1. **P1 — Structural drift**: `rai drift check packages/<changed-module>/`
   Review output: orphaned symbols? dead public APIs?
2. **P2 — Beck-R2**: Does this fix add necessary complexity only?
   No speculative abstractions, no unused parameters, no dead branches.
3. **P3 — Convention**: Naming, module placement, public API surface consistent with codebase?

After confirming all three, write the session-scoped marker and run the gate:

```bash
MARKER=".raise/rai/sessions/${RAISE_CC_SESSION_ID}/ar-reviewed"
mkdir -p "$(dirname "$MARKER")" && touch "$MARKER"
rai gate check gate-ar-bugfix
rm -f "$MARKER"
```

Escape hatch (XS/docs/tooling — no production code changed):
```bash
RAISE_AR_SKIP_REASON="<reason>" rai gate check gate-ar-bugfix
```

| Condition | Action |
|-----------|--------|
| Gate passes | Continue to Step 2 |
| Gate fails (no session) | Set `RAISE_CC_SESSION_ID` or use escape hatch |
| Gate fails (no marker) | Complete P1/P2/P3 checklist, then create marker |
| Escape hatch used | Reason logged in gate result — continues |

<verification>
AR gate passed. Reason logged if escape hatch was used.
</verification>

### Step 2: Push & Create MR

**Never merge locally to `{dev_branch}`.**

```bash
git push origin bug/{issue_key}/{slug} -u

glab mr create \
  --source-branch bug/{issue_key}/{slug} \
  --target-branch {dev_branch} \
  --title "fix({issue_key}): {summary}" \
  --description "Root cause: {one line}

Co-Authored-By: Rai <rai@humansys.ai>" \
  --no-editor
```

If `glab` is not available, provide the GitLab URL from `git push` output for manual MR creation.

<verification>
MR created in GitLab targeting `{dev_branch}`.
</verification>

<if-blocked>
`glab` not available → provide push URL for manual MR creation.
</if-blocked>

### Step 2b: Update Backlog

Query done statuses for this issue type:
```bash
rai backlog statuses list --issue-type Bug
```

Infer close status:
- Look for `category=done` states whose name suggests completion
  (Done, DONE, Closed, Resolved, Complete, Finished…)
- Exclude cancellation states (Cancelled, Rejected, Abandoned, Void)
- Single clear candidate → use it silently
- Ambiguous → ask developer

Transition (non-blocking — MR already created):
```bash
rai backlog transition {bug_key} {done_slug}
```

| Condition | Action |
|-----------|--------|
| Clear done candidate | Transition silently |
| Ambiguous | Ask developer |
| No ticket | Skip |
| Transition fails | Log warning and continue |

<if-blocked>
Adapter not configured or transition fails → log and continue. MR already exists.
</if-blocked>

### Step 3: Cleanup

```bash
git checkout {dev_branch}
git branch -D bug/{issue_key}/{slug}
```

<verification>
Local branch deleted.
</verification>

## Scope Constraints (CRITICAL)

Close is a **merge-request-only operation**:

- **NEVER edit source code, skill files, config, or governance docs**
- **NEVER create "fix" or "refactor" commits**
- **NEVER delete directories or files outside the bug branch**
- **NEVER revert or modify commits on `{dev_branch}`**

If something looks wrong, return it as a finding — do not act on it.

## Output

| Item | Destination |
|------|-------------|
| Merge request | GitLab MR: bug branch → `{dev_branch}` |
| Backlog update | via `rai backlog transition` (best-effort) |

```bash
rai signal emit-work bugfix "{bug_id}" --event complete --phase close 2>/dev/null || true
```

**STOP HERE.** Return your summary to the orchestrator. Do NOT invoke any further skill.

## Quality Checklist

- [ ] All 4 artifacts verified before closing
- [ ] Working tree clean before push
- [ ] MR created in GitLab targeting `{dev_branch}`
- [ ] Local branch deleted after MR creation
- [ ] No files modified outside scope constraints
- [ ] NEVER merge locally to `{dev_branch}` — always via MR

## References

- Previous: `/rai-bugfix-review`
- Complement: `/rai-bugfix-start`
- Branch model: `AGENTS.md` § Branch Model
