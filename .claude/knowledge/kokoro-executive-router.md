# Kokoro Executive Router

Purpose: map a business user's plain-language intent to the right Kokoro workflow.

This file is the route map for `/kokoro`. It keeps the command concise while giving Kokoro enough structure to guide founders, marketing directors, and sales leaders.

## Routing Principle

First classify the request:

| User Need | Route Type | Meaning |
|---|---|---|
| "I need clarity" | Strategic phase | Diagnose the business before operating |
| "I need a decision" | Operating run | Use connected context/data to recommend action |
| "I need to share safely" | Safety run | Verify privacy and public readiness |
| "I need a specific asset" | Production skill | Use the relevant tactical Kokoro command |

If the request is ambiguous, ask one question:

> "¿Buscas claridad estrategica o una decision operativa con datos?"

## Strategic Phase Routes

Use these when the user is unsure about the business itself, not just a marketing channel.

| Intent | Primary Route | Reason |
|---|---|---|
| "No se por donde empezar" | `/kokoro-diagnose` | Clarify terrain before choosing a workflow |
| "No tengo vision clara" | `/kokoro-mountain` | Define direction before measuring activity |
| "Tengo demasiadas creaciones" | `/kokoro-prune` | Reduce dispersion before scaling |
| "No conozco mis numeros" | `/kokoro-finance` | Ground decisions in margins and acquisition economics |
| "Necesito validar mi modelo" | `/kokoro-canvas` | Structure the model before launch |
| "No se que mueve al invitado" | `/kokoro-forces` | Understand switching forces before messaging |
| "Necesito validar supuestos" | `/kokoro-interviews` or `/kokoro-validate` | Talk to real people before investing |

## Executive Operating Routes

These are the E40 operating-system routes. Some are planned orchestrators; until their command contracts exist, use the available-now fallback.

All executive operating routes must follow `kokoro-orchestrator-contract.md`.
That contract defines phases, gates, fallback behavior, output format, privacy
rules, and the permission gate before action.

| Intent | Primary Route | Status | Available Now | First Gates |
|---|---|---:|---|---|
| Review Google Ads | `/kokoro-google-ads-run` | Planned | `/kokoro-gads` + `/kokoro-connect` + `/kokoro-analytics` | guest resolved, Google Ads MCP healthy, no credentials in repo |
| Weekly marketing read | `/kokoro-weekly-marketing-run` | Planned | `/kokoro-scorecard` + `/kokoro-analytics` + `/kokoro-pulse` | platforms connected, date range clear, private report handling |
| Launch a creation | `/kokoro-launch-run` | Planned | `/kokoro-canvas` + `/kokoro-forces` + `/kokoro-pescar` + `/kokoro-experiment` + `/kokoro-launch` | stage clear, offer/context loaded, tracking plan |
| Improve acquisition | `/kokoro-acquisition-run` | Planned | `/kokoro-funnel` + `/kokoro-mafia` + `/kokoro-landing` + `/kokoro-analytics` + `/kokoro-tracking-check` | funnel context, platform data if used, no private exports committed |
| Share Kokoro safely | `/kokoro-share-readiness` | Planned | `.claude/knowledge/kokoro-share-readiness.md` | no guest data, no credentials, no runtime state |
| Connect platforms | `/kokoro-connect` | Available | `/kokoro-connect` | guest resolved, MCP discovery, explicit account selection |
| Review tracking health | `/kokoro-tracking-check` | Available | `/kokoro-tracking-check` | website/context available, no credentials requested |
| Build content calendar | `/kokoro-parrilla` | Available | `/kokoro-parrilla` | guest context, tracking readiness, feed audit when available |

## Production Skill Routes

Use these when the user already knows the desired output.

| Intent | Route |
|---|---|
| Meta Ads copy and targeting | `/kokoro-ads` |
| Google Ads optimization | `/kokoro-gads` |
| Creative generation | `/kokoro-creative` |
| Creative review | `/kokoro-creative-review` |
| Landing evaluation | `/kokoro-landing` |
| Video/audio transcription | `/kokoro-listen` |
| Shorts/cuts | `/kokoro-cuts`, `/kokoro-shorts` |
| Captions/render | `/kokoro-overlay`, `/kokoro-render` |
| Luxury positioning | `/kokoro-luxury` |
| Meetings and decisions | `/kokoro-meeting`, `/kokoro-adr` |

## Response Pattern

When routing, answer in this shape:

```markdown
Veo que buscas: {intent}

Ruta principal: `{route}` {status if planned}
Disponible ahora: {fallback if needed}
Primer gate: {context/MCP/privacy gate}

Antes de avanzar, necesito una cosa:
{one question only}
```

## Safety Rules

- Never ask the user to paste API keys, access tokens, refresh tokens, or client secrets.
- Never suggest committing guest context, exports, reports, or generated private assets.
- If a route depends on MCP data, say "primero verificamos conexion" before any analysis.
- If an E40 route is planned, say "planned" and route to available skills today.
- Use "invitado", "creacion", "inversion", "compartir", and "reto/oportunidad".

## Examples

### Google Ads

Input:

```text
Revisa Google Ads.
```

Route:

```markdown
Veo que buscas una decision operativa sobre Google Ads.

Ruta principal: `/kokoro-google-ads-run` (planned)
Disponible ahora: `/kokoro-gads` + `/kokoro-connect` + `/kokoro-analytics`
Primer gate: resolver invitado y verificar MCP de Google Ads.

Antes de avanzar, necesito una cosa:
¿De que invitado hablamos?
```

### Weekly Marketing

Input:

```text
Como va mi marketing esta semana?
```

Route:

```markdown
Veo que buscas una lectura semanal de marketing.

Ruta principal: `/kokoro-weekly-marketing-run` (planned)
Disponible ahora: `/kokoro-scorecard` + `/kokoro-analytics` + `/kokoro-pulse`
Primer gate: plataformas conectadas y rango de fechas.

Antes de avanzar, necesito una cosa:
¿Quieres vista de un invitado especifico o de todo tu portafolio?
```

### Strategic Clarity

Input:

```text
No se por donde empezar.
```

Route:

```markdown
Veo que buscas claridad estrategica.

Ruta principal: `/kokoro-diagnose`
Disponible ahora: `/kokoro-diagnose`
Primer gate: permiso para escuchar antes de guiar.

Antes de avanzar, necesito una cosa:
¿Me das tu invitacion para hacerte unas preguntas y entender el terreno?
```
