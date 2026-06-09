# Google Ads Negative Keywords — Local Adapter Contract

> Kokoro local adapter layer for negative keyword operations.
> The official Google Ads MCP server is read-only for negatives;
> mutation, audit, and state tracking live in this adapter.

## Runtime Path

This contract lives in the Kokoro public repository (`.claude/knowledge/`).
The adapter runtime executes in the operator's private workspace (`~/.hermes/`,
`.kokoro/`, or project-local Python adapter) — never in the public repo.

At story close, the implementability check (AC5) confirmed: the adapter
executes as a Hermes skill or local Python module in the operator's private
runtime. The public repo only carries the contract and command surface.

## Adapter: `negative_keyword.delete`

### Input

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `action` | `"delete"` | Yes | Fixed value for this operation |
| `text` | `string` | Yes | Negative keyword text to remove |
| `match_type` | `"EXACT"\|"PHRASE"\|"BROAD"` | Yes | Match type of the keyword |
| `scope` | `object` | Yes | `{customer_id, campaign_id?, ad_group_id?}` |
| `dry_run` | `boolean` | No | Default `false`. When `true`, resolves but does not mutate |

### Output

| Field | Type | Description |
|-------|------|-------------|
| `status` | `"removed"\|"not_found"\|"already_removed"\|"partial"` | Operation result |
| `removed` | `array` | Keywords successfully removed (id, text, match_type, scope) |
| `not_found` | `array` | Keywords that didn't match any active negative (idem to report) |
| `already_removed` | `array` | Keywords already in removed state before this call |
| `errors` | `array` | Partial failures with `{keyword, reason, code}` |
| `audit_event_id` | `string` | Trace ID for this operation (UUIDv4) |
| `dry_run` | `boolean` | Echo of input; when `true`, `removed` is empty |

### Behavior

1. **Discovery first.** The adapter uses the official MCP tools
   (`search`, `get_resource_metadata`, `execute_gaql`) to resolve the
   target keyword's current state before any mutation.

2. **Idempotent.** Calling delete on an already-removed keyword returns
   `status: "already_removed"` with the keyword in `already_removed` — no
   error, no double-counting.

3. **Partial is valid.** When deleting a batch and some keywords don't exist
   or are already removed, the adapter returns `status: "partial"` with
   affected keywords split across `removed`, `not_found`, and
   `already_removed`.

4. **Audit parity with `add`.** Every delete event produces an
   `audit_event_id` and writes an entry to the operator's session log
   with the same structure as `add_negative_keywords`.

5. **No provider mutation assumption.** The adapter never calls a mutation
   tool on the external MCP server. All state changes are local.

### Example

```json
{
  "action": "delete",
  "text": "gratis",
  "match_type": "BROAD",
  "scope": {
    "customer_id": "1234567890",
    "campaign_id": "9876543210"
  },
  "dry_run": false
}
```

Response:
```json
{
  "status": "removed",
  "removed": [
    {
      "id": "nkw-abc123",
      "text": "gratis",
      "match_type": "BROAD",
      "scope": {"customer_id": "1234567890", "campaign_id": "9876543210"}
    }
  ],
  "not_found": [],
  "already_removed": [],
  "errors": [],
  "audit_event_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "dry_run": false
}
```

## Adapter: `negative_keyword.add` (existing, documented for parity)

Already defined in `kokoro-gads.md` Action table. The `add` adapter follows
the same discovery-first, audit-parity, no-provider-mutation pattern. This
contract exists for reference to ensure `delete` and `add` stay aligned.

### Parity Checklist

| Concern | `add` | `delete` |
|---------|:-----:|:--------:|
| Discovery before mutation | ✅ | ✅ |
| Idempotent | ✅ | ✅ |
| Partial success | ✅ | ✅ |
| Audit event per operation | ✅ | ✅ |
| `dry_run` support | ✅ | ✅ |
| No provider mutation | ✅ | ✅ |
| Error codes per keyword | ✅ | ✅ |

## Safety and Regression

- `add_negative_keywords` is unchanged. The delete adapter is additive.
- Both adapters share the same discovery path (official MCP tools only).
- No mutation tool is ever called on the external provider.
- The adapter runtime is private — no credentials, env vars, or account
  mappings live in the public repo.

## Related

- `/kokoro-gads` — tactical Google Ads command including negative keyword
  operations (`.claude/commands/kokoro-gads.md`)
- `/kokoro-google-ads-run` — executive orchestrator with gate structure
- `/kokoro-mcp-reference` — MCP installation and tool catalog
- MCP knowledge: `.claude/knowledge/kokoro-mcp-google-ads.md`
