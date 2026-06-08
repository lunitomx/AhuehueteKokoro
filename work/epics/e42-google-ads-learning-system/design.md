# Epic Design: Google Ads Learning System

## Affected Surface (Gemba)

| Module/File | Current State | Changes |
|-------------|---------------|---------|
| `.claude/knowledge/kokoro-session-log.md` | Defines a generic session log schema and open/close usage. | Add Google Ads learning guidance, optional fields, and a client-readable recap pattern. |
| `.claude/commands/kokoro-open.md` | Shows recent sessions and proposes a focus. | Surface Google Ads learning history as the default context for returning invitado work. |
| `.claude/commands/kokoro-close.md` | Persists summary, hallazgos, and next_action. | Make the closeout language consistently represent Google Ads learning and control history. |
| `.claude/commands/kokoro-gads.md` | Includes a session_log write pattern. | Align the writeback contract with the learning system vocabulary and client control goals. |
| `.claude/commands/kokoro-google-ads-run.md` | Runs Google Ads diagnostics with gates and recommendations. | Make the run output explicitly feed the learning loop so each diagnostic becomes reusable history. |
| `.claude/commands/kokoro-session.md` | Tracks session context across the broader Kokoro workflow. | Keep the Google Ads learning loop visible as part of the broader session model. |
| `.claude/knowledge/kokoro-learning-dashboard.md` | Formal control model for Plan / Execution / Learning. | Make the dashboard the mother artifact that ties plan, session log, and experiment learning together. |
| Private runtime / MCP layer | Not part of this repository. | Execute against Google Ads, env, and credentials outside the public repo. |

## Target Components

| Component | Responsibility | Key Interface |
|-----------|---------------|---------------|
| `SessionLogEntry` | Represents one learning event for a client session. | JSON object stored in `ClientProfile.metadata["session_log"]` |
| Learning Dashboard | Formal control board that connects plan, execution, and learning. | `kokoro-learning-dashboard.md` |
| Google Ads learning recap | Compresses recent sessions into a readable control surface. | Open-time summary with last sessions, hallazgos, and next_action |
| Closeout writer | Persists the learning record after a session ends. | Existing `/kokoro-close` write path with Google Ads-specific vocabulary |
| Run-time learner | Turns a diagnostic run into reusable knowledge. | `/kokoro-google-ads-run` and `/kokoro-gads` output contract |

## Key Contracts

```ts
type SessionLogEntry = {
  date: string; // YYYY-MM-DD
  type: "gads" | "ads" | "strategy" | "research" | "launch" | "experiment" | "onboarding" | "general";
  skill?: string;
  client_id: string;
  summary: string;
  hallazgos?: string[];
  artifacts?: string[];
  next_action?: string;
  platform?: "google_ads";
  campaign_type?: "search" | "display" | "pmax" | "shopping" | "other";
  learning_state?: "learning" | "stable" | "needs_attention";
};

type SessionLog = SessionLogEntry[];
```

Rules:
- Existing entries stay valid if they only have the current fields.
- New Google Ads fields are optional and additive.
- The entry must stay compact enough to read in `/kokoro-open`.
- `next_action` remains the primary control signal for the next session.
- The public repo does not store `.env`, MCP config, credentials, or private
  runtime bootstrapping.

## Migration Path

1. Keep all current session logs readable without backfill.
2. Add Google Ads-specific guidance to the existing knowledge file first.
3. Update open/close/run commands to emit the same learning vocabulary.
4. Only after the schema is stable, consider deeper reporting or exports.
5. Keep all execution wiring in the private runtime, not in this repo.
