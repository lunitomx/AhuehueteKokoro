# Transcripción de Contenido Multi-Fuente

> Knowledge file para `/kokoro-listen`.

## Fuentes soportadas

- Video (MP4, MOV)
- Audio (MP3, WAV, M4A)
- YouTube (URL)
- BigBlueButton (grabaciones)

## Pipeline

1. Descarga/extracción de audio
2. Transcripción (Whisper local o API)
3. Limpieza de texto
4. Extracción de insights (con `/kokoro-cuts`)

Ver también: `kokoro-shorts-ffmpeg.md` para herramientas de video.
