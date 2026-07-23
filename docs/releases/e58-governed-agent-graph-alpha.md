# Kokoro Agent Graph v0.2.0-alpha.1

This alpha adds one bounded, local-first growth-diagnosis graph to the public
Kokoro package.

## What is included

- An append-only, hash-chained local event ledger.
- Deterministic `start`, `next`, `submit`, `status`, `resume`, `doctor` and
  `close --abandon` operations.
- One built-in `growth-diagnosis-v1` workflow with plan, execute, critique,
  verify and host-attested user approval nodes.
- Canonical JSON artifacts rendered into the existing Spanish diagnosis format.
- Claude/Codex-compatible host packets executed sequentially by one host.

## What is not included

This alpha does not call model providers, execute MCP tools, mutate campaigns,
CRM records or repositories, promote memory automatically, perform automatic
reflection, or claim independent multi-agent collaboration. Those capabilities
remain governed follow-up work.

## Local run

Initialize a separate project with Kokoro, then use the installed runtime:

```text
python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" graph start \
  --workflow growth-diagnosis-v1 --target <project> \
  --input-file <project>/growth-input.json --idempotency-key <key>
```

The run stays under `.kokoro/local/agent-runs/`. The event ledger is canonical;
`state.json` is a rebuildable projection. Do not place credentials in input or
result files. A host-attested approval records an interaction provenance label;
it is not cryptographic identity authentication.

## Release identity

The public merge SHA is the primary immutable identity for this alpha. The
annotated tag `v0.2.0-alpha.1` is a human-readable alias and must resolve to
that same merge commit.
