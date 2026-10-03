# Open Questions v1

> What Kokoro does not know yet, written so it can be answered.

An open question (a *loop*) is a precise thing Kokoro does not know about a
guest, tied to a decision that would change with the answer. Loops are how
"we should look into the audience" becomes "¿Los despachos con 20 o más RFC
valoran más reducir cambios de portal o reducir errores de seguimiento?".

Rules live in `runtime/evidence.py`; events and views in
`runtime/evidence_ledger.py`. The evidence states and provenance fields are in
`kokoro-evidence-model.md`.

## Lifecycle

```
captured ─► ranked ─► promoted ─► hypothesis ─► closed
    │          │          │                       (validation recorded)
    └──────────┴──────────┴─► archived (with reason)
```

| Status | Event | What it means |
|---|---|---|
| `captured` | `loop_captured` | Passed the capture gates. Not prioritized yet. |
| `ranked` | `loop_ranked` | Scored on 5 dimensions. Can be re-ranked. |
| `promoted` | `loop_promoted` | Chosen to become a hypothesis. Only from `ranked`. |
| `hypothesis` | `hypothesis_created` | Has a hypothesis with a precommitted bar. |
| `closed` | `validation_recorded` | Resolved: validated, invalidated, inconclusive or insufficient. |
| `archived` | `loop_archived` | Dropped. The reason stays in the ledger. |

A loop that ends `inconclusive` or `insufficient` is closed, but its
`validation.new_loops` can name follow-up questions to capture.

## Fields

| Field | Meaning | Example |
|---|---|---|
| `id` | `LOOP-…` | `LOOP-001` |
| `guest` | Guest slug, never a real name. | `cliente_01` |
| `phase` | One of the 4 phases. | `semilla` |
| `territory` | One of the 6 territories. | `mensaje` |
| `observation` | What was seen that raised the question. | `En 4 de 6 entrevistas…` |
| `question` | The exact question, ending in `?`. | `¿Los despachos… valoran más…?` |
| `why_it_matters.decision` | The decision that changes with the answer. | `Qué beneficio encabeza la landing` |
| `why_it_matters.impact` | What is at stake. | `Define el mensaje de la campaña` |
| `evidence_routes` | Where the answer could come from. At least one. | `Prueba de dos encabezados` |
| `provenance` | Provenance v1 for the observation. At least one item. | see the evidence model |
| `links` | Related loops, hypotheses or files (relative). | `[]` |
| `freshness` | Optional. When the question's context stops being current (Freshness v1). | `{freshness_class: medium, …}` |
| `status` | Set by the ledger, never by input. | `ranked` |
| `priority` | Set by `loop_ranked`. | `{impact: 5, …}` |

## Territories

Territories say *what part of the business* the question is about. They are an
extra dimension and do not replace the 4 phases, which say *when* in the
journey it comes up. Every loop carries both.

| Territory (`territory`) | Question is about | Typical phases |
|---|---|---|
| Invitado (`invitado`) | Who the person is, what they need, what they fear | Suelo, Semilla |
| Creación/Oferta (`creacion_oferta`) | What is offered, how it is packaged, the investment | Semilla, Cosecha |
| Mensaje (`mensaje`) | What is said and which benefit leads | Semilla, Germinación |
| Canal/Creativo (`canal_creativo`) | Where it is said and in what format | Germinación |
| Conversión/Seguimiento (`conversion_seguimiento`) | What happens after the first contact | Germinación, Cosecha |
| Economía/Medición (`economia_medicion`) | Whether it pays off and how it is measured | Suelo, Cosecha |

## Ranking

`loop_ranked` scores 5 dimensions from 1 to 5. The open-loops view sorts
active loops by the total, highest first.

| Dimension | 5 means |
|---|---|
| `impact` | The decision moves a lot of revenue or effort. |
| `uncertainty` | We really do not know; both answers are plausible. |
| `learnability` | We can get an answer soon and cheaply. |
| `urgency` | The decision is due soon. |
| `reversibility` | The decision is hard to undo, so learning first matters. |

The score orders the queue. It does not promote anything. Promotion is an
explicit `loop_promoted` with a reason.

## Gates

Capture applies 5 gates (see `kokoro-quality-gates.md`):

1. GATE-QUESTION-EXACT
2. GATE-DECISION-LINKED
3. GATE-SOURCE-POSSIBLE
4. GATE-NOT-DUPLICATE
5. GATE-UNTRUSTED-CONTENT-ISOLATED

Promotion to hypothesis adds GATE-HYPOTHESIS-FALSIFIABLE and
GATE-EVIDENCE-BAR-PRECOMMITTED.

## Examples

| Draft | Problem | Rewrite |
|---|---|---|
| "Investigar más a los contadores" | A task, not a question. | "¿Qué porcentaje de despachos con 20 o más RFC ya paga una herramienta de seguimiento?" |
| "¿Por qué el mensaje de portales funciona mejor?" | The answer is hidden inside. | "¿El mensaje de portales consigue más leads calificados que el de seguimiento?" |
| "¿Les gusta la marca?" | No decision changes. | Add `decision`: "Si mantenemos el nombre en la campaña de noviembre". |

## Anti-patterns

- **Questions as a to-do list.** Every loop needs a decision; if none, archive it.
- **One giant question.** Split "¿Quién es el invitado y qué quiere?" into
  questions that each one source can answer.
- **Capturing the same doubt twice.** The duplicate gate checks active loops for
  the same guest.
- **Promoting by score alone.** The human decides what becomes a hypothesis.

## Commands

```bash
K="python3 $KOKORO_PACKAGE_HOME/runtime/kokoro.py"
$K evidence check  --kind loop --input-file loop.json
$K evidence append --type loop_captured --input-file ev.json --idempotency-key loop-001
cat .kokoro/shared/views/evidence/open-loops.yaml
```

`ev.json` wraps the record: `{"loop": { …fields above… }}`.
