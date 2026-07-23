# /kokoro-creative-campaign-run — Corrida de Campana Creativa

> Orquestador E40: estrategia, storyboard, direccion visual, generacion,
> revision y copy para campanas visuales y carruseles.

> "No estamos haciendo artes bonitos. Estamos construyendo una decision
> mental en pantallas."

## Proposito

Usa este run cuando el usuario pida:

- un carrusel para Meta Ads
- imagenes para una campana
- copies y headlines para piezas visuales
- prompts para generar creativos
- revision de un concepto visual antes de pauta
- adaptar una campana a un hilo narrativo

Este comando NO reemplaza `/kokoro-creative`, `/kokoro-creative-review` ni
`/kokoro-ads`. Los encadena en el orden correcto.

## Integracion Tactiq 2025

Si falta fuerza de eleccion, hook, objecion dominante, landing o seguimiento,
usa primero `/kokoro-campaign-lab-run`. La corrida creativa E40 produce piezas;
Campaign Lab ordena la decision de campo que esas piezas deben amplificar.

## Contrato Obligatorio

Antes de producir assets, lee y aplica:

- `.claude/knowledge/kokoro-orchestrator-contract.md`
- `.kokoro/memoria.md`
- `.claude/knowledge/kokoro-ads-meta.md`
- `.claude/knowledge/kokoro-meta-ai-ecosystem.md`
- `.claude/knowledge/kokoro-creative-gemini.md`
- `.claude/knowledge/kokoro-creative-diversification.md`

Usa estos skills como capas tacticas:

- `/kokoro-ads` para copy, headlines, WhatsApp y audiencia.
- `/kokoro-creative` para construir specs y generar imagenes.
- `/kokoro-creative-review` para evaluar claridad, clusters y journey.
- `/kokoro-analytics` solo si el usuario pide lectura post-pauta.

## Entrada

Formato sugerido:

```text
/kokoro-creative-campaign-run {invitado_o_contexto} {formato} {objetivo}
```

Ejemplos publicos:

```text
/kokoro-creative-campaign-run cliente_01 carrusel Meta Ads sesion informativa
/kokoro-creative-campaign-run cliente_01 imagen unica awareness
/kokoro-creative-campaign-run sin_contexto storyboard lanzamiento
```

`cliente_01` es placeholder publico. No guardes contexto real, imagenes,
modelos, logos, specs ni reportes creativos en el repo publico.

## Fase 1 — Invitacion y Objetivo

Refleja la intencion:

```markdown
Veo que quieres crear una campana visual.
Antes de generar imagenes, voy a ordenar la promesa, la audiencia, el hilo
narrativo y la direccion visual. Si falta una pieza, la marco como gate
pendiente en lugar de producir un arte suelto.
```

Si falta informacion, pregunta solo una cosa. Prioridad:

1. objetivo de la campana
2. formato: carrusel, imagen unica, story/reel, display
3. audiencia
4. promesa/evento real
5. assets de marca o restricciones visuales

## Fase 2 — Contexto y Promesa Real

Resuelve:

