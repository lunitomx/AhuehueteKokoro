# /kokoro-overlay — Agregar Captions a Shorts

> Herramienta transversal: captions sincronizados sobre video
> Aplica en cualquier fase del proceso Kokoro

> "Las palabras que acompanan la imagen multiplican su impacto."

## Contexto

Este skill toma un short (de `/kokoro-shorts`) y un transcript (Whisper verbose_json)
y produce un video vertical 9:16 con captions sincronizados usando ffmpeg drawtext.

80%+ de usuarios ven video en redes sociales sin audio. Los captions no son
opcionales — son la diferencia entre contenido que se ve y contenido que se salta.

### Dependencias

- **ffmpeg**: Instalado via brew (`brew install ffmpeg`)
- **Short video**: Producido por `/kokoro-shorts`
- **Whisper JSON**: Producido por `/kokoro-listen` o `/kokoro-shorts` (verbose_json format)

### Costo

Sin costo adicional — no usa APIs. Solo procesamiento local con ffmpeg.

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio previamente con
`/kokoro-open`, guardar los outputs en la carpeta del invitado.

Si no hay invitado, guardar junto al archivo de entrada.

## Instrucciones para la sesion

### Argumentos requeridos

El usuario debe proporcionar:
1. Ruta al video short (o al JSON de shorts de /kokoro-shorts)
2. Ruta al Whisper verbose_json

```
/kokoro-overlay {ruta_video_o_shorts_json} {ruta_whisper_json}
```

Si faltan argumentos, preguntar:

> "Para agregar captions necesito dos cosas:
> 1. El video short (o el JSON de shorts de `/kokoro-shorts`)
> 2. El transcript Whisper (verbose_json)
>
> ¿Cuales son las rutas?"

### Modo Single vs Batch

- **Single**: Un video + whisper JSON → un video con captions
- **Batch**: Un shorts JSON (de /kokoro-shorts) + whisper JSON → todos los shorts con captions

El skill detecta automaticamente: si el primer argumento termina en `-shorts.json`, es batch mode.

### Proceso — 6 pasos

#### Paso 1: Validar inputs

1. Verificar que ffmpeg esta instalado: `which ffmpeg`
2. Verificar que el video o shorts JSON existe
3. Verificar que el Whisper JSON existe y tiene campo `segments`
4. Si es batch mode, leer el shorts JSON y listar los shorts disponibles

Mostrar resumen:

> "Video: {filename} — {duration}s
> Transcript: {segments_count} segmentos
> Modo: single | batch ({shorts_count} shorts)
> Formato de salida: vertical 9:16 (default)"

#### Paso 2: Extraer segmentos del transcript

Para single mode:
1. Leer el Whisper JSON completo
2. Obtener la duracion del video con ffprobe
3. Filtrar segmentos que caigan dentro de la duracion del video
4. Ajustar timestamps si es necesario (si el short tiene offset del video original)

Para batch mode:
1. Leer el shorts JSON para obtener `start_time` y `end_time` de cada short
2. Filtrar segmentos del Whisper JSON para cada rango de tiempo
3. Ajustar timestamps para que sean relativos al inicio del short (restar start_time)

#### Paso 3: Escapar texto para drawtext

Aplicar escaping de caracteres especiales de ffmpeg drawtext:

```python
def escape_drawtext(text):
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "'\\''")
    text = text.replace(":", "\\:")
    text = text.replace("%", "%%")
    return text
```

Caracteres que se escapan: `\`, `'`, `:`, `%`

#### Paso 4: Wrap de lineas largas

Si un segmento excede ~35 caracteres, dividir en 2 lineas en el limite
de palabra mas cercano:

```python
def wrap_text(text, max_chars=35):
    if len(text) <= max_chars:
        return text
    # Buscar el espacio mas cercano al punto medio
    mid = len(text) // 2
    # Buscar espacio hacia atras desde el medio
    space = text.rfind(' ', 0, mid + 5)
    if space == -1:
        space = text.find(' ', mid)
    if space == -1:
        return text  # No hay espacios, dejarlo como esta
    return text[:space] + '\\n' + text[space+1:]
```

#### Paso 5: Construir y ejecutar ffmpeg

Construir el comando ffmpeg con la cadena de filtros:

```bash
ffmpeg -y -i "{input_video}" \
  -vf "crop=ih*9/16:ih,scale=1080:1920,\
drawtext=text='{escaped_text_1}':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.80:enable='between(t,{start1},{end1})',\
drawtext=text='{escaped_text_2}':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.80:enable='between(t,{start2},{end2})'" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output_video}"
```

**Estilo de captions:**
- `fontsize=48` — legible en movil
- `fontcolor=white` — alto contraste
- `borderw=3` + `bordercolor=black` — legible contra cualquier fondo
- `x=(w-text_w)/2` — centrado horizontal
- `y=h*0.80` — tercio inferior (80% desde arriba)
- `enable='between(t,start,end)'` — timing sincronizado

**Vertical reformat (default):**
- `crop=ih*9/16:ih` — recorta centro a 9:16
- `scale=1080:1920` — resolucion estandar vertical

Si el usuario pide "keep original" o "sin reformat", omitir crop+scale.

Si el video ya es vertical (width < height), omitir crop+scale. Detectar con:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "{input}"
```

Mostrar el comando antes de ejecutar. Pedir confirmacion.

Ejecutar y mostrar progreso.

#### Paso 6: Presentar resultados y guardar JSON

##### Formato de presentacion

```
## Captions aplicados — {filename}

Entrada: {input_path}
Salida: {output_path}
Formato: vertical 9:16 (1080x1920)
Captions: {count} segmentos sincronizados
Duracion: {duration}s

| # | Texto | Inicio | Fin |
|---|-------|--------|-----|
| 1 | {text} | {start}s | {end}s |
| 2 | {text} | {start}s | {end}s |

---

### Siguiente paso

1. Revisa el video para verificar sincronizacion y legibilidad
2. `/kokoro-creative` para generar thumbnail
3. Publica directamente si se ve bien
4. `/kokoro-render` para agregar intro/outro (cuando este disponible)
```

##### JSON resumen

Guardar como `{basename}-captioned.json`:

```json
{
  "source_video": "{input_path}",
  "output_video": "{output_path}",
  "whisper_json": "{whisper_path}",
  "format": "vertical_9_16",
  "resolution": "1080x1920",
  "captions_count": 4,
  "duration_seconds": 14.0,
  "style": {
    "font_size": 48,
    "font_color": "white",
    "border_width": 3,
    "border_color": "black",
    "position": "lower_80pct"
  },
  "captions": [
    {"text": "...", "start": 0.0, "end": 3.2},
    {"text": "...", "start": 3.2, "end": 6.8}
  ]
}
```

## Notas para Claude

- Usa la voz de Eduardo: los captions "acompanan la imagen", no son "subtitulos"
- Vocabulario Kokoro: invitado (no cliente), creacion (no producto)
- Siempre mostrar el comando ffmpeg ANTES de ejecutar
- Pedir confirmacion antes de ejecutar ffmpeg
- Si ffmpeg falla, consultar `kokoro-overlay-ffmpeg.md` para troubleshooting
- IMPORTANTE: Default es VERTICAL 9:16 — leccion de M1
- IMPORTANTE: Guardar JSON resumen automaticamente
- Responde en el idioma del usuario
- Complemento natural de `/kokoro-shorts` — shorts extrae, overlay agrega captions
