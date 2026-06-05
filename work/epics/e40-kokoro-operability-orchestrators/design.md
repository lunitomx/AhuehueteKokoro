# E40 Design: Kokoro Operability Orchestrators

## Gemba

The user is not a developer browsing command files. The user is a founder, marketing director, sales leader, or agency operator who has a business question:

- "How is my marketing doing this week?"
- "Where is my ad investment leaking?"
- "What should my team do next?"
- "Can I share this system safely with guests?"

The current repo has strong individual skills, but the user experience depends on knowing which skill to invoke and in what order. This epic adds an operating layer that makes Kokoro process-led.

## Target Components

### 1. Executive Router

Purpose: convert plain-language business intent into the correct orchestrator.

Example routes:

| User Intent | Orchestrator |
|---|---|
| "Review Google Ads" | `/kokoro-google-ads-run` |
| "How is marketing this week?" | `/kokoro-weekly-marketing-run` |
| "Create a visual campaign" | `/kokoro-creative-campaign-run` |
| "Launch this creation" | `/kokoro-launch-run` |
| "Improve acquisition" | `/kokoro-acquisition-run` |
| "Is this ready to share?" | `/kokoro-share-readiness` |

### 2. Shared Orchestrator Contract

Every run must follow the same skeleton:

1. Invitation and objective.
2. Guest/context resolution.
3. Runtime capability check.
4. MCP health check when data is needed.
5. Data extraction plan.
6. Knowledge file load.
7. Analysis.
8. Executive recommendation.
9. Permission gate before actions.
10. Session close / next action capture.

### 3. Gate Catalog

Reusable gates:

- `GATE-CONTEXT-RESOLVED`
- `GATE-MCP-REGISTERED`
- `GATE-MCP-HEALTHY`
- `GATE-DATA-COMPLETE`
- `GATE-KNOWLEDGE-LOADED`
- `GATE-NO-SENSITIVE-DATA`
- `GATE-RECOMMENDATION-ONLY`
- `GATE-ACTION-INVITED`
- `GATE-RUNTIME-DOCS-ACCURATE`

### 4. Google Ads Proof Run

The Google Ads run should explicitly require:

- guest profile or temporary context
- Google Ads MCP discovery
- account selection
- campaigns
- campaign performance
- status and budget
- keywords
- search terms
- negatives
- bidding strategy
- conversion signal
- geographic and demographic breakdowns where available
- auction/competition context where the MCP supports it
- landing and tracking context

No recommendation should be made until the run knows whether the missing data is truly unavailable or simply not queried.

### 5. Creative Campaign Run

The creative campaign run should explicitly require:

- campaign objective and true operating promise
- audience stage, tension, and desired decision
- format constraints such as carousel, static ad, story, or reel
- storyboard before generation
- one dominant thought per visual unit
- visual attention direction for every frame: gaze, focal point, hierarchy, and CTA path
- brand assets and non-negotiables to preserve
- prohibited changes, especially model, brand, claim, or offer changes
- generation specifications only after the storyboard is approved
- creative review before Meta copy and targeting
- permission before generating, exporting, publishing, or saving guest-specific assets

For carousels, the run should treat the asset as a decision journey, not a stack of slides:

1. Hook.
2. Tension or doubt.
3. Reframe.
4. Choice or proof.
5. Invitation.

The core standard is: one image, one thought, one emotion, one advance.

### 6. Privacy Model

Public repo:

- methodology
- command contracts
- placeholders
- examples with fake IDs only
- validation checklists

Private workspace:

- `.kokoro/clients.json`
- guest context files
- platform account mappings
- exports
- generated reports
- session artifacts with private details
- `.env`
- `.raise` runtime state if it contains local identity, sessions, or private telemetry

## Key Contracts

### Orchestrator Output Contract

Every orchestrator should produce:

```markdown
## {Run Name} — {Guest or Context}

| Gate | Status | Evidence |
|---|---|---|
| Context resolved | Pass/Blocked/Skipped | {path or reason} |
| MCP health | Pass/Blocked/Skipped | {server status} |
| Data completeness | Pass/Partial/Blocked | {datasets queried} |
| Knowledge loaded | Pass | {files} |
| Privacy check | Pass | no sensitive data persisted |

### Executive Read
{plain-language interpretation}

### What I Would Not Touch Yet
{patience and no-action recommendations}

### Recommended Next Actions
{ranked by leverage and confidence}

### Permission Gate
{explicit ask before mutation}
```

### Naming

Use direct business names:

- `/kokoro-google-ads-run`
- `/kokoro-weekly-marketing-run`
- `/kokoro-launch-run`
- `/kokoro-acquisition-run`
- `/kokoro-share-readiness`

Avoid internal names that require understanding RaiSE lifecycle terminology.

## Decisions

No ADR required yet. This epic is primarily command-contract and governance work. If later stories add executable CLIs or MCP wrappers, create ADRs for runtime architecture.

## Open Questions

- Should orchestrators live under `.claude/commands/` only, or also as `.agents/skills/` once stabilized?
- Should private guest workspaces be documented as sibling repos instead of folders inside this repo?
- Should Kokoro include a demo guest with fake data for first-run confidence?
