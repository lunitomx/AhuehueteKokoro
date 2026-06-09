# /kokoro-google-ads-run — Corrida Ejecutiva de Google Ads

> Orquestador E40: diagnostico completo de Google Ads con contexto, MCP,
> datasets, conocimiento, paciencia estrategica y permiso antes de actuar.

> "Antes de tocar la raiz, hay que saber si la tierra esta seca, si la
> semilla esta viva y si el sistema ya tuvo tiempo de aprender."

## Proposito

Usa este run cuando un fundador, director de marketing, lider comercial o
agencia diga algo como:

- "Revisa Google Ads"
- "Dime que ves en mis campanas"
- "Que deberiamos optimizar en Google?"
- "Por que subio el CPA?"
- "Debemos cambiar pujas, keywords o negativos?"

Este comando NO reemplaza `/kokoro-gads`. Lo orquesta despues de verificar
contexto, conexion, datos, conocimiento y permisos.

## Contrato Obligatorio

Antes de recomendar, lee y aplica:

- `.claude/knowledge/kokoro-orchestrator-contract.md`
- `.claude/knowledge/kokoro-mcp-google-ads.md`
- `.claude/knowledge/google-ads/Optimisaciones_Google_Ads.md`
- `.claude/knowledge/google-ads/Service_Based_Checklist.md`

Luego carga los archivos especificos segun tipo de campana:

| Tipo | Knowledge obligatorio |
|---|---|
| Search | `google-ads/Optimisa_Tus_Campanas_Busqueda.md` + `google-ads/Keyword_Targeting_Search_Term_Audits_Bidding_DETAILED.md` |
| Shopping | `google-ads/Keyword_Targeting_Search_Term_Audits_Bidding_DETAILED.md` |
| Display | `google-ads/Optimise_Your_Display_Campaigns_DETAILED.md` |
| Performance Max / PMax | `google-ads/Optimiza_Tus_Campanas_Performance_Max.md` |
| Multiple / unclear | Load every relevant file before recommendation |

## Entrada

Formato sugerido:

```text
/kokoro-google-ads-run {invitado_o_contexto} {tipo_de_campana} {rango}
```

Ejemplos publicos:

```text
/kokoro-google-ads-run cliente_01 Search last_30_days
/kokoro-google-ads-run cliente_01 PMax ultimos_90_dias
/kokoro-google-ads-run sin_contexto general last_7_days
```

Usa `cliente_01` solo como placeholder publico. No guardes nombres reales,
account IDs reales, exports, reportes ni screenshots en este repo.

## Fase 1 — Invitacion y Objetivo

Primero refleja el objetivo en lenguaje de negocio:

```markdown
Veo que buscas una decision operativa sobre Google Ads.
Antes de recomendar cambios, voy a revisar contexto, conexion, datos,
ritmo de optimizacion y permisos. Si falta algun dato, lo voy a marcar
como faltante en lugar de adivinar.
```

Si falta una sola pieza critica, pregunta solo una cosa. Prioridad:

1. invitado/contexto
2. rango de fechas
3. tipo de campana

## Fase 2 — Contexto del Invitado

Resuelve contexto en este orden:

1. `.kokoro/clients.json` si existe y el usuario menciona un invitado.
2. `metadata.platform_accounts.google_ads` si el invitado esta registrado.
3. `context_file` del invitado si existe.
4. Contexto temporal compartido en la conversacion.
5. Continuar "sin contexto guardado" solo con confirmacion explicita.

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-CONTEXT-RESOLVED` | Invitado y Google Ads account mapping localizados | Contexto temporal suficiente | No se sabe que cuenta o negocio revisar |

Si no hay invitado registrado, ofrece:

```markdown
Podemos seguir como diagnostico general, pero no hare claims de cuenta.
Para datos reales, primero usa `/kokoro-connect` para mapear Google Ads.
```

## Fase 3 — Runtime y MCP

Verifica Google Ads MCP antes de cualquier claim de plataforma.

Herramientas de lectura esperadas:

| Tool | Uso |
|---|---|
| `list_customers` | Descubrir cuentas disponibles |
| `get_campaigns` | Campanas, estado, tipo |
| `get_campaign_performance` | Metricas por campana |
| `get_campaign_status_and_budget` | Estado e inversion diaria/mensual |
| `get_customer_insights_summary` | Resumen ejecutivo |
| `get_keywords_performance` | Keywords, CTR, CPC, Quality Score |
| `get_search_terms` | Terminos reales de busqueda |
| `get_demographic_breakdown` | Edad, genero, dispositivo |
| `get_geographic_breakdown` | Ubicacion |
| `get_ad_details` | Anuncios |
| `execute_gaql` | Auction Insights u otras consultas avanzadas |

Gates:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-MCP-REGISTERED` | `google-ads` es callable | MCP documentado pero no callable en runtime | No hay servidor MCP disponible |
| `GATE-MCP-HEALTHY` | Discovery o consulta de lectura exitosa | Algunas consultas fallan | Ninguna consulta responde |

