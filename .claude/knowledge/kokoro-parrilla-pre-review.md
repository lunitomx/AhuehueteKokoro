# Parrilla Pre-Review Protocol — 4 Capas

> Knowledge file para S46.1. Antes de crear una parrilla de contenido,
> se revisan 4 capas. Si falta una, la parrilla sale genérica.

## Principio

Una parrilla que nace de "buenas ideas" produce contenido que cualquier
competidor podría firmar. Una parrilla que nace de data, visuales reales,
estrategia y feedback produce contenido que solo este negocio puede crear.

## Las 4 Capas

### Capa 1 — Performance Data

**Qué revisar:** Datos reales de campañas previas (Meta Ads, Google Ads,
analítica web). No opiniones — números.

| Pregunta | Fuente |
|----------|--------|
| ¿Qué piezas gastaron presupuesto? | Meta Ads → Campaign Performance |
| ¿Cuáles generaron resultados (leads, conversiones, engagement)? | Meta Ads → Results by Ad |
| ¿Cuáles gastaron sin resultado? | Meta Ads → Cost per Result |
| ¿Qué términos de búsqueda trajeron tráfico? | Google Ads → Search Terms |
| ¿Qué páginas convierten? | GA4 → Conversion Paths |

**Output:** Lista de ganadores y perdedores con evidencia numérica.

### Capa 2 — Visual Artifacts

**Qué revisar:** Las piezas reales que se pautaron. No basta leer el copy —
hay que ver imagen/video, primer segundo, jerarquía, y claridad.

| Pregunta | Cómo verificarlo |
|----------|------------------|
| ¿El primer segundo justifica detenerse? | Ver el video sin sonido, 0-3 segundos |
| ¿Se entiende qué se ofrece en 2 segundos? | Mostrar a alguien que no conoce la marca |
| ¿El precio o llamado a la acción es visible? | Revisar overlay text, caption, CTA button |
| ¿La imagen es real o stock genérica? | Identificar si es foto del negocio o banco de imágenes |

**Output:** Lista de piezas visuales con diagnóstico de claridad, jerarquía
y autenticidad.

### Capa 3 — Business Strategy

**Qué revisar:** Buyer personas, propuesta de valor, pricing, funnel,
objeciones comunes, y prioridades del dueño del negocio.

| Pregunta | Fuente |
|----------|--------|
| ¿A quién le hablamos? | Buyer personas (Fase A de la parrilla) |
| ¿Qué problema resolvemos? | Propuesta de valor + diferenciadores |
| ¿Cuánto cuesta y por qué? | Pricing actual + objeción de precio |
| ¿Qué objeciones frenan la decisión? | Feedback de ventas + preguntas frecuentes |
| ¿Qué quiere el dueño que se comunique? | Prioridades explícitas del negocio |

**Output:** Brief estratégico de 1 página con buyer persona, propuesta,
objeciones y prioridades.

### Capa 4 — Owner/CMO Feedback

**Qué revisar:** Correcciones, preferencias y reglas explícitas de quien
toma las decisiones finales. El feedback del dueño no es sugerencia —
es regla creativa.

| Pregunta | Cómo obtenerlo |
|----------|----------------|
| ¿Qué piezas previas rechazó y por qué? | Historial de feedback |
| ¿Qué palabras o conceptos prohibió? | Lista de "nunca digas" del cliente |
| ¿Qué tono quiere (y cuál no)? | Brief de voz de marca |
| ¿Qué considera "genérico" vs "de nosotros"? | Ejemplos concretos que él mismo dio |

**Output:** Lista de reglas no-negociables + ejemplos de lo que SÍ quiere.

## Gate

Antes de pasar a crear contenido, las 4 capas deben tener respuesta.
Si una capa está vacía, la parrilla tendrá un punto ciego.

| Capa | ¿Lista? | Acción si falta |
|------|:-------:|-----------------|
| Performance data | □ | Ejecutar `/kokoro-analytics` o `/kokoro-google-ads-run` |
| Visual artifacts | □ | Revisar el feed de Meta Ads o pedir acceso |
| Business strategy | □ | Ejecutar `/kokoro-onboard` o leer buyer personas |
| Owner feedback | □ | Preguntar al dueño: "¿qué nunca quieres ver en tu contenido?" |

## Output Template

```markdown
## Pre-Review — {Nombre del proyecto}

### Capa 1: Performance
- Ganadores: {lista con números}
- Perdedores: {lista con números}
- Patrón detectado: {qué tienen en común los ganadores}

### Capa 2: Visuales
- Piezas claras: {lista}
- Piezas confusas: {lista}
- Diagnóstico: {qué hace que una pieza sea clara para este negocio}

### Capa 3: Estrategia
- Buyer persona principal: {nombre + necesidad}
- Propuesta de valor: {1 frase}
- Objeción #1: {la más frecuente}
- Prioridad del dueño: {qué quiere comunicar hoy}

### Capa 4: Feedback
- Reglas no-negociables: {lista}
- Lo que SÍ quiere ver: {ejemplos}
```

Si las 4 capas tienen contenido sustancial — no frases de relleno — la
parrilla que salga será específica de este negocio, no un template.
