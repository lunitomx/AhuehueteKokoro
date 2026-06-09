---
epic_id: E43
title: Meta Ads Learning System
status: complete
completed: 2026-06-09
stories:
  S43.1: Meta Ads Learning Record Schema — Done (1h)
  S43.2: Persist Meta Ads Learning on Close — Done (30m)
  S43.3: Surface Meta Ads Learning on Open — Done (30m)
  S43.4: Cross-Platform Client Guide — Done (30m)
---

# E43 Retrospective: Meta Ads Learning System

## Summary

E43 replicated the Google Ads learning loop pattern (E42) for Meta Ads.
The learning record is now cross-platform: Google Ads and Meta Ads share
the same schema vocabulary, same open/close/persist flow, same client
guide. Four stories, one unified system.

## What Shipped

| Story | Result |
|-------|--------|
| S43.1 | Extended learning record schema to Meta Ads: 6 platform-specific fields + shared fields |
| S43.2 | Updated kokoro-ads.md to persist full Meta Ads context on close |
| S43.3 | Updated kokoro-open.md to surface Meta Ads context alongside Google Ads |
| S43.4 | Rewrote client guide to cover both platforms + cross-platform coexistence |

## Operating Doctrine

- The learning record is platform-agnostic. `platform` field distinguishes
  Google Ads (`"google_ads"`) from Meta Ads (`"meta_ads"`).
- Same open → surface → close → persist pattern for both platforms.
- All platform-specific fields are optional — no migration, no breaking changes.
- The client guide explains both platforms in plain Spanish.

## Done Criteria

| Criteria | Status |
|----------|:------:|
| Returning Meta Ads invitado sees campaign context + next step | ✅ S43.3 |
| Learning history supports client control across both platforms | ✅ S43.1 + S43.2 + S43.4 |
| Epic retrospective captures the reusable pattern | ✅ This document |
| Merged to main | ✅ |

## What went well

- Reusing the E42 pattern made E43 fast — same structure, different fields.
- Making the schema cross-platform (single doc for both) was cleaner than
  creating a separate Meta Ads schema file.
- The client guide rewrite naturally unified the two platforms under one
  explanation.

## Cross-platform pattern (reusable for GA4, etc.)

1. Add platform-specific fields to the canonical schema doc
2. Update the platform's skill to write those fields on close
3. Add a platform-specific section to kokoro-open
4. Update the client guide

This pattern can be applied to GA4, Search Console, or any future platform.
