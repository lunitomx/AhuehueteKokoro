---
epic_id: "E42"
title: "Google Ads Learning System"
status: "draft"
created: "2026-06-08"
---

# Epic Brief: Google Ads Learning System

## Hypothesis
If Kokoro turns every Google Ads interaction into a structured learning record and
surfaces that history at open, run, and close time, then each invitado can keep
clear control of what was reviewed, what was learned, and what should happen next.
Unlike ad-hoc chat notes, this system gives a repeatable memory loop instead of a
single-session recommendation.

## Success Metrics
- **Leading:** Every Google Ads session that reaches `/kokoro-close` can persist a
  structured learning entry with summary, hallazgos, and next_action.
- **Lagging:** A returning invitado can open Kokoro, see the last Google Ads
  sessions, and understand the pending next step without re-explaining context.

## Appetite
M — 4 stories

## Scope Boundaries
### In (MUST)
- Define a learning record schema for Google Ads sessions that is compatible with
  the existing `session_log` model.
- Make `/kokoro-google-ads-run`, `/kokoro-gads`, `/kokoro-open`, and
  `/kokoro-close` participate in the same learning loop.
- Expose the most recent Google Ads learnings, hallazgos, and next_action as the
  default control surface for returning invitado work.
- Keep the system invitation-based: recommend and record first, mutate only when
  the user explicitly asks for action.

### In (SHOULD)
- Add Google Ads-specific examples for Search, Display, and PMax sessions.
- Add a short "how to read your learning history" guide for clients.
- Add a compact recap format so clients can reuse the history outside the chat.

### No-Gos
- Building a separate dashboard or UI in this epic.
- Storing private exports, account IDs, or raw screenshots in the public repo.
- Replacing the Google Ads strategy logic with automation that acts without
  invitation.

### Rabbit Holes
- Designing a new database or runtime storage layer before the schema is stable.
- Treating the learning loop as generic marketing notes instead of a client-facing
  control system for Google Ads decisions.
- Rewriting all Kokoro session tooling instead of extending the existing log model.