Si MCP falta o no responde:

- No digas CPC, CPA, ROAS, conversiones ni terminos de busqueda reales.
- Redirige a `/kokoro-connect` y `kokoro-mcp-google-ads.md`.
- Puedes dar una ruta de preparacion, no un diagnostico de rendimiento.

## Fase 4 — Plan de Extraccion de Datos

Antes de analizar, presenta el plan de datasets.

| Dataset | Fuente preferida | Estado | Por que importa |
|---|---|---|---|
| Cuenta | `list_customers` o mapping local | Pass/Partial/Blocked | Seleccion correcta de cuenta |
| Campanas | `get_campaigns` | Pass/Partial/Blocked | Tipo, estado y estructura |
| Rendimiento | `get_campaign_performance` | Pass/Partial/Blocked | Inversion, clics, conversiones, CPA/ROAS |
| Estado e inversion | `get_campaign_status_and_budget` | Pass/Partial/Blocked | Pacing y limites de inversion |
| Keywords | `get_keywords_performance` | Pass/Skipped/Blocked | Search/Shopping keyword health |
| Search Terms | `get_search_terms` | Pass/Skipped/Blocked | Positivos, negativos y relevancia real |
| Negativos/exclusiones | MCP o contexto exportado | Pass/Partial/Skipped | Evitar fugas de inversion |
| Bidding | campaign data, GAQL o contexto | Pass/Partial/Blocked | Madurez y volatilidad |
| Conversiones | performance + tracking context | Pass/Partial/Blocked | Confiabilidad de decisiones |
| Demografia | `get_demographic_breakdown` | Pass/Partial/Skipped | Senal de audiencia |
| Geografia | `get_geographic_breakdown` | Pass/Partial/Skipped | Senal de ubicacion |
| Auction/competencia | `execute_gaql` o unavailable | Pass/Partial/Skipped | Si CPC subio por mercado o relevancia |
| Ads | `get_ad_details` | Pass/Partial/Skipped | Copy y pruebas |
| Landing/tracking | contexto, GA4/GSC, `/kokoro-tracking-check` | Pass/Partial/Blocked | Confianza de conversion |

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-DATA-COMPLETE` | Datasets criticos consultados o marcados como no aplicables | Faltan datasets no criticos o herramientas no disponibles | Faltan datos criticos para el claim solicitado |

## Fase 5 — Datasets por Tipo de Campana

### Search

Requiere:

- campaign performance
- campaign status and budget
- keywords performance
- search terms
- conversion signal
- Quality Score si esta disponible
- Auction Insights si CPC subio o hay presion competitiva
- landing/tracking context

No recomiendes agregar negativos sin ver Search Terms o un export privado
que el usuario ya haya compartido en un espacio seguro.

### Display

Requiere:

- campaign performance
- placements o "where ads showed" si el MCP lo soporta via GAQL/export
- audience performance o insights cuando este disponible
- ad details
- conversion signal

Si placements no estan disponibles, marca el diagnostico como parcial. No
afirmes fugas por placement sin evidencia.

### Performance Max

Requiere:

- campaign performance
- asset group o campaign segmentation si esta disponible
- audience/search category insights si estan disponibles
- landing page context
- conversion value / ROAS cuando aplique
- bidding history o madurez de datos

Si el MCP no expone asset groups o insights, marca la recomendacion como
parcial y orienta a que dataset se debe revisar en Google Ads UI.

## Fase 6 — Gate de Ritmo y Paciencia

Lee `Service_Based_Checklist.md` antes de recomendar timing.

| Ventana | Revisiones permitidas |
|---|---|
| Cada 72 horas | Negativos urgentes en Search Terms |
| Semanal | Terminos positivos, audiencias, recommendations tab, pacing |
| Mensual | Ads, Quality Score, conversiones, ubicaciones, landing irrelevante |
| Cada 90 dias | Bidding strategy, segmentacion de campanas, landing quality profunda |

Reglas:

- No recomendar cambio de bidding antes de la ventana de 90 dias salvo incidente critico de tracking.
- No recomendar Target CPA/ROAS sin conversiones suficientes y estables.
- No llamar "mala" una campana joven; reporta que esta en aprendizaje o sin datos suficientes.
- Si conversiones caen fuerte, revisa tracking, landing y cambios recientes antes de tocar pujas.

## Fase 7 — Analisis y Recomendacion

Primero separa:

- Hallazgos con evidencia.
- Supuestos.
- Datos faltantes.
- Acciones que no se deben tocar aun.

Luego usa `/kokoro-gads` como lente experto para interpretar:

- Search Terms
- keywords
- bidding
- budget/inversion pacing
- conversion signal
- auction/competencia
- landing/tracking
- campaign type

## Fase 8 — Permiso Antes de Mutar

Gate obligatorio:

| Gate | Pass | Blocked |
|---|---|---|
| `GATE-RECOMMENDATION-ONLY` | Recomendaciones separadas de acciones | El output intenta cambiar la cuenta |
| `GATE-ACTION-INVITED` | El usuario pide explicitamente crear/cambiar/agregar/pausar | No hay permiso de accion |

Acciones que requieren invitacion explicita:

- crear campanas
- crear budgets
- cambiar inversion, budget o bidding
- crear ad groups
- crear anuncios
- agregar keywords
- agregar negative keywords via el adapter local de Kokoro
- eliminar negative keywords via el adapter local de Kokoro (delete_negative_keywords)
- pausar, activar o eliminar campanas
- cambiar ubicaciones o idiomas
- cambiar landing pages
- guardar reportes privados o exports

Pregunta de permiso:

```markdown
La recomendacion esta clara, pero todavia no voy a tocar la cuenta.
¿Quieres que prepare los cambios exactos para que los revises, o prefieres
que solo dejemos el plan de accion?
```

## Plantilla de Salida

```markdown
## Google Ads Run — {invitado o contexto}

