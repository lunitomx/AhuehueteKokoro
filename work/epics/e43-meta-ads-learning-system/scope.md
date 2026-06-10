# Epic E43: Meta Ads Learning System — Scope

> **Status:** COMPLETE
> **Created:** 2026-06-09

## Objective

Replicate the Google Ads learning loop pattern (E42) for Meta Ads so
returning invitados who work with Meta campaigns see what was reviewed,
what was learned, and what remains pending — without restarting from zero.

**Value:** Meta Ads invitados get the same control surface that Google Ads
invitados already have. The learning system unifies both platforms under
the same schema vocabulary.

## Stories (4 planned)

| ID | Story | Size | Status | Description |
|----|-------|:----:|:------:|-------------|
| S43.1 | Meta Ads Learning Record Schema | M | Planned | Define Meta Ads-specific fields for the learning record: campaign_objective, audience_type, placements, creative_count, corpus_angle. Extend S42.1 schema. |
| S43.2 | Persist Meta Ads Learning on Close | M | Planned | Update kokoro-ads.md to write full Meta Ads context on session close. Add platform, campaign_objective, audience_type, placements, creative_count, learning_state. |
| S43.3 | Surface Meta Ads Learning on Open | M | Planned | Update kokoro-open.md to show Meta Ads context when last session was Meta Ads. |
| S43.4 | Meta Ads + Cross-Platform Client Guide | S | Planned | Extend the client guide to cover Meta Ads and explain how Google Ads + Meta Ads learning coexist. |

**Total:** 4 stories, 10 SP

## Scope

### In scope (MUST)
- Define Meta Ads-specific fields additive to the E42 learning record schema.
- Make kokoro-ads.md write the full context on close.
- Make kokoro-open.md show Meta Ads context alongside Google Ads context.
- Extend the client guide to cover both platforms.
- Preserve backward compatibility with existing session_log entries.

### In scope (SHOULD)
- Unify the presentation template so both platforms use the same block pattern.

### Out of scope
- New MCP server for Meta Ads (already exists: `meta-ads-mcp`).
- Meta Ads analytics dashboard or UI.
- Changing Meta Ads bidding or campaign structure.
- Private runtime or credential storage.

## Done Criteria

### Per story
- [x] Schema fields defined, additive, and backward compatible.
- [x] kokoro-ads.md writes platform, campaign_objective, audience_type, placements, creative_count, learning_state.
- [x] kokoro-open.md shows Meta Ads context for returning invitados.
- [x] Client guide covers Meta Ads + cross-platform learning.

### Epic complete
- [x] A returning Meta Ads invitado sees campaign context and next step on open.
- [x] The learning history supports client control across both platforms.
- [x] The epic retrospective captures the reusable cross-platform pattern.
- [x] Merged to main.

## Dependencies

```
S43.1 (schema, extends S42.1)
  ↓
S43.2 (persist on close)
  ↓
S43.3 (surface on open)
  ↓
S43.4 (client guide)
```

**External:** E42 Google Ads Learning System (complete). The schema, persist,
and surface patterns are proven and reusable.

## Architecture

| Decision | Rationale |
|----------|-----------|
| Extend S42.1 schema, don't create a separate one | One learning record vocabulary for both platforms |
| Meta Ads fields are additive and optional | Same backward-compatibility strategy as E42 |
| Same open/close/persist pattern as E42 | Proven, consistent, teachable |

## Risks

| Risk | L/I | Mitigation |
|------|:---:|------------|
| Meta Ads fields diverge from Google Ads vocabulary | M/M | Keep field naming aligned; both platforms share `platform`, `learning_state`, `summary`, `hallazgos`, `next_action` |
| kokoro-ads.md is a large command file | M/L | Patch the session_log block only; don't refactor the whole file |

## Implementation Plan

### Sequence

| Order | Story | Rationale |
|-------|-------|-----------|
| 1 | S43.1 | Schema first — defines what fields exist |
| 2 | S43.2 | Once schema stable, close path writes it |
| 3 | S43.3 | After writeback exists, open surfaces it |
| 4 | S43.4 | Finish with client explanation |

### Milestones

| Milestone | Stories | Success Criteria |
|-----------|---------|------------------|
| M1: Schema ready | S43.1 | Meta Ads fields defined, backward compatible |
| M2: Close writeback | S43.2 | kokoro-ads.md writes full Meta Ads context |
| M3: Open surface | S43.3 | Returning Meta Ads invitado sees context on open |
| M4: Client ready | S43.4 | Guide covers both platforms |

## Parking Lot

- Analytics integration: auto-detect learning_state from Meta Ads MCP data.
- Creative performance tracking: which creatives fed which angles in the corpus.
- Cross-platform learning summary: unified view of Google Ads + Meta Ads sessions.
