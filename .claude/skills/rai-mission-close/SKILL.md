---
allowed-tools:
- Read
- Bash
description: Close a mission with reflective retrospective. Use when finishing a bounded
  initiative.
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: end
  raise.frequency: per-mission
  raise.gate: ''
  raise.inputs: '- mission_id: string, optional, argument (defaults to active mission)

    '
  raise.next: ''
  raise.outputs: '- retrospective: file_path, file

    '
  raise.prerequisites: ''
  raise.version: 1.0.0
  raise.visibility: public
  raise.work_cycle: mission
name: rai-mission-close
---

# Mission Close

## Purpose

Close a mission by reflecting on what was accomplished, what was learned, and persisting a retrospective to the mission's memory directory.

## Mastery Levels (ShuHaRi)

- **Shu**: Explain each section of the retrospective, ask for review
- **Ha**: Generate retro, present summary, ask only about promotion decisions
- **Ri**: Generate retro, save, present one-liner — "Go."

## Context

**When to use:** When a bounded initiative is complete (accomplished) or being abandoned.

**Inputs:** Active mission (or mission ID as argument). Optional: outcome, closing note.

## Steps

### Step 1: Identify Mission & Outcome

```bash
rai mission list
```

Confirm with the developer: which mission, accomplish or abandon, optional note/reason.

### Step 2: Close via CLI

```bash
# Accomplish:
rai mission close --note "{note}" --force
# Abandon:
rai mission abandon --reason "{reason}"
```

### Step 3: Gather Context

1. **Mission YAML**: `cat .raise/rai/missions/{mission_id}.yaml`
2. **CC auto-memory**: read `.md` files from mission memory dir (frontmatter `description` field)
3. **Session index**: match `mission.sessions[]` IDs against `.raise/rai/personal/sessions/{prefix}/index.jsonl`

### Step 4: Generate Reflective Retrospective

Produce `mission-retro.md` with:

- **Header**: name, status, duration, session count, note
- **Objectives table**: each objective with status marker (✓/○/◑/✗)
- **What Happened**: inference-generated narrative from session summaries — arc, decisions, blockers
- **Patterns Emerged**: CC auto-memory descriptions + synthesis (themes, promotion candidates)
- **Sessions table**: ID, summary, type, duration
- **Reflection**: what to do differently, what carries forward, kaizen observations

The reflective sections (What Happened, Reflection) are where inference adds value. Use session summaries and patterns as evidence.

### Step 5: Save & Update

Resolve the path and publish `mission-retro.md` via CLI:

```bash
RETRO_DIR=$(python3 -c "from raise_cli.config.paths import get_mission_memory_dir; from pathlib import Path; print(get_mission_memory_dir(Path.cwd(), '{mission_id}'))")
rai docs write mission-retro \
  --title "{mission_id}: retrospective" \
  --stdin \
  --output-path "$RETRO_DIR/mission-retro.md" << 'EOF'
[retrospective content from Step 4]
EOF
RETRO_PATH="$RETRO_DIR/mission-retro.md"
```

Update `Mission.retrospective_path`:

```bash
python3 -c "
from raise_cli.session.mission import LocalMissionRegistry
from pathlib import Path
reg = LocalMissionRegistry(project=Path.cwd())
m = reg.get_mission('{mission_id}')
reg._write_mission(m.model_copy(update={'retrospective_path': '{retro_path}'}))
"
```

### Step 6: Present Summary

```
## Mission Closed
**Mission:** {id} — {name}  |  **Status:** {outcome}  |  **Objectives:** {done}/{total}
**Retrospective:** {retro_path}
```

## Output

| Item | Destination |
|------|-------------|
| Mission status | Via `rai mission close/abandon` |
| Retrospective | `{cc_memory}/missions/{id}/mission-retro.md` |
| retrospective_path | Updated in mission YAML |

## Quality Checklist

- [ ] Mission status transitioned before retro generation
- [ ] Reflective sections use inference, not mechanical template
- [ ] Retro saved to correct CC mission memory dir
- [ ] retrospective_path updated in mission YAML

## References

- Mission model: `packages/raise-cli/src/raise_cli/session/mission.py`
- CC memory paths: `packages/raise-cli/src/raise_cli/config/paths.py`
- Complement: `/rai-session-close`, `/rai-story-review`
