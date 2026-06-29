# Kokoro — Router Codex

Use this skill when the user asks for Kokoro, Ahuehuete Kokoro, a Kokoro
slash command, or any Kokoro methodology such as Lean Canvas, Customer Forces,
PESCAR, Funnel Consciente, Oferta Mafia, Google Ads, Meta Ads, launch,
tracking, content, onboarding, or session open/close.

Kokoro commands are authored in `.claude/commands/`. Codex does not load those
files as native slash commands, so this skill is the public Codex bridge.

## Instructions

1. Read `AGENTS.md` first and follow its repository boundary rules.
2. Read `IDENTITY_kokoro.md` before answering in Kokoro voice.
3. Route the user's request to the matching markdown file in `.claude/commands/`.
   If the user names a command such as `/kokoro-canvas`, read
   `.claude/commands/kokoro-canvas.md`.
4. If the user does not name a command, read `.claude/commands/kokoro.md` and
   use it as the executive router.
5. When a command references `.claude/knowledge/`, read only the knowledge files
   required by that command before acting.
6. Do not invent live metrics, campaign data, client records, or MCP results.
   Verify live connections before claiming live data.
7. Do not store private exports, client data, reports, generated media, or MCP
   credentials in this public repository.

## Command Map

- `/kokoro`: `.claude/commands/kokoro.md`
- `/kokoro-onboard`: `.claude/commands/kokoro-onboard.md`
- `/kokoro-open`: `.claude/commands/kokoro-open.md`
- `/kokoro-close`: `.claude/commands/kokoro-close.md`
- `/kokoro-canvas`: `.claude/commands/kokoro-canvas.md`
- `/kokoro-forces`: `.claude/commands/kokoro-forces.md`
- `/kokoro-interviews`: `.claude/commands/kokoro-interviews.md`
- `/kokoro-validate`: `.claude/commands/kokoro-validate.md`
- `/kokoro-google-ads-run`: `.claude/commands/kokoro-google-ads-run.md`
- `/kokoro-weekly-marketing-run`: `.claude/commands/kokoro-weekly-marketing-run.md`
- `/kokoro-creative-campaign-run`: `.claude/commands/kokoro-creative-campaign-run.md`
- `/kokoro-launch-run`: `.claude/commands/kokoro-launch-run.md`
- `/kokoro-acquisition-run`: `.claude/commands/kokoro-acquisition-run.md`
- `/kokoro-share-readiness`: `.claude/commands/kokoro-share-readiness.md`

For other Kokoro commands, resolve by exact filename:
`.claude/commands/{command-name-without-leading-slash}.md`.
