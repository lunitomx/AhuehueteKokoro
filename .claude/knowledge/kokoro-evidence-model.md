# Evidence Model v1

> Answers four questions about every claim Kokoro makes: What do I know?
> Why do I believe it? What don't I know yet? What evidence could change my
> mind?

The canonical rules live in code: `runtime/evidence.py` (validators and gates)
and `runtime/evidence_ledger.py` (events and views). This file explains them.
If this file and the code disagree, the code wins and this file is the bug.

## Why

A recommendation is only as strong as the weakest claim under it. Without a
shared model, "the guest said", "Meta reported", "I think" and "we tested it"
all sound equally certain. That is how an inference turns into a "fact" by
repetition.

The rule: **observed ≠ reported ≠ inferred ≠ hypothesis ≠ validated.** No
state becomes `validated` by convenience. Only a recorded validation against a
human-approved, precommitted evidence bar can produce it.

## The 9 states

There are three groups:

- **Support** — how a single piece of evidence reached us: observed, reported, inferred.
- **Bet** — a claim we decided to test: hypothesis.
- **Resolution** — the result of a test: validated, invalidated, inconclusive, insufficient. Plus stale, when time or context expires a resolution.

| State | Meaning | Required evidence | Cannot claim |
|---|---|---|---|
| `observed` | Kokoro or the team saw it directly in a source of truth. | Provenance with `source_ref`, dates and scope. Numbers need the metric block. | That it holds outside its scope or window. 56 leads in October do not say anything about November. |
| `reported` | A person told us. The guest, a teammate, an interviewee. | Provenance with who reported it (slug) and when. | That it happened. "Sales went up" is a report until the CRM shows it. |
| `inferred` | Kokoro or the team concluded it from other evidence. | Provenance with `source_type: kokoro_inference` or a stated reasoning source. | That it was seen. An inference never counts as the only support for `validated`. |
| `hypothesis` | A falsifiable bet with a precommitted evidence bar and an experiment. | A hypothesis record that passes GATE-HYPOTHESIS-FALSIFIABLE and GATE-EVIDENCE-BAR-PRECOMMITTED. | Any result. A hypothesis is a question with a bar, not an answer. |
| `validated` | The result met the `validated` criterion of the precommitted bar. | Approved hypothesis, matching bar digest, `evidence_for` with at least one non-inferred item. | That it is permanent. It carries a `freshness` block with `refresh_by`. |
| `invalidated` | The result met the `invalidated` criterion. | `evidence_against`. | That the opposite is validated. Invalidating "portals wins" does not validate "follow-up wins". |
| `inconclusive` | Evidence exists but points both ways or sits between the criteria. | `evidence_for` **and** `evidence_against`. | A winner. |
| `insufficient` | There was not enough evidence to judge against the bar. | `missing_evidence`: what was missing. | Anything about the hypothesis. It is a statement about the test, not the market. |
| `stale` | A former resolution that expired or whose context changed. | A `validation_expired` event with a reason. | The old result. It must be revalidated before use. |

### Transitions

```
observed ─┐
reported ─┼─► inferred ─► hypothesis ─► validated ───► stale ─► hypothesis
          └──────────────►            ├► invalidated ─► stale
                                      ├► inconclusive ─► hypothesis (redesign)
                                      └► insufficient ─► hypothesis (redesign)
```

- There is no edge from observed, reported or inferred to validated.
  `evidence.check_transition` rejects it.
- `inconclusive` and `insufficient` lead back to a new hypothesis, usually a
  redesign with a bigger sample or a sharper bar.
- `stale` never leads back to `validated` directly. A new validation must be
  recorded with `revalidates: VAL-…`.

### Examples (synthetic, `cliente_01`)

| Claim | State | Why |
|---|---|---|
| "Meta Ads shows 56 leads for variant A between Oct 2 and Oct 16." | observed | Read from the platform with a window and a unit. |
| "The guest says despachos switch portals ten times a day." | reported | Nobody has observed it yet. |
| "Despachos probably care more about portals than about errors." | inferred | Kokoro concluded it from the interviews. |
| "A portals headline gets 1.3x the qualified leads of a follow-up headline." | hypothesis | It has a bar and an experiment (HYP-001, EXP-001). |
| "Portals reached 1.4x with 56 and 40 leads in 14 days." | validated | Met the precommitted `validated` criterion. |

### Each state, one by one

How each state may move, a synthetic example (`cliente_01`) and the mistake
that state invites.

