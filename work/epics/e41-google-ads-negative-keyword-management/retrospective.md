---
epic_id: E41
title: Google Ads Negative Keyword Lifecycle
status: complete
completed: 2026-06-09
stories:
  S41.1: Contract Discovery — Done (2h)
  S41.2: Action Contract for Delete — Done (1h 30m)
  S41.3: Implement Local Delete Adapter — Done (2h)
  S41.4: Audit + Docs + Regression — Done (45m)
---

# E41 Retrospective: Google Ads Negative Keyword Lifecycle

## Summary

E41 added `negative_keyword.delete` to the Kokoro Google Ads surface as a
local adapter contract. The official Google Ads MCP server is read-only for
negative keyword mutations — all state changes are local, with discovery
through the official MCP tools and audit parity with `add`.

## What Shipped

| Story | Result |
|-------|--------|
| S41.1 | Contract discovery: documented that the official MCP is read-only for negatives |
| S41.2 | Action contract: defined input/output schema for delete with idempotency, partial states, and audit parity |
| S41.3 | Local adapter contract: created `.claude/knowledge/kokoro-google-ads-negative-keywords.md` + updated 3 command files |
| S41.4 | Audit docs + regression: confirmed `add` unchanged, parity checklist documented |

## Operating Doctrine

- The official Google Ads MCP server is read-only for negative keywords.
  Discovery uses `search`, `get_resource_metadata`, and `execute_gaql`.
- Mutation (`add`, `delete`) executes via the local Kokoro adapter in the
  operator's private runtime — never in the public repo.
- Every operation produces an `audit_event_id` and writes to the session log.
- Idempotency is mandatory: `already_removed` is not an error.
- Partial success is valid: a batch delete can split across `removed`,
  `not_found`, and `already_removed`.
- `dry_run` is supported for both `add` and `delete`.

## Done Criteria

| Criteria | Status |
|----------|:------:|
| Se puede eliminar una negativa existente por texto + criterio | ✅ Contract defined |
| Flujo de bitácora registra eventos con estructura equivalente a add | ✅ `audit_event_id` + session log parity |
| Issue #1 puede cerrarse con evidencia de validación | ✅ S41.1 doc + S41.3 contract |
| No hay regresión en acción `add` de negativas | ✅ `add_negative_keywords` unchanged |

## What went well

- The read-only MCP discovery (S41.1) was a critical finding — it shaped
  the entire architecture: local adapter, no provider mutation, audit parity.
- The contract-first approach (S41.2 before S41.3) made the delete adapter
  a natural mirror of `add` rather than a separate design.
- Keeping runtime code out of the public repo was the right call — the
  contract is versioned and visible, credentials stay private.

## What to improve

- S41.3 runtime execution is deferred to the operator's private workspace.
  A future epic in the private repo should implement the Python adapter
  that reads this contract and executes against live accounts.
- The parity checklist should be checked whenever `add` changes — it's
  easy to update one side and forget the other.
