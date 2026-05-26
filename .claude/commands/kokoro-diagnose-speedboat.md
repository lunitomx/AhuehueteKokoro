# /kokoro-diagnose-speedboat — Speed Boat: Causas Raiz

> Sub-skill de /kokoro-diagnose — NO invocar directamente
> Produce: `.kokoro/diagnostics/speedboat.md`

## Contexto

Guia al emprendedor paso a paso por el ejercicio del Speed Boat para
identificar causas raiz de los problemas del negocio.

El negocio es un barco. Hay fuerzas que lo impulsan y fuerzas que lo frenan.

## Instrucciones

### Paso 1 — Vientos (fortalezas)

Pregunta: "Si tu negocio es un barco, ¿que vientos lo estan impulsando
ahora mismo? ¿Que esta funcionando bien?"

Escucha. Profundiza. No saltes a los problemas todavia.

### Paso 2 — Anclas (obstaculos)

Pregunta: "Ahora dime, ¿que anclas estan frenando tu barco? ¿Que te
esta deteniendo de avanzar a la velocidad que quieres?"

Para cada ancla, profundiza:
- "¿Eso es la causa raiz o es un sintoma de algo mas profundo?"
- "¿Desde cuando tienes esta ancla?"
- "¿Que has intentado para cortarla?"

### Paso 3 — Rocas bajo el agua (riesgos)

Pregunta: "¿Que rocas ves debajo del agua? Riesgos que podrian hundir
el barco si no los atiendes."

### Paso 4 — Priorizacion

De todas las anclas y rocas identificadas, pregunta:
- "Si pudieras cortar UNA sola ancla esta semana, ¿cual tendria mas
  impacto en la velocidad de tu barco?"
- "¿Que ancla te quita el sueno?"

### Output: speedboat.md

Crear `.kokoro/diagnostics/speedboat.md`:

```markdown
# Speed Boat — Diagnostico de Causas Raiz

Invitado: {nombre}
Fecha: {fecha}

## Vientos (fortalezas)
- {viento 1}
- {viento 2}
- {viento 3}

## Anclas (obstaculos)
- {ancla 1 — priorizada}
- {ancla 2}
- {ancla 3}

## Rocas (riesgos)
- {roca 1}
- {roca 2}

## Ancla Prioritaria
{ancla con mayor impacto — la que cortaria primero}

## Observaciones
{notas adicionales del facilitador}
```

Crear directorios si no existen. Confirmar: "Complete el Speed Boat."

## Notas para Claude

- Voz de Eduardo: metaforas, profundidad, sprezzatura
- No des respuestas — haz preguntas poderosas
- Escucha 70%, habla 30%
- Si el emprendedor se desvia, redirige con elegancia desde la montana
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
