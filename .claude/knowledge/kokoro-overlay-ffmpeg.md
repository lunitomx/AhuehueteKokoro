# ffmpeg Reference — /kokoro-overlay

> Skill: `/kokoro-overlay`
> Herramienta transversal: aplica en cualquier fase

> "Las palabras que acompanan la imagen multiplican su impacto."

## Proposito

Referencia tecnica de comandos ffmpeg drawtext para el skill `/kokoro-overlay`.
Documenta la sintaxis de filtros drawtext, escaping, timing con enable/between,
y combinacion con crop+scale para video vertical.

## drawtext Filter — Sintaxis Base

```bash
drawtext=text='Texto aqui':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.80:enable='between(t,0.0,3.2)'
```

**Parametros:**
- `text='...'` — Texto a mostrar (con escaping)
- `fontsize=48` — Tamano de fuente en pixeles
- `fontcolor=white` — Color del texto
- `borderw=3` — Ancho del borde/stroke en pixeles
- `bordercolor=black` — Color del borde
- `x=(w-text_w)/2` — Posicion X (centrado horizontal)
- `y=h*0.80` — Posicion Y (80% del alto = tercio inferior)
- `enable='between(t,start,end)'` — Cuando mostrar el texto

## Escaping para drawtext

ffmpeg drawtext tiene caracteres especiales que DEBEN escaparse:

| Caracter | Escape | Ejemplo |
|----------|--------|---------|
| `\` | `\\` | `texto\\con\\barras` |
| `'` | `'\''` | `texto'\\''con'\\''comillas` |
| `:` | `\:` | `Hora\: 3pm` |
| `%` | `%%` | `100%%` |

**Funcion de escaping (Python):**

```python
def escape_drawtext(text: str) -> str:
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "'\\''")
    text = text.replace(":", "\\:")
    text = text.replace("%", "%%")
    return text
```

**IMPORTANTE:** El orden de escaping importa — escapar `\` primero, luego el resto.

## Timing con enable/between

```
enable='between(t,start_seconds,end_seconds)'
```

- `t` es la variable de tiempo del video (en segundos, float)
- `between(t,0.0,3.2)` muestra el texto desde el segundo 0 hasta el 3.2
- Los valores son floats: `between(t,3.2,6.8)`

**Multiples drawtext en cadena:**

```bash
-vf "drawtext=...:enable='between(t,0.0,3.2)',\
drawtext=...:enable='between(t,3.2,6.8)',\
drawtext=...:enable='between(t,6.8,10.5)'"
```

Separados por coma dentro del mismo `-vf`.

## Comando Completo — Vertical 9:16 con Captions

```bash
ffmpeg -y -i "{input}" \
  -vf "crop=ih*9/16:ih,scale=1080:1920,\
drawtext=text='{text1}':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.80:enable='between(t,0.0,3.2)',\
drawtext=text='{text2}':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h*0.80:enable='between(t,3.2,6.8)'" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  "{output}"
```

**Orden de filtros (importa):**
1. `crop=ih*9/16:ih` — Recortar a 9:16
2. `scale=1080:1920` — Escalar a resolucion estandar
3. `drawtext=...` (x N) — Agregar captions

El crop+scale DEBE ir antes de drawtext porque las posiciones de texto
(`y=h*0.80`) referencian las dimensiones del frame final.

## Deteccion de Video Vertical

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=p=0 "{input}"
```

Si `width < height`, el video ya es vertical — omitir crop+scale.

## Duracion del Video

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "{input}"
```

## Line Wrapping

Para 1080px de ancho a fontsize 48, ~35 caracteres por linea.
Si el texto excede 35 chars, insertar `\n` (newline literal para drawtext):

```
drawtext=text='se mide en la capacidad\nde crear valor':...
```

## Errores Comunes

### 1. "Unable to find a suitable output format for pipe:"

**Causa:** Error de sintaxis en el filtro drawtext (comillas mal cerradas).
**Solucion:** Verificar que cada `text='...'` tiene comillas balanceadas.

### 2. "No such filter: drawtext"

**Causa:** ffmpeg compilado sin soporte de libfreetype.
**Solucion:** Reinstalar con brew: `brew reinstall ffmpeg`

### 3. Texto no aparece

**Causa:** `enable='between(t,start,end)'` con timestamps incorrectos.
**Solucion:** Verificar que los timestamps son relativos al short, no al video original.

### 4. Texto cortado o fuera de frame

**Causa:** Texto largo sin line wrapping.
**Solucion:** Aplicar wrap_text() a ~35 chars antes de construir el filtro.

### 5. Caracteres especiales causan error de filtro

**Causa:** `:`, `'`, `\`, o `%` sin escapar en el texto.
**Solucion:** Usar escape_drawtext() en todo el texto antes de construir el filtro.

## Flujo con Otros Skills

```
/kokoro-listen  → descarga video + transcripcion (Whisper verbose_json)
/kokoro-cuts    → identifica cortes (JSON con start/end sentences)
/kokoro-shorts  → extrae segmentos con timestamps precisos
/kokoro-overlay → agrega captions sincronizados ← ESTE SKILL
/kokoro-render  → ensambla video final con intro/outro (futuro)
/kokoro-creative → genera thumbnails
```
