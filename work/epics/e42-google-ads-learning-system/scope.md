# Epic E42: Google Ads Learning System — Scope

> **Status:** IN PROGRESS
> **Created:** 2026-06-08

## Objective

Build a Google Ads learning loop inside Kokoro so each invitado can see what was
reviewed, what was learned, and what remains pending across sessions. The goal is
to give clients control over their Adwords interactions through a structured
history, not through a one-off diagnosis. This epic defines the knowledge model
only; execution against MCP, env, or private runtime lives elsewhere.

**Value:** Returning clients stop restarting from zero. Kokoro becomes a memory
system for Google Ads work: each session leaves a trace, the next session picks up
that trace, and the control surface stays readable for the invitado.

## Stories (4 planned)

| ID | Story | Size | Status | Description |
|----|-------|:----:|:------:|-------------|
| S42.1 | Learning Record Schema | M | Planned | Define the Google Ads learning entry so it fits the existing session log and stays backward compatible. |
| S42.2 | Persist Learning on Close | M | Planned | Make Google Ads closeout write hallazgos, summary, and next_action in a consistent format. |
| S42.3 | Surface Learning on Open | M | Planned | Show the most recent Google Ads sessions and the proposed focus when a returning invitado opens Kokoro. |
| S42.4 | Client Learning Guide | S | Planned | Document how clients read, trust, and reuse the Google Ads learning history. |

**Total:** 4 stories, 10 SP

## Scope

**In scope (MUST):**
- Define a Google Ads-specific learning entry that is additive to `session_log`.
- Make the open/close/run flow reuse the same learning vocabulary.
- Keep the history useful for clients who want to review previous Adwords
  interactions before deciding the next step.
- Preserve invitation-based behavior and avoid silent account mutations.
- Keep the public repository free of `.env`, MCP wiring, and private runtime
  secrets.

**In scope (SHOULD):**
- Add compact examples for Search, Display, and PMax.
- Add a client-readable recap format for recent sessions and next_action.

**Out of scope:**
- A separate analytics dashboard → defer to a future product surface.
- Any new MCP server or provider integration → defer to runtime epics.
- Storing raw account exports or screenshots in the public repo → defer to the
  private workspace only.
- Any env, credential, or runtime bootstrap work → defer to private operational
  setup.

## Done Criteria

**Per story:**
- [ ] Contract or doc change is explicit and backward compatible.
- [ ] The learning loop remains readable for non-technical clients.
- [ ] Sensitive data is not added to the public repository.

**Epic complete:**
- [ ] A returning invitado can see the last Google Ads sessions and the pending
      next step.
- [ ] The learning history supports client control over Adwords interactions
      without requiring them to re-explain context.
- [ ] The epic retrospective captures the reusable learning pattern for Kokoro.
- [ ] Merged to `main`.

## Dependencies

```
S42.1 (schema)
  ↓
S42.2 ──┐
  ↓      │
S42.3 ◄──┘
  ↓
S42.4 (guide)
```

**External:** None

## Implementation Plan

### Sequence

| Order | Story | Rationale | Status |
|---|---|---|---|
| 1 | S42.1 Learning Record Schema | Foundation first: the schema defines what the rest of the epic can persist and display. | Planned |
| 2 | S42.2 Persist Learning on Close | Once the schema is stable, the close flow can write it consistently. | Planned |
| 3 | S42.3 Surface Learning on Open | After writeback exists, open can use the stored learning as the control surface. | Planned |
| 4 | S42.4 Client Learning Guide | Finish with the client-facing explanation once the system shape is stable. | Planned |

### Milestones

| Milestone | Stories | Success Criteria |
|---|---|---|
| M1: Schema ready | S42.1 | The learning record is explicit and backward compatible. |
| M2: Close writeback | S42.2 | Google Ads sessions persist the same learning vocabulary consistently. |
| M3: Open surface | S42.3 | Returning invitado work starts from recent learning, not from scratch. |
| M4: Client ready | S42.4 | Clients can read and reuse the learning system without internal context. |

### Progress Tracking

| Story | Size | Status | Actual | Velocity | Notes |
|---|---:|---|---:|---:|---|
| S42.1 | M | Done | 2h | — | Schema canónico; 10 campos Google Ads opcionales, backward compatible |
| S42.2 | M | Planned | - | - | Persist learning on close. |
| S42.3 | M | Planned | - | - | Surface recent learning on open. |
| S42.4 | S | Planned | - | - | Write the client learning guide. |

## Architecture

| Decision | ADR | Summary |
|----------|-----|---------|
| Extend the existing `session_log` model instead of creating a separate learning store | N/A | Keeps the system compatible with current Kokoro open/close behavior and avoids a second history mechanism. |
| Surface learning through the existing command flow rather than a new UI | N/A | Makes the control loop available where clients already work today. |

> Problem Brief: N/A

## Risks

| Risk | L/I | Mitigation |
|------|:---:|------------|
| The learning log becomes too generic to be useful | M/H | Keep Google Ads examples and language in the schema, open flow, and guide. |
| The history becomes a dump of raw session notes | M/H | Require compact summary, hallazgos, and next_action fields, and keep the entry format small. |
| Clients confuse learning history with automatic account control | M/H | Keep the invitation gate explicit and separate recommendations from action. |

## Parking Lot

- Client-facing recap format for other channels beyond Google Ads → future epic.
- Optional visual summary export → defer until a real delivery surface exists.
