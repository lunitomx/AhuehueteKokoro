# ffmpeg Reference — /kokoro-shorts

> Skill: `/kokoro-shorts`
> Herramienta transversal: aplica en cualquier fase

> "El corte preciso revela lo que siempre estuvo ahi."

## Proposito

Referencia tecnica de comandos ffmpeg para el skill `/kokoro-shorts`.
Documenta la estrategia de two-pass, configuracion de codecs, fades,
reformateo vertical, y manejo de errores comunes.

## Descarga con yt-dlp

Descargar video y audio del video fuente:

```bash
# Video en mp4
mkdir -p /tmp/kokoro-shorts
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "/tmp/kokoro-shorts/%(id)s.%(ext)s" \
  "{video_url}"

# Audio en mp3 para Whisper
yt-dlp -x --audio-format mp3 \
  -o "/tmp/kokoro-shorts/%(id)s.%(ext)s" \
  "{video_url}"
```

## Transcripcion con Whisper verbose_json

Codigo Python para obtener timestamps por segmento:

```python
import json, uuid, os
from urllib.request import Request, urlopen
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def transcribe_with_timestamps(file_path, language="es"):
    boundary = uuid.uuid4().hex
    with open(file_path, 'rb') as f:
        audio_data = f.read()

    lines = []
    for key, value in {"model": "whisper-1", "language": language, "response_format": "verbose_json"}.items():
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
        return json.loads(resp.read().decode())
```

## Fuzzy Matching de Cortes a Timestamps

Codigo Python para emparejar oraciones de cortes con segmentos de Whisper:

```python
from difflib import SequenceMatcher

def find_timestamp(sentence, segments):
    best_ratio = 0
    best_segment = None
    for seg in segments:
        ratio = SequenceMatcher(None, sentence.lower(), seg["text"].lower().strip()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_segment = seg
    return best_segment, best_ratio
```

Umbral minimo de confianza: 0.5. Por debajo, advertir y saltar el corte.

## Estrategia Two-Pass

Se usan dos pasadas para optimizar velocidad y calidad:

### Pass 1 — Stream Copy (rapido, lossless)

Copia el segmento sin re-encodear. Es casi instantaneo porque no procesa
frames — solo corta en los keyframes mas cercanos.

```bash
ffmpeg -y -ss {start} -to {end} -i "{input_video}" \
  -c copy "{output_dir}/{basename}-short-{NN}-raw.mp4"
```

**Flags:**
- `-y` — Sobreescribir sin preguntar
- `-ss {start}` — Seek al tiempo de inicio (segundos, float)
- `-to {end}` — Cortar hasta este tiempo (absoluto, no relativo)
- `-c copy` — Copiar streams sin re-encodear
- El orden `-ss` antes de `-i` es importante: hace input seeking (rapido)

**Nota:** El corte por stream copy no es frame-exact. Puede incluir hasta
0.5s extra al inicio/final. Pass 2 corrige esto con el re-encode.

### Pass 2 — Re-encode con Fades (calidad)

Re-encoda solo el segmento corto (segundos, no minutos), agregando fades
de audio y video para transiciones profesionales.

```bash
ffmpeg -y -i "{raw_file}" \
  -vf "fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5" \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st={duration-0.5}:d=0.5" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output_dir}/{basename}-short-{NN}.mp4"
```

**Flags de video:**
- `-vf "fade=..."` — Filtro de fade visual
  - `t=in` / `t=out` — Tipo de fade
  - `st=0` — Start time del fade (0 = inicio del clip)
  - `d=0.5` — Duracion del fade en segundos
