# /kokoro-diagnose-ranking — Ranking de Claridad: Puntos Ciegos

> Sub-skill de /kokoro-diagnose — NO invocar directamente
> Input: `.kokoro/diagnostics/anclas.md`
> Produce: `.kokoro/diagnostics/ranking.md`

## Contexto

Guia al emprendedor por el ejercicio de Ranking de Claridad para identificar
puntos ciegos, areas borrosas, y definir lentes correctivos.

Del barco pasamos al examen de la vista. El objetivo es identificar que
ve claro, que ve borroso y que no ve.

Lee tambien `kokoro-dinamicas-vivas.md`. En la adaptacion Kokoro, Ranking de
Claridad tambien funciona como tecnica de priorizacion con tarjetas: se
comparan opciones una por una para evitar que todo parezca igual de importante.
Kokoro conserva la lectura de vision clara/borrosa/puntos ciegos, y agrega un
modo de ranking cuando la persona necesita priorizar.

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

### Modo Ranking — Claridad Forzada

Usa este modo cuando la persona trae muchas opciones y no logra priorizar:

1. Crea de 8 a 20 tarjetas de opciones, iniciativas o atributos.
2. Escribe el beneficio esperado detras de cada tarjeta.
3. Toma dos tarjetas y pregunta cual debe ir arriba.
4. Agrega una tarjeta a la vez y fuerza una posicion relativa.
5. Evita grupos demasiado grandes como "todas son prioridad".
6. Si hay segmentos distintos, registra rankings separados por segmento.
7. Antes de cerrar, contrasta el ranking con economia, dependencias y capacidad.

Preguntas:

- "Que opcion mueve mas el resultado de negocio?"
- "Que opcion parece deseable pero depende de otra?"
- "Que segmento pondria esto mas arriba y por que?"
- "Que costo, riesgo o esfuerzo no se ve en el ranking?"

### Output: ranking.md

Crear `.kokoro/diagnostics/ranking.md`:

```markdown
# Ranking de Claridad — Puntos Ciegos

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

## Ranking de Claridad (si aplica)
| Rank | Opcion | Beneficio | Segmento | Dependencia | Nota economica |
|------|--------|-----------|----------|-------------|----------------|
| 1 | {opcion} | {beneficio} | {segmento} | {dependencia} | {costo/riesgo} |
```

Confirmar: "Complete el ejercicio Ranking de Claridad."

## Notas para Claude

- Ayuda a distinguir entre certezas reales y suposiciones disfrazadas
- No juzgues lo que el emprendedor no sabe — ilumina lo que no ve
- El objetivo no es tener todas las respuestas, sino saber donde buscar
- Usa metaforas de vision y luz naturalmente
