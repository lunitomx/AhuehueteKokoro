# Skill Orchestration Pattern

> 1 skill = 1 responsibility = 1 verifiable artifact.

## Pattern Statement

Every Kokoro skill must own exactly one responsibility and produce exactly one
verifiable artifact. When a workflow requires multiple artifacts or sequences
multiple responsibilities, the work is split into an orchestrator skill that
holds sequencing logic and quality gates, plus focused sub-skills that each
produce a single output. Knowledge files carry domain data; skills carry process
logic. This separation keeps prompts focused, enables independent testing, and
allows domain knowledge to evolve without restructuring skills.

## Decision Tree

Use this tree to determine whether a new skill should be atomic or an
orchestrator:

```
Does the skill produce multiple artifact types?
  YES → Orchestrator + sub-skills
  NO  ↓

Does the skill exceed ~200 lines of guidance?
  YES → Consider splitting into orchestrator + sub-skills
  NO  ↓

Does the skill sequence other existing skills?
  YES → Orchestrator
  NO  ↓

Single exercise or single output?
  YES → Atomic skill (keep as-is)
```

## Good Example: kokoro-gads

The kokoro-gads skill (445 lines) demonstrates the orchestration pattern well:

- **Structure:** Orchestrator sequencing 5 phases — diagnosis, read, consult,
  analyze, recommend
- **Knowledge files:** References 5 separate knowledge files for Google Ads
  domain data (metrics, strategy, bidding, audiences, quality score)
- **Gates:** Each phase produces a verifiable intermediate artifact before the
  orchestrator proceeds to the next phase
- **Reusability:** The knowledge files are independently updatable as Google Ads
  evolves, without touching the skill's process logic

**Why it works:** The orchestrator's job is sequencing and gating. Each phase
focuses the AI context on exactly the instructions needed for that step,
producing higher-quality output than a monolithic prompt would.

## Refactor Candidate: kokoro-onboard

The kokoro-onboard skill (316 lines) is a monolithic skill that should become
an orchestrator:

- **Current structure:** 7 dimension blocks (identity, business, market,
  finances, digital presence, goals, blockers) + synthesis + 3 persistence
  operations (state write, graph node, session log)
- **Problem:** Cannot test individual dimensions in isolation. The AI must hold
  all 7 dimension instructions simultaneously even though it processes them
  sequentially. Persistence logic is tangled with exploration logic.
- **Proposed refactoring:**
  - `kokoro-onboard` becomes orchestrator (sequencing + gates)
  - `kokoro-onboard-explore` handles the 7-dimension interview
  - `kokoro-onboard-synthesize` produces the client profile artifact
  - `kokoro-onboard-persist` handles state, graph, and session writes
- **Benefit:** Each sub-skill becomes testable. The exploration phase can evolve
  (add dimensions, reorder) without touching persistence logic.

## Guidelines for New Skills

Before creating a new skill, verify it passes this checklist:

- [ ] **Single output artifact** — The skill produces exactly one type of
      artifact (a canvas, a diagnosis, a report, a campaign brief, etc.)
- [ ] **Under ~200 lines of guidance** — If the skill prompt exceeds 200 lines,
      it likely contains multiple responsibilities that should be split
- [ ] **Knowledge files for domain data** — Domain-specific data (metrics
      definitions, platform rules, methodology steps) lives in knowledge files,
      not inline in the skill prompt
- [ ] **Quality gate at end** — The skill ends with a verification step that
      confirms the artifact meets its contract before declaring success
- [ ] **No embedded sequencing of other skills** — If the skill calls or
      references other skills in sequence, it should be declared as an
      orchestrator with explicit phase transitions

If the skill violates any of these and the violation is intentional, document
the justification in the skill's header comment.