- `-c:v libx264` — Codec de video H.264 (maxima compatibilidad)
- `-preset fast` — Balance velocidad/compresion (opciones: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
- `-crf 23` — Constant Rate Factor (0=lossless, 23=default, 28=baja calidad)

**Flags de audio:**
- `-af "afade=..."` — Filtro de fade de audio (misma sintaxis que video)
- `-c:a aac` — Codec de audio AAC
- `-b:a 128k` — Bitrate de audio 128 kbps

### Por que Two-Pass

1. **Velocidad:** Pass 1 es casi instantaneo (stream copy)
2. **Precision:** Pass 2 solo procesa segundos de video, no el archivo completo
3. **Calidad:** Los fades requieren re-encode, pero solo del segmento corto
4. **Economia:** Re-encodear 45s es muy diferente a re-encodear 30 minutos

## Reformateo Vertical (9:16)

Para plataformas como YouTube Shorts, Instagram Reels, TikTok:

```bash
ffmpeg -y -i "{input}" \
  -vf "crop=ih*9/16:ih,scale=1080:1920,fade=t=in:st=0:d=0.5,fade=t=out:st={duration-0.5}:d=0.5" \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st={duration-0.5}:d=0.5" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

**Filtros de video encadenados:**
1. `crop=ih*9/16:ih` — Recorta el centro del frame a aspect ratio 9:16
   - `ih*9/16` = ancho (proporcion del alto)
   - `ih` = alto (mantiene el alto original)
   - El crop es centrado por defecto
2. `scale=1080:1920` — Escala a resolucion estandar vertical
3. `fade=...` — Fades como en pass 2

**Nota:** Si el video fuente ya es vertical (9:16), saltar el crop/scale.
Detectar con:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 "{input}"
```

Si `width < height`, el video ya es vertical.

## Configuracion de Codecs

### Video: H.264 (libx264)

| Parametro | Valor | Razon |
|-----------|-------|-------|
| Codec | libx264 | Compatibilidad universal |
| Preset | fast | Buen balance velocidad/calidad para clips cortos |
| CRF | 23 | Calidad visual buena, archivo compacto |

**Cuando ajustar CRF:**
- CRF 18-20: Si el invitado necesita calidad alta (presentaciones, luxury)
- CRF 23: Default para redes sociales
- CRF 28: Si el archivo debe ser muy compacto

### Audio: AAC

| Parametro | Valor | Razon |
|-----------|-------|-------|
| Codec | aac | Compatible con todos los players |
| Bitrate | 128k | Suficiente para voz hablada |

**Cuando ajustar bitrate:**
- 96k: Solo voz, sin musica
- 128k: Default (voz + ambiente)
- 192k: Si hay musica importante en el clip

## Fades

Los fades de 0.5s son el default para transiciones suaves:

### Fade de video

```
fade=t=in:st=0:d=0.5       — Fade in al inicio
fade=t=out:st={D-0.5}:d=0.5 — Fade out al final
```

Donde `{D-0.5}` es la duracion del clip menos 0.5 segundos.

### Fade de audio

```
afade=t=in:st=0:d=0.5       — Fade in al inicio
afade=t=out:st={D-0.5}:d=0.5 — Fade out al final
```

**Calcular duracion del clip:**

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "{file}"
```

## Errores Comunes y Soluciones

### 1. "codec not currently supported in container"

**Causa:** El video fuente usa un codec que no es compatible con el contenedor mp4.

**Solucion:** Forzar re-encode en pass 1 en lugar de stream copy:

```bash
ffmpeg -y -ss {start} -to {end} -i "{input}" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

### 2. "Non-monotonous DTS" o timestamps desordenados

**Causa:** Stream copy corta en keyframes imprecisos.

**Solucion:** Agregar `-avoid_negative_ts make_zero` despues de `-c copy`:

```bash
ffmpeg -y -ss {start} -to {end} -i "{input}" \
  -c copy -avoid_negative_ts make_zero "{output}"
```

### 3. Video sin audio o audio sin video

**Causa:** El archivo fuente tiene streams separados que no se unieron bien.

**Solucion:** Verificar streams disponibles:

```bash
ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "{input}"
```

Si falta audio, generar silencio:

```bash
ffmpeg -y -i "{input}" \
  -f lavfi -i anullsrc=r=44100:cl=stereo \
  -c:v copy -c:a aac -b:a 128k \
  -shortest "{output}"
```

### 4. Archivo corrupto o truncado

**Causa:** Descarga incompleta o archivo danado.

**Solucion:** Verificar integridad:

```bash
ffmpeg -v error -i "{input}" -f null - 2>&1 | head -20
```

Si hay errores, re-descargar con yt-dlp.

### 5. Fade out time negativo

**Causa:** El clip es mas corto que 1 segundo (0.5s fade in + 0.5s fade out).

**Solucion:** Si la duracion < 1s, reducir fades a 0.25s o eliminarlos:

```bash
# Para clips muy cortos (< 1s)
ffmpeg -y -i "{input}" \
  -vf "fade=t=in:st=0:d=0.25,fade=t=out:st={D-0.25}:d=0.25" \
  -af "afade=t=in:st=0:d=0.25,afade=t=out:st={D-0.25}:d=0.25" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

## Flujo con Otros Skills

```
/kokoro-listen  → descarga video + transcripcion
/kokoro-cuts    → identifica cortes (JSON con start/end sentences)
/kokoro-shorts  → extrae segmentos con timestamps precisos ← ESTE SKILL
/kokoro-overlay → agrega captions sincronizados
/kokoro-creative → genera thumbnails
```
