# /kokoro-acquisition-run — Corrida de Adquisicion

> Orquestador E40: Customer Factory, Funnel Consciente, Oferta Mafia,
> landing, analitica, tracking, CRM/follow-up y pulso semanal.

> "Mas trafico no sana una raiz rota. Primero vemos donde se detiene la
> energia: descubrimiento, decision, experiencia, medicion o seguimiento."

## Proposito

Usa este run cuando el usuario diga:

- "Necesito mas invitados"
- "Quiero mejorar adquisicion"
- "Llegan leads pero no cierran"
- "Tengo clics pero pocos contactos"
- "Ventas bajo y no se donde esta el cuello"
- "Que parte del embudo debo mejorar?"
- "Donde invierto la siguiente semana?"

Este comando NO reemplaza `/kokoro-funnel`, `/kokoro-mafia`, `/kokoro-landing`
ni `/kokoro-analytics`. Los orquesta para diagnosticar el sistema completo
antes de recomendar mas inversion, mas canales o mas activos.

## Integracion Tactiq 2025

Este run es el puente E40 natural para `/kokoro-growth-diagnosis-run`. Si el
usuario trae una situacion ambigua de crecimiento, usa Growth Diagnosis primero
para separar suelo, semilla, germinacion y cosecha. Si ya hay datos de funnel,
usa Acquisition Run para mapear el cuello con Customer Factory, Funnel
Consciente, oferta, landing, tracking y seguimiento.

## Contrato Obligatorio

Antes de recomendar, lee y aplica:

- `.claude/knowledge/kokoro-orchestrator-contract.md`
- `.kokoro/memoria.md`
- `.claude/knowledge/kokoro-phase4-factory.md`
- `.claude/knowledge/kokoro-phase4-funnel.md`
- `.claude/knowledge/kokoro-phase4-mafia.md`
- `.claude/knowledge/kokoro-lean-landing.md`
- `.claude/knowledge/kokoro-analytics-metrics.md`
- `.claude/knowledge/kokoro-tracking-checklist.md`

Usa estos skills como capas tacticas:

- `/kokoro-factory` para mapear adquirir, activar, retener, ingresos y referir.
- `/kokoro-funnel` para mapear conciencia, consideracion, decision, experiencia y lealtad.
- `/kokoro-mafia` para evaluar claridad de oferta, friccion, garantia e inversion.
- `/kokoro-landing` para auditar la secuencia de decision y CTA.
- `/kokoro-analytics` para consultas puntuales de plataformas conectadas.
- `/kokoro-scorecard` para vista panoramica cross-platform.
- `/kokoro-tracking-check` para validar medicion antes de cambios.
- `/kokoro-google-ads-run` cuando el cuello parezca busqueda/pauta Google.
- `/kokoro-weekly-marketing-run` para readback y ritmo operativo.

## Entrada

Formato sugerido:

```text
/kokoro-acquisition-run {invitado_o_contexto} {reto_de_adquisicion} {periodo}
```

Ejemplos publicos:

```text
/kokoro-acquisition-run cliente_01 necesito mas invitados last_30_days
/kokoro-acquisition-run cliente_01 muchos clics pocos contactos
/kokoro-acquisition-run cliente_01 ventas bajaron esta semana
/kokoro-acquisition-run sin_contexto diagnosticar embudo
```

`cliente_01` es placeholder publico. No guardes reportes, CRM exports,
platform mappings, IDs reales, landings privadas ni datos sensibles en este repo.

## Fase 1 — Invitacion y Objetivo

Refleja la intencion:

```markdown
Veo que quieres mejorar adquisicion.
Antes de pedir mas trafico, voy a revisar el sistema completo: como llegan
las personas, donde se activan, que oferta ven, que pagina recorren, que
tracking existe y que pasa despues del lead.
```

Si falta informacion, pregunta solo una cosa. Prioridad:

1. cual es el reto principal: mas leads, mas calidad, mas cierre o menor inversion por adquisicion
2. que invitado/contexto se analiza
3. que periodo importa
4. donde ocurre la friccion visible: ads, landing, formulario, CRM, cierre o retencion

