---
allowed-tools:
- Bash(rai:*)
description: 'Configure a Jira instance for all RaiSE skills in one session: connection,
  custom fields, workflow statuses, and link types — backlog.yaml complete.

  '
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '0'
  raise.frequency: once
  raise.gate: ''
  raise.next: rai-bugfix-triage
  raise.prerequisites: ''
  raise.version: 3.1.0
  raise.visibility: public
  raise.work_cycle: utility
name: rai-backlog-setup
---

# Backlog Setup

## Purpose

Configure `.raise/backlog.yaml` for a new Jira instance by running four discovery commands in sequence — the user ends with a fully configured backlog adapter ready for all skills.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow all 6 steps; explain purpose of each section before running
- **Ha**: Run steps 1–5 directly; verify once at the end
- **Ri**: `rai adapter setup jira && rai backlog fields discover ... && rai backlog statuses ... && rai backlog link-types`

## Context

**When to use:** After `rai init`, when connecting to a new Jira instance, or when `/rai-doctor` reports missing adapter config.

**When to skip:** `rai backlog fields list` shows configured fields — adapter is already set up.

**Prerequisites:** `JIRA_API_TOKEN` + `JIRA_USERNAME` env vars set; `rai init` complete.

## Steps

### Step 1: Base Adapter Setup

```bash
rai adapter setup jira
```

Prompts for site domain, instance name, and project selection. Use `--overwrite` to regenerate.

**Warning:** Running `--overwrite` after Steps 3–5 are complete will erase all custom fields, workflow, and link-type config. Only use it to reset the base config before running discovery again.

<verification>
`.raise/backlog.yaml` exists and `rai backlog get PROJECT-1` succeeds.
</verification>

### Step 2: Get Project Key

Ask the user for the project key to use for discovery (e.g. `MYPROJ`, `ACME`).

### Step 3: Discover Custom Fields

Before running, explain: "Custom fields let RaiSE skills read and write structured data on issues (e.g. classification fields for bugs, priority tiers, etc.)."

Run first to show available issue types (project key is a positional argument, no flag):

```bash
rai backlog issue-types {KEY}
```

Ask (one at a time):
1. "Which issue types do you want to configure custom fields for?"
2. For each chosen type: "What custom fields? If unsure, I can search first." — if unsure, run `rai backlog fields search --project {KEY} "{term}"` for each term

```bash
rai backlog fields discover --names "{field1},{field2},..." --issue-type {IssueTypeName}
```

`--issue-type` here accepts the **display name** returned by `issue-types` (e.g. `Historia`, `Error`).

Repeat for each chosen issue type.

<verification>
`rai backlog fields list` shows `custom_fields.{IssueTypeName}` with ≥1 field for each configured type.
</verification>

### Step 4: Discover Workflow Statuses

Ask: "Which issue types should I configure workflow statuses for?"

**Important — naming mismatch:** `--issue-type` here uses Jira's **internal English type names**, NOT the display names shown by `rai backlog issue-types`. This is a known inconsistency between two Jira API endpoints.

Mapping for standard Jira types (even when the instance shows them in another language):

| Display name (any language) | `--issue-type` value |
|-----------------------------|----------------------|
| Historia / Story / Histoire | `Story` |
| Tarea / Task / Tâche | `Task` |
| Subtarea / Subtask | `Sub-task` |
| Error / Bug / Défaut | `Bug` |
| Epic | `Epic` |

If the instance has custom types beyond the standard ones, run without `--issue-type` first to get all statuses deduplicated, then probe type names by trial and error.

Run once per selected type:

```bash
rai backlog statuses discover {PROJECT_KEY} --issue-type {INTERNAL_TYPE_NAME}
```

Each run saves statuses under `workflow.{IssueType}` — running for multiple types accumulates without overwriting.

Verify with:

```bash
rai backlog statuses list
```

<verification>
`.raise/backlog.yaml` contains `workflow.{IssueType}.states` for each selected type.
</verification>

### Step 5: Discover Link Types

```bash
rai backlog link-types
```

0 link types is valid — some instances don't use them.

<verification>
`.raise/backlog.yaml` contains `link_types` (may be empty list).
</verification>

### Step 6: Verify

```bash
rai backlog fields list
```

Show the output. Confirm `custom_fields.{IssueTypeName}` for each configured type, `workflow.states`, and `link_types` are present.

## Output

| Artifact | Destination |
|----------|-------------|
| Base adapter config | `.raise/backlog.yaml` — organizations, projects |
| Custom fields | `.raise/backlog.yaml` — `custom_fields.{IssueTypeName}` |
| Workflow statuses | `.raise/backlog.yaml` — `workflow.states` |
| Link types | `.raise/backlog.yaml` — `link_types` |

## Quality Checklist

- [ ] Ran `rai backlog issue-types {KEY}` (positional, no `--project`) before asking for custom fields
- [ ] Used display names for `fields discover --issue-type` (e.g. `Historia`)
- [ ] Used Jira internal English names for `statuses discover --issue-type` (e.g. `Story`, `Task`, `Bug`, `Sub-task`, `Epic`)
- [ ] Asked user to confirm field names (or ran search first)
- [ ] `rai backlog fields list` shows entries for each configured issue type
- [ ] NEVER use `--context` flag — use `--issue-type` instead
- [ ] Did NOT run `adapter setup jira --overwrite` after discovery steps

## References

- CLI help: `rai adapter setup --help`, `rai backlog fields --help`
- Complement: `/rai-adapter-setup` (also configures Confluence)
- Custom field discovery: `rai backlog fields search --project KEY "term"`
