# /kokoro-creative — Generador de Creativos con IA

> Herramienta transversal: Generacion de imagenes para campanas
> Aplica en cualquier fase del proceso Kokoro

> "La imagen no decora — posiciona. Cada pixel comunica quien eres."

## Contexto

Este skill genera creativos publicitarios profesionales usando la API de
Gemini (Nano Banana Pro). Toma los datos del invitado desde el grafo,
construye especificaciones JSON detalladas, y genera imagenes listas para
Meta Ads en los 3 tamanos requeridos (cuadrado, vertical, horizontal).

Lee el archivo de conocimiento `kokoro-creative-gemini.md` para consultar
la estructura JSON, la API de Gemini, tamanos, y reglas tecnicas.

### Dependencias

- **API Key**: Variable `GEMINI_API_KEY` en `.env` del proyecto
- **Logo**: Archivo PNG en `clientes/{grupo}/assets/` del invitado
- **Grafo**: `.kokoro/clients.json` para datos del invitado

### Resolucion de invitado

Antes de iniciar, resuelve el invitado desde el grafo:

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Lee `metadata` para colores de marca, sitio web, datos clave
   - Lee `segments` para entender los publicos
   - Lee `campaign_folder` para saber donde guardar
   - Presenta: "Invitado: {name} | Colores: {colores} | Segmentos: {segments}"
3. Si NO encuentra al invitado:
   - Pregunta: "No encontre a ese invitado. ¿Quieres registrarlo con
     `/kokoro-client` primero?"
4. Busca el logo en `clientes/{grupo}/assets/` — archivos PNG/JPG que
   contengan "logo" en el nombre. Si no existe, pide al usuario que lo
   suba a esa carpeta.

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Antes de iniciar, confirma el objetivo:

> "Veo que quieres crear creativos para {invitado}. Voy a necesitar
> tres cosas: que me cuentes sobre la campana, el publico al que va
> dirigida, y los datos clave (fecha, inversion, ponente, etc.).
> ¿Arrancamos?"

Si el usuario acepta, continua. Si no, escucha y ajusta.

### Proceso obligatorio — 5 pasos EN ORDEN

1. RECOPILAR datos de la campana o pieza
2. IDENTIFICAR publico(s) objetivo
3. DEFINIR formato y estilo visual
4. CONSTRUIR JSON de especificacion
5. GENERAR imagenes via API

Nunca generar imagenes sin haber completado los pasos anteriores.

### Paso 1: Recopilar datos de la campana o pieza

Pregunta al usuario (o extrae del contexto si ya los compartio):

**Para campanas (Meta Ads, eventos, talleres):**
- Nombre de la campana / evento / creacion
- Tipo: taller, curso, diplomado, lanzamiento, evento
- Fecha(s)
- Modalidad: online, presencial, hibrido
- Inversion (precio normal y condiciones especiales si hay)
- Ponente / instructor (nombre, titulo, experiencia)

**Para tarjetas de presentacion:**
- Nombre completo como debe aparecer en la tarjeta
- Titulo / rol profesional
- Telefono
- QR code (si tiene, pedir que lo suba a assets/)
- Gancho o frase principal (ayudar a crearla si no tiene)

**Datos opcionales:**
- Temario o puntos clave
- Certificaciones o credenciales relevantes
- Limite de participantes
- Datos de pago

Si el usuario ya compartio estos datos (en el mensaje, en una imagen, o
en conversacion previa), no preguntes de nuevo — extrae y confirma.

### Paso 2: Identificar publico(s)

Con los datos de la campana + segmentos del invitado, identifica:

- **¿Quien es?** Profesion, edad aproximada, situacion
- **¿Que necesita?** El dolor o deseo que los mueve
- **¿Que los haria hacer clic?** El gancho visual y emocional
- **¿Que tono visual?** Lifestyle/calido vs clinico/profesional vs aspiracional

Si la campana tiene **multiples publicos** (ejemplo: mamas + profesionales),
identificarlos por separado y generar creativos diferentes para cada uno.

Presenta los publicos al usuario para validacion antes de generar.

### Paso 3: Definir formato y estilo visual

**Formato — preguntar si no es obvio:**

