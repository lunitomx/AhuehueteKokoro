# Implementation notes — Living Learning (E60)

Source plan: `docs/research/parker-to-kokoro-evolution.md` (§13–18, §21,
§24–26, §30–37). Release note: `docs/releases/e60-living-learning.md`.

## Deviations

- **§15 governed workflows are manual sequences, not agent_graph workflows.**
  The plan names `hypothesis-validation-v1`, `creative-iteration-v1` and
  `knowledge-refresh-v1` as graph workflows. `runtime/agent_graph.py`
  hard-codes `WORKFLOW_ID = "growth-diagnosis-v1"`; adding three more would
  mean generalizing the E58 runner, its state machine and its tests in the same
  change. Instead each workflow is a documented command sequence with
  human-gate events (`hypothesis_approved`, `idea_selected`, the human review
  on `creative_iteration_reviewed`, `learning_trace_promoted`). The ledger
  already records who decided and when, so the audit trail exists without the
  graph runner. Moving them into the graph is a separate change.
- **Router table covers 13 commands in 14 rows.** §17 lists the signals per
  command; `/kokoro-iterate` gets two rows ("haz variaciones" and the request
  to iterate on the strongest pieces).
- **Learning dashboard keeps `session_log` as a section.** §36 lists 10
  sections; the old Google Ads `session_log` guide stays as sections 13–16
  until every guest has a ledger.

## Decisions

- **One ledger, domain modules joined by projections.** Freshness, ideas,
  learning and creative each own their event types, reducers, validation and
  views. `runtime/projections.py` joins them into the single hash-chained
  E59 ledger and refuses a duplicate event type. One chain means one
  `evidence verify`, one tamper check and one idempotency store. A second
  ledger per domain would have split provenance across files.
- **Reducers get a replay ctx (`sequence`, `occurred_at`).** Timestamps in
  views come from event time, not wall-clock time. Replaying the same events
  on another machine, or on another day, rebuilds byte-identical views
  (`test_replay_is_deterministic`).
- **A Blocked gate exits 3, like E58.** `freshness gate`, `grounding check`
  and `signal check` use the same `_gate_exit` convention as the E58 graph.
  A ledger refusal stays exit 2; tampering stays exit 4. Scripts can tell
  "stop and ask a person" apart from "bad input".
- **Learning never edits skills.** `learning_trace_applied` only records a
  human-reviewed `change_ref` (a PR or commit reference, never a local path)
  for a trace that a person already promoted. The change itself goes through
  the normal review. Kokoro has no code path that writes to
  `.claude/commands/` or `.claude/knowledge/`.
- **Routines are declarative recipes, never scheduled.** 7 built-in recipes
  (freshness-review, loop-rollup, revalidation-queue, idea-harvest,
  creative-signal-read, learning-review, weekly-scorecard). Each declares what
  it reads, what it writes, its command and a cadence suggestion. A recipe that
  writes needs `requires_action_permission`. There is no cron, no scheduler and
  no background process.
- **Performance thresholds come only from an account-declared baseline.**
  `GATE-PERFORMANCE-SIGNAL` reads `min_spend_share`, `min_results`,
  `result_stage`, `fatigue_frequency` and `outcome_lag_days` from a baseline
  with a `source_ref`. No baseline means Blocked. Global defaults would turn a
  cheap lead in one account into a "result" for every account.
- **Voice review is advisory.** `voice check` always exits 0. Vocabulary is a
  matter of style; blocking on it would push people to skip the check.
- **Grounding runs before creative review.** `/kokoro-creative-review` no
  longer carries factual truth. It reads the `GATE-GROUNDED` result and
  reports it.
- **Scorecard emits signals, not recommendations.** A contradiction between
  metrics (lower cost per lead, lower show rate) becomes an open loop.
- **Phase 5.5 instead of renumbering.** The orchestrator contract inserts
  Evidence Integrity as 5.5 so existing references to phases 6–9 stay valid.

## Surprises

- **`kokoro-package.yaml` excluded `runtime/learning.py`.** The exclusion
  came from the E68 curated release, when a different `learning.py` was kept
  out of the package. The E60 `learning.py` is required by
  `projections.py` and by `install/verify.sh`. The entry was removed.
- **The README command count was 89, and `.claude/commands/` also holds a
  `work/` directory.** Counting with `ls .claude/commands/*.md` gives the
  number of commands; a recursive count would include the folder. The README
  now says 102 (89 + 13).
- **The `creative`, `learning` and `routines` CLI groups do not exist under
  those names.** The CLI exposes `signal check`, `routine list|show|check`,
  `grounding check` and `voice check`. Docs use the real names.
- **The binary-framing forbidden list cited in `/kokoro-creative-review`
  (`tests/skills/_forbidden/binary_framing.txt`) is not in this repository.**
  The new sections avoid those terms anyway; restoring the test is out of
  scope.
- **`install/install.sh` copies whole directories.** It has no explicit list
  of commands or knowledge files, so new files ship without installer changes.
  `install/verify.sh` now requires the 12 new knowledge files.
- **Routines pointed at a folder git does not ignore.** The first version of
  `routines.py` allowed private writes under `.kokoro/private/`. The workspace
  `.gitignore` covers `.kokoro/local/` and `.kokoro/secrets/`, not `private/`.
  Fixed in a separate commit, with a test.
- **The research doc and the runtime use different field names.** Examples:
  `guest_id` vs `guest`, `validated_on` vs `generated_on`, `running` hypothesis
  status. The runtime is the contract; commands and knowledge files follow it.
- **A blocked `evidence check` on a loop exits 2, not 3.** That behavior comes
  from PR A (E59) and is kept. `freshness gate`, `signal check` and
  `grounding check` exit 3 when Blocked.
- **`origin` is a string on hypotheses and an object elsewhere.** It is
  inherited from E59 and documented as is; unifying it would break stored
  ledgers.
