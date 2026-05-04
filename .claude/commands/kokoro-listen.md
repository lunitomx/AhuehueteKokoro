# /kokoro-listen — Descargar y Transcribir Video/Audio

> Herramienta transversal: Transcripcion de contenido multimedia
> Aplica en cualquier fase del proceso Kokoro

> "Para entender un mercado, primero hay que escucharlo."

## Contexto

Este skill descarga audio de cualquier URL (YouTube, Instagram, TikTok) y
lo transcribe usando OpenAI Whisper API. Entrega la transcripcion lista
para analisis con `/kokoro-research`, `/kokoro-intel`, o directamente en
conversacion.

### Dependencias

- **yt-dlp**: Instalado via brew/pip (`brew install yt-dlp`)
- **ffmpeg**: Instalado via brew (`brew install ffmpeg`)
- **OPENAI_API_KEY**: En `.env` del proyecto (Whisper API)

### Costo

Whisper API: $0.006 USD por minuto de audio.
Un video de 15 min = ~$0.09 USD = ~$1.63 MXN.

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio previamente con
`/kokoro-open`, asociar la transcripcion a ese invitado y guardarla
en su carpeta.

Si no hay invitado, guardar en `/tmp/kokoro-listen/`.

## Instrucciones para la sesion

### Antes de comenzar

Si el usuario comparte una URL, procede directamente. No preguntes
permiso — si te dan un link, quieren que lo proceses.

Si el usuario pide analizar contenido sin URL, pregunta:

> "¿Tienes el link del video que quieres analizar?"

### Proceso — 4 pasos

1. DESCARGAR audio de la URL
2. TRANSCRIBIR con Whisper API
3. GUARDAR transcripcion
4. PRESENTAR y ofrecer analisis

### Paso 1: Descargar audio

Usar yt-dlp para extraer solo audio en formato mp3:

```bash
yt-dlp --extract-audio --audio-format mp3 --audio-quality 5 \
  -o "{output_dir}/{video_id}.%(ext)s" \
  --no-playlist \
  "{url}" 2>&1
```

Flags importantes:
- `--extract-audio --audio-format mp3` — solo audio, formato mp3
- `--audio-quality 5` — calidad media (suficiente para Whisper, menor tamano)
- `--no-playlist` — no descargar playlists completas
- Si es una busqueda (`/results?search_query=`), usar `--playlist-items 1-N`
  para descargar los primeros N resultados

Capturar metadata del video:
```bash
yt-dlp --print title --print duration --print webpage_url --no-download "{url}"
```

### Paso 2: Transcribir con Whisper API

**Si el audio es menor a 25MB** (limite de Whisper API): enviar directo.

**Si el audio es mayor a 25MB**: dividir con ffmpeg en segmentos de 20 min:
```bash
ffmpeg -y -i {input} -f segment -segment_time 1200 -acodec libmp3lame -ab 32k {output_dir}/segment_%03d.mp3
```

Llamar a Whisper API para cada segmento:

```python
import json, uuid
from urllib.request import Request, urlopen

api_key = os.getenv("OPENAI_API_KEY")  # from .env

def transcribe_audio(file_path, language="es"):
    boundary = uuid.uuid4().hex

    with open(file_path, 'rb') as f:
        audio_data = f.read()

    # Build multipart form
    lines = []
    for key, value in {"model": "whisper-1", "language": language, "response_format": "text"}.items():
        lines.append(f'--{boundary}'.encode())
        lines.append(f'Content-Disposition: form-data; name="{key}"'.encode())
        lines.append(b'')
        lines.append(value.encode())

    lines.append(f'--{boundary}'.encode())
    lines.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"'.encode())
    lines.append(b'Content-Type: audio/mpeg')
    lines.append(b'')
    lines.append(audio_data)
    lines.append(f'--{boundary}--'.encode())
    lines.append(b'')

    body = b'\r\n'.join(lines)

    req = Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        },
        method="POST"
    )

    with urlopen(req, timeout=300) as resp:
        return resp.read().decode()
```

Concatenar transcripciones de todos los segmentos.

### Paso 3: Guardar transcripcion

**Si hay invitado resuelto:**
```
clientes/{grupo}/transcripciones/{video_id}-{slug}.txt
```

**Si no hay invitado:**
```
/tmp/kokoro-listen/{video_id}-{slug}.txt
```

Formato del archivo:

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

{transcripcion completa}
```

### Paso 4: Presentar y ofrecer analisis

Despues de transcribir, mostrar:

```
## Transcripcion completada

| Campo | Detalle |
|-------|---------|
| Titulo | {titulo} |
| Duracion | {duracion} |
| Palabras | {word_count} |
| Costo | ~${costo} USD (~${costo_mxn} MXN) |
| Archivo | {path} |

### Primeros 500 caracteres
{preview}

### Siguiente paso

1. Puedo analizar el contenido ahora mismo — preguntame lo que quieras
2. `/kokoro-intel` para analizar multiples videos y encontrar patrones
3. `/kokoro-research` para triangular con otras fuentes
```

## Modo batch — Multiples URLs

Si el usuario da multiples URLs o un search query, procesar secuencialmente:

1. Descargar todos los audios primero
2. Transcribir uno por uno (respetar rate limits)
3. Guardar todas las transcripciones
4. Presentar resumen consolidado

Para busquedas de YouTube:
```bash
yt-dlp --extract-audio --audio-format mp3 --audio-quality 5 \
  --playlist-items 1-{N} \
  -o "{output_dir}/%(playlist_index)s-%(id)s.%(ext)s" \
  "ytsearch{N}:{query}" 2>&1
```

Donde `{N}` es el numero de resultados (default 5, max 10).

## Idioma

Whisper detecta automaticamente el idioma, pero para mejorar precision:
- Si el usuario menciona que es en espanol: `language="es"`
- Si es en ingles: `language="en"`
- Si no se sabe: omitir el parametro (auto-detect)

## Manejo de Errores

### URL no soportada
"yt-dlp no pudo descargar de esta URL. Soporta YouTube, Instagram,
TikTok, Twitter/X, Facebook, y cientos mas. ¿Verificas que el link
este completo?"

### Audio muy largo (>3 horas)
"Este video dura mas de 3 horas. Lo divido en segmentos y transcribo
por partes. El costo sera ~${costo} USD. ¿Continuo?"

Pedir confirmacion si el costo estimado supera $1 USD (~$18 MXN).

### API key invalida
"La OPENAI_API_KEY no funciona. Verifica que este correcta en .env."

## Notas para Claude

- Usa la voz de Eduardo: "escuchar el mercado antes de hablar"
- No transcribas sin que el usuario lo pida o de una URL
- Si el video es muy largo, avisar del costo antes de transcribir
- Responde en el idioma del usuario
- IMPORTANTE: Siempre mostrar el costo estimado
- IMPORTANTE: Para videos >25MB, dividir en segmentos
- IMPORTANTE: Guardar la transcripcion siempre — es el asset valioso
- Complemento natural de `/kokoro-intel` — listen descarga, intel analiza
