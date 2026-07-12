---
allowed-tools:
- Read
- Bash(rai:*)
description: Retrospective, pattern extraction, and process improvement. Phase 6 of
  bugfix pipeline.
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '6'
  raise.frequency: per-bug
  raise.gate: ''
  raise.inputs: '- bug_id: string, required, argument

    - scope_md: file_path, required, from_previous

    '
  raise.next: bugfix-close
  raise.outputs: '- retro_md: file_path, next_skill

    - patterns: list, cli

    '
  raise.prerequisites: bugfix-fix
  raise.skillset: raise-maintainability
  raise.version: 2.4.0
  raise.visibility: public
  raise.work_cycle: bugfix
name: rai-bugfix-review
---

# Bugfix Review

## Purpose

Verify the fix addresses root cause, extract process improvements and causal patterns, and produce the retrospective artifact. This is where bugs become organizational learning.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow all steps, answer every checkpoint question, add patterns
- **Ha**: Skip checkpoint for trivial fixes; focus patterns on novel insights
- **Ri**: Feed systemic findings to graph; cross-bug pattern analysis

## Context

**When to use:** After `/rai-bugfix-fix` has completed all planned tasks with passing gates.

**When to skip:** Never — even trivial fixes produce learnings. Skipping review is the #1 step-skipping failure mode.

**Inputs:** Bug ID, all prior artifacts (`scope.md`, `analysis.md`, `plan.md`), code commits.

**Expected state:** On bug branch. All tasks committed. All gates pass. Bug no longer reproduces.

## Steps

### Step 0: Instrument

```bash
rai signal emit-work bugfix "{bug_id}" --event start --phase review 2>/dev/null || true
```

### Step 1: Heutagogical Checkpoint

Answer with specific examples:
1. What did you learn about this system or codebase?
2. What would you change about the fix process?
3. Are there improvements for the framework (skill, guardrail, template)?
4. What are you more capable of now?

### Step 2: Extract Patterns & Process Improvements

**Add patterns** worth preserving using `raise_pattern_add` MCP tool with content="{causal insight}", context="{keywords}", pattern_type="process", from_story="{issue_key}".

Types: `process`, `technical`, `architecture`, `codebase`.

**Reinforce behavioral patterns** loaded at session start using `raise_pattern_reinforce` MCP tool with pattern_id={pattern_id}, vote={1|0|-1}, from_story="{issue_key}".

If MCP tools are not available, fall back to:
```bash
rai pattern add "{causal insight}" --context "{keywords}" --type process --scope project --from {issue_key}
rai pattern reinforce {pattern_id} --vote {1|0|-1} --from {issue_key}
```

| Vote | Meaning |
|:----:|---------|
| `1` | Fix followed the pattern |
| `0` | Pattern not relevant (does NOT count toward scoring) |
| `-1` | Fix contradicted the pattern |

**Process improvement** — answer with specifics:

1. What change in process or tooling would prevent this **class** of bug?
2. What classification pattern does this bug represent?

### Step 3: Write Retrospective

Publish `work/bugs/{issue_key}/retro.md` via CLI:

```bash
rai docs write bugfix-retro \
  --title "{issue_key}: retrospective" \
  --stdin \
  --output-path work/bugs/{issue_key}/retro.md << 'EOF'
## Retrospective: {issue_key}

### Summary
- Root cause: {one line}
- Fix approach: {one line}
- Classification: {Bug Type}/{Severity}/{Origin}/{Qualifier}

### Process Improvement
**Prevention:** {specific change that would prevent this class of bug}
**Pattern:** {Bug Type}={X} + {Origin}={Y} → {systemic insight}

### Heutagogical Checkpoint
1. Learned: ...
2. Process change: ...
3. Framework improvement: ...
4. Capability gained: ...

### Patterns
- Added: {pattern IDs or "none"}
- Reinforced: {pattern IDs and votes, or "none evaluated"}
EOF
```

Commit:

```bash
git add work/bugs/{issue_key}/retro.md
git commit -m "bug({issue_key}): review — retro and patterns

Co-Authored-By: Rai <rai@humansys.ai>"
```

<verification>
Retro written. Patterns added/reinforced.
</verification>

## Output

| Item | Destination |
|------|-------------|
| Retrospective | `work/bugs/{issue_key}/retro.md` |
| Patterns | `.raise/rai/memory/patterns.jsonl` |

Transition bug to ready status before signaling completion (non-blocking):
```bash
rai backlog statuses list --issue-type Bug
```
Infer ready status: `category=indeterminate` + name contains Ready, Approved, Listo, Merge.
Single candidate → transition silently. Multiple or ambiguous → ask developer. None → skip silently.
```bash
rai backlog transition {bug_key} {ready_slug}
```

```bash
rai signal emit-work bugfix "{bug_id}" --event complete --phase review 2>/dev/null || true
```

**STOP HERE.** Return your summary to the orchestrator. Do NOT invoke any further skill.

## Quality Checklist

- [ ] Heutagogical checkpoint answered with specifics
- [ ] Process improvement extracted with prevention + pattern
- [ ] Patterns added with `--scope project` if applicable
- [ ] Retro artifact committed
- [ ] NEVER merge without retro — learnings compound
- [ ] NEVER skip pattern reinforce — scoring system depends on it

## References

- Previous: `/rai-bugfix-fix`
- Next: `/rai-bugfix-close`
- Pattern scoring: RAISE-170 (temporal decay + Wilson scorer)
