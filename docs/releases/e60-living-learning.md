# Kokoro Living Learning (E60, unreleased)

E59 gave Kokoro one way to say what it knows and why. E60 makes that knowledge
age, grow and correct itself. Kokoro now knows when a fact is no longer current,
keeps ideas and open questions until someone decides on them, records what each
correction taught it, and plans the next version of a creative one variable at
a time. In every case Kokoro recommends and a person decides.

## Why

Three gaps showed up after E59:

- A validation from six months ago read with the same authority as one from
  last week. Nothing marked context as old, or marked the artifacts built on
  top of it.
- Corrections a person gave Kokoro were lost at the end of the session, or
  were rewritten into skills with no review.
- Creative iteration changed several variables at once. A drop in cost per
  lead was read as a result even when show rate fell further down the funnel.

## What is included

- **Freshness graph** (`runtime/freshness.py`). Artifacts and validations
  carry `refresh_by` and declared dependencies. Statuses: current,
  potentially_stale, stale_by_dependency, stale, superseded. `freshness
  report` gives a recommendation for each node (refresh,
  review_against_upstream, revalidate, and others). Nothing refreshes by
  itself.
- **Revalidation.** `validation_expired` and dependency changes feed a
  revalidation queue (`/kokoro-revalidate`).
- **Loop rollup.** `loop_merged` joins duplicate open questions and keeps the
  provenance of every source loop.
- **Idea bank** (`runtime/ideas.py`). raw → evaluated → selected (human) →
  briefed → tested → learned, or archived. Excerpts are capped at 280
  characters.
- **Learning traces** (`runtime/learning.py`). Five scopes: output, guest,
  team, skill, system. Only a person promotes a trace. Promotion needs an
  approver, a basis (explicit rule, 3 repetitions, a validated result, or
  confirmation) and cannot narrow the scope. `learning_trace_applied` records
  a human-reviewed change reference. It never edits a skill.
- **Creative iteration** (`runtime/creative.py`). 16 iteration families, a
  Preservation Contract, and Signal Distance 1–4. Only distance 1–2 counts as
  a controlled test. A Creative Learning Record mirrors its validation and
  cannot claim validated or invalidated from an uncontrolled test.
- **Grounding** (`runtime/grounding.py`). 7 checks on copy: sources present,
  numbers sourced, testimonials labeled, no AI testimony (Blocked), untrusted
  text isolated, inference not stated as fact, sources fresh (Partial).
- **Voice review** (`runtime/voice.py`). Advisory lint that mirrors the
  Kokoro vocabulary table. Always exits 0.
- **Performance signal** (`kokoro.py signal check`). Reads variants against a
  baseline that the account declares. No baseline means Blocked. Downstream
  stages outrank cost per lead.
- **Routines** (`runtime/routines.py`). 7 declarative recipes:
  freshness-review, loop-rollup, revalidation-queue, idea-harvest,
  creative-signal-read, learning-review, weekly-scorecard. A recipe that
  writes needs action permission. No recipe writes skills, commands or rules.
- **4 gates** in `kokoro-quality-gates.md`: GATE-CONTEXT-FRESH,
  GATE-GROUNDED, GATE-PERFORMANCE-SIGNAL and GATE-LEARNING-PROMOTION.
  Phase 5.5 Evidence Integrity in `kokoro-orchestrator-contract.md`.
- **13 commands**: `/kokoro-loop-capture`, `/kokoro-loop-rollup`,
  `/kokoro-hypothesis`, `/kokoro-hypothesis-validate`, `/kokoro-revalidate`,
  `/kokoro-iterate`, `/kokoro-idea-harvest`, `/kokoro-idea-evaluate`,
  `/kokoro-idea-brief`, `/kokoro-refresh`, `/kokoro-grounding-review`,
  `/kokoro-voice-review`, `/kokoro-learn`. The router maps signals to them.
- **12 knowledge files** for the contracts above, and an updated
  `kokoro-learning-dashboard.md` with 10 sections fed by the ledger.
- Existing commands gained focused sections: `/kokoro-creative-review` reads
  the grounding result, `/kokoro-experiment` opens loops and records freshness
  after the verdict, `/kokoro-retrospective` lists memory candidates, and
  `/kokoro-scorecard` reads `evidence summary` and emits signals, not
  recommendations.
- Policies: `docs/policies/supply-chain.md` and `docs/policies/licenses.md`.

## Architecture

```text
freshness.py  ideas.py  learning.py  creative.py     (domain modules)
      \           |          |           /
       +------ runtime/projections.py ------+        (joins reducers, views, summary)
                          |
              runtime/evidence_ledger.py             (one hash-chained ledger)
                          |
     .kokoro/shared/events/evidence/*.json  ->  .kokoro/shared/views/evidence/*.yaml
```

- Each domain module owns its event types, reducers, validation and views.
  `projections.py` joins them and refuses a duplicate event type.
- There is one ledger. The E59 hash chain, idempotency and tamper checks
  cover every new event. The ledger now has 24 event types.
- Reducers receive a replay context (`sequence`, `occurred_at`), so a replay
  rebuilds the same views on any machine.
- `grounding.py`, `voice.py`, `routines.py` and `signal check` are pure
  checks. They do not write to the ledger.
- `agent_graph.py` is unchanged. It still runs only `growth-diagnosis-v1`.

## Safety

- A Blocked gate exits 3, like the E58 graph. A ledger refusal exits 2.
  Tampering exits 4.
- No cron, no scheduler, no automatic refresh and no automatic promotion.
- Learning never edits skills, commands or rules.
- Copy that fails grounding is not sent to creative review as ready.
- External text (web pages, reviews, transcripts) is data, never instructions.
- Performance thresholds come only from the baseline the account declares.
  There are no global defaults.
- No Parker code, prompts, dependency or MCP. No external package was added.

## Tests

`python3 -m unittest discover -s tests -p 'test_*.py'`: 123 tests, OK.
`tests/test_living_learning.py` covers the domain modules, projections,
replay determinism, gate exit codes and the CLI.

## What is not included

- The governed workflows `hypothesis-validation-v1`, `creative-iteration-v1`
  and `knowledge-refresh-v1` are documented as manual command sequences with
  human-gate events. They are not added to `agent_graph`, which hard-codes
  `growth-diagnosis-v1`.
- No cron, no automatic refresh, no automatic promotion of learning traces.
- No Parker code, prompts, dependency or MCP.
- No creative generation changes, no new MCP servers, no dreaming or
  self-modification.

## Local run

```text
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence summary --target <project>
K freshness report --target <project>
K freshness gate --ids ART-001,VAL-002 --use decide --target <project>
K grounding check --input-file copy.json
K voice check --input-file copy.txt
K signal check --input-file signal.json
K routine list
```

Evidence lives in the private project workspace, never in this package.