- invitado o contexto temporal
- objetivo: awareness, trafico, leads, conversion, remarketing
- formato y superficie: Feed, Stories, Reels, WhatsApp, Display
- audiencia y etapa de consciencia
- creacion/evento/oferta real
- CTA real
- restricciones de marca, modelos, logo, colores, tono y claims

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-CONTEXT-RESOLVED` | Invitado/contexto y marca claros | Contexto temporal suficiente | No se sabe para quien se crea |
| `GATE-PROMISE-TRUE` | La promesa coincide con el evento/oferta real | Promesa necesita ajuste menor | La pieza promete algo que no ocurrira |

Si el usuario pide directamente "haz las imagenes" y falta promesa:

```markdown
Todavia no genero. Primero necesito asegurar que lo que la pieza promete
sea exactamente lo que la persona vivira despues del clic.
```

## Fase 3 — Audiencia, Tension y Decision

Define:

| Elemento | Pregunta |
|---|---|
| Persona | Quien esta viendo la pieza? |
| Momento mental | Que duda o deseo trae antes de verla? |
| Tension | Que frase interna la detiene? |
| Reframe | Que nueva lectura le queremos dar? |
| Decision | Que debe sentir que puede elegir? |
| CTA | Que invitacion concreta cierra el camino? |

Salida minima:

```markdown
Audiencia: {persona}
Tension: {duda/deseo}
Promesa real: {promesa}
Decision deseada: {decision}
CTA: {invitacion}
```

## Fase 4 — Storyboard

Para carruseles, crea primero el storyboard. No escribas prompts de imagen
ni copies finales antes de este gate.

| Frame | Role | Question | Output |
|---:|---|---|---|
| 1 | hook | What stops the scroll? | una idea dominante |
| 2 | tension | What doubt already exists? | una friccion reconocible |
| 3 | reframe | What changes the interpretation? | una nueva lectura |
| 4 | choice/proof | What grounds the decision? | opcion, prueba o criterio |
| 5 | invitation | What action closes the journey? | CTA claro |

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-STORYBOARD-APPROVED` | Cada frame tiene una idea, emocion y avance | Falta pulir un frame | No hay hilo o son piezas aisladas |

Regla:

```text
1 imagen = 1 pensamiento = 1 emocion = 1 avance.
```

## Fase 5 — Direccion Visual por Frame

Antes de generar, define visual direction para cada frame:

| Campo | Que debe resolver |
|---|---|
| gaze | Mirada a camara, mirada al texto, mirada a accion o mirada introspectiva |
| focal point | Donde debe caer el ojo primero |
| hierarchy | Orden de lectura: sujeto, texto, logo, CTA |
| CTA path | Como el ojo llega a la accion |
| emotion | Que emocion debe sentirse |
| composition | Plano, recorte, espacio negativo, ubicacion de texto |
| preserve | Que no se debe cambiar: modelo, merch, logo, color, estilo |
| avoid | Que no debe aparecer o repetirse |

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-VISUAL-DIRECTION-CLEAR` | Cada frame tiene gaze, focal point, hierarchy y CTA path | Falta detalle en algunos frames | No hay direccion de atencion |

Ejemplo de direccion:

```markdown
Frame 1
- gaze: a camara para detener scroll
- focal point: rostro + headline
- hierarchy: rostro, headline, logo discreto, CTA secundario
- CTA path: mirada frontal conduce al texto y baja hacia la invitacion
- preserve: mismo modelo, merch de marca, paleta existente
- avoid: pose contemplativa mirando fuera del anuncio
```

## Fase 6 — Specs de Generacion

Solo despues de aprobar storyboard y visual direction, construye specs para
`/kokoro-creative`.

Cada spec debe incluir:

- prompt_instruction
- text_critical_rules
- scene
- lighting
- color_scheme
- text_overlays
- brand_guidelines
- technical
- preserve
- avoid
- frame_role
- visual_attention

No generes imagenes todavia si el usuario solo pidio planeacion. Pregunta:

```markdown
Ya tengo storyboard y direccion visual.
¿Quieres que ahora construya los prompts/specs de generacion, o prefieres
revisar primero el hilo del carrusel?
```

## Fase 7 — Revision Creativa

Antes de pasar a copy final o pauta, aplica `/kokoro-creative-review`.

Gate:

| Gate | Pass | Partial | Blocked |
|---|---|---|---|
| `GATE-CREATIVE-REVIEWED` | Concepto/spec o draft revisado con Meta AI lens | Revision parcial por falta de imagen | No se reviso claridad, clusters ni journey |

Revisar:

- GEM: claridad de intencion
- Andromeda: cluster visual
- Lattice: adaptabilidad por superficie
- Sequence Learning: lugar en el journey
- carga cognitiva
- legibilidad en movil
- continuidad narrativa
- coherencia entre promesa y CTA

## Fase 8 — Copy y Targeting

Solo despues de storyboard + visual direction + review:

- usa `/kokoro-ads` para primary text, headlines, WhatsApp y audience
- conserva el hilo narrativo del carrusel
- no repitas el mismo pensamiento en cinco variantes
- adapta copy a la etapa del journey

## Fase 9 — Permission Gate

Acciones que requieren invitacion explicita:

- generar imagenes
- guardar JSON specs
- guardar imagenes
- exportar ZIP
- publicar contenido
- crear o editar campanas
- enviar assets al equipo o invitado
- commitear cualquier artefacto con contexto privado

Pregunta:

```markdown
El sistema creativo esta listo.
¿Quieres que genere los assets ahora, o dejamos aprobado el storyboard y
la direccion visual como guia de produccion?
```

## Plantilla de Salida

```markdown
## Creative Campaign Run — {invitado o contexto}

