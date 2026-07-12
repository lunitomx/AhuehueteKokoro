# /kokoro-share-readiness — Verificacion para Compartir Kokoro

> Orquestador E40: privacidad, runtime, MCP boundaries, demo path y decision
> Pass/Hold/Private Only antes de compartir Kokoro.

> "La confianza no empieza cuando invitas a alguien a tu sistema. Empieza
> antes, cuando revisas que nada privado viaje escondido en la maleta."

## Proposito

Usa este run cuando el usuario diga:

- "Quiero compartir Kokoro"
- "Esta listo para mis clientes?"
- "Puedo subir o publicar este repo?"
- "Revisa si hay datos sensibles"
- "Quiero hacer demo sin MCP"
- "Que tengo que revisar antes de compartir?"

Este comando NO publica, empaqueta, sube ni envia archivos. Audita readiness y
pide invitacion explicita antes de cualquier accion de distribucion.

## Integracion Tactiq 2025

Para E48, este run es el gate de S48.8 y S48.15. Debe tratar transcripts
Tactiq, raw files, extracted snippets, client/invitado context, account IDs,
URLs privadas, screenshots, reports y runtime state como privados hasta que
exista una curacion explicita. Los assets exportables son doctrina,
plantillas, comandos y patrones anonimizados.

## Contrato Obligatorio

Antes de recomendar, lee y aplica:

- `.claude/knowledge/kokoro-orchestrator-contract.md`
- `.claude/knowledge/kokoro-tactiq-field-patterns.md`
- `.claude/knowledge/kokoro-privacy-protocol.md`
- `.claude/knowledge/kokoro-share-readiness.md`
- `.claude/knowledge/kokoro-executive-router.md`

## Entrada

Formato sugerido:

```text
/kokoro-share-readiness {alcance}
```

Ejemplos publicos:

```text
/kokoro-share-readiness repo-publico
/kokoro-share-readiness antes-demo
/kokoro-share-readiness sin-mcp
```

## Fase 1 — Invitacion y Alcance

Refleja la intencion:

```markdown
Veo que quieres compartir Kokoro con seguridad.
Voy a revisar tres cosas: que el runtime no prometa de mas, que el repo no
contenga datos privados y que exista un camino de demo aun sin MCP.
```

Si falta informacion, pregunta solo una cosa:

```markdown
¿Lo quieres compartir como repo publico, demo para un invitado, o workspace
privado para colaborador?
```

## Fase 2 — Runtime Readiness

Tabla obligatoria:

| Runtime | Identity | Commands | Share Note |
|---|---|---|---|
| Claude Code | `.claude/CLAUDE.md` | `.claude/commands/` como slash commands de Claude | Camino nativo para comandos Kokoro |
| Codex CLI | `AGENTS.md` | leer e invocar markdown manualmente | Codex no auto-carga `.claude/commands/` como slash commands nativos |
| Hermes Agent | `AGENTS.md` o skill bundle instalado | depende de instalacion Hermes | No asumir que clonar el repo instala skills nativos |

Gate:

| Gate | Status | Evidence | If Blocked |
|---|---|---|---|
| Runtime docs accurate | Pass/Partial/Blocked | README/AGENTS dicen la verdad | actualizar docs antes de compartir |
| Commands discoverable | Pass/Partial/Blocked | router y operating runs listados | documentar rutas disponibles |
| No-MCP demo path | Pass/Partial/Blocked | metodologia funciona con gates Skipped/Blocked | explicar demo sin datos vivos |

## Fase 3 — Public Repo Safety Gates

Aplica `kokoro-share-readiness.md` y `kokoro-privacy-protocol.md`.

| Gate | Status | Evidence | If Blocked |
|---|---|---|---|
| `GATE-NO-SENSITIVE-DATA` | Pass/Partial/Blocked | sin secretos trackeados | mover a privado y limpiar |
| Guest identity safe | Pass/Partial/Blocked | placeholders `cliente_NN` | anonimizar |
| Platform accounts safe | Pass/Partial/Blocked | IDs reales no trackeados | mover mappings a `.kokoro/` |
| Reports and exports safe | Pass/Partial/Blocked | `exports/`, `reports/`, `generated/` ignored | sacar del repo publico |
| Runtime state safe | Pass/Partial/Blocked | `.kokoro/`, `.rai/`, runtime state ignored | actualizar `.gitignore` |
| MCP boundaries safe | Pass/Partial/Blocked | docs nombran MCPs, no credenciales | documentar placeholders |

