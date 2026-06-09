---
epic_id: E42
title: Google Ads Learning System
status: complete
completed: 2026-06-09
stories:
  S42.1: Learning Record Schema — Done (2h)
  S42.2: Persist Learning on Close — Done (1h)
  S42.3: Surface Learning on Open — Done (1h)
  S42.4: Client Learning Guide — Done (1h)
---

# E42 Retrospective: Google Ads Learning System

## Summary

E42 built a Google Ads learning loop inside Kokoro so returning invitados
see what was reviewed, what was learned, and what remains pending — without
restarting from zero. Four stories, four knowledge artifacts, one coherent
system.

## What Shipped

| Story | Result |
|-------|--------|
| S42.1 | Canonical schema: `.claude/knowledge/kokoro-google-ads-learning-record.md` — 18 fields (8 core + 10 Google Ads) |
| S42.2 | Persist on close: `kokoro-close.md` and `kokoro-gads.md` now write full Google Ads context (task, cadence, landing, changes) |
| S42.3 | Surface on open: `kokoro-open.md` shows campaign_type, learning_state, cadence, landing, change_made, reason |
| S42.4 | Client guide: `.claude/knowledge/kokoro-client-learning-guide.md` — plain Spanish, non-technical |

## Operating Doctrine

- Every Google Ads session leaves a trace in the session_log with full context.
- The schema is flat and optional — no migration, no breaking changes.
- `kokoro-open` surfaces learning without overwhelming the invitado.
- `kokoro-close` persists learning with audit parity.
- The client guide explains the system without code, schemas, or jargon.
- LeanStack attribution (Ash Maurya) is maintained where the framework is used.

## Done Criteria

| Criteria | Status |
|----------|:------:|
| Returning invitado sees last Google Ads sessions + next step | ✅ S42.3 |
| Learning history supports client control without re-explaining | ✅ S42.1 + S42.2 + S42.4 |
| Epic retrospective captures reusable learning pattern | ✅ This document |
| Merged to main | ✅ |

## What went well

- The schema-first approach (S42.1) made persistence (S42.2) and
  presentation (S42.3) straightforward — one canonical source.
- Keeping all fields optional preserved backward compatibility without
  any migration ceremony.
- The client guide (S42.4) in plain Spanish makes the system accessible
  to non-technical invitados.

## What to improve

- The learning loop currently covers Google Ads. Meta Ads, GA4, and
  other platforms would benefit from the same pattern.
- `learning_state` detection is manual — a future story could infer it
  from campaign performance data via MCP.
