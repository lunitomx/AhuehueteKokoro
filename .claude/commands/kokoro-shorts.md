# /kokoro-shorts — Extraer Shorts de Video

> Herramienta transversal: extraccion automatizada de segmentos de video
> Aplica en cualquier fase del proceso Kokoro

> "Los momentos que brillan merecen su propio escenario."

## Contexto

Este skill toma los cortes identificados por `/kokoro-cuts` y los extrae del
video fuente como archivos individuales listos para publicar. Usa Whisper para
obtener timestamps precisos y ffmpeg para cortar con fades profesionales.

### Dependencias

- **yt-dlp**: Instalado via brew/pip (`brew install yt-dlp`)
- **ffmpeg**: Instalado via brew (`brew install ffmpeg`)
- **OPENAI_API_KEY**: En `.env` del proyecto (Whisper API para timestamps)
- **Cuts JSON**: Generado por `/kokoro-cuts`

### Costo

Whisper API (verbose_json): $0.006 USD por minuto de audio.
Un video de 15 min = ~$0.09 USD. Mostrar costo estimado antes de procesar.

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio previamente con
`/kokoro-open`, guardar los shorts en la carpeta del invitado.

Si no hay invitado, guardar en `/tmp/kokoro-shorts/`.

## Instrucciones para la sesion

### Argumento requerido

El usuario debe proporcionar la ruta al archivo JSON de cortes:

`/kokoro-shorts {ruta_al_archivo_cuts_json}`

Si no se proporciona, preguntar:

> "Necesito el archivo de cortes para extraer los momentos que brillan.
> ¿Cual es la ruta del JSON? Si aun no tienes cortes identificados,
> `/kokoro-cuts` te ayuda a encontrarlos."

### Proceso — 6 pasos

1. LEER y validar el JSON de cortes
2. LOCALIZAR el video fuente
3. RE-TRANSCRIBIR con Whisper verbose_json para timestamps
4. FUZZY-MATCH cortes a timestamps
5. EXTRAER con ffmpeg (two-pass)
6. PRESENTAR resultados y guardar JSON resumen

### Paso 1: Leer y validar JSON de cortes

Leer el archivo JSON proporcionado. Validar que tiene los campos requeridos:
`source_transcript`, `video_url`, y `cuts` (array con `start_sentence` y
`end_sentence` por corte).

Mostrar resumen:

> "Video: {video_title} — {cuts_count} cortes para extraer.
> Costo estimado de re-transcripcion: ~${costo} USD."

Si falta `video_url`, preguntar al usuario.
Si `cuts` esta vacio, informar y sugerir `/kokoro-cuts` primero.

### Paso 2: Localizar video fuente

1. Extraer video ID de la URL (para YouTube: el parametro `v=` o la ruta)
2. Buscar en `/tmp/kokoro-listen/` archivos que contengan el video ID
3. Si existe, usar el archivo local
4. Si no existe, descargar con yt-dlp (video mp4 + audio mp3)
5. Guardar en `/tmp/kokoro-shorts/`

Ver `kokoro-shorts-ffmpeg.md` para comandos de descarga.

### Paso 3: Re-transcribir con Whisper verbose_json

La transcripcion original de `/kokoro-listen` no tiene timestamps por segmento.
Re-transcribir con `response_format=verbose_json` para obtener segmentos con
`start` y `end` en segundos.

Ver `kokoro-shorts-ffmpeg.md` para el codigo Python de transcripcion y el
codigo de fuzzy matching.

La respuesta tiene un array `segments`, cada uno con:
- `id` — indice del segmento
- `start` — tiempo de inicio en segundos (float)
- `end` — tiempo de fin en segundos (float)
- `text` — texto del segmento

Guardar la respuesta como `{basename}-whisper.json` para referencia.

### Paso 4: Fuzzy-match cortes a timestamps

Usar `difflib.SequenceMatcher` para encontrar el mejor match entre las
oraciones del corte y los segmentos de Whisper.

