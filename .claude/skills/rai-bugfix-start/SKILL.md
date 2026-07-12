---
allowed-tools:
- Read
- Edit
- Grep
- Glob
- Bash(git:*)
- Bash(rai:*)
description: Initialize bug branch, reproduce, and create scope artifact. Phase 1
  of bugfix pipeline.
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '1'
  raise.frequency: per-bug
  raise.gate: ''
  raise.inputs: '- bug_id: string, required, argument (e.g. RAISE-251)

    - dev_branch: string, required, config

    '
  raise.next: bugfix-triage
  raise.outputs: '- bug_branch: string, next_skill

    - scope_md: file_path, next_skill

    '
  raise.prerequisites: ''
  raise.skillset: raise-maintainability
  raise.version: 2.4.0
  raise.visibility: public
  raise.work_cycle: bugfix
name: rai-bugfix-start
---

# Bugfix Start

## Purpose

Create a bug branch from the development branch, reproduce the bug, and write the scope artifact that defines what the bug is and when it's fixed.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow all steps, reproduce bug, create scope with all 5 fields
- **Ha**: Streamline scope for well-understood bugs
- **Ri**: Custom initialization patterns for specific domains

## Context

**When to use:** A tracked bug (Jira issue) needs formal resolution with branch, artifacts, and traceability.

**When to skip:** Trivial fix (typo, obvious one-liner) — commit directly. Already started (scope.md exists).

**Inputs:** Bug ID (e.g., RAISE-251), problem statement or reproduction steps.

**Expected state:** On `{dev_branch}`, up to date with remote. No `work/bugs/{issue_key}/` directory yet.

**Branch config:** Read `branches.development` from `.raise/manifest.yaml` for `{dev_branch}`.

## Steps

### Step 0: Instrument

```bash
rai signal emit-work bugfix "{bug_id}" --event start --phase init 2>/dev/null || true
```

### Step 1: Create Bug Branch

```bash
git checkout {dev_branch} && git pull origin {dev_branch}
git checkout -b bug/{issue_key}/{bug-slug}
```

<verification>
On `bug/{issue_key}/{slug}` branch.
</verification>

<if-blocked>
Dev branch has conflicts → resolve before branching.
</if-blocked>

### Step 2: Reproduce & Write Scope

Reproduce the bug — confirm it is observable. Publish the scope artifact via CLI:

```bash
rai docs write bugfix-scope \
  --title "{issue_key}: scope" \
  --stdin \
  --output-path work/bugs/{issue_key}/scope.md << 'EOF'
WHAT:      {behavior observed}
WHEN:      {conditions / triggers}
WHERE:     {file:line or component}
EXPECTED:  {correct behavior}
Done when: {specific observable outcome}
EOF
```

Commit the scope artifact:

```bash
git add work/bugs/{issue_key}/scope.md
git commit -m "bug({issue_key}): initialize scope

WHAT: {summary}
Done when: {criteria}

Co-Authored-By: Rai <rai@humansys.ai>"
```

<verification>
Bug reproduces. Scope artifact committed on bug branch.
</verification>

### Step 2b: Update Backlog Status

Query available statuses for this issue type:
```bash
rai backlog statuses list --issue-type Bug
```

Infer start status from output:
- Look for `category=indeterminate` states whose name suggests active work
  (Implement, In Progress, Started, Active, WIP, Doing…)
- Single clear candidate → use it silently
- Multiple candidates or ambiguous name → ask developer:
  *"Which status means 'work started'? Options: [list]"*

Transition (non-blocking):
```bash
rai backlog transition {bug_key} {start_slug}
```
`{start_slug}` = status name lowercased, spaces→hyphens
("Implement" → `implement`, "In Progress" → `in-progress`)

| Condition | Action |
|-----------|--------|
| Clear candidate found | Transition silently |
| Ambiguous | Ask developer before transitioning |
| No ticket | Skip |
| Transition fails | Log warning and continue |

<if-blocked>
Adapter not configured or transition fails → log and continue. Backlog sync is best-effort.
</if-blocked>

### Step 2c: Bind Session to Jira Key

When the bug has a Jira key, bind it to the per-session context file:
```bash
rai session bind RAISE_SESSION_JIRA_KEY "{bug_key}"
```

Emit session_bind event (fire-and-forget):
```bash
python3 .claude/hooks/_emit_hansei.py \
    --event-type session_bind \
    --title "Bound {bug_key}" \
    --summary "Late-bind jira_key to session" \
    --jira-key "{bug_key}" \
    --session-id "$RAISE_CC_SESSION_ID" \
    --tags "kind:lifecycle"
```

| Condition | Action |
|-----------|--------|
| Bug has Jira key | Bind + emit event |
| No Jira key | Skip silently |

<verification>
`.raise/rai/sessions/$RAISE_CC_SESSION_ID/context.env` contains `RAISE_SESSION_JIRA_KEY={bug_key}` (other keys preserved).
`session_bind` event emitted (or skipped silently if no server).
</verification>

## Output

| Item | Destination |
|------|-------------|
| Bug branch | `bug/{issue_key}/{slug}` from `{dev_branch}` |
| Scope artifact | `work/bugs/{issue_key}/scope.md` |
| Backlog update | via `rai backlog transition` (best-effort) |

```bash
rai signal emit-work bugfix "{bug_id}" --event complete --phase init 2>/dev/null || true
```

**STOP HERE.** Return your summary to the orchestrator. Do NOT invoke any further skill.

## Quality Checklist

- [ ] Bug branch created from `{dev_branch}`
- [ ] Bug reproduces before any investigation
- [ ] Scope artifact committed with WHAT/WHEN/WHERE/EXPECTED/Done-when
- [ ] NEVER investigate before reproducing

## References

- Next: `/rai-bugfix-triage`
- Complement: `/rai-bugfix-close`
- Branch model: `AGENTS.md` § Branch Model
