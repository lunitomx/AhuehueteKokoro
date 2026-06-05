# Kokoro Orchestrator Contract

Use this contract for every Kokoro operating run: Google Ads, weekly marketing, creative campaign, launch, acquisition, share readiness, and future executive workflows.

## Purpose

An orchestrator does not give isolated advice. It guides a complete decision process:

1. understand the objective
2. resolve context
3. verify runtime capability
4. gather available evidence
5. load Kokoro knowledge
6. interpret the signal
7. recommend next actions
8. ask permission before mutation
9. capture the next step

## Phases

| Phase | Name | Required Output |
|---:|---|---|
| 1 | Invitation and objective | One-sentence objective and one clarifying question if needed |
| 2 | Context resolution | Guest, temporary context, or explicit "without saved context" decision |
| 3 | Runtime capability | Which tools/files/MCPs are available or missing |
| 4 | Data extraction plan | What will be queried or inspected before analysis |
| 5 | Knowledge load | Which Kokoro knowledge files guide interpretation |
| 6 | Analysis | Findings separated from assumptions |
| 7 | Executive recommendation | Ranked actions, confidence, and what not to touch yet |
| 8 | Permission gate | Explicit invitation before account or artifact mutation |
| 9 | Close and next step | Saved/communicated next action and unresolved blockers |

## Gate Statuses

Use only these statuses:

| Status | Meaning | Continue? |
|---|---|---|
| Pass | Enough evidence exists for the next phase | Yes |
| Partial | Some evidence exists; recommendation must lower confidence | Yes, with caveat |
| Blocked | Required condition is missing | No data-backed claim |
| Skipped | Gate does not apply to this route | Yes |

Never convert `Blocked` into a guess. A blocked data gate can still produce a setup recommendation.

## Required Gates

| Gate | Applies When | Pass Evidence | Blocked Behavior |
|---|---|---|---|
| `GATE-OBJECTIVE-CLEAR` | Every run | Objective restated in business language | Ask one clarifying question |
| `GATE-CONTEXT-RESOLVED` | Every run | Guest profile, context file, or explicit temporary context | Continue only as general guidance |
| `GATE-MCP-REGISTERED` | Data-backed platform runs | MCP server is registered or callable | Provide setup path, no platform-data claim |
| `GATE-MCP-HEALTHY` | Data-backed platform runs | Health check or successful discovery call | Continue with other sources only |
| `GATE-DATA-COMPLETE` | Data-backed analysis | Required datasets queried or marked unavailable | Mark recommendation confidence Partial/Blocked |
| `GATE-KNOWLEDGE-LOADED` | Every run | Relevant `.claude/knowledge/` files named | Load before recommendation |
| `GATE-NO-SENSITIVE-DATA` | Every run | No secrets, real guest data, exports, or reports persisted publicly | Stop and move data private |
| `GATE-RECOMMENDATION-ONLY` | Before action | Recommendation separated from mutation | Do not call action tools yet |
| `GATE-ACTION-INVITED` | Any mutation | User explicitly asks to create/update/publish/change | Stop until invited |

## Standard Output Template

```markdown
## {Run Name} — {Guest or Context}

| Gate | Status | Evidence |
|---|---|---|
| Objective clear | {Pass/Partial/Blocked/Skipped} | {evidence} |
| Context resolved | {Pass/Partial/Blocked/Skipped} | {evidence} |
| MCP registered | {Pass/Partial/Blocked/Skipped} | {evidence} |
| MCP healthy | {Pass/Partial/Blocked/Skipped} | {evidence} |
| Data completeness | {Pass/Partial/Blocked/Skipped} | {evidence} |
| Knowledge loaded | {Pass/Partial/Blocked/Skipped} | {evidence} |
| Privacy check | {Pass/Partial/Blocked/Skipped} | {evidence} |

### Executive Read
{plain-language interpretation of what the evidence says}

### What I Would Not Touch Yet
{changes to avoid because evidence is insufficient, learning period is active, or risk is high}

### Recommended Next Actions
| Priority | Action | Confidence | Why |
|---:|---|---|---|
| 1 | {action} | High/Medium/Low | {evidence} |

### Permission Gate
{explicit invitation question before mutation}

### Next Step
{one next action or blocker}
```