Para cada corte:
1. Buscar `start_sentence` — usar el `start` del segmento coincidente
2. Buscar `end_sentence` — usar el `end` del segmento coincidente
3. Si el ratio < 0.5, advertir y saltar ese corte
4. Agregar 0.5s de padding antes del inicio y despues del final

Pedir confirmacion al usuario antes de proceder con la extraccion.

### Paso 5: Extraer con ffmpeg (two-pass)

Ver knowledge file `kokoro-shorts-ffmpeg.md` para referencia completa de
comandos ffmpeg, estrategia two-pass, y manejo de errores.

Para cada corte con match exitoso:
- Pass 1: Stream copy (rapido, lossless) para aislar el segmento
- Pass 2: Re-encode con fades de 0.5s (video + audio)
- Opcional: Reformat vertical 9:16 si el usuario lo pide
- Limpiar archivos raw despues de re-encode exitoso

### Paso 6: Presentar resultados y guardar JSON

#### Formato de presentacion (human-readable)

```
## Shorts extraidos — {video_title}

Fuente: {video_url}
Cortes procesados: {total} | Exitosos: {success} | Omitidos: {skipped}
Costo Whisper: ~${costo} USD

| # | Titulo | Duracion | Inicio | Fin | Confianza | Archivo |
|---|--------|----------|--------|-----|-----------|---------|
| 1 | {title} | {duration}s | {start}s | {end}s | {ratio} | `{path}` |
| 2 | {title} | {duration}s | {start}s | {end}s | {ratio} | `{path}` |
| 3 | {title} | {duration}s | {start}s | {end}s | {ratio} | `{path}` |

---

### Detalle por short

**Short 1 — {title}**
- Archivo: `{path}`
- Duracion: {duration}s ({start}s a {end}s)
- Match confianza: {ratio}
- Formato: horizontal | Para vertical: solicitar reformat 9:16

**Short 2 — {title}**
- Archivo: `{path}`
- Duracion: {duration}s ({start}s a {end}s)
- Match confianza: {ratio}
- Formato: horizontal | Para vertical: solicitar reformat 9:16

---

### Resumen JSON

Guardado en: `{json_path}`

---

### Siguiente paso

1. `/kokoro-overlay` para agregar captions + formato vertical 9:16 al short
2. `/kokoro-creative` para generar thumbnails
3. Publica directamente si el short se ve bien sin captions
```

#### Formato JSON (guardar como archivo)

Guardar como `{output_dir}/{basename}-shorts.json` con la estructura:
- `source_video` — ruta al video fuente
- `source_cuts` — ruta al JSON de cortes
- `shorts_count` — cantidad de shorts generados
- `shorts` — array con rank, title, file, duration_seconds, start_time,
  end_time, y status por cada short

**Ruta de guardado:**

Si hay invitado resuelto: `clientes/{grupo}/shorts/{basename}-shorts.json`

Si no hay invitado: `/tmp/kokoro-shorts/{basename}-shorts.json`

## Session Log

Despues de presentar los shorts, persistir el resultado:

1. Guardar el JSON automaticamente (no esperar a que el usuario lo pida)
2. Mostrar la ruta de cada archivo generado
3. Si hay session activa (`/kokoro-open`), registrar en el log de sesion

## Notas para Claude

- Usa la voz de Eduardo: los shorts son "momentos que brillan", no "clips"
- Vocabulario Kokoro: invitado (no cliente), creacion (no producto)
- Siempre mostrar costo estimado de Whisper ANTES de ejecutar
- Pedir confirmacion despues del fuzzy-match, ANTES de extraer
- Si ffmpeg falla, consultar `kokoro-shorts-ffmpeg.md` para troubleshooting
- Limpiar archivos raw despues de cada extraccion exitosa
- El two-pass es intencional: pass 1 es rapido para aislar el segmento,
  pass 2 solo re-encoda el segmento corto (segundos, no el video completo)
- IMPORTANTE: Siempre guardar el JSON resumen — es el registro del trabajo
- IMPORTANTE: Los fades (0.5s in/out) son para transiciones suaves, no opcionales
- Responde en el idioma del usuario
- Complemento natural de `/kokoro-cuts` — cuts identifica, shorts extrae
