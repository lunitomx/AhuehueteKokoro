# E40 Brief: Kokoro Operability Orchestrators

## Hypothesis

If Kokoro ships opinionated business orchestrators instead of isolated skill files, then a founder, marketing director, or sales leader can install the repo and get executive-grade decisions without knowing the internal command map.

## Business Outcome

Make Ahuehuete Kokoro feel like a usable marketing and sales operating system:

- A new user knows what to run first.
- Platform diagnostics verify context and MCP health before analysis.
- Recommendations are grounded in real data, Kokoro knowledge, and explicit business context.
- Sensitive guest data stays out of the public repository.
- Execution remains invitation-based: diagnose and recommend first, act only with explicit permission.

## Appetite

Medium epic. This should produce a public-ready operating layer, not rewrite every underlying skill.

## Success Metrics

- At least 6 executive orchestrators documented as runnable Kokoro flows.
- Every orchestrator includes gates for context, data source health, privacy, and action confirmation.
- Google Ads has a complete end-to-end diagnostic flow because it is the clearest proof case.
- README and AGENTS agree on what Claude, Codex, and Hermes can actually load automatically.
- Public repository hygiene prevents `.env`, `.kokoro`, `.raise` runtime state, and guest data from accidental commits.
- A non-technical business user can choose the right flow from a short "What do you want to do?" router.

## Constraints

- Preserve Kokoro voice and vocabulary.
- Do not add real guest data, account IDs, tokens, screenshots, or private exports to the repo.
- Do not require MCPs to be present for install; do require graceful health checks before data-backed claims.
- Keep Claude/Codex/Hermes differences explicit.
- Favor markdown skill contracts and validation gates before adding code.

## Rabbit Holes

- Building full MCP servers inside this epic.
- Creating a dashboard UI.
- Connecting real ad accounts.
- Rewriting every existing skill.
- Adding client-specific playbooks to the public repo.

## First Proof

The proof case is a business user asking:

> "Kokoro, revisa Google Ads."

Expected behavior:

1. Resolve the guest or ask for context.
2. Check Google Ads MCP registration and health.
3. Discover accessible accounts only if connected.
4. Pull campaigns, search terms, keywords, negatives, budgets, bidding, conversion signal, and auction context where available.
5. Load Google Ads knowledge files.
6. Produce prioritized executive recommendations.
7. Ask for explicit permission before any account mutation.
