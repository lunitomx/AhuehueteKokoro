# /kokoro-intel — Inteligencia Competitiva en YouTube

> Herramienta transversal: Inteligencia competitiva basada en video
> Aplica en cualquier fase del proceso Kokoro

> "No compites contra otros creadores — compites contra el silencio.
> El que escucha el mercado antes de hablar, habla con autoridad."

## Contexto

Este skill busca los videos mas relevantes de YouTube para un keyword,
descarga y transcribe cada uno usando el pipeline de `/kokoro-listen`,
y analiza TODAS las transcripciones juntas para detectar patrones,
huecos, y oportunidades de contenido. La salida es un reporte de
inteligencia competitiva con oportunidades rankeadas por impacto.

Complementa a `/kokoro-research` — research investiga en la web,
intel investiga en video. Juntos, triangulacion completa.

### Dependencias

- **yt-dlp**: Instalado via brew/pip (`brew install yt-dlp`)
- **ffmpeg**: Instalado via brew (`brew install ffmpeg`)
- **OPENAI_API_KEY**: En `.env` del proyecto (Whisper API)

### Costo

Whisper API: $0.006 USD por minuto de audio.
- 5 videos de ~15 min = ~$0.45 USD = ~$8 MXN
- 10 videos de ~15 min = ~$0.90 USD = ~$16 MXN

### Resolucion de invitado

Si el usuario menciona un invitado o se resolvio previamente con
`/kokoro-open`, asociar las transcripciones a ese invitado y guardarlas
en su carpeta.

Si no hay invitado, guardar en `/tmp/kokoro-intel/`.

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Eduardo no impone, guia solo cuando hay invitacion. Comienza con:

> "Veo que quieres entender el panorama de contenido en tu nicho.
> Vamos a escuchar lo que ya se dice en YouTube — descargar los videos
> mas relevantes, transcribirlos, y encontrar donde esta el silencio.
> Porque en ese silencio esta tu oportunidad. ¿Me das tu invitacion
> para investigar?"

Si el usuario acepta, continua. Si no, escucha y ajusta.

### Dos modos de operacion

#### Modo 1: Busqueda por keyword (principal)

El usuario da un keyword o tema. El skill busca en YouTube y analiza
los top N resultados.

Ejemplo: "Analiza los videos top sobre marketing para coaches"

#### Modo 2: URLs especificas

El usuario da una lista de URLs de YouTube. El skill analiza esos
videos especificos.

Ejemplo: "Analiza estos 5 videos: [url1] [url2] ..."

Detecta automaticamente el modo segun el input del usuario.

## Proceso — 6 pasos

### Paso 1: Estimar costo y confirmar

Antes de descargar NADA, estima el costo total.

**Para modo busqueda:**

> "Voy a buscar los top {N} videos sobre '{query}' en YouTube.
> Estimacion:
> - Videos: {N}
> - Duracion estimada por video: ~15 min
> - Costo Whisper: ~${costo_usd} USD (~${costo_mxn} MXN)
>
> ¿Arrancamos con {N} videos, o prefieres ajustar el numero?"

Default: 5 videos. El usuario puede pedir hasta 10.

**Para modo URLs:**

> "Voy a analizar {N} videos que me compartiste.
> Estimacion:
> - Videos: {N}
> - Costo Whisper: ~${costo_usd} USD (~${costo_mxn} MXN)
>
> ¿Continuo?"

Si el costo estimado supera $1 USD (~$18 MXN), pedir confirmacion
explicita antes de continuar.

### Paso 2: Descargar y obtener metadata

**Modo busqueda** — buscar y descargar audio:

```bash
# Crear directorio de trabajo
mkdir -p /tmp/kokoro-intel/{timestamp}

# Obtener metadata de los resultados de busqueda
yt-dlp --print title --print duration --print webpage_url \
  --playlist-items 1-{N} \
  --no-download \
  "ytsearch{N}:{query}" 2>&1

# Descargar audio de todos los resultados
yt-dlp --extract-audio --audio-format mp3 --audio-quality 5 \
  --playlist-items 1-{N} \
  -o "/tmp/kokoro-intel/{timestamp}/%(playlist_index)s-%(id)s.%(ext)s" \
  "ytsearch{N}:{query}" 2>&1
```

