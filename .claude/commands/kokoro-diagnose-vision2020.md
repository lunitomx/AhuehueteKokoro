# /kokoro-diagnose-vision2020 — Vision 20/20: Puntos Ciegos

> Sub-skill de /kokoro-diagnose — NO invocar directamente
> Input: `.kokoro/diagnostics/speedboat.md`
> Produce: `.kokoro/diagnostics/vision2020.md`

## Contexto

Guia al emprendedor por el ejercicio de Vision 20/20 para identificar
puntos ciegos, areas borrosas, y definir lentes correctivos.

Del barco pasamos al examen de la vista. El objetivo es identificar que
ve claro, que ve borroso y que no ve.

## Instrucciones

### Zona 1 — Vision Clara

Pregunta: "¿Que sabes con certeza sobre tu negocio? No intuicion —
datos, hechos, numeros que puedes defender."

Ayuda a distinguir entre certezas reales y suposiciones disfrazadas.

### Zona 2 — Vision Borrosa

Pregunta: "¿Que intuyes pero nunca has validado? ¿Que 'crees' que
es cierto sobre tu mercado, tu creacion, tus invitados?"

Nota: usar "creacion" en lugar de "producto" e "invitados" en lugar
de "clientes" — vocabulario de Eduardo.

### Zona 3 — Puntos Ciegos

Pregunta: "Si un consultor externo revisara tu negocio con ojos
frescos, ¿que encontraria que tu no ves?"

Preguntas adicionales para revelar puntos ciegos:
- "¿Que preguntas evitas hacerte sobre tu negocio?"
- "¿Que feedback has recibido que descartaste demasiado rapido?"
- "¿En que areas no tienes metricas?"

### Zona 4 — Lentes Correctivos

Para cada zona borrosa y punto ciego, pregunta:
- "¿Que necesitarias para pasar esto de borroso a claro?"
- "¿Que accion concreta podrias tomar esta semana para validar?"

### Output: vision2020.md

Crear `.kokoro/diagnostics/vision2020.md`:

```markdown
# Vision 20/20 — Puntos Ciegos

Invitado: {nombre}
Fecha: {fecha}

## Vision Clara
- {certeza 1}
- {certeza 2}

## Vision Borrosa
- {suposicion 1}
- {suposicion 2}

## Puntos Ciegos
- {punto ciego 1}
- {punto ciego 2}

## Lentes Correctivos
| Area | Accion | Plazo |
|------|--------|-------|
| {borrosa 1} | {que hacer} | {1 semana} |
| {ciego 1} | {que hacer} | {2 semanas} |
```

Confirmar: "Complete el ejercicio Vision 20/20."

## Notas para Claude

- Ayuda a distinguir entre certezas reales y suposiciones disfrazadas
- No juzgues lo que el emprendedor no sabe — ilumina lo que no ve
- El objetivo no es tener todas las respuestas, sino saber donde buscar
- Usa metaforas de vision y luz naturalmente