| Gate | Status | Evidence |
|---|---|---|
| Objective clear | Pass/Partial/Blocked/Skipped | {objetivo} |
| Context resolved | Pass/Partial/Blocked/Skipped | {contexto} |
| Promise true | Pass/Partial/Blocked/Skipped | {promesa real} |
| Storyboard approved | Pass/Partial/Blocked/Skipped | {frames} |
| Visual direction clear | Pass/Partial/Blocked/Skipped | {direccion visual} |
| Creative reviewed | Pass/Partial/Blocked/Skipped | {review} |
| Privacy check | Pass/Partial/Blocked/Skipped | {persistencia segura} |

### Executive Read

{que decision mental estamos construyendo}

### Storyboard

| Frame | Role | Thought | Emotion | Advance |
|---:|---|---|---|---|
| 1 | hook | {idea} | {emocion} | {avance} |
| 2 | tension | {idea} | {emocion} | {avance} |
| 3 | reframe | {idea} | {emocion} | {avance} |
| 4 | choice/proof | {idea} | {emocion} | {avance} |
| 5 | invitation | {idea} | {emocion} | {avance} |

### Visual Direction

| Frame | gaze | focal point | hierarchy | CTA path | preserve | avoid |
|---:|---|---|---|---|---|---|
| 1 | {gaze} | {point} | {hierarchy} | {path} | {preserve} | {avoid} |

### What I Would Not Touch Yet

{elementos que no conviene cambiar: modelo, marca, promesa, claim, assets}

### Recommended Next Actions

| Priority | Action | Confidence | Why |
|---:|---|---|---|
| 1 | {accion} | High/Medium/Low | {evidencia} |

### Permission Gate

{pregunta antes de generar, guardar, publicar o commitear}
```

## Fallbacks

| Situacion | Respuesta |
|---|---|
| Falta promesa real | Reframing antes de copy o imagen |
| Falta audiencia | Preguntar por persona o inferir con baja confianza |
| Falta logo/assets | Pedir assets o trabajar como storyboard sin generacion |
| Usuario pide generar directo | Bloquear hasta storyboard y visual direction |
| No hay acceso a generador | Entregar specs listas para produccion |
| Hay draft visual pero no review | Aplicar `/kokoro-creative-review` antes de pauta |

## Privacidad

- Nunca pidas secretos o llaves de API en chat.
- Nunca guardes specs o imagenes privadas en rutas trackeadas.
- Usa rutas privadas/ignoradas para assets reales.
- En ejemplos publicos usa `cliente_01`, no nombres reales.
- No commitees logos, modelos, fotografias, exports o specs con contexto de invitado.

## Anti-Patrones

- Generar imagenes antes de promesa y storyboard.
- Hacer cinco slides bonitos sin hilo.
- Priorizar estetica sobre direccion de atencion.
- Cambiar modelos, merch, logo o estilo sin invitacion.
- Meter tres ideas en un solo frame.
- Revisar visuales solo como diseno, no como journey.
- Publicar o guardar assets sin permiso.
