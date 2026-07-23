# /kokoro-weekly-marketing-run — Pulso Semanal de Marketing

> Orquestador E40: lectura semanal ejecutiva de Meta Ads, Google Ads, GA4 y
> Search Console con contexto, conexion, datos, interpretacion y permiso.

> "La semana no se mide para juzgarla. Se mide para escuchar que senal esta
> creciendo, que raiz pide agua y que rama todavia no debe podarse."

## Proposito

Usa este run cuando el usuario diga algo como:

- "Como va marketing esta semana?"
- "Dame el pulso semanal"
- "Que cambio en mis plataformas?"
- "Que deberia revisar mi equipo esta semana?"
- "Prepara la lectura semanal de marketing"

Este comando NO reemplaza `/kokoro-scorecard` ni `/kokoro-analytics`. Los
orquesta para producir direccion ejecutiva semanal.

## Integracion Tactiq 2025

El pulso semanal debe conectar plataforma con operacion. Si la semana muestra
leads sin avance, conversaciones sin seguimiento, CRM confuso o valor no
visible, deriva a `/kokoro-growth-diagnosis-run`. Si la senal apunta a hook,
landing, promesa o creativo, deriva a `/kokoro-campaign-lab-run`. No cierres
con "optimizar plataforma" cuando el aprendizaje vive en seguimiento u oferta.

## Contrato Obligatorio

Antes de recomendar, lee y aplica:

- `.claude/knowledge/kokoro-orchestrator-contract.md`
- `.kokoro/memoria.md`
- `.claude/knowledge/kokoro-analytics-metrics.md`
- `.claude/knowledge/kokoro-mcp-meta-ads.md`
- `.claude/knowledge/kokoro-mcp-google-ads.md`
- `.claude/knowledge/kokoro-mcp-ga4.md`
- `.claude/knowledge/kokoro-mcp-search-console.md`
- `.claude/knowledge/kokoro-tracking-checklist.md`

Usa estos skills como capas tacticas cuando correspondan:

- `/kokoro-connect` para mapear plataformas.
- `/kokoro-analytics` para consultas puntuales.
- `/kokoro-scorecard` para vista unificada de metricas.
- `/kokoro-google-ads-run` para profundizar en Google Ads.
- `/kokoro-tracking-check` cuando la confianza de conversion sea baja.

## Entrada

Formato sugerido:

```text
/kokoro-weekly-marketing-run {invitado_o_contexto} {rango}
```

Ejemplos publicos:

```text
/kokoro-weekly-marketing-run cliente_01 last_7_days
/kokoro-weekly-marketing-run cliente_01 esta_semana
/kokoro-weekly-marketing-run sin_contexto metodologia
```

`cliente_01` es placeholder publico. No guardes IDs reales, exports,
screenshots, reportes ni contexto privado en este repo.

## Fase 1 — Invitacion y Objetivo

Refleja la intencion:

```markdown
Veo que buscas una lectura semanal de marketing.
Primero voy a resolver el invitado, confirmar el periodo, revisar que
plataformas estan conectadas y separar datos disponibles de datos faltantes.
No voy a convertir ausencia de datos en conclusion.
```

Si falta informacion, pregunta solo una cosa. Prioridad:

1. invitado/contexto
2. rango semanal
3. plataformas a incluir

## Fase 2 — Periodo Semanal

Default si el usuario no especifica:

- Periodo actual: `last_7_days`
- Comparativo: `previous_7_days`

Si el usuario dice "esta semana", interpreta:

- Semana actual hasta hoy.
- Aclara que el periodo puede estar incompleto si se consulta antes de cerrar semana.

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-DATE-RANGE-CLEAR` | Periodo y comparativo definidos | Periodo definido sin comparativo | No se sabe que semana medir |

## Fase 3 — Contexto y Plataformas

Resuelve en este orden:

1. `.kokoro/clients.json` si existe.
2. `metadata.platform_accounts` del invitado.
3. `context_file` si existe.
4. Contexto temporal si el usuario lo dio.
5. Sin contexto guardado solo con confirmacion explicita.

Plataformas esperadas:

| Plataforma | Metadata key | MCP |
|---|---|---|
| Meta Ads | `platform_accounts.meta_ads` | `meta-ads` |
| Google Ads | `platform_accounts.google_ads` | `google-ads` |
| GA4 | `platform_accounts.ga4` | `google-analytics` |
| Search Console | `platform_accounts.gsc` | `not_bundled`; requiere exportacion |

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-CONTEXT-RESOLVED` | Invitado y plataforma(s) localizadas | Contexto temporal o solo algunas plataformas | No hay invitado ni decision de seguir sin contexto |
| `GATE-PLATFORMS-MAPPED` | Al menos una plataforma conectada | Algunas plataformas ausentes | Ninguna plataforma conectada |