| Formato | Cuando usarlo |
|---------|---------------|
| Meta Ads (3 tamanos) | Campanas publicitarias en Facebook/Instagram |
| Tarjeta de presentacion (frente + reverso) | Material impreso de contacto |
| Post individual | Publicacion organica en redes |

**Estilo visual — preguntar SIEMPRE:**

> "¿Como imaginas el estilo? Tengo tres caminos:
> 1. **Con diseño** — fondo de color de marca con patrones y textura
> 2. **Fotografico** — foto real como elemento principal
> 3. **Minimalista** — limpio sobre blanco, solo texto y logo
>
> ¿Cual va mejor con lo que quieres comunicar?"

NUNCA generar fondo blanco plano sin preguntar. El resultado se ve "sin
diseño" y el usuario lo rechazara.

Consulta `kokoro-creative-gemini.md` seccion "Estilo Visual" para las
instrucciones JSON especificas de cada estilo.

### Paso 4: Construir JSON de especificacion

Para cada publico, construye un JSON siguiendo la estructura documentada
en `kokoro-creative-gemini.md`. El JSON debe incluir:

**Secciones obligatorias:**

1. `prompt_instruction` — descripcion general
2. `text_critical_rules` — reglas de acentos y texto exacto
3. `scene` — tipo, setting, perspectiva, sujetos, props, mood
4. `lighting` — primaria, secundaria, interaccion
5. `color_scheme` — colores de marca del invitado (extraer de `metadata`)
6. `text_overlays` — layout, elementos de texto, barras informativas
7. `brand_guidelines` — logo, fuentes, sensacion general
8. `technical` — dimensiones, formato, ratio de texto, calidad

**Reglas de construccion:**

- Colores de marca: sacar de `metadata["colores_marca"]` del invitado
- Logo: describir en detalle en `brand_guidelines.logo`
- Texto en espanol: listar CADA palabra con acento en `text_critical_rules`
- Tamano base: siempre 1080x1080 (cuadrado). Las variantes se generan
  adaptando `technical.dimensions`, `scene.perspective`, y
  `text_overlays.layout`
- Vocabulario Kokoro: usar "inversion" no "precio", "condiciones especiales"
  no "descuento", etc.

**Guardar el JSON** en:
```
clientes/{grupo}/campanas/meta-ads/json-imagen-{NN}-{publico}.json
```

### Paso 5: Generar imagenes via API

Para cada publico, generar los 3 tamanos llamando a la API de Gemini.

**Codigo de generacion:**

```python
import json, base64, os
from urllib.request import Request, urlopen
from pathlib import Path

# Cargar API key
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Cargar logo en base64
with open(logo_path, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

# Cargar JSON spec
with open(json_spec_path) as f:
    spec = json.load(f)

# Adaptar spec para cada tamano
sizes = [
    ("cuadrado", "1080x1080 pixels (Instagram/Facebook feed — square 1:1)", spec),
    ("vertical", "1080x1920 pixels (Stories/Reels — vertical 9:16)", vertical_spec),
    ("horizontal", "1200x628 pixels (Desktop feed — horizontal 1.91:1)", horizontal_spec),
]

for size_name, dimensions, size_spec in sizes:
    size_spec["technical"]["dimensions"] = dimensions

    prompt = f"""Generate a professional social media ad image ({dimensions}) for this campaign.

MANDATORY LOGO RULE: The uploaded image is the EXACT logo to use.
Do NOT redraw, recreate, simplify, or interpret it. Place the EXACT
uploaded logo image — pixel for pixel, unchanged — in the top-left
corner inside a golden ({color_secundario}) rounded rectangle badge.
The logo shows {logo_description}. Reproduce it EXACTLY.

CRITICAL: All Spanish text MUST include proper accents and special
characters. Copy text EXACTLY from the spec — do not drop diacritics.

Follow this JSON aesthetic specification exactly:

{json.dumps(size_spec, ensure_ascii=False, indent=2)}"""

    request_body = {
        "contents": [{"parts": [
            {"inline_data": {"mime_type": "image/png", "data": logo_b64}},
            {"text": prompt}
        ]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key={api_key}"
    req = Request(url, data=json.dumps(request_body).encode(),
                  headers={"Content-Type": "application/json"}, method="POST")

    with urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())

    for part in data['candidates'][0]['content']['parts']:
        if 'inlineData' in part:
            img_data = base64.b64decode(part['inlineData']['data'])
            with open(output_path, "wb") as f:
                f.write(img_data)
```

