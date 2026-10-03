# Implementation notes — Evidence Foundation (PR A) + issue #43

Source plan: `docs/research/parker-to-kokoro-evolution.md` (P0 + PR A).

## Deviations

- **Ledger lives in `evidence/` subfolders.** The spec named
  `.kokoro/shared/events/` and `.kokoro/shared/views/`. Memory v2 already writes
  `events/<year>/*.yaml` (found with `rglob`) and owns `views/open-loops.yaml`.
  Sharing those paths would give one file two writers. The ledger uses
  `events/evidence/*.json` and `views/evidence/*.yaml`, so each file has one
  writer and Memory v2 never parses ledger events.
- **8 event types, not the reference list.** Added `loop_archived` (the
  lifecycle needs it). Dropped `hypothesis_resolved` (derived from
  `validation_recorded`), `revalidation_recorded` (it is `validation_recorded`
  with `revalidates`) and a `running` hypothesis status (the experiment owns
  run state).
- **GATE-NO-CONCLUSION-HIDDEN folded into GATE-QUESTION-EXACT.** The research
  doc lists it separately; the spec asked for exactly 7 gates.
- **Hypothesis ids accept `HIP-` and `HYP-`.** `/kokoro-validate` already emits
  `HIP-001`; renaming would break existing state files.

## Decisions

- **Redesign is a new hypothesis, not a new event type.** `hypothesis_created`
  with `supersedes` + `redesign_reason` marks the old one `superseded` and needs
  a fresh human approval. The bar digest is checked at creation, approval and
  validation.
- **Views are canonical JSON with a `.yaml` extension.** Valid YAML 1.2, no
  YAML dependency, byte-identical on rebuild.
- **`privacy_class` reuses Memory v2 visibility.** Only `team` enters shared
  evidence; the other three tiers are rejected rather than redacted.
- **Untrusted content is Partial, never Blocked.** Blocking would let a hostile
  review suppress real evidence. The text is stored as a claim and flagged.
- **Validations may propose only `guest_knowledge` or `open_question`
  updates.** System rules change only through a reviewed pull request.
- **One confidence constant.** `growth_diagnosis.CONFIDENCE_LEVELS` is now the
  single source for low/medium/high.
- **`directory_lock` extracted from `agent_graph`** so the ledger reuses the E58
  lock instead of copying it.
- **#43 fixed with a standard-library port, not by restoring `src/`.** The
  package has no installable Python project; `runtime/` is what install copies.

## Surprises

- `/kokoro-client` and 27 commands referenced `src/kokoro/clients/`, which the
  public package never shipped. 7 commands embedded Python snippets that
  imported it and could only fail.
- `privacy_scan.py` flags any path part named `clients`, so test fixtures use
  `cliente_01` slugs and fake tokens are assembled at runtime.
- zsh does not word-split `$VAR` holding a command; smoke scripts use a shell
  function instead.
- The session-log knowledge file used a real-looking guest id; replaced with
  `cliente_01`.
