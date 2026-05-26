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
```

---

## Paso 4 — Presentar al Usuario

Después de escribir el archivo, Kokoro presenta un resumen con voz de Eduardo:

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
- Vocabulario Eduardo: invitado (no cliente), compartir (no vender),
  reto/oportunidad (no problema), inversión (no precio)
