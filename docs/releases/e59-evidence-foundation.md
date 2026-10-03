# Kokoro Evidence Foundation (E59, unreleased)

This change gives Kokoro one shared way to say what it knows, why it believes
it, what it does not know yet, and what evidence could change its mind. It also
restores the guest registry that `/kokoro-client` and 27 other commands depend
on (issue #43).

## What is included

- **Evidence Model v1** (`.claude/knowledge/kokoro-evidence-model.md`): 9
  epistemic states (observed, reported, inferred, hypothesis, validated,
  invalidated, inconclusive, insufficient, stale), allowed transitions, and
  Provenance v1 for every piece of evidence. Numbers carry numerator,
  denominator, window, unit, platform and attribution. Guest words are a
  verified quote, a paraphrase or illustrative copy; AI-written phrases are never
  stored as testimonials.
- **Open Questions v1** (`.claude/knowledge/kokoro-open-questions.md`): loops
  with a lifecycle (captured → ranked → promoted → hypothesis → closed or
  archived), six business territories next to the four phases, and a 5-dimension
  ranking.
- **7 evidence gates** in `kokoro-quality-gates.md`, enforced in code.
- **Evidence ledger** (`runtime/evidence_ledger.py`): 8 event types, append-only
  and hash-chained under `.kokoro/shared/events/evidence/`, with rebuildable
  views under `.kokoro/shared/views/evidence/`. Idempotent retries replay; key
  conflicts and tampering fail closed with exit code 4.
- **Precommitted evidence bar**: a hypothesis stores the digest of its four
  outcome criteria; human approval and every validation must match it. Moving
  the bar requires an explicit redesign (`supersedes` + `redesign_reason`).
- `/kokoro-validate` produces the hypothesis id, the bar and the experiment id.
  `/kokoro-experiment` keeps 3x3x3, takes `source_hypothesis_id`, and records its
  result as a formal validation.
- **Guest registry** (`runtime/clients.py`, `kokoro.py client …`): standard
  library replacement for the missing `src/kokoro/clients/`. Unknown fields,
  absolute paths and secret-like values are rejected; writes are atomic and
  refused inside the package checkout.
- Unit tests (`tests/test_evidence.py`, `tests/test_clients.py`) now run in CI;
  `install/verify.sh` smoke-tests both CLIs in a temporary workspace.

## What is not included

No creative iteration, full idea bank, freshness graph, dreaming, automatic
self-improvement, schedules, external hooks, creative generation or new MCP
servers. No external package was added.

## Local run

```text
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K client find --name "<nombre>" --target <project>
K evidence check  --kind loop --input-file loop.json --target <project>
K evidence append --type loop_captured --input-file event.json \
  --idempotency-key <key> --target <project>
K evidence verify --target <project>
```

Evidence lives in the private project workspace. Only `team` privacy class
evidence enters the shared ledger. Text from web pages, reviews, comments,
competitor pages, transcripts or documents is stored as data and never changes
rules, statuses or approvals.
