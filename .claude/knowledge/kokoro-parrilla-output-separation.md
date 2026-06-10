# Output Separation System — 4 Columnas

> Knowledge file para S46.3. Separación estricta de 4 columnas con
> propósito y consumidor distinto. Si se mezclan, el equipo produce mal.

## Principio

Cada pieza de contenido tiene 4 consumidores distintos:
1. La audiencia que scrollea (2 segundos para decidir si se detiene)
2. El equipo creativo que produce (necesita saber qué grabar, en qué orden)
3. La audiencia que lee (el caption público en el feed)
4. El equipo interno que revisa (notas, advertencias, validaciones)

Mezclar estos 4 consumidores en un solo bloque de texto produce confusión.
Cada columna se escribe para UN consumidor.

## Las 4 Columnas

| Columna | Consumidor | Propósito | ¿Dónde se ve? |
|---------|-----------|-----------|---------------|
| **A — Hook Visible** | Audiencia (0-3s) | Detener el scroll | Texto en video/imagen, primer segundo |
| **B — Guion Visual** | Equipo creativo | Saber qué grabar y en qué orden | Brief de producción |
| **C — Caption Público** | Audiencia (lectura) | Texto del post | Feed de Meta/Instagram |
| **D — Revisión Interna** | Equipo interno | Validar antes de publicar | Notas para el equipo |

## Reglas de Separación

### Columna A — Hook Visible

- Máximo 10 palabras
- Debe ser el texto que aparece EN el video/imagen, no en el caption
- Ejemplo: "Cuando tu rutina ya no cabe entre tráfico y ruido..."
- **No poner aquí:** instrucciones al equipo, precios, CTAs largos

### Columna B — Guion Visual

- Describe qué se graba, en qué orden, con qué texto en pantalla
- Incluye: planos, supers, audio, duración
- Formato: "Plano 1 (0-3s): Persona a cámara desde [ubicación]. Super: '[hook]'..."
- **No poner aquí:** copy público, opiniones sobre la pieza

### Columna C — Caption Público

- Texto listo para publicar tal cual
- Sin notas internas, sin "validar con cliente", sin hipótesis
- Si alguien lo lee en el feed, debe sonar a post real
- **No poner aquí:** instrucciones de producción, advertencias legales

### Columna D — Revisión Interna

- Notas para el equipo que revisa antes de publicar
- "Validar precio vigente", "No publicar como testimonio real",
  "Confirmar ubicación con el cliente"
- **No poner aquí:** copy que debería ir en el caption

## Anti-patrones

| Error | Consecuencia |
|-------|-------------|
| Poner instrucciones de producción en el caption | El caption suena a brief interno, no a post |
| Poner copy público en el guion visual | El equipo no sabe qué es texto en pantalla vs caption |
| Mezclar revisión con caption | "Validar precio" aparece en el feed |
| Hook genérico ("esto te va a interesar") | No detiene a nadie — no dice nada específico |

## Output Template

```markdown
### Pieza: {nombre}

**A — Hook Visible (0-3s)**
{10 palabras máximo}

**B — Guion Visual**
{Descripción de producción: planos, supers, audio, duración}

**C — Caption Público**
{Texto listo para publicar}

**D — Revisión Interna**
{Notas de validación antes de publicar}
```