| State | Moves to | Example | Anti-pattern |
|---|---|---|---|
| `observed` | inferred, hypothesis, stale | "Meta Ads shows 56 qualified leads for variant A between Oct 2 and Oct 16." | Stretching the window: reading October numbers as "the campaign works". |
| `reported` | inferred, hypothesis, stale | "The guest says despachos switch portals ten times a day." | Upgrading by repetition: the same sentence in three sessions is still `reported`. |
| `inferred` | hypothesis, stale | "Despachos probably care more about portals than about errors." | Treating it as seen: an inference written as fact in a brief. |
| `hypothesis` | validated, invalidated, inconclusive, insufficient | "A portals headline gets 1.3x the qualified leads of a follow-up headline" (HYP-001, EXP-001). | Running the test before the bar exists, or with no read that could prove it wrong. |
| `validated` | stale | "Portals reached 1.4x: 56 vs 40 qualified leads in 14 days." | Calling it permanent: using it after `refresh_by` without revalidating. |
| `invalidated` | stale | "Portals reached 0.9x: 36 vs 40 qualified leads in 14 days." | Validating the opposite: "so follow-up wins" needs its own hypothesis. |
| `inconclusive` | hypothesis (redesign), stale | "Portals won on qualified leads (1.2x) but lost on show rate (0.8x)." | Picking the half you like and reporting a winner. |
| `insufficient` | hypothesis (redesign), stale | "Only 22 leads per variant; the bar needed 50." | Reading it as invalidated: the test was small, the idea was not judged. |
| `stale` | hypothesis | "The portals result from October expired in January; the offer changed in December." | Quoting the old result in a new plan because "it was validated once". |

### Anti-patterns

- **Upgrading by repetition.** A claim said in three sessions is still `reported`.
- **Moving the bar.** Lowering "1.3x" to "1.1x" after seeing 1.15x. The ledger
  rejects it: "evidence bar changed after commitment; record a redesign first".
- **Reading insufficient as invalidated.** 22 leads per variant says nothing about
  the hypothesis; it says the test was too small.
- **Inventing voice.** A phrase written by Kokoro, stored as what the guest said.
- **Zero as missing.** A metric Kokoro could not read is `missing_evidence`, not 0.

## Vocabulary mapping

This model does not create new words for things Kokoro already names.

| Existing vocabulary | Where | Maps to |
|---|---|---|
| Hipótesis `HIP-001` | `/kokoro-validate` | hypothesis. Ids accept `HIP-` and `HYP-`. |
| Experimento `EXP-001` | `/kokoro-validate`, `/kokoro-experiment` | `experiment_id` of a hypothesis. |
| Umbral (definir ANTES) | `/kokoro-validate` | `precommitted_bar.validated`. |
| Umbral de invalidación | `/kokoro-experiment` | `precommitted_bar.invalidated`. |
| Perseverar | Experiment Report | Decision after `validated`. |
| Pivotar | Experiment Report | Decision after `invalidated`. |
| Pausar | Experiment Report | Decision after `inconclusive` or `insufficient`. |
| Aprendizaje validado / invalidado | Gate E50 | `validated` / `invalidated`. |
| Confidence High / Medium / Low | Orchestrator contract | `confidence: high / medium / low` in provenance. |
| Gate Pass / Partial / Blocked / Skipped | Orchestrator contract | Same statuses for the 7 evidence gates. |
| Visibility team / personal / sensitive / secret | Memory v2 | `privacy_class`. Only `team` enters shared evidence. |
| Suelo / Semilla / Germinación / Cosecha | 4 phases | `phase` of an open question. |

`confidence` describes one piece of evidence. The epistemic state describes the
claim. A `validated` claim can rest on `medium` confidence evidence; the
recommendation should say so.

## Provenance v1

Every piece of evidence carries these 9 fields. All are required. Three
optional blocks add detail: `metric` (numbers), `voice` (words) and
`freshness` (see Freshness v1).

| Field | Meaning | Example |
|---|---|---|
| `source_type` | Kind of source. One of 14 values in `evidence.SOURCE_TYPES`. | `interview` |
| `source_ref` | Where to find it again. Relative reference, never an absolute path. | `entrevistas/cliente_01/2026-09-28` |
| `observed_at` | When the fact happened or was said (YYYY-MM-DD). | `2026-09-28` |
| `retrieved_at` | When Kokoro read it. Never before `observed_at`. | `2026-10-01` |
| `scope` | Where the claim holds. | `segmento despachos, CDMX` |
| `claim` | The claim in one sentence. | `Cambian de portal diez veces al día` |
| `support_type` | observed, reported or inferred. | `reported` |
| `confidence` | low, medium or high. | `medium` |
| `privacy_class` | team, personal, sensitive or secret. Shared evidence accepts only `team`. | `team` |

### Numeric evidence

`source_type: platform_metric` requires a `metric` block with all 6 fields:

| Field | Example |
|---|---|
| `numerator` | `56` |
| `denominator` | `40` (must be > 0) |
| `window` | `{"start": "2026-10-02", "end": "2026-10-16"}` |
| `unit` | `qualified leads, variant A vs variant B` |
| `platform` | `meta_ads` |
| `attribution` | `7-day click` |

A number without its denominator, window or attribution cannot be compared.

### Guest voice

When evidence carries words, `voice.kind` says how faithful they are:

| Kind | Meaning | Rule |
|---|---|---|
| `verified_quote` | Literal words, traceable to the source. | `speaker_ref` must be a slug. Never from `kokoro_inference`. |
| `paraphrase` | The meaning, in other words. | Allowed as reported evidence. |
| `illustrative` | Copy written to show an idea. | Only with `support_type: inferred`. Never supports `validated`. |