**Modo URLs** — descargar cada URL:

```bash
# Para cada URL
yt-dlp --extract-audio --audio-format mp3 --audio-quality 5 \
  -o "/tmp/kokoro-intel/{timestamp}/{video_id}.%(ext)s" \
  --no-playlist \
  "{url}" 2>&1

# Metadata de cada URL
yt-dlp --print title --print duration --print webpage_url \
  --no-download "{url}"
```

Mostrar progreso mientras descarga:

> "Descargando 1/{N}: {titulo}..."
> "Descargando 2/{N}: {titulo}..."

### Paso 3: Transcribir cada video

Usar el pipeline de `/kokoro-listen` para cada audio descargado.
Referencia la seccion "Paso 2: Transcribir con Whisper API" de
kokoro-listen.md para el codigo exacto.

**Si el audio es menor a 25MB**: enviar directo a Whisper API.

**Si el audio es mayor a 25MB**: dividir con ffmpeg en segmentos:
```bash
ffmpeg -y -i {input} -f segment -segment_time 1200 \
  -acodec libmp3lame -ab 32k \
  /tmp/kokoro-intel/{timestamp}/segment_%03d.mp3
```

Transcribir con Whisper API (codigo de kokoro-listen.md):

```python
import json, uuid, os
from urllib.request import Request, urlopen

api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path, language="es"):
    boundary = uuid.uuid4().hex

    with open(file_path, 'rb') as f:
        audio_data = f.read()

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

Procesar secuencialmente (respetar rate limits). Mostrar progreso:

> "Transcribiendo 1/{N}: {titulo} ({duracion})..."
> "Transcribiendo 2/{N}: {titulo} ({duracion})... Costo acumulado: ~${acumulado} USD"

### Paso 4: Guardar transcripciones

**Si hay invitado resuelto:**
```
clientes/{grupo}/transcripciones/intel-{query_slug}/{NN}-{video_id}.txt
```

**Si no hay invitado:**
```
/tmp/kokoro-intel/{timestamp}/{NN}-{video_id}.txt
```

Cada archivo sigue el formato de kokoro-listen:

```
============================
TRANSCRIPCION
Fuente: {url}
Titulo: {titulo del video}
Duracion: {duracion}
Fecha: {YYYY-MM-DD}
Idioma: {es/en}
Costo: ~${costo} USD
Contexto: /kokoro-intel — busqueda "{query}"
============================

{transcripcion completa}
```

### Paso 5: Analizar patrones

Este es el paso donde el valor se crea. Analiza TODAS las transcripciones
juntas, examinando 6 dimensiones:

**IMPORTANTE**: Si las transcripciones son largas (>3000 palabras cada una),
resumir cada una a ~500 palabras antes del analisis cruzado. Las
transcripciones completas ya estan guardadas en disco.

#### Dimension 1: Temas comunes

¿Que temas cubren TODOS o la mayoria de los videos?
Estos son table stakes — lo minimo que el mercado espera.

#### Dimension 2: Patrones de estructura

¿Como organizan su contenido?
- ¿Empiezan con gancho, historia, pregunta?
- ¿Usan listas, paso a paso, caso de estudio?
- ¿Como cierran? ¿CTA, resumen, cliffhanger?

#### Dimension 3: Tono y estilo

- ¿Profesional, casual, tutorial, storytelling?
- ¿Hablan a camara, screencast, animacion?
- ¿Usan humor, urgencia, autoridad?
- ¿Que nivel de tecnicismo?

#### Dimension 4: Patrones de duracion

- ¿Cuanto duran los videos exitosos?
- ¿Los temas profundos son mas largos?
- ¿Hay oportunidad en formato corto o largo?

#### Dimension 5: HUECOS (lo mas valioso)

¿Que NO cubre nadie? ¿Que esta mal explicado, desactualizado,
o superficialmente tratado?

Busca:
- Temas mencionados pero no desarrollados
- Preguntas que los comentarios harian pero el video no responde
- Informacion desactualizada que necesita version actual
- Complejidad que nadie simplifica

#### Dimension 6: ANGULOS faltantes

¿Que perspectivas no existen?
- ¿Falta la perspectiva del principiante?
- ¿Falta el caso de estudio real (no teoria)?
- ¿Falta el angulo contrarian?
- ¿Falta el formato corto / snackable?
- ¿Falta la perspectiva latino / en espanol?

### Paso 6: Presentar reporte de inteligencia

## Plantilla de Salida

```
## Reporte de Inteligencia — "{query}"
Fecha: {YYYY-MM-DD}
Videos analizados: {N}
Costo total: ~${costo_usd} USD (~${costo_mxn} MXN)

