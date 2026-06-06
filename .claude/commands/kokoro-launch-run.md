# /kokoro-launch-run — Corrida de Lanzamiento

> Orquestador E40: claridad de modelo, fuerzas del invitado, PESCAR,
> experimento, activos de lanzamiento, landing, tracking y pulso semanal.

> "Lanzar no es hacer ruido. Lanzar es compartir una creacion validada con
> la persona correcta, por el canal correcto, midiendo la senal correcta."

## Proposito

Usa este run cuando el usuario diga:

- "Quiero lanzar esta creacion"
- "Prepara el lanzamiento"
- "Vamos a sacar esto al mercado"
- "Necesito landing, copy y campana para lanzar"
- "Que nos falta para lanzar?"

Este comando NO reemplaza `/kokoro-launch`. Lo orquesta despues de verificar
si la creacion esta lista para encontrarse con sus invitados.

## Contrato Obligatorio

Antes de recomendar, lee y aplica:

- `.claude/knowledge/kokoro-orchestrator-contract.md`
- `.claude/knowledge/kokoro-phase2-canvas.md`
- `.claude/knowledge/kokoro-phase2-forces.md`
- `.claude/knowledge/kokoro-phase3-pescar.md`
- `.claude/knowledge/kokoro-phase3-experiment.md`
- `.claude/knowledge/kokoro-phase3-launch.md`
- `.claude/knowledge/kokoro-lean-landing.md`
- `.claude/knowledge/kokoro-tracking-checklist.md`

Usa estos skills como capas tacticas:

- `/kokoro-canvas` para modelo y PUV.
- `/kokoro-forces` para trigger, push, inercia y friccion.
- `/kokoro-pescar` para estrategia de comunicacion.
- `/kokoro-experiment` para validacion 3x3x3.
- `/kokoro-launch` para copy, landing y secuencia de lanzamiento.
- `/kokoro-landing` para auditar la secuencia de decision.
- `/kokoro-tracking-check` para medir antes de invertir.
- `/kokoro-weekly-marketing-run` para readback post-lanzamiento.

## Entrada

Formato sugerido:

```text
/kokoro-launch-run {invitado_o_contexto} {creacion} {fecha_o_periodo}
```

Ejemplos publicos:

```text
/kokoro-launch-run cliente_01 nueva creacion septiembre
/kokoro-launch-run cliente_01 taller validado next_30_days
/kokoro-launch-run sin_contexto evaluar readiness
```

`cliente_01` es placeholder publico. No guardes planes, reportes, landings,
assets ni datos privados en este repo.

## Fase 1 — Invitacion y Objetivo

Refleja la intencion:

```markdown
Veo que quieres lanzar una creacion.
Antes de hacer copy, pauta o landing, voy a revisar si la raiz esta lista:
modelo, invitado, promesa, validacion, medicion y camino de conversion.
Si algo falta, te dire que preparar antes de lanzar.
```

Si falta informacion, pregunta solo una cosa. Prioridad:

1. que creacion se lanza
2. a que invitado va dirigida
3. cuando quiere lanzar
4. que evidencia de validacion existe

## Fase 2 — Contexto y Launch Readiness

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
| Creation defined | Pass/Partial/Blocked | que se comparte | aclarar creacion |
| Audience clear | Pass/Partial/Blocked | segmento/invitado | usar `/kokoro-canvas` |
| `GATE-PROMISE-TRUE` | Pass/Partial/Blocked | promesa y realidad | ajustar promesa antes de copy |
| Forces known | Pass/Partial/Blocked | trigger/push/inercia/friccion | usar `/kokoro-forces` |
| Strategy selected | Pass/Partial/Blocked | canal/contenido/CTA | usar `/kokoro-pescar` |
| Validation evidence | Pass/Partial/Blocked | experimento/datos | usar `/kokoro-experiment` |
| Primary metric | Pass/Partial/Blocked | una metrica | definir en experimento |
| Success threshold | Pass/Partial/Blocked | criterio antes de lanzar | definir umbral |
| Invalidation threshold | Pass/Partial/Blocked | criterio de pausa/pivot | definir umbral |
| Landing path | Pass/Partial/Blocked | URL/estructura | usar `/kokoro-launch` o `/kokoro-landing` |
| Tracking plan | Pass/Partial/Blocked | pixel/UTM/CRM/eventos | usar `/kokoro-tracking-check` |
| Readback rhythm | Pass/Partial/Blocked | semanal | usar `/kokoro-weekly-marketing-run` |

## Fase 3 — Decision de Ruta

Clasifica el estado:

| Estado | Significado | Ruta |
|---|---|---|
| Ready to prepare | modelo/audiencia/promesa claros, validacion parcial | preparar experimento o prelaunch |
| Ready to launch | promesa validada, landing y tracking listos | construir plan de lanzamiento |
| Blocked | faltan contexto, promesa o medicion basica | resolver gate antes de activos |

Nunca trates `Blocked` como listo para publicar.

## Fase 4 — Method Chain

Usa esta cadena en orden. Si un gate esta bloqueado, esa es la siguiente ruta.

| Gate faltante | Ruta primaria | Output esperado |
|---|---|---|
| Modelo o PUV | `/kokoro-canvas` | segmento, reto, PUV, canales, metricas |
| Fuerzas del invitado | `/kokoro-forces` | trigger, push, inercia, friccion |
| Estrategia de comunicacion | `/kokoro-pescar` | PESCAR, pilares, CTA, metrica |
| Validacion | `/kokoro-experiment` | hipotesis, metrica, umbrales, sprint |
| Copy/landing/secuencia | `/kokoro-launch` | copy, landing, secuencia, checklist |
| Landing existente | `/kokoro-landing` | mapa de 9 bloques y ajustes |
| Tracking | `/kokoro-tracking-check` | GO/WAIT y gaps criticos |
| Readback | `/kokoro-weekly-marketing-run` | pulso semanal post-lanzamiento |