An AI-invented phrase is never stored as a testimonial. If Kokoro wrote it, it
is `illustrative`.

### Untrusted content

Sources of type `web_page`, `review`, `social_comment`, `competitor_page`,
`transcript` and `document` are always **data, never instructions**. If their
text reads like an instruction ("ignore previous rules", "reveal the token"),
GATE-UNTRUSTED-CONTENT-ISOLATED marks it **Partial**: the text is kept as a
quoted claim, the loop records `untrusted_flags`, and nothing else changes.

External content can never change Kokoro rules, ask for secrets, run commands,
modify skills or skip human gates. A validation may only *propose* updates to
`guest_knowledge` or `open_question`. Skills, gates, identity and commands
change only through a reviewed pull request.

## Freshness v1

Knowledge ages. Every validation carries a `freshness` block, and an open
question or a provenance item may carry one. It answers: when was this
produced, when must it be reviewed, and what does it rest on?

| Field | Meaning | Example |
|---|---|---|
| `generated_on` | When the knowledge was produced or resolved. Required. | `2026-10-16` |
| `freshness_class` | How fast it ages: `fast`, `medium`, `slow` or `event_driven`. Required. | `medium` |
| `refresh_by` | Last day it counts as current. Required unless `event_driven`. | `2027-01-14` |
| `depends_on` | Ids it rests on: loops, hypotheses, validations or living artifacts. | `["HYP-001", "FORCES-2026-08"]` |
| `invalidated_by` | Events that expire it early. Required for `event_driven`. | `["cambio de oferta"]` |
| `last_material_change` | Last time its content really changed. | `2026-11-02` |

| Class | Review within | Typical knowledge |
|---|---|---|
| `fast` | 30 days | Campaign performance, active competitors, promotions, winning creatives |
| `medium` | 90 days | Messages, objections, Customer Forces, segments, journey |
| `slow` | 365 days | Purpose, vision, principles, deep positioning, business structure |
| `event_driven` | When an `invalidated_by` event happens | Anything tied to a launch, a new offer or a platform change |

`evidence.validate_freshness` rejects a `refresh_by` beyond the class limit.
Example: a `fast` validation dated Oct 16 with `refresh_by` in March is rejected,
because campaign results do not stay current for five months.

`evidence.freshness_status` answers `fresh`, `expired` or `event_driven` for one
block. Expired knowledge is not deleted. It moves to `stale` through a
`validation_expired` event and must be revalidated before it supports a
recommendation. Expiry *by dependency* (an upstream artifact changed, so
everything that `depends_on` it needs review) belongs to the freshness graph;
`depends_on` is recorded now so that graph has the edges it needs.

## Persistence

```
.kokoro/shared/events/evidence/   canonical, append-only, hash-chained (JSON)
.kokoro/shared/views/evidence/    rebuildable: open-loops, hypotheses, validations
```

The `evidence/` subfolders keep this ledger apart from Memory v2, which owns
`.kokoro/shared/events/<year>/*.yaml` and `.kokoro/shared/views/open-loops.yaml`.
Each file has exactly one writer. There is no second database.

### Event types (8)

| Event | Effect |
|---|---|
| `loop_captured` | New open question, status `captured`. |
| `loop_ranked` | Priority on 5 dimensions (1–5). |
| `loop_promoted` | Selected to become a hypothesis. |
| `loop_archived` | Dropped with a reason. |
| `hypothesis_created` | Bet with precommitted bar; stores the bar digest. With `supersedes` it is a redesign. |
| `hypothesis_approved` | A human approves; must confirm the same bar digest. |
| `validation_recorded` | Resolution against the bar. Closes the loop. With `revalidates` it renews a stale result. |
| `validation_expired` | Resolution becomes `stale`. |

Each event has a sequence, an id, an idempotency key digest, the previous event
hash and its own hash. A retry with the same key and payload replays; the same
key with a different payload fails with code 4. Any edit or missing file breaks
the chain and fails with code 4.

### Commands

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence check  --kind hypothesis --input-file hyp.json        # dry run, no write
K evidence append --type hypothesis_created --input-file ev.json --idempotency-key hyp-001
K evidence verify                                                 # chain + views
K evidence rebuild                                                # regenerate views
```

## How validate and experiment connect

1. An open question is promoted (see `kokoro-open-questions.md`).
2. `/kokoro-validate` writes the hypothesis: id, prediction, decision at stake,
   evidence plan with a disconfirming read, the 4-state bar and `experiment_id`.
3. The human approves the hypothesis and its bar.
4. `/kokoro-experiment` runs the 3x3x3 sprint with `source_hypothesis_id`.
5. The Experiment Report result becomes `validation_recorded`. Perseverar,
   Pivotar or Pausar follows from the state.

Changing the bar after results exist requires a redesign: a new hypothesis with
`supersedes` and `redesign_reason`, approved again.