## Fallback Rules

### MCP Missing

If MCP is not registered:

- Do not claim live platform data.
- Say which MCP is missing.
- Offer setup via `/kokoro-mcp-reference` or `/kokoro-connect`.
- Continue only with static context or general methodology if useful.

### MCP Unhealthy

If MCP is registered but unhealthy:

- Report "not connected" or "not responding"; do not expose tracebacks.
- Query other available platforms if relevant.
- Mark data completeness `Partial` or `Blocked`.

### Data Missing

If a dataset is unavailable:

- State exactly what is missing.
- Lower recommendation confidence.
- Prefer "what to verify next" over "what to change now."

## Permission Boundaries

The following actions require explicit invitation:

- creating or editing campaigns
- changing budgets or bidding
- adding keywords or negatives
- publishing ads or content
- changing landing pages
- uploading reports or files
- committing guest-specific artifacts
- sending messages to guests or teams

Allowed without extra permission:

- reading public repo files
- reading local methodology files
- summarizing already-provided context
- querying MCP read-only tools after the user asks for a data-backed review
- drafting recommendations

## Privacy Rules

- Never ask for API keys, access tokens, refresh tokens, or client secrets in chat.
- Never persist real guest data in public repo files.
- Use `cliente_NN` in public artifacts.
- Treat exports, reports, generated assets, and platform mappings as private.
- Apply `kokoro-share-readiness.md` before sharing or packaging.

## Knowledge Load Rules

Every orchestrator must name the knowledge files it uses.

Examples:

| Run | Required Knowledge |
|---|---|
| Google Ads | `kokoro-mcp-google-ads.md`, relevant `google-ads/` files |
| Weekly Marketing | `kokoro-analytics-metrics.md`, `kokoro-pulse-guide.md`, platform MCP refs |
| Creative Campaign | `kokoro-ads-meta.md`, `kokoro-meta-ai-ecosystem.md`, `kokoro-creative-gemini.md`, `kokoro-creative-diversification.md` |
| Launch | `kokoro-phase2-canvas.md`, `kokoro-phase2-forces.md`, `kokoro-phase3-pescar.md`, `kokoro-phase3-launch.md` |
| Acquisition | `kokoro-phase4-funnel.md`, `kokoro-phase4-mafia.md`, `kokoro-lean-landing.md`, `kokoro-tracking-checklist.md` |
| Share Readiness | `kokoro-privacy-protocol.md`, `kokoro-share-readiness.md` |

## Creative Asset Rules

When the requested output is a visual campaign, carousel, ad image, or paid creative, the orchestrator must add these gates before generation:

| Gate | Pass Evidence | Blocked Behavior |
|---|---|---|
| `GATE-PROMISE-TRUE` | The real offer, event, or next step is stated without overstating what happens | Reframe the promise before copy or image generation |
| `GATE-STORYBOARD-APPROVED` | Each frame has one thought, one emotion, and one role in the decision journey | Do not generate assets yet |
| `GATE-VISUAL-DIRECTION-CLEAR` | Gaze, focal point, hierarchy, brand assets, and prohibited changes are specified per frame | Ask for or infer only the minimum missing visual decision |
| `GATE-CREATIVE-REVIEWED` | Draft assets or specs have been reviewed for attention, clarity, Meta AI signal, and CTA path | Treat output as draft only |

For carousel work, do not produce five isolated images. Produce a story arc first:

1. hook
2. tension
3. reframe
4. choice or proof
5. invitation

Use this operating standard: one image, one thought, one emotion, one advance.

## Confidence Language

Use these confidence labels:

| Confidence | Use When |
|---|---|
| High | Context, MCP/data, and knowledge gates pass |
| Medium | Context and knowledge pass, data is partial |
| Low | General guidance only; data gates blocked |

## Anti-Patterns

- Giving recommendations before loading the relevant knowledge.
- Calling action tools during diagnosis.
- Treating missing MCP data as zero performance.
- Showing raw JSON without business interpretation.
- Saving private exports or reports in the public repo.
- Asking multiple clarifying questions when one question can unlock the next step.