## Fase 5 — Plan de Lanzamiento

Solo si readiness es `Ready to launch` o `Ready to prepare` con gaps claros.

Incluye:

- objetivo del lanzamiento
- audiencia principal y anti-segmento
- promesa verdadera
- PUV
- CTA unico
- hipotesis principal
- metrica principal
- success threshold
- invalidation threshold
- canales
- assets necesarios
- landing/conversion path
- tracking plan
- calendario
- plan de readback semanal

## Fase 6 — Asset Plan

No generes assets automaticamente. Define inventario:

| Asset | Skill | Gate |
|---|---|---|
| Landing copy | `/kokoro-launch` | promesa y PUV claras |
| Landing audit | `/kokoro-landing` | URL/texto disponible |
| Carrusel/visual | `/kokoro-creative-campaign-run` | storyboard y direccion visual |
| Meta copy/targeting | `/kokoro-ads` | creativo o hilo claro |
| Google Ads | `/kokoro-google-ads-run` | MCP/data si se optimiza cuenta |
| Weekly readback | `/kokoro-weekly-marketing-run` | plataformas/tracking |

## Fase 7 — What I Would Not Touch Yet

Debes nombrar lo que no conviene tocar:

- pauta si tracking esta `WAIT`
- landing si la promesa no esta clara
- copy si no hay fuerzas del invitado
- escalamiento si experimento no supero umbral
- automatizacion si el proceso manual aun no valida
- assets finales si el CTA no esta definido

## Fase 8 — Permission Gate

Acciones que requieren invitacion explicita:

- guardar plan privado
- crear landing o editar sitio
- generar assets visuales
- publicar contenido
- crear campanas
- cambiar tracking
- enviar plan al equipo o invitado
- commitear cualquier artefacto con contexto real

Pregunta:

```markdown
Ya sabemos si esto esta listo para preparar o para lanzar.
¿Quieres que construya los activos concretos ahora, o dejamos primero el
plan de readiness con los gates pendientes?
```

## Plantilla de Salida

```markdown
## Launch Run — {creacion}

| Gate | Status | Evidence | Next |
|---|---|---|---|
| Context resolved | {status} | {evidence} | {next} |
| Creation defined | {status} | {evidence} | {next} |
| Audience clear | {status} | {evidence} | {next} |
| Promise true | {status} | {evidence} | {next} |
| Validation evidence | {status} | {evidence} | {next} |
| Primary metric | {status} | {evidence} | {next} |
| Tracking plan | {status} | {evidence} | {next} |

### Executive Read

{ready to prepare / ready to launch / blocked y por que}

### Evidence vs Assumptions

| Type | Item | Confidence |
|---|---|---|
| Evidence | {hecho validado} | High/Medium/Low |
| Assumption | {supuesto} | High/Medium/Low |

### Launch Plan

| Area | Decision |
|---|---|
| Audience | {invitado} |
| Promise | {promesa} |
| CTA | {cta} |
| Primary metric | {metrica} |
| Success threshold | {umbral} |
| Invalidation threshold | {umbral} |
| Channels | {canales} |
| Timeline | {fechas} |

### Asset Plan

| Asset | Status | Next Skill |
|---|---|---|
| Landing | {status} | `/kokoro-launch` or `/kokoro-landing` |
| Creative campaign | {status} | `/kokoro-creative-campaign-run` |
| Paid copy | {status} | `/kokoro-ads` |
| Tracking | {status} | `/kokoro-tracking-check` |
| Weekly readback | {status} | `/kokoro-weekly-marketing-run` |

### What I Would Not Touch Yet

{acciones que conviene esperar}

### Recommended Next Actions

| Priority | Action | Confidence | Why |
|---:|---|---|---|
| 1 | {accion} | High/Medium/Low | {evidencia} |

### Permission Gate

{pregunta antes de guardar, publicar, editar o crear activos}
```

## Fallbacks

| Situacion | Respuesta |
|---|---|
| No hay modelo claro | usar `/kokoro-canvas` |
| No se entiende por que el invitado actuaria | usar `/kokoro-forces` |
| No hay estrategia de comunicacion | usar `/kokoro-pescar` |
| No hay validacion | usar `/kokoro-experiment` |
| No hay landing | usar `/kokoro-launch` para estructura |
| Landing existe pero no convierte | usar `/kokoro-landing` |
| Tracking incierto | usar `/kokoro-tracking-check` |
| Ya lanzo y quiere leer resultados | usar `/kokoro-weekly-marketing-run` |

## Privacidad

- Nunca pidas llaves, tokens o secretos en chat.
- Nunca guardes planes reales de lanzamiento en rutas trackeadas sin permiso.
- Usa placeholders como `cliente_01` en docs publicos.
- Treat landings, reports, generated assets, exports, CRM data, and platform mappings as private.

## Anti-Patrones

- Lanzar porque hay prisa, no porque hay readiness.
- Crear copy antes de entender fuerzas del invitado.
- Publicar sin metrica principal.
- Optimizar sin tracking confiable.
- Confundir actividad de lanzamiento con aprendizaje.
- Guardar datos privados en el repo publico.
