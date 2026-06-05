# E40 Scope: Kokoro Operability Orchestrators

## Objective

Transform Ahuehuete Kokoro from a rich collection of standalone marketing skills into a public-ready operating system for founders, marketing directors, and sales leaders. The epic creates orchestrators that chain existing Kokoro skills into executive workflows with data, MCP, privacy, and decision gates.

## Value

Kokoro becomes easier to trust and easier to use. A business leader can state an outcome in plain language, and Kokoro chooses the right process instead of making the user memorize command names.

## In Scope

### Must

- Define the executive orchestrator model for Kokoro.
- Create a business-facing router for "what do you want to accomplish?"
- Create Google Ads end-to-end diagnostic orchestration.
- Create weekly marketing pulse orchestration.
- Create launch orchestration for a new creation.
- Create acquisition/funnel orchestration across ads, analytics, landing, and offer.
- Create privacy and public-repo hygiene gates.
- Update documentation so install expectations are accurate for Claude, Codex, and Hermes.

### Should

- Add reusable gate language that every orchestrator can include.
- Add a short demo path that works even without MCP connections.
- Add a validation checklist for sharing Kokoro with guests.

## Out of Scope

- Connecting real guest accounts.
- Storing private guest work inside this public repo.
- Building a web UI.
- Implementing new MCP servers.
- Rewriting all 68 Kokoro command files.
- Guaranteeing every third-party MCP exists in every runtime.

## Planned Stories

| Story | Name | Description | Size | Dependencies |
|---|---|---|---|---|
| S40.1 | Public Repo Safety Gate | Harden `.gitignore`, define sensitive-data policy, and add a pre-share checklist for public distribution. | S | None |
| S40.2 | Executive Router | Design the business-facing router that maps plain-language needs to orchestrators. | M | S40.1 |
| S40.3 | Orchestrator Contract | Define the shared structure: context resolution, MCP health, data completeness, knowledge load, recommendation, permission to act. | M | S40.2 |
| S40.4 | Google Ads Run | Create the proof-case orchestrator for Google Ads diagnostics from MCP health to prioritized recommendations. | L | S40.3 |
| S40.5 | Weekly Marketing Pulse Run | Chain Meta Ads, Google Ads, GA4, GSC, scorecard, and executive interpretation into a weekly operating rhythm. | M | S40.3 |
| S40.6 | Launch Run | Chain canvas, forces, PESCAR, experiment, launch, landing, tracking, and scorecard into a guided launch workflow. | M | S40.3 |
| S40.7 | Acquisition Run | Chain acquisition diagnosis, funnel, offer, landing, analytics, and tracking into a sales and marketing improvement workflow. | M | S40.3 |
| S40.8 | Runtime Documentation & Share Readiness | Align README/AGENTS, document Claude/Codex/Hermes differences, and add a final operational checklist. | M | S40.4, S40.5, S40.6, S40.7 |

## Done Criteria

- All planned orchestrators exist as markdown command contracts.
- Every orchestrator has explicit gates:
  - guest/context resolved
  - MCP registered and healthy when data-backed analysis is requested
  - fallback path when MCP is unavailable
  - knowledge files loaded before recommendation
  - no sensitive data committed or displayed unnecessarily
  - action tools require explicit invitation
- Google Ads flow includes search terms, keywords, negatives, bidding, budget, conversion, auction/competition context where available, and landing/tracking considerations.
- README no longer overpromises automatic command loading in Codex.
- `.gitignore` protects runtime state and guest data.
- A business leader can read the router and choose the correct flow in under five minutes.
- Epic retrospective captures what should become reusable Kokoro operating doctrine.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Orchestrators become too verbose to use | Medium | High | Keep each flow outcome-based, with detailed gates hidden below the executive entrypoint. |
| MCP names differ by runtime | High | Medium | Use health/discovery gates and graceful degradation instead of hard failure. |
| Public repo accidentally attracts private guest data | Medium | High | Harden ignore rules and document private workspace pattern clearly. |

## Implementation Plan

### Sequence

| Order | Story | Rationale | Status |
|---|---|---|---|
| 1 | S40.1 Public Repo Safety Gate | Risk-first: protect the public repo before adding workflows that mention guest data. | Planned |
| 2 | S40.2 Executive Router | Establish the user-facing entrypoint before designing individual runs. | Planned |
| 3 | S40.3 Orchestrator Contract | Walking skeleton: one shared contract prevents each run from inventing its own process. | Planned |
| 4 | S40.4 Google Ads Run | Proof case from the user's clearest example and highest data-dependency risk. | Planned |
| 5 | S40.5 Weekly Marketing Pulse Run | Turns platform data into recurring executive operating rhythm. | Planned |
| 6 | S40.6 Launch Run | Covers creation-to-market workflows beyond ad diagnostics. | Planned |
| 7 | S40.7 Acquisition Run | Covers sales and funnel improvement for leaders of sales/marketing. | Planned |
| 8 | S40.8 Runtime Documentation & Share Readiness | Final integration and public-readiness pass after all orchestrators exist. | Planned |

### Milestones

| Milestone | Stories | Success Criteria |
|---|---|---|
| M1: Safe Skeleton | S40.1-S40.3 | Public safety rules, router, and shared orchestrator contract exist. |
| M2: Data-Backed Proof | S40.4 | Google Ads run can be followed without missing gates or unsupported claims. |
| M3: Executive Operating Layer | S40.5-S40.7 | Weekly, launch, and acquisition flows are documented as end-to-end Kokoro runs. |
| M4: Share Ready | S40.8 | Docs and readiness checklist align with real runtime behavior. |

### Parallel Opportunities

After S40.3, S40.5, S40.6, and S40.7 can be drafted independently because they share the same orchestrator contract. S40.8 should remain last.

### Progress Tracking

| Story | Size | Status | Actual | Velocity | Notes |
|---|---:|---|---|---|---|
| S40.1 | S | Done | 75m | 1.2x | Public repo safety gate; merged to main |
| S40.2 | M | Done | 85m | 1.41x | Executive router; merged to main |
| S40.3 | M | Done | 70m | 1.71x | Shared orchestrator contract; merged to main |
| S40.4 | L | Planned |  |  | Google Ads proof run |
| S40.5 | M | Planned |  |  | Weekly marketing pulse run |
| S40.6 | M | Planned |  |  | Launch run |
| S40.7 | M | Planned |  |  | Acquisition run |
| S40.8 | M | Planned |  |  | Runtime docs and share readiness |