### Videos Analizados

| # | Titulo | Duracion | Canal | URL |
|---|--------|----------|-------|-----|
| 1 | {titulo} | {dur} | {canal} | {url} |
| 2 | ... | ... | ... | ... |

### Dimension 1: Temas Comunes (Table Stakes)

{analisis de lo que todos cubren — esto es lo minimo, no tu diferenciador}

### Dimension 2: Patrones de Estructura

{como organizan contenido los videos exitosos}

### Dimension 3: Tono y Estilo

{que tono domina y que tono falta}

### Dimension 4: Patrones de Duracion

{que duraciones funcionan y donde hay espacio}

### Dimension 5: HUECOS — Lo que nadie cubre

{los huecos son ORO — aqui esta la ventaja competitiva}

- Hueco 1: {descripcion + evidencia}
- Hueco 2: {descripcion + evidencia}
- Hueco 3: {descripcion + evidencia}

### Dimension 6: ANGULOS — Perspectivas faltantes

{que angulo o enfoque no existe todavia}

- Angulo 1: {descripcion}
- Angulo 2: {descripcion}

### Dimension 7: DEBILIDADES — Lo que esta mal hecho

{contenido que existe pero es deficiente — aqui se gana facil}

- Debilidad 1: {que video/tema esta mal explicado + por que}
- Debilidad 2: {que informacion esta desactualizada + desde cuando}
- Debilidad 3: {que contenido es superficial y merece profundidad}

### Analisis de Oportunidades (rankeado por impacto)

Para cada oportunidad, evaluar 3 criterios:

| Criterio | Pregunta | Peso |
|----------|----------|:----:|
| **Demanda** | ¿Cuanta gente busca esto? (views de videos relacionados) | 40% |
| **Vacio** | ¿Que tan grande es el hueco? (nadie vs todos lo cubren mal) | 35% |
| **Capacidad** | ¿El invitado tiene conocimiento/autoridad en esto? | 25% |

| # | Oportunidad | Tipo | Demanda | Vacio | Capacidad | Score | Formato |
|---|------------|------|:-------:|:-----:|:---------:|:-----:|---------|
| 1 | {tema + angulo} | hueco/debilidad/angulo | A/M/B | A/M/B | A/M/B | {0-10} | Horizontal 12 min |
| 2 | {tema + angulo} | {tipo} | A/M/B | A/M/B | A/M/B | {0-10} | Short 60s + Horizontal |
| 3 | ... | ... | ... | ... | ... | ... | ... |

**Top 3 oportunidades con brief de contenido:**

Para las 3 oportunidades con mayor score, generar un brief:

**Oportunidad 1: {titulo}**
- Angulo: {que perspectiva unica ofreces}
- Gancho: {primeros 5 segundos — que dice para enganchar}
- Estructura: {intro → desarrollo → cierre}
- Duracion: {minutos}
- Short derivado: {que fragmento de 60s funciona solo}
- Diferenciador: {por que TU version sera mejor que lo existente}

### Transcripciones guardadas en

{path donde se guardaron los archivos}

### Siguiente paso

1. `/kokoro-calendar` para generar plan semanal desde estas oportunidades
2. `/kokoro-listen {url}` para profundizar en un video especifico
3. `/kokoro-research` para triangular con fuentes web
4. `/kokoro-creative` para disenar thumbnails de los videos priorizados
```

## Variante: Analisis rapido (sin transcripcion)

Si el usuario quiere solo un vistazo rapido SIN transcribir (sin costo):

```bash
yt-dlp --print title --print duration --print view_count \
  --print upload_date --print webpage_url \
  --playlist-items 1-{N} \
  --no-download \
  "ytsearch{N}:{query}" 2>&1