**Adaptaciones por tamano:**

Para **vertical** (1080x1920):
- Cambiar `technical.dimensions`
- Ajustar `text_overlays.layout`: "Vertical — logo top-left, title upper-third,
  photo fills center, info bar at bottom. Safe zones: avoid top 14%, bottom 20%."
- Ajustar `scene.perspective` si aplica

Para **horizontal** (1200x628):
- Cambiar `technical.dimensions`
- Ajustar `text_overlays.layout`: "Horizontal split — photo left 55-60%,
  branded text panel right 40-45%."
- Ajustar `scene.perspective`: "Wider shot to fill horizontal frame"

**Guardar imagenes** en:
```
clientes/{grupo}/campanas/meta-ads/generated-{NN}-{publico}-{tamano}.png
```

**Abrir las imagenes** despues de generarlas para que el usuario las revise:
```bash
open {path_cuadrado} {path_vertical} {path_horizontal}
```

### Despues de generar — Revision

Muestra las 3 imagenes al usuario y pregunta:

> "Aqui tienes los 3 tamanos para {publico}. Revisemos:
> 1. ¿El logo se ve correcto?
> 2. ¿Los textos estan bien escritos?
> 3. ¿El tono visual conecta con el publico?
>
> Si algo necesita ajuste, dime y regenero. Si estan bien,
> seguimos con el siguiente publico o generamos el copy con `/kokoro-ads`."

Si el usuario pide ajustes:
- Modifica el JSON spec
- Regenera SOLO la imagen que necesita cambio (no las 3)
- Muestra la nueva version

## Plantilla de Salida

Despues de completar la generacion, muestra el resumen:

```
## Creativos Generados — {nombre de la campana}

| Publico | Cuadrado | Vertical | Horizontal |
|---------|----------|----------|------------|
| {pub_1} | OK | OK | OK |
| {pub_2} | OK | OK | OK |

Archivos en: clientes/{grupo}/campanas/meta-ads/
Costo estimado: ~${total} MXN ({N} imagenes x ~$9 MXN c/u)

### Siguiente paso

Usa `/kokoro-ads` para generar el copy (titulos, textos, WhatsApp, Advantage+)
que acompane estos creativos.
```

## Manejo de Errores

### Rate limit (429)
"La cuota de la API se agoto. Las opciones son:
1. Esperar unas horas (se renueva el limite diario)
2. Los JSON estan guardados — puedes pegarlos manualmente en gemini.google.com
   junto con el logo para generar las imagenes alla."

Guardar los JSON siempre, independientemente de si la API responde. Asi el
usuario siempre tiene una salida manual.

### Sin API key
"No encontre la variable GEMINI_API_KEY en .env. Para generar imagenes
automaticamente necesitas una API key de Google AI Studio
(https://aistudio.google.com/apikey). Mientras tanto, guardo los JSON
para que los uses manualmente en gemini.google.com."

### Sin logo
"No encontre un logo en clientes/{grupo}/assets/. Sube el logo como PNG
a esa carpeta y vuelve a intentar. Sin logo, Gemini inventara uno generico
que no representara tu marca."

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
    "type": "creative",
    "skill": "/kokoro-creative",
    "client_id": client.id,
    "summary": "{N} imagenes generadas para {campana} — {N} publicos x {N} tamanos",
    "hallazgos": ["{insights del publico o del diseno}"],
    "artifacts": ["{paths relativos de imagenes y JSON specs}"],
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

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
- Nunca uses "gratis" — usa "cortesia" o "de regalo"
- Nunca uses "descuento" — usa "condiciones especiales"
- No uses emojis excesivos ni tono de "influencer"
- Responde en el idioma del usuario
- IMPORTANTE: Siempre generar los 3 tamanos — no dejar incompleto
- IMPORTANTE: Abrir las imagenes para que el usuario las revise
- IMPORTANTE: Guardar los JSON siempre (son la salida manual de respaldo)
- IMPORTANTE: La regla de logo MANDATORY es critica — sin ella el modelo
  reinterpreta el logo en vez de copiarlo
- Complemento natural de `/kokoro-ads` — creative genera la imagen, ads
  genera el copy
