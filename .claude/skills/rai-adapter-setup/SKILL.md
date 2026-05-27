---
allowed-tools:
- Read
- Edit
- Bash(rai:*)
description: 'Interactive adapter setup for Jira and Confluence. Detects available
  backends, discovers projects/spaces, generates validated YAML config. 3-4 questions
  max.

  '
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '0'
  raise.frequency: once
  raise.gate: ''
  raise.next: rai-doctor
  raise.prerequisites: ''
  raise.version: 3.0.0
  raise.visibility: public
  raise.work_cycle: utility
name: rai-adapter-setup
---

# Adapter Setup

## Purpose

Guide the user through configuring Jira and/or Confluence adapters using the `rai adapter setup` CLI commands. Uses live discovery to auto-detect projects, workflows, issue types, and spaces — the user never needs to look up IDs manually.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow all steps in order, verify each with `rai doctor`
- **Ha**: Run both setup commands directly, verify once at the end
- **Ri**: Skip to `rai adapter setup jira && rai adapter setup confluence`

## Context

**When to use:** New project setup, after `rai init`, or when `/rai-doctor` reports missing adapter config.

**When to skip:** Adapter config already exists and is working. Use `/rai-doctor` to verify.

**Inputs:** Environment variables must be set for the backends to configure:
- Jira: `JIRA_API_TOKEN` + `JIRA_USERNAME`
- Confluence: `CONFLUENCE_API_TOKEN` + `CONFLUENCE_USERNAME`

## Steps

### Step 1: Check Prerequisites

Ask the user which adapters to configure (jira, confluence, or both).

The setup commands detect credentials automatically and exit with guidance
if any are missing. The required environment variables are:
- Jira: `JIRA_API_TOKEN` + `JIRA_USERNAME`
- Confluence: `CONFLUENCE_API_TOKEN` + `CONFLUENCE_USERNAME`

Token generation: https://id.atlassian.com/manage-profile/security/api-tokens

### Step 2: Configure Jira

```bash
rai adapter setup jira
```

The command interactively:
1. Verifies credentials
2. Prompts for Atlassian site domain and instance name
3. Discovers projects via Jira API
4. Asks which projects to include
5. Generates and previews the config YAML
6. Confirms and writes `.raise/backlog.yaml` (under the `jira:` section)

Use `--overwrite` if config already exists and the user wants to regenerate.

### Step 3: Configure Confluence

```bash
rai adapter setup confluence
```

The command interactively:
1. Verifies credentials
2. Prompts for Atlassian site domain and instance name
3. Discovers spaces via Confluence API
4. Asks which space to use
5. Discovers page tree and suggests artifact routing
6. Generates and previews the config YAML
7. Confirms and writes `.raise/confluence.yaml`

Use `--overwrite` if config already exists and the user wants to regenerate.

### Step 4: Verify

```bash
rai doctor
rai backlog get <KEY-1>
rai docs search "test"
```

Report adapter check results. If all pass, confirm success.

## Output

| Artifact | Destination |
|----------|-------------|
| Jira config | `.raise/backlog.yaml` (section `jira:`) |
| Confluence config | `.raise/confluence.yaml` |
| Verification | Via `rai doctor` |

## Quality Checklist

- [ ] Environment variables set before running setup commands
- [ ] `rai adapter setup jira` completed successfully (if Jira selected)
- [ ] `rai adapter setup confluence` completed successfully (if Confluence selected)
- [ ] `rai doctor` reports no adapter errors
- [ ] `rai backlog get` works without `-a jira` flag

## References

- CLI help: `rai adapter setup --help`
- Diagnostics: `/rai-doctor`
- Credential tokens: https://id.atlassian.com/manage-profile/security/api-tokens