```

Con solo metadata (titulo, duracion, vistas, fecha), hacer un analisis
superficial de:
- Que temas dominan los titulos
- Que duraciones predominan
- Que tan recientes son los videos

Presentar como "vista desde la montaña" antes de invertir en transcripcion:

> "Desde la montaña, el panorama se ve asi: {resumen}. Si quieres
> bajar al valle y escuchar lo que realmente dicen, podemos transcribir
> los {N} mas relevantes por ~${costo} MXN. ¿Bajamos?"

## Manejo de Errores

### yt-dlp no encuentra resultados
"La busqueda '{query}' no arrojo resultados en YouTube. Intenta con
terminos mas amplios o en otro idioma."

### Video no disponible / privado
"El video {titulo} no esta disponible (privado o eliminado). Lo salto
y continuo con los demas."

Saltar videos no disponibles y continuar. Ajustar el conteo final.

### Whisper API falla en un video
"Whisper no pudo transcribir {titulo}. Lo incluyo en el reporte con
solo metadata. El analisis se hace con los {N-1} videos restantes."

No detener todo el proceso por un video fallido.

### Demasiados videos largos (costo alto)
Si al obtener metadata los videos suman >60 min totales y el costo
supera $1 USD:

> "Los {N} videos suman {total} minutos. El costo seria ~${costo} USD
> (~${costo_mxn} MXN). Puedo:
> 1. Analizar solo los {M} mas cortos (~${costo_reducido} MXN)
> 2. Analizar los {M} mas recientes
> 3. Hacer analisis rapido sin transcripcion (cortesia)
> ¿Que prefieres?"

### OPENAI_API_KEY no configurada
"No encontre la OPENAI_API_KEY en .env. La necesitas para transcribir
con Whisper. Puedo hacer el analisis rapido (solo metadata, sin costo)
mientras la configuras."

## Idioma

- Si el query es en espanol, pasar `language="es"` a Whisper
- Si es en ingles, pasar `language="en"`
- Si hay mezcla, omitir el parametro (auto-detect)
- El reporte se escribe en el idioma del usuario

## Notas para Claude

- Usa la voz de Eduardo: "escuchar el mercado", "desde la montaña",
  "donde esta el silencio, esta tu oportunidad"
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion"
  no "precio"
- Los huecos y angulos son el VALOR PRINCIPAL del reporte — dedica mas
  tiempo y profundidad a las dimensiones 5 y 6
- No transcribas sin estimar costo primero — siempre
- Procesa videos secuencialmente, no en paralelo
- Si las transcripciones son muy largas, resume antes de analizar
- Responde en el idioma del usuario
- IMPORTANTE: El analisis rapido (sin transcripcion) es un fallback
  valioso — ofrecer cuando el costo sea alto o la API no este disponible
- IMPORTANTE: Los huecos que detectes deben ser especificos y accionables,
  no genericos. "Nadie habla de X" es mejor que "hay oportunidad en el tema"
- Complemento natural de `/kokoro-research` — intel hace video, research
  hace web. Juntos, inteligencia completa
- Complemento natural de `/kokoro-listen` — listen procesa un video,
  intel procesa muchos

## Persistencia

### Session Log (si hay invitado resuelto)

Si se resolvio un invitado del grafo al inicio del skill, registrar la
sesion en su session_log al terminar. Consultar `kokoro-session-log.md`
para el schema completo.

```python
from pathlib import Path
from datetime import datetime, timezone
from kokoro.clients.store import load_registry, save_registry

project = Path(".")
registry = load_registry(project)
client = registry.find_by_id("{client_id}")

if "session_log" not in client.metadata:
    client.metadata["session_log"] = []

entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "intel",
    "skill": "/kokoro-intel",
    "client_id": client.id,
    "summary": "{N} videos analizados para '{query}' — {M} oportunidades detectadas",
    "hallazgos": ["{huecos y angulos descubiertos}"],
    "artifacts": ["{paths relativos de transcripciones y reporte}"],
    "next_action": "{siguiente paso logico}"
}

client.metadata["session_log"].insert(0, entry)
if len(client.metadata["session_log"]) > 20:
    client.metadata["session_log"] = client.metadata["session_log"][:20]

client.updated = datetime.now(tz=timezone.utc)
registry.updated = client.updated
save_registry(project, registry)
```

Si no hay invitado resuelto (backward compatible), omitir este paso.
