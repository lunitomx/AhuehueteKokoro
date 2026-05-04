# /kokoro-render — Ensamblar Video Final

> Herramienta transversal: ensamblaje profesional de video
> Aplica en cualquier fase del proceso Kokoro

> "El toque final que transforma momentos en memorias."

## Contexto

Este skill toma un video (tipicamente el output de `/kokoro-overlay` con captions)
y produce un video final con intro/outro de branding y audio normalizado.
El pipeline completo: video captioned → loudnorm → concat intro/main/outro → export.

### Dependencias

- **ffmpeg**: Instalado via brew (`brew install ffmpeg`)
- **Video input**: Producido por `/kokoro-overlay` o cualquier video MP4
- **Templates**: Intro/outro en MP4 (opcionales — el skill funciona sin ellos)

### Costo

Sin costo adicional — procesamiento local con ffmpeg.

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio previamente con
`/kokoro-open`, buscar templates en la carpeta del invitado primero.

## Instrucciones para la sesion

### Argumento requerido

El usuario debe proporcionar la ruta al video:

```
/kokoro-render {ruta_al_video}
```

Argumentos opcionales via mensaje:
- `--intro path/to/intro.mp4` — ruta explicita al intro
- `--outro path/to/outro.mp4` — ruta explicita al outro
- `--no-intro` — omitir intro
- `--no-outro` — omitir outro

Si no se proporciona ruta, preguntar:

> "Para ensamblar el video final necesito la ruta del video.
> Normalmente es el output de `/kokoro-overlay` (con captions).
> ¿Cual es la ruta?"

### Proceso — 5 pasos

#### Paso 1: Validar inputs

1. Verificar que ffmpeg esta instalado: `which ffmpeg`
2. Verificar que el video existe y es un archivo valido
3. Obtener duracion y codec info con ffprobe:
   ```bash
   ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height \
     -of json "{input}"
   ```

Mostrar resumen:

> "Video: {filename} — {duration}s ({width}x{height})
> Codec: {video_codec} + {audio_codec}
> Buscando templates..."

#### Paso 2: Descubrir templates

Buscar intro/outro en orden de prioridad (explicito gana sobre convencion):

1. Si el usuario paso `--intro` / `--outro`, usar esas rutas (override explicito)
2. Si hay invitado resuelto: `clientes/{grupo}/assets/intro.mp4` / `outro.mp4`
3. Default del proyecto: `assets/templates/intro.mp4` / `outro.mp4`

Si `--no-intro` o `--no-outro`, saltar la busqueda para ese segmento.

Mostrar resultado:

> "Intro: {path} ({duration}s) | No encontrado — se omite
> Outro: {path} ({duration}s) | No encontrado — se omite"

Si no hay intro ni outro, el skill solo normaliza audio y exporta.

#### Paso 3: Normalizar audio (loudnorm two-pass)

**Pass 1 — Medir:**

```bash
ffmpeg -i "{input}" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null - 2>&1
```

Parsear la salida JSON para extraer: `measured_I`, `measured_TP`, `measured_LRA`,
`measured_thresh`, `offset`.

Mostrar medicion:

> "Audio medido: {measured_I} LUFS (target: -16 LUFS)
> Ajuste necesario: {offset} dB"

**Pass 2 — Aplicar:**

```bash
ffmpeg -y -i "{input}" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={mI}:measured_TP={mTP}:measured_LRA={mLRA}:measured_thresh={mThresh}:offset={offset}:linear=true" \
  -c:v copy -c:a aac -b:a 128k \
  "{normalized_output}"
```

Nota: `-c:v copy` evita re-encodear video durante normalizacion.
El re-encode de video ocurre solo una vez, en el paso de concat.

Si no hay templates (normalization-only mode), pass 2 produce el output final
directamente como `{basename}-final.mp4`.

#### Paso 4: Concatenar con ffmpeg concat filter

Si hay intro y/o outro, concatenar usando el concat filter:

**Full (intro + main + outro):**
```bash
ffmpeg -y -i "{intro}" -i "{normalized_main}" -i "{outro}" \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

**Parcial (main + outro, sin intro):**
```bash
ffmpeg -y -i "{normalized_main}" -i "{outro}" \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

**Parcial (intro + main, sin outro):**
```bash
ffmpeg -y -i "{intro}" -i "{normalized_main}" \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

El parametro `n=` se ajusta dinamicamente segun cuantos segmentos hay.

Mostrar el comando antes de ejecutar. Pedir confirmacion.

#### Paso 5: Presentar resultados y guardar JSON

##### Formato de presentacion

```
## Video final ensamblado — {filename}

Entrada: {input_path}
Salida: {output_path}
Duracion: {duration}s ({intro_duration}s intro + {main_duration}s main + {outro_duration}s outro)
Audio: normalizado a -16 LUFS (two-pass loudnorm)
Formato: MP4 H.264 + AAC 128k

| Segmento | Archivo | Duracion |
|----------|---------|----------|
| Intro | {intro_path} | {duration}s |
| Main | {main_path} | {duration}s |
| Outro | {outro_path} | {duration}s |

---

### Siguiente paso

1. Revisa el video final — verifica cortes, audio, y branding
2. `/kokoro-creative` para generar thumbnail
3. Publica cuando este listo
4. Si necesitas ajustar templates de intro/outro, reemplaza los archivos y re-ejecuta
```

##### JSON resumen

Guardar como `{basename}-final.json`:

```json
{
  "source_video": "{input_path}",
  "output_video": "{output_path}",
  "intro": "{intro_path_or_null}",
  "outro": "{outro_path_or_null}",
  "audio_normalization": {
    "target_lufs": -16,
    "method": "loudnorm_two_pass",
    "measured_I": -18.3,
    "measured_TP": -2.1
  },
  "duration_seconds": 48.5,
  "segments": ["intro", "main", "outro"],
  "codec": {"video": "H.264", "audio": "AAC 128k"}
}
```

## Notas para Claude

- Usa la voz de Eduardo: el video final es "el toque que transforma momentos en memorias"
- Vocabulario Kokoro: invitado (no cliente), creacion (no producto)
- Siempre mostrar el comando ffmpeg ANTES de ejecutar
- Pedir confirmacion antes de cada comando ffmpeg
- Si ffmpeg falla, mostrar stderr completo y sugerir verificar formato de templates
- IMPORTANTE: Si no hay templates, el skill FUNCIONA — solo normaliza audio y exporta
- IMPORTANTE: Guardar JSON resumen automaticamente
- IMPORTANTE: loudnorm pass 2 usa `-c:v copy` para no re-encodear video
- Responde en el idioma del usuario
- Pipeline completo: `/kokoro-listen` → `/kokoro-cuts` → `/kokoro-shorts` → `/kokoro-overlay` → `/kokoro-render`