## Fase 2 — Contexto y Acquisition Readiness

Resuelve contexto desde:

1. `.kokoro/clients.json` si existe.
2. `context_file`, `segments`, `metadata`, `repos` del invitado.
3. `.kokoro/state.json` si existe.
4. contexto temporal compartido por el usuario.
5. decision explicita de continuar sin contexto guardado.

Tabla obligatoria:

| Gate | Status | Evidence | If Blocked |
|---|---|---|---|
| `GATE-CONTEXT-RESOLVED` | Pass/Partial/Blocked | invitado/contexto | usar `/kokoro-client` o contexto temporal |
| `GATE-OBJECTIVE-CLEAR` | Pass/Partial/Blocked | mas leads/calidad/cierre/CPA/LTV | hacer una pregunta |
| Acquisition stage known | Pass/Partial/Blocked | adquirir/activar/decision/follow-up | mapear con `/kokoro-factory` |
| Channel mix known | Pass/Partial/Blocked | Meta/Google/organico/referidos/directo | usar `/kokoro-scorecard` o contexto |
| Landing path known | Pass/Partial/Blocked | URL/texto/flujo | usar `/kokoro-landing` |
| Offer clarity known | Pass/Partial/Blocked | PUV/oferta/garantia/inversion | usar `/kokoro-mafia` |
| `GATE-TRACKING-HEALTH` | Pass/Partial/Blocked | pixel/UTM/eventos/CRM | usar `/kokoro-tracking-check` |
| CRM/follow-up visible | Pass/Partial/Blocked | llegada, asignacion, tiempos, cierre | pedir evidencia manual o MCP privado |
| Unit economics known | Pass/Partial/Blocked | CPA/LTV/conversion/inversion | estimar o medir |
| Readback rhythm | Pass/Partial/Blocked | pulso semanal | usar `/kokoro-weekly-marketing-run` |

## Fase 3 — Data and Runtime Gates

Si el usuario quiere una recomendacion con datos, aplica estos gates antes de
interpretar performance:

| Gate | Status | Evidence | If Blocked |
|---|---|---|---|
| `GATE-MCP-REGISTERED` | Pass/Partial/Blocked/Skipped | Meta/Google/GA4/GSC/CRM disponible | no afirmar datos vivos |
| `GATE-MCP-HEALTHY` | Pass/Partial/Blocked/Skipped | discovery o lectura exitosa | usar otras fuentes o setup |
| `GATE-DATA-COMPLETE` | Pass/Partial/Blocked/Skipped | plataformas/periodo/datasets consultados | bajar confianza |
| `GATE-KNOWLEDGE-LOADED` | Pass/Partial/Blocked | knowledge files nombrados y leidos | cargar antes de recomendar |
| `GATE-NO-SENSITIVE-DATA` | Pass/Partial/Blocked | sin secretos/export privados en repo | detener y mover a privado |

Datasets deseables:

| Area | Evidence |
|---|---|
| Traffic | impresiones, clics, CTR, CPC, fuente/canal |
| Landing | sesiones, bounce, CTA, formularios, bloqueos de decision |
| Lead capture | leads, conversion rate, duplicates, UTM persistence |
| Sales follow-up | speed to lead, contacto, calificacion, oportunidades, cierre |
| Offer | PUV, objeciones, garantia, prueba, inversion, ROI |
| Economics | CPA, LTV, ratio LTV/CPA, valor por lead, conversion a ingreso |

Nunca trates datos no disponibles como rendimiento cero.

## Fase 4 — Bottleneck Map

Primero ubica el cuello de botella. Usa dos mapas juntos.

### Customer Factory

| Stage | Question | Metric / Evidence | Possible Bottleneck |
|---|---|---|---|
| Acquire | Llegan las personas correctas? | CTR, CPC, fuentes, calidad | canal, mensaje, segmentacion |
| Activate | Experimentan valor o dejan senal? | lead rate, agenda, diagnostico, primera respuesta | landing, CTA, friccion |
| Retain | Se quedan o siguen el proceso? | asistencia, continuidad, churn | experiencia, onboarding |
| Revenue | La relacion produce ingreso sano? | cierre, CPA, LTV, ticket, margen | oferta, seguimiento, pricing de inversion |
| Refer | Recomiendan o vuelven? | referidos, NPS, repeticion | experiencia, comunidad, prueba |

