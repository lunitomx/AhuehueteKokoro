# /kokoro-cuts — Identificar Cortes de Video para Shorts

> Herramienta transversal: analisis de transcripciones para contenido corto
> Aplica en cualquier fase del proceso Kokoro

> "No todo lo que se dice merece un escenario propio — pero los momentos
> que brillan merecen ser encontrados."

## Contexto

Este skill analiza una transcripcion generada por `/kokoro-listen` e identifica
los mejores momentos para convertir en shorts o clips. Usa la inferencia de
Claude para detectar densidad de contenido, potencial de hook, transiciones
tematicas, picos emocionales y valor autonomo de cada segmento.

### Dependencias

- **Transcripcion existente**: Generada por `/kokoro-listen` con formato de
  header (titulo, duracion, URL, fecha)
- No requiere APIs externas — el analisis es puramente inferencial

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio previamente con
`/kokoro-open`, guardar el JSON de cortes en la carpeta del invitado.

Si no hay invitado, guardar en `/tmp/kokoro-cuts/`.

## Instrucciones para la sesion

### Argumento requerido

El usuario debe proporcionar la ruta al archivo de transcripcion:

```
/kokoro-cuts {ruta_al_archivo_de_transcripcion}
```

Si no se proporciona, preguntar:

> "Necesito la transcripcion para encontrar los momentos que brillan.
> ¿Cual es la ruta del archivo? Si aun no tienes transcripcion,
> `/kokoro-listen` te ayuda a crearla."

### Proceso — 5 pasos

1. LEER la transcripcion y parsear metadata del header
2. ANALIZAR el texto completo identificando momentos candidatos
3. PUNTUAR cada momento en 5 dimensiones
4. APLICAR regla de cantidad segun duracion
5. PRESENTAR cortes rankeados y guardar JSON

### Paso 1: Leer y parsear

Leer el archivo de transcripcion. Extraer metadata del header:

```
============================
TRANSCRIPCION
Fuente: {url}
Titulo: {titulo del video}
Duracion: {duracion}
Fecha: {YYYY-MM-DD}
Idioma: {es/en}
Costo: ~${costo} USD
============================
```

Campos a extraer:
- `video_title` del campo Titulo
- `video_duration` del campo Duracion
- `video_url` del campo Fuente
- El texto despues de la linea de cierre `====` es la transcripcion

### Paso 2: Analizar el texto

Leer la transcripcion completa. Identificar momentos candidatos buscando
las 5 senales de corte (ver knowledge file `kokoro-cuts-signals.md`):

1. **Densidad de contenido** — Pasajes donde se concentra una idea completa
   en pocas oraciones, sin divagacion
2. **Potencial de hook** — Frases que funcionan como apertura impactante,
   pregunta provocadora, o afirmacion contracultural
3. **Transicion tematica** — Cambios claros de tema que marcan limites
   naturales de segmento
4. **Pico emocional** — Momentos de intensidad, anecdotas personales,
   humor, o vulnerabilidad
5. **Valor autonomo** — El segmento se entiende solo, sin necesitar
   contexto del resto del video

### Paso 3: Puntuar cada momento

Cada candidato recibe una puntuacion de 1-10 basada en las 5 dimensiones.
La puntuacion final es el promedio ponderado:

- Densidad de contenido: 25%
- Potencial de hook: 25%
- Valor autonomo: 20%
- Pico emocional: 20%
- Transicion tematica: 10%

Solo considerar candidatos con puntuacion >= 6.

### Paso 4: Aplicar regla de cantidad

La cantidad de cortes depende de la duracion del video fuente:

| Duracion del video | Cortes a sugerir |
|--------------------|------------------|
| Menos de 5 min | 1-3 cortes |
| 5 a 30 min | 3-7 cortes |
| Mas de 30 min | 5-10 cortes |

Priorizar calidad sobre cantidad. Si un video de 20 min solo tiene 2
momentos que brillan, sugerir 2 — no llenar por llenar.

### Paso 5: Presentar y guardar

#### Formato de presentacion (human-readable)

```
## Cortes identificados — {video_title}

| # | Score | Titulo sugerido | Duracion est. |
|---|-------|----------------|---------------|
| 1 | 9/10  | {title}        | ~45s          |
| 2 | 8/10  | {title}        | ~60s          |

---

### Corte 1 — {title} (9/10)

**Hook:** "{hook text}"

**Extracto:**
> {quoted text of the segment}

**Por que este corte:** {rationale}

---

### Corte 2 — {title} (8/10)

**Hook:** "{hook text}"

**Extracto:**
> {quoted text of the segment}

**Por que este corte:** {rationale}

---

### Siguiente paso

1. Aprueba los cortes que quieras convertir en shorts
2. `/kokoro-shorts` para extraer los segmentos de video
3. `/kokoro-creative` para generar thumbnails
```

#### Formato JSON (guardar como archivo)

Guardar junto a la transcripcion como `{basename}-cuts.json`:

```json
{
  "source_transcript": "/path/to/transcript.txt",
  "video_title": "...",
  "video_duration": "3:43",
  "video_url": "...",
  "cuts_count": 2,
  "cuts": [
    {
      "rank": 1,
      "score": 9,
      "title": "Suggested short title",
      "hook": "Opening hook text for overlay",
      "excerpt": "Full text of the segment",
      "start_sentence": "First sentence of the cut...",
      "end_sentence": "Last sentence of the cut...",
      "estimated_duration_seconds": 45,
      "rationale": "Why this moment was selected"
    }
  ]
}
```

**Ruta de guardado:**

Si hay invitado resuelto:
```
clientes/{grupo}/transcripciones/{basename}-cuts.json
```

Si no hay invitado:
```
/tmp/kokoro-cuts/{basename}-cuts.json
```

Donde `{basename}` es el nombre del archivo de transcripcion sin extension.

## Session Log

Despues de presentar los cortes, persistir el resultado:

1. Guardar el JSON automaticamente (no esperar a que el usuario lo pida)
2. Mostrar la ruta del archivo guardado
3. Si hay session activa (`/kokoro-open`), registrar en el log de sesion

## Notas para Claude

- Usa la voz de Eduardo: los cortes son "momentos que brillan", no "clips"
- Vocabulario Kokoro: invitado (no cliente), creacion (no producto)
- El hook es la frase de apertura del short — debe funcionar en los primeros
  3 segundos para retener atencion
- Estima la duracion del corte contando palabras (~150 palabras/minuto hablado)
- Si la transcripcion no tiene momentos fuertes (todo score < 6), decirlo
  con honestidad: "Este contenido fluye como conversacion continua — no tiene
  momentos que se sostengan solos como short. Considera grabar contenido
  pensado para formato corto."
- IMPORTANTE: Siempre guardar el JSON — es el insumo para `/kokoro-shorts`
- IMPORTANTE: Los titulos sugeridos deben funcionar como titulo de YouTube Short
  o Instagram Reel — concisos, con gancho, sin clickbait vacio
- Responde en el idioma del usuario
- Complemento natural de `/kokoro-listen` — listen transcribe, cuts analiza
