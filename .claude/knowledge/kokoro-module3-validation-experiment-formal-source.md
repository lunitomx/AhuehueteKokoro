# Kokoro Module 3 Validation Plan And Experiment Report Source Notes

> Private source-backed notes for E50. Do not export raw transcript content.

## Source

- Raw ID: `RAW-E50-002`
- Title: `Módulo 3 | Clase 2: Experiment Report y Validation Plan`
- Raw path:
  `work/epics/e50-kokoro-module3-curriculum-reconstruction/raw/raw-e50-002-m3-c2-experiment-report-validation-plan.txt`
- Matching field corpus source: `TACTIQ-2025-038`
- Classification: formal Module 3 curriculum with live class interaction.

## Curriculum Placement

This class continues the PESCAR opening of Module 3. It turns campaign thinking
into a validation discipline: first align the plan, then run small experiments,
then learn from market evidence before scaling.

## Doctrine To Preserve

- Campaigns should be treated as validation experiments. A campaign does not
  deserve confidence just because it was planned and produced.
- Validation Plan is the macro launch plan. It can cover 3 months, 6 months, or
  1 year, and it should contain multiple Experiment Reports.
- Experiment Report is the sprint-level evidence artifact. It captures the
  hypothesis, execution, metrics, qualitative observations, learning, and next
  action.
- The class-specific `3x3x3` rhythm is:
  - 3 hours to create strategy, brief, key message, and creative concept.
  - 3 days to produce minimum viable assets, campaign setup, and automation.
  - 3 weeks to test in market.
- The goal is to launch quickly, measure clearly, and learn with agility.
- Production should avoid perfectionism, but should not fall below the quality
  threshold that protects trust in the creation.
- Qualitative evidence matters: site/session behavior, conversations, reasons
  for churn, sales objections, and follow-up signals can reveal why metrics move.
- Hypotheses must be falsifiable. A good hypothesis can be proven wrong by
  evidence.
- Validation Plan keeps the team aligned. If an experiment stops matching the
  plan, either the plan changes consciously or the experiment should stop.

## Validation Plan Fields Inferred From Class

- Background and commercial need.
- Channel or message to validate.
- Hypothesis driving action.
- Current condition.
- Future condition / goal.
- Analysis of why the objective is not yet being achieved.
- Validation proposal.
- Success criteria and measured outcomes.

## Experiment Report Fields Inferred From Class

- Experiment name and channel.
- Audience or segment.
- Budget/investment.
- Hypotheses.
- Metrics and thresholds.
- Launch details.
- Results.
- Validated or invalidated learning.
- Next action.

## Skill Implications

- `/kokoro-validate` should create the macro Validation Plan before tactical
  campaign assets.
- `/kokoro-experiment` should produce one small Experiment Report per test,
  not a large bundled campaign plan.
- `/kokoro-experiment` should support the formal 3 hours / 3 days / 3 weeks
  rhythm from this source.
- `/kokoro-launch` should gate campaign build until Validation Plan and at
  least one Experiment Report hypothesis exist.
- The router should detect "quiero lanzar campaña", "quiero validar canal",
  "qué hipótesis pongo", "cómo mido si funcionó", and "tengo resultados pero
  no sé qué hacer" as Phase 3 validation/experiment intent.

## Evidence Handling

Use the raw transcript only in private E50 artifacts. Public export should
preserve doctrine, templates, and examples only after removing participant
details, private business numbers, URLs, and operational context.