| Gate | Status | Evidence |
|---|---|---|
| Objective clear | Pass/Partial/Blocked/Skipped | {objetivo} |
| Context resolved | Pass/Partial/Blocked/Skipped | {invitado, temporal, o razon} |
| MCP registered | Pass/Partial/Blocked/Skipped | {google-ads status} |
| MCP healthy | Pass/Partial/Blocked/Skipped | {discovery/query evidence} |
| Data completeness | Pass/Partial/Blocked/Skipped | {datasets queried/missing} |
| Knowledge loaded | Pass/Partial/Blocked/Skipped | {files loaded} |
| Privacy check | Pass/Partial/Blocked/Skipped | {no private data persisted} |

### Dataset Coverage

| Dataset | Status | Evidence |
|---|---|---|
| Campaigns | {status} | {tool/result or missing reason} |
| Performance | {status} | {tool/result or missing reason} |
| Status and budget | {status} | {tool/result or missing reason} |
| Keywords | {status} | {tool/result or skipped} |
| Search Terms | {status} | {tool/result or skipped} |
| Bidding | {status} | {source or missing reason} |
| Conversion signal | {status} | {source or missing reason} |
| Geography/demography | {status} | {source or skipped} |
| Auction/competition | {status} | {source or unavailable} |
| Landing/tracking | {status} | {source or follow-up} |

### Executive Read

{interpretacion clara para direccion}

### What I Would Not Touch Yet

{acciones que conviene esperar}

### Recommended Next Actions

| Priority | Action | Confidence | Why |
|---:|---|---|---|
| 1 | {accion} | High/Medium/Low | {evidencia y timing} |

### Permission Gate

{pregunta explicita antes de mutar cuenta o guardar artefactos privados}

### Next Step

{una accion siguiente}
```

## Fallbacks

| Situacion | Respuesta |
|---|---|
| No hay MCP | "Primero conectamos Google Ads; sin eso solo puedo dar metodologia." |
| MCP no responde | "La conexion no esta sana; no voy a inferir datos." |
| No hay account mapping | "Usa `/kokoro-connect` para seleccionar la cuenta correcta." |
| Falta date range | "Uso `last_30_days` solo si el usuario acepta ese default." |
| Falta campaign type | Consultar `get_campaigns`; si no hay MCP, pedir tipo de campana |
| Falta Search Terms | No recomendar negativos ni positivos concretos |
| Falta conversion tracking | Priorizar `/kokoro-tracking-check` antes de optimizar pujas |
| Faltan Auction Insights | No afirmar que el CPC subio por competencia |

## Privacidad

- Nunca pidas API keys, access tokens, refresh tokens, developer tokens o client secrets en chat.
- Nunca guardes exports, screenshots, reportes, IDs reales o contexto privado en este repo.
- Si se requiere persistencia privada, usar rutas ignoradas como `.kokoro/`, `clientes/`, `exports/` o un workspace privado.
- En artefactos publicos usa `cliente_01` y `1234567890` solo como placeholders.

## Anti-Patrones

- Recomendar cambios antes de verificar MCP y datasets.
- Tratar "MCP faltante" como "la cuenta no tiene datos".
- Recomendar cambiar bidding sin revisar madurez, conversiones y ventana de 90 dias.
- Agregar negativos sin Search Terms.
- Afirmar presion competitiva sin Auction Insights o evidencia equivalente.
- Mostrar JSON crudo sin interpretacion ejecutiva.
- Usar "tips" sueltos en vez de proceso.
- Ejecutar acciones sin invitacion explicita.