Si no hay plataformas conectadas:

```markdown
Todavia no hay cuentas mapeadas para este invitado.
El siguiente paso es `/kokoro-connect`; sin conexion no voy a inventar
metricas de la semana.
```

## Fase 4 — Runtime y Salud MCP

Consulta solo plataformas conectadas o explicitamente solicitadas.

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-MCP-REGISTERED` | MCP requerido callable | Algunos MCP faltan | Ningun MCP requerido callable |
| `GATE-MCP-HEALTHY` | Discovery o lectura exitosa | Algunas plataformas fallan | Ninguna lectura responde |

Si una plataforma falla, continua con las demas y marca la fallida como
`Blocked`. No conviertas falla de MCP en caida de rendimiento.

## Fase 5 — Dataset Coverage

### Meta Ads

| Dataset | Fuente preferida | Uso |
|---|---|---|
| Account summary | `get_account_insights_summary` | inversion, alcance, resultados |
| Campaign performance | `get_campaign_performance` | distribucion de senal por campana/angulo |
| Campaign status and budget | `get_campaign_status_and_budget` | pacing y estado |
| Campaigns | `get_campaigns` | corpus activo |
| Demographics | `get_demographic_breakdown` | senal de audiencia |
| Creative details | `get_ad_creative_details` | continuidad entre creativo y resultado |

### Google Ads

| Dataset | Fuente preferida | Uso |
|---|---|---|
| Cuentas | `customers_list_accessible_customers` | resolver customer ID |
| Metadata | `metadata_get_resource_metadata` | validar campos antes de consultar |
| Campaign performance | `search_search` sobre `campaign` | inversion, clics, conversiones |
| Keywords | `search_search` sobre recurso validado | relevancia si aplica |
| Search terms | `search_search` sobre `search_term_view` | intencion real si aplica |

Si el pulso detecta un reto serio en Google Ads, no resuelvas todo ahi.
Ruta de profundidad: `/kokoro-google-ads-run`.

### GA4

| Dataset | Fuente preferida | Uso |
|---|---|---|
| Traffic overview | `run_report` | sesiones, usuarios, canales |
| Landing pages | `run_report` | calidad del aterrizaje |
| Events/conversions | `run_report` | acciones de valor |
| Property details | `get_property_details` | configuracion y moneda |
| Google Ads links | `list_google_ads_links` | continuidad Ads -> Analytics |

### Search Console

No llames un MCP en esta version. Usa una exportacion aportada con propiedad,
rango y columnas verificables. Sin archivo o evidencia de interfaz, marca
Search Console como `Skipped: not_bundled` y no inventes tendencia organica.

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-DATA-COMPLETE` | Plataformas conectadas consultadas o marcadas skipped | Algunas lecturas fallan | No hay datos vivos para el periodo |

## Fase 6 — Interpretacion Cross-Platform

La lectura ejecutiva debe responder:

1. Que cambio esta semana?
2. Donde se concentra la senal?
3. La inversion pagada llega a sitio con calidad?
4. La demanda organica acompana o contradice la pauta?
5. El tracking permite confiar en las conversiones?
6. Que conviene esperar?
7. Que accion tiene mas apalancamiento esta semana?

No presentes solo tablas. Traduce los datos al lenguaje de direccion.

## Fase 7 — Lenguaje de Corpus, No Podio

Evita ranking binario de campanas o anuncios.

Usa:

- "angulo con mayor concentracion de senal"
- "cluster con baja distribucion"
- "corpus activo"
- "continuidad entre pauta y sitio"
- "plataforma sin lectura esta semana"

No uses lenguaje de podio, competencia binaria o juicio absoluto sobre
campanas/anuncios. Si una frase suena a "primer lugar contra ultimo lugar",
reescribela como distribucion de senal, cluster cubierto, cluster ausente,
madurez de datos o etapa del journey.

## Fase 8 — Privacidad y Permiso

Gate:

| Gate | Pass | Blocked |
|---|---|---|
| `GATE-NO-SENSITIVE-DATA` | No se persisten datos privados en repo publico | Se intenta guardar reporte/export privado |
| `GATE-RECOMMENDATION-ONLY` | Se recomiendan acciones sin mutar plataformas | El output intenta cambiar configuracion |
| `GATE-ACTION-INVITED` | El usuario pide explicitamente crear/cambiar/publicar/guardar | No hay permiso de accion |

Requiere permiso explicito:

- guardar reporte semanal privado
- exportar CSV, PDF, XLSX o screenshot
- cambiar budgets, campañas, pujas, anuncios, landings o tracking
- enviar el pulso a un equipo o invitado
- crear tareas en backlog externo

## Plantilla de Salida

```markdown
## Weekly Marketing Run — {invitado o contexto}

Periodo: {periodo} vs {comparativo}

| Gate | Status | Evidence |
|---|---|---|
| Objective clear | Pass/Partial/Blocked/Skipped | {objetivo} |
| Date range clear | Pass/Partial/Blocked/Skipped | {periodo y comparativo} |
| Context resolved | Pass/Partial/Blocked/Skipped | {invitado/contexto} |
| Platforms mapped | Pass/Partial/Blocked/Skipped | {plataformas} |
| MCP healthy | Pass/Partial/Blocked/Skipped | {lecturas exitosas/fallidas} |
| Data completeness | Pass/Partial/Blocked/Skipped | {datasets} |
| Knowledge loaded | Pass/Partial/Blocked/Skipped | {files} |
| Privacy check | Pass/Partial/Blocked/Skipped | {persistencia segura} |

### Executive Read

{lectura de direccion en 3-5 lineas}

### Platform Coverage

| Plataforma | Status | Lectura |
|---|---|---|
| Meta Ads | Pass/Partial/Blocked/Skipped | {senal disponible o razon} |
| Google Ads | Pass/Partial/Blocked/Skipped | {senal disponible o razon} |
| GA4 | Pass/Partial/Blocked/Skipped | {senal disponible o razon} |
| Search Console | Pass/Partial/Blocked/Skipped | {senal disponible o razon} |

### Cross-Platform Signals

| Signal | Reading | Confidence |
|---|---|---|
| Paid to site continuity | {lectura} | High/Medium/Low |
| Search demand | {lectura} | High/Medium/Low |
| Tracking confidence | {lectura} | High/Medium/Low |
| Corpus distribution | {lectura} | High/Medium/Low |

### What I Would Not Touch Yet

{acciones que conviene esperar por falta de datos, aprendizaje o tracking}

### Recommended Next Actions

| Priority | Action | Confidence | Why |
|---:|---|---|---|
| 1 | {accion} | High/Medium/Low | {evidencia} |

### Permission Gate

{pregunta explicita antes de guardar reporte privado o mutar plataformas}

### Next Weekly Rhythm

{que revisar la proxima semana y que dataset falta conectar}
```

## Fallbacks

| Situacion | Respuesta |
|---|---|
| Ninguna plataforma conectada | Ofrecer `/kokoro-connect`; no inventar metricas |
| Una plataforma falla | Reportarla Blocked y continuar con las demas |
| Sin comparativo | Usar previous_7_days si el usuario acepta |
| Tracking incierto | Priorizar `/kokoro-tracking-check` antes de optimizar |
| Google Ads muestra reto profundo | Redirigir a `/kokoro-google-ads-run` |
| Meta creativo parece saturado | Redirigir a `/kokoro-creative-review` o `/kokoro-ads` segun necesidad |

## Persistencia

No guardes reportes reales en el repo publico.

Si el usuario pide guardar el pulso, usa una ruta privada/ignorada como:

```text
reports/cliente_01/weekly-pulse-YYYY-MM-DD.md
```

Antes de guardar, pregunta:

```markdown
¿Quieres que lo guarde como reporte privado? No lo voy a commitear al repo publico.
```

## Anti-Patrones

- Presentar tablas sin lectura ejecutiva.
- Omitir plataformas no conectadas.
- Tratar MCP caido como rendimiento cero.
- Usar lenguaje de podio para ads o campanas.
- Recomendar acciones sin comparar periodo anterior.
- Optimizar pauta sin confianza minima de tracking.
- Guardar datos privados en el repo publico.