### Funnel Consciente

| Stage | Question | Metric / Evidence | Possible Bottleneck |
|---|---|---|---|
| Conciencia | El invitado reconoce el reto? | alcance, engagement, busquedas | trigger debil |
| Consideracion | Puede evaluar opciones? | visitas profundas, social proof | prueba/confianza |
| Decision | Puede elegir sin friccion? | CTA, formularios, tasa conversion | oferta/CTA/garantia |
| Experiencia | Recibe valor rapido? | onboarding, show rate, aha moment | activacion |
| Lealtad | Quiere compartir? | referidos, NPS, recompra | experiencia/referidos |

## Fase 5 — Decision de Ruta

Clasifica el estado:

| Estado | Significado | Ruta |
|---|---|---|
| Data Blocked | no hay medicion suficiente | `/kokoro-tracking-check` o `/kokoro-connect` |
| Traffic Bottleneck | no llega suficiente persona correcta | revisar canales, `/kokoro-google-ads-run`, Meta/SEO segun datos |
| Landing Bottleneck | llega trafico pero no avanza | `/kokoro-landing` y oferta |
| Offer Bottleneck | entiende pero no elige | `/kokoro-mafia` |
| Follow-up Bottleneck | deja senal pero no cierra | revisar CRM, speed to lead, calificacion |
| Economics Bottleneck | adquiere pero no hay margen | `/kokoro-factory` y unit economics |
| Readback Needed | cambios existen pero falta ritmo | `/kokoro-weekly-marketing-run` |

Nunca recomiendes aumentar inversion si `GATE-TRACKING-HEALTH` esta Blocked
o si el cuello principal esta en landing, oferta o follow-up.

## Fase 6 — Method Chain

Usa esta cadena en orden. Si un gate esta bloqueado, esa es la siguiente ruta.

| Gate faltante | Ruta primaria | Output esperado |
|---|---|---|
| Sistema incompleto | `/kokoro-factory` | CPA, LTV, activacion, retencion, referidos |
| Funnel no visible | `/kokoro-funnel` | etapas, contenido, metricas, fricciones |
| Oferta debil | `/kokoro-mafia` | PUV, garantia, objeciones, inversion, ROI |
| Landing incierta | `/kokoro-landing` | 9 bloques, CTA, prueba, fricciones |
| Datos por plataforma | `/kokoro-analytics` | metricas interpretadas |
| Vista ejecutiva | `/kokoro-scorecard` | panorama cross-platform |
| Tracking incierto | `/kokoro-tracking-check` | GO/WAIT y gaps criticos |
| Google Ads parece cuello | `/kokoro-google-ads-run` | diagnostico con search terms/keywords/tracking |
| Ritmo posterior | `/kokoro-weekly-marketing-run` | lectura semanal y acciones |

## Fase 7 — Diagnostico Ejecutivo

Entrega un diagnostico de una raiz principal y maximo dos secundarias:

- raiz principal
- evidencia
- supuestos
- impacto esperado si se corrige
- riesgo de tocar otra cosa primero
- skill tactico recomendado
- siguiente accion medible

Usa lenguaje de direccion:

- "el cuello esta en..."
- "la senal se pierde entre..."
- "no conviene invertir mas hasta..."
- "la siguiente inversion deberia ir a..."
- "esto es una hipotesis porque falta..."

## Fase 8 — Action Plan

Incluye:

- objetivo de adquisicion
- stage principal afectado
- cuello de botella
- metrica principal
- proxy metric si falta data completa
- accion de 7 dias
- accion de 30 dias
- owner sugerido: marketing, ventas, operaciones, direccion
- readback semanal
- condicion de no tocar

## Fase 9 — What I Would Not Touch Yet

Debes nombrar lo que no conviene tocar:

- aumentar inversion si tracking esta `WAIT`
- lanzar mas ads si landing/CTA no convierte
- cambiar todos los canales a la vez
- reescribir oferta sin evidencia de friccion
- optimizar Google Ads si el cuello esta en seguimiento
- automatizar CRM si aun no existe proceso manual claro
- escalar una creacion si LTV/CPA no esta sano o no se conoce
- juzgar un canal con ventana de datos incompleta

