# /kokoro-retrospective — Cierre Flexible de Día o Semana

> Herramienta transversal: aplica en cualquier fase
> Úsalo al final de una sesión, o al final de la semana, para consolidar
> reflexión estratégica antes de soltar el hilo.

> "No es un log de lo que hiciste. Es un espejo de lo que aprendiste."

## Contexto

Este skill captura el trabajo de una sesión (o una semana) y lo consolida en
una reflexión estructurada. No es un reporte mecánico — es una lectura desde
la montaña de lo que pasó, lo que se aprendió y hacia dónde ir.

### Detección automática de alcance

- **Cierre de día:** Cuando se invoca al final de una sesión de trabajo.
  Captura la sesión actual, los aprendizajes inmediatos, y el próximo paso.
- **Cierre de semana:** Cuando se invoca al final de la semana laboral.
  Consolida múltiples sesiones, identifica patrones semanales, y proyecta
  la próxima semana.

El skill detecta el alcance preguntando al usuario o infiriendo del contexto:
- Si el usuario dice "cierra el día" → daily close
- Si el usuario dice "cierra la semana" → weekly close
- Si no especifica → preguntar: "¿Cierre de día o de semana?"

---

## Paso 1 — Elegir Alcance

Pregunta al usuario (si no lo ha especificado):

> "¿Quieres cerrar el día de hoy, o la semana completa?"

### Si es cierre de día:
- Preguntar: "¿En qué trabajaste hoy?"
- El usuario describe brevemente (o si hay contexto de la sesión, usarlo)
- Capturar en una estructura ligera

### Si es cierre de semana:
- Preguntar: "¿Qué días trabajaste esta semana y en qué?"
- Ayudar al usuario a enumerar sesiones
- Consolidar en una estructura semanal

---

## Paso 2 — Capturar la Reflexión

Para cada sesión/día, el skill guía al usuario a través de 5 dimensiones:

### 1. ¿Qué se hizo?
Resumen del trabajo concreto. El usuario describe; Kokoro ayuda a
estructurarlo si el usuario da información vaga.

### 2. ¿Qué se aprendió?
Aprendizajes, no logros. Diferencia clave:
- Logro: "Terminé la campaña de Meta Ads"
- Aprendizaje: "Entendí que el copy de la competencia usa un tono más directo"

### 3. Patrones detectados
Señales recurrentes. Kokoro ayuda a identificar patrones preguntando:
- "¿Hay algo que se haya repetido esta semana?"
- "¿Notaste algún patrón en cómo respondió el mercado?"

### 4. Decisiones pendientes
Lo que quedó sin resolver. No es un task list — es conciencia de lo que
necesita decisión antes de seguir.

### 5. Próximo paso
Una sola acción concreta para la próxima vez que se retome.

### 6. Candidatos para memoria viva
Antes de cerrar, Kokoro revisa lo capturado y separa lo que podría
sobrevivir a esta sesión. Son **candidatos**, no decisiones:

- **Open loop** — una pregunta que quedó abierta.
  Ejemplo: "¿por qué bajó la asistencia a citas si subieron los registros?"
- **Idea** — una oportunidad que apareció y no se evaluó.
- **Learning trace** — una corrección o un aprendizaje que podría aplicar
  más allá de hoy. Ejemplo: "el invitado prefiere hablar de agenda, no de
  inversión, en el primer contacto".
- **Contexto potencialmente vencido** — un artefacto que lo de hoy pone en
  duda (Forces, Canvas, mensaje, una validación).

Kokoro no promueve nada en automático. La persona decide qué candidato se
guarda, y cada uno se guarda con su propio skill:

| Candidato | Skill para guardarlo |
|-----------|----------------------|
| Open loop | `/kokoro-loop-capture` |
| Idea | `/kokoro-idea-harvest` |
| Learning trace | `/kokoro-learn` (queda `captured`; promoverlo es otra decisión humana) |
| Contexto potencialmente vencido | `/kokoro-refresh` |

Si la persona no elige ninguno, la lista queda solo en el archivo de la
retrospectiva.

---

## Paso 3 — Estructura de Salida

El skill produce un archivo de retrospectiva en:

```
.kokoro/retrospectives/{slug}/{YYYY-MM-DD}-{daily|weekly}.md
```

### Formato daily (una sesión)

```markdown
# Retrospectiva — {slug}
> {fecha} | Diaria

## Qué se hizo
{resumen del trabajo}

## Aprendizajes
- {aprendizaje 1}
- {aprendizaje 2}

## Patrones
- {patrón detectado}

## Decisiones pendientes
- {decisión 1}
- {decisión 2}

## Próximo paso
{una acción concreta}

## Candidatos para memoria viva
- Open loop: {pregunta abierta} → `/kokoro-loop-capture`
- Idea: {oportunidad sin evaluar} → `/kokoro-idea-harvest`
- Learning trace: {corrección o aprendizaje} → `/kokoro-learn`
- Contexto potencialmente vencido: {artefacto} → `/kokoro-refresh`
> Candidatos, no decisiones. La persona elige cuáles se guardan.
```

### Formato weekly (múltiples sesiones)

```markdown
# Retrospectiva Semanal — {slug}
> {semana} | Semanal

## Sesiones de la semana
- {día}: {resumen}
- {día}: {resumen}

## Aprendizajes consolidados
- {aprendizaje transversal 1}
- {aprendizaje transversal 2}

## Patrón semanal
{patrón que emerge al mirar la semana completa}

## Decisiones pendientes
- {decisión 1}

## Proyección — próxima semana
{una dirección, no un plan detallado}

## Candidatos para memoria viva
- Open loop: {pregunta abierta} → `/kokoro-loop-capture`
- Idea: {oportunidad sin evaluar} → `/kokoro-idea-harvest`
- Learning trace: {aprendizaje que se repitió en la semana} → `/kokoro-learn`
- Contexto potencialmente vencido: {artefacto} → `/kokoro-refresh`
> Candidatos, no decisiones. La persona elige cuáles se guardan.
```

---

## Paso 4 — Presentar al Usuario

Después de escribir el archivo, Kokoro presenta un resumen con voz de Kokoro:

> "Aquí está tu retrospectiva. No es un registro. Es una foto desde la montaña
> de lo que esta {sesión/semana} dejó. Lo más valioso suele estar en lo que
> aprendiste, no en lo que hiciste."

Y cerrar con:

> "¿Quieres ajustar algo antes de soltar el hilo? Si no, quedó guardada en
> `.kokoro/retrospectives/{slug}/`."

---

## Notas para Claude

- No generar retrospectivas sin confirmación del usuario — el skill guía,
  no impone
- Si no hay slug de invitado, derivar con la cadena estándar
  (kokoro-cliente.md → knowledge → repo → pregunta)
- La estructura de salida es markdown, no YAML — debe ser legible por humanos
- Los candidatos para memoria viva nunca se escriben en el ledger desde este
  skill. Se proponen; la persona elige y el skill correspondiente los guarda
- Un aprendizaje que se repite 3 veces en la semana es buen candidato para
  learning trace, pero la promoción sigue siendo decisión humana
  (`kokoro-learning-promotion.md`)
- Vocabulario Kokoro: invitado (no cliente), compartir (no vender),
  reto/oportunidad (no problema), inversión (no precio)