## Fase 4 — Checks Recomendados

Ejecuta o pide ejecutar estos checks cuando el entorno lo permita.

```bash
git status --short
git check-ignore -v .kokoro/clients.json reports/cliente_01/pulse.md generated/cliente_01/ad.png exports/cliente_01/export.csv
rg -n --hidden --glob '!/.git/**' --glob '!/.agents/**' --glob '!work/research/**' \
  "(sk-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{20,}|EAA[A-Za-z0-9]{20,}|access[_-]?token|refresh[_-]?token|client[_-]?secret)" .
```

Interpretacion:

- Hits en docs de regex/checklist pueden ser `Partial` si son ejemplos y no valores reales.
- Hits con valores reales son `Blocked`.
- Untracked private folders pueden ser `Hold` si estan seguros localmente pero no deben compartirse.

## Fase 5 — Operating Run Readiness

Verifica que los runs E40 esten disponibles y tengan gates:

| Run | Required Check |
|---|---|
| `/kokoro-google-ads-run` | MCP health, datasets, privacy, permission |
| `/kokoro-weekly-marketing-run` | platform coverage, date range, private report handling |
| `/kokoro-creative-campaign-run` | promise, storyboard, visual direction, creative review |
| `/kokoro-launch-run` | readiness, validation, tracking, readback |
| `/kokoro-acquisition-run` | bottleneck, tracking, CRM/follow-up, unit economics |
| `/kokoro-share-readiness` | privacy, runtime truth, share decision |

If MCP is unavailable, demo with methodology only:

- Use placeholder context like `cliente_01`.
- Mark MCP and live data gates as `Skipped` or `Blocked`.
- Show the setup path via `/kokoro-connect` or `/kokoro-mcp-reference`.
- Do not invent metrics.

## Fase 6 — Decision

Use the strictest applicable result:

| Result | Condition | Action |
|---|---|---|
| Pass | Only public methodology, placeholders, safe docs, and ignored private paths are present | Share after normal review |
| Hold | Untracked private files are safe locally but docs/ignore/routing need cleanup | Fix before sharing |
| Private Only | Real guest data, exports, credentials, account mappings, or private reports are required | Move work to private workspace |

## Plantilla de Salida

```markdown
## Share Readiness — {alcance}

| Gate | Status | Evidence | Next |
|---|---|---|---|
| Runtime docs accurate | {status} | {evidence} | {next} |
| Commands discoverable | {status} | {evidence} | {next} |
| No-MCP demo path | {status} | {evidence} | {next} |
| No sensitive data | {status} | {evidence} | {next} |
| Guest identity safe | {status} | {evidence} | {next} |
| Platform accounts safe | {status} | {evidence} | {next} |
| Reports and exports safe | {status} | {evidence} | {next} |
| Runtime state safe | {status} | {evidence} | {next} |
| MCP boundaries safe | {status} | {evidence} | {next} |

### Decision

{Pass / Hold / Private Only}

### Evidence

{commands run and relevant findings}

### What Must Stay Private

{files, folders, mappings, exports, reports, or runtime state}

### Before Sharing

| Priority | Action | Owner | Why |
|---:|---|---|---|
| 1 | {action} | {owner} | {evidence} |

### Permission Gate

{question before publishing, packaging, uploading, sending, or committing private artifacts}
```

## Permission Gate

Acciones que requieren invitacion explicita:

- publicar repo
- crear release o zip
- enviar Kokoro a un invitado
- subir archivos a un drive
- limpiar o mover archivos privados
- borrar exports/reportes/generados
- cambiar configuracion MCP
- commitear artefactos con contexto real

Pregunta:

```markdown
Ya tengo el veredicto de share readiness.
¿Quieres que solo te deje la lista de bloqueos, o me invitas a preparar la
version compartible?
```

## Privacidad

- Nunca pidas llaves, tokens o secretos en chat.
- Nunca guardes reportes reales de invitados en rutas trackeadas.
- Usa `cliente_01` y placeholders en docs publicos.
- Treat `.kokoro/`, exports, reports, generated assets, platform mappings,
  runtime state, account IDs, meeting notes, and private landings as private.

## Anti-Patrones

- Compartir porque "parece limpio" sin correr checks.
- Confundir untracked local con seguro para publicar.
- Decir que Codex carga comandos como Claude.
- Hacer demo con metricas inventadas si MCP no esta conectado.
- Subir exports o reportes porque "son necesarios para que se entienda".