## Fase 10 — Permission Gate

Acciones que requieren invitacion explicita:

- cambiar campanas, presupuestos, pujas, keywords o negativos
- editar landing o sitio
- cambiar eventos, pixels, UTMs o CRM
- crear reportes privados
- exportar datos
- guardar contexto real de invitado
- enviar recomendaciones al equipo
- commitear cualquier artefacto con contexto real

Pregunta:

```markdown
Ya ubicamos el cuello de adquisicion y el siguiente movimiento.
¿Quieres que lo convierta en un plan privado accionable, o primero resolvemos
el gate bloqueado antes de tocar campanas, landing, tracking o CRM?
```

## Plantilla de Salida

```markdown
## Acquisition Run — {invitado/contexto}

| Gate | Status | Evidence | Next |
|---|---|---|---|
| Context resolved | {status} | {evidence} | {next} |
| Objective clear | {status} | {evidence} | {next} |
| Channel mix known | {status} | {evidence} | {next} |
| Landing path known | {status} | {evidence} | {next} |
| Offer clarity known | {status} | {evidence} | {next} |
| Tracking health | {status} | {evidence} | {next} |
| CRM/follow-up visible | {status} | {evidence} | {next} |
| Unit economics known | {status} | {evidence} | {next} |

### Bottleneck Map

| Stage | Status | Evidence | Interpretation |
|---|---|---|---|
| Acquire | {status} | {evidence} | {interpretation} |
| Activate | {status} | {evidence} | {interpretation} |
| Revenue | {status} | {evidence} | {interpretation} |
| Follow-up | {status} | {evidence} | {interpretation} |

### Executive Read

{raiz principal, raiz secundaria, confianza y por que}

### Evidence vs Assumptions

| Type | Item | Confidence |
|---|---|---|
| Evidence | {hecho validado} | High/Medium/Low |
| Assumption | {supuesto} | High/Medium/Low |

### Acquisition Action Plan

| Priority | Action | Owner | Confidence | Why |
|---:|---|---|---|---|
| 1 | {accion} | {marketing/ventas/operaciones/direccion} | {confidence} | {evidencia} |

### What I Would Not Touch Yet

{acciones que conviene esperar}

### Permission Gate

{pregunta antes de guardar, publicar, editar, conectar o cambiar}
```

## Fallbacks

| Situacion | Respuesta |
|---|---|
| No hay contexto | usar `/kokoro-client` o contexto temporal |
| No hay datos vivos | usar `/kokoro-connect`, `/kokoro-analytics` o diagnostico manual |
| Tracking incierto | usar `/kokoro-tracking-check` antes de invertir |
| No se entiende la maquina | usar `/kokoro-factory` |
| No se entiende el camino del invitado | usar `/kokoro-funnel` |
| Oferta no es clara | usar `/kokoro-mafia` |
| Landing existe pero no convierte | usar `/kokoro-landing` |
| Google Ads parece cuello | usar `/kokoro-google-ads-run` |
| Ya hay acciones y falta lectura | usar `/kokoro-weekly-marketing-run` |

## Privacidad

- Nunca pidas llaves, tokens o secretos en chat.
- Nunca guardes reportes reales de adquisicion en rutas trackeadas sin permiso.
- Usa placeholders como `cliente_01` en docs publicos.
- Treat CRM data, exports, reports, generated assets, platform mappings, account IDs, lead details, and private landings as private.
- Si el usuario comparte datos sensibles, resume lo necesario y sugiere mover el trabajo a un espacio privado antes de persistir.

## Anti-Patrones

- Pedir mas trafico antes de ubicar el cuello.
- Optimizar campanas con tracking roto.
- Culpar al canal cuando la oferta no se entiende.
- Reescribir landing sin conocer el CTA unico.
- Ignorar CRM/follow-up porque "marketing ya genero leads".
- Escalar una creacion sin LTV/CPA o proxy economico.
- Guardar datos privados en el repo publico.
