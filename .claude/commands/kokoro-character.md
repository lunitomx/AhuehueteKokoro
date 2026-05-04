# /kokoro-character — Generador de Personajes Hiper-Realistas

> Herramienta transversal: Generacion de avatares y personajes con IA
> Aplica en cualquier fase del proceso Kokoro

> "Un personaje bien construido no es una foto — es una historia que se lee en los ojos."

## Contexto

Este skill genera personajes hiper-realistas usando la API de Gemini
(Nano Banana Pro). Construye prompts detallados a partir de las preferencias
del usuario, generando retratos cinematicos con nivel de fotografia profesional.

Lee el archivo de conocimiento `kokoro-character-prompts.md` para consultar
la plantilla base, los presets de personalizacion, y la referencia de la API.

### Dependencias

- **API Key**: Variable `GEMINI_API_KEY` en `.env` del proyecto
- **Knowledge**: `kokoro-character-prompts.md` para plantilla y presets

### Resolucion de proyecto

Antes de crear personajes, establecer contexto:

1. Preguntar: "¿Para que proyecto o invitado es este personaje?"
2. Si menciona un invitado, buscar en `.kokoro/clients.json`
   - Si existe: usar colores de marca para fondo/vestimenta si aplica
   - Si no existe: preguntar si quiere registrarlo o si es uso general
3. Si es uso general, pedir nombre del proyecto para organizar archivos
4. Preguntar: "¿Que quieres lograr con este personaje?"
   - Avatar para redes sociales
   - Personaje para campana publicitaria
   - Representacion de un arquetipo de invitado (buyer persona visual)
   - Imagen para sitio web o landing page
   - Otro (dejar que el usuario explique)

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Veo que quieres crear un personaje hiper-realista. Necesito entender
> dos cosas antes de empezar: para que proyecto es, y que quieres lograr
> con este personaje. Con eso puedo guiarte mejor. ¿Me cuentas?"

Si el usuario acepta, continua. Si no, escucha y ajusta.

### Proceso obligatorio — 5 pasos EN ORDEN

1. CONTEXTUALIZAR — proyecto, objetivo, uso final
2. DISENAR — construir el personaje con el usuario
3. ENSAMBLAR — armar el prompt tecnico completo
4. GENERAR — llamar a Gemini API
5. REFINAR — revisar y ajustar si es necesario

Nunca generar sin haber completado los pasos anteriores.

### Paso 1: Contextualizar

Recopilar:

- **Proyecto**: ¿Para que invitado o proyecto?
- **Objetivo**: ¿Para que se usara? (avatar, campana, web, buyer persona visual)
- **Tamano**: ¿Donde se publicara?
  - Redes cuadrado: 1080x1080 (1:1)
  - Historia/Reel: 1080x1920 (9:16)
  - Feed horizontal: 1920x1080 (16:9)
  - Retrato editorial: 1080x1350 (4:5)
  - Avatar/profile: 512x512 (1:1)
- **Cantidad**: ¿Cuantos personajes necesitas?

Si el usuario ya compartio esta info, no repetir — confirmar y avanzar.

### Paso 2: Disenar el personaje

Guiar al usuario a traves de cada dimension del personaje. Para cada una,
ofrecer los presets disponibles (ver `kokoro-character-prompts.md`) y dejar
que personalice libremente si ninguno encaja.

**Preguntar EN ESTE ORDEN:**

1. **Sujeto** — "Descríbeme al personaje: genero, edad aproximada, rasgos
   etnicos, y si tiene un rol o contexto (emprendedor, coach, chef...)"

2. **Expresion** — "¿Que emocion quieres que transmita?"
   Ofrecer presets: neutral confiado, sonrisa sutil, determinado, amigable,
   pensativo, serio profesional. O dejar que describa libremente.

3. **Vestimenta** — "¿Como lo imaginas vestido?"
   Presets: casual premium, profesional, creativo, deportivo. O personalizado.

4. **Cabello** — "¿Como es su cabello?"
   Guiar: color + textura + largo + estilo.

5. **Ojos** — "¿Color de ojos?"

6. **Piel** — "¿Algun detalle especifico? ¿Pecas, barba, cicatrices,
   tatuajes visibles?"

7. **Iluminacion** — "¿Que atmosfera quieres?"
   Presets: dramatico suave, golden hour, estudio Rembrandt, luz natural,
   cinematico. O personalizado.

8. **Fondo** — "¿Que hay detras del personaje?"
   Presets: desenfocado neutro, estudio de color, ambiente natural, color de
   marca. O personalizado.

9. **Composicion** — "¿Que encuadre?"
   Presets: retrato centrado, tres cuartos, perfil editorial, ambiental.

**IMPORTANTE**: Si el usuario dice "tu decide" o "lo que se vea bien",
elegir presets coherentes con el objetivo declarado y presentar la seleccion
para validacion antes de generar.

**IMPORTANTE**: El usuario puede querer personalizar CADA detalle libremente.
Cuando el usuario da una descripcion en texto libre en vez de elegir preset,
usarla tal cual en el prompt — no forzar presets.

### Paso 3: Ensamblar el prompt

Con todos los datos recopilados, construir el JSON de especificacion siguiendo
la plantilla de `kokoro-character-prompts.md`. Reemplazar TODAS las variables.

**Guardar el JSON** en:
- Con invitado: `clientes/{grupo}/assets/json-character-{NN}-{slug}.json`
- Sin invitado: `characters/{proyecto}/json-character-{NN}-{slug}.json`

Mostrar un resumen al usuario antes de generar:

> "Voy a generar: {descripcion breve del personaje}
> Tamano: {ratio} ({pixeles})
> Estilo: hiper-realista, cinematico
> Iluminacion: {preset elegido}
>
> ¿Le damos?"

### Paso 4: Generar via API

**Codigo de generacion:**

```python
import json, base64, os
from urllib.request import Request, urlopen
from pathlib import Path

# Cargar API key
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Cargar JSON spec
with open(json_spec_path) as f:
    spec = json.load(f)

# Construir prompt narrativo a partir del JSON
prompt = f"""Generate a hyper-realistic portrait at {spec['aspect_ratio']} aspect ratio.

{spec['description']}

Expression: {spec['expression']}

Clothing: {spec['clothing']}

Composition: {spec['composition']}

Lighting: {spec['lighting']}

Style: {spec['style']}

Resolution: {spec['resolution']}. {spec['focus']}
Lens: {spec['lens']}
Camera: {spec['camera_angle']}

CRITICAL: This must look like a real photograph, not AI-generated. Every
detail — pores, hair strands, eye reflections, skin imperfections — must
be indistinguishable from a professional photo shoot."""

request_body = {
    "contents": [{"parts": [
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

**Con imagen de referencia** (si el usuario sube una foto de estilo/pose):

Agregar la imagen como primer part con inline_data, y anadir al prompt:
```
Use the uploaded reference image ONLY for style and pose inspiration.
Generate a completely NEW person — do NOT copy or reproduce the face
from the reference image.
```

**Guardar imagen** en:
- Con invitado: `clientes/{grupo}/assets/character-{NN}-{slug}.png`
- Sin invitado: `characters/{proyecto}/character-{NN}-{slug}.png`

**Abrir la imagen** para que el usuario la revise:
```bash
open {output_path}
```

### Paso 5: Refinar

Despues de abrir la imagen:

> "Aqui esta tu personaje. Revisemos:
> 1. ¿Los rasgos coinciden con lo que imaginabas?
> 2. ¿La expresion es la correcta?
> 3. ¿La iluminacion y el fondo funcionan?
>
> Si algo necesita ajuste, dime que cambiar y regenero.
> Si esta bien, puedo generar variaciones (otro angulo, otra expresion)
> o crear mas personajes."

Si el usuario pide ajustes:
- Modificar el JSON spec en la seccion correspondiente
- Regenerar (solo la imagen, no todo el proceso)
- Mostrar la nueva version

Si el usuario quiere multiples tamanos del mismo personaje:
- Adaptar composicion y encuadre por tamano (ver presets en knowledge)
- Generar cada tamano por separado
- Abrir todos para revision

## Generacion de multiples personajes

Si el usuario necesita varios personajes (ej: equipo, buyer personas), mantener
un JSON spec por personaje y numerarlos secuencialmente:

```
character-01-wellness-coach.png
character-02-tech-founder.png
character-03-creative-director.png
```

## Plantilla de Salida

```
## Personaje Generado — {nombre/slug}

| Atributo | Valor |
|----------|-------|
| Proyecto | {nombre del proyecto o invitado} |
| Objetivo | {para que se usa} |
| Tamano | {ratio} ({pixeles}) |
| Costo | ~$2.50 MXN |

Archivo: `{path_de_imagen}`
Spec: `{path_de_json}`

### Siguiente paso

{sugerencia contextual — variaciones, mas personajes, o integracion
con /kokoro-creative para campana}
```

## Manejo de Errores

### Rate limit (429)
"La cuota de la API se agoto. Las opciones son:
1. Esperar unas horas (se renueva el limite diario)
2. El JSON esta guardado — puedes pegarlo manualmente en gemini.google.com"

### Sin API key
"No encontre la variable GEMINI_API_KEY en .env. Para generar imagenes
necesitas una API key de Google AI Studio. Mientras tanto, guardo el JSON
para uso manual."

### Solicitud de persona real
"La creacion de personajes es para personas ficticias o representaciones
arquetipicas. No puedo generar retratos de personas reales identificables.
¿Que tal si creamos un personaje original inspirado en las cualidades que
quieres comunicar?"

## Persistencia

### Session Log (si hay invitado resuelto)

```python
entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "character",
    "skill": "/kokoro-character",
    "client_id": client.id,
    "summary": "{N} personaje(s) generado(s) para {objetivo}",
    "hallazgos": ["{observaciones sobre el personaje o el proceso}"],
    "artifacts": ["{paths relativos de imagenes y JSON specs}"],
    "next_action": "{siguiente paso logico}"
}
```

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- Usa "invitado" no "cliente", "creacion" no "producto"
- No uses emojis excesivos ni tono de influencer
- Responde en el idioma del usuario
- IMPORTANTE: Siempre guardar el JSON (es el respaldo manual)
- IMPORTANTE: Abrir la imagen para que el usuario la revise
- IMPORTANTE: Nunca generar retratos de personas reales
- IMPORTANTE: Dejar que el usuario personalice CADA detalle si quiere —
  los presets son guia, no restriccion
- Si el usuario describe al personaje en texto libre, convertir esa
  descripcion en el formato tecnico sin perder su intencion original
- Complemento natural de `/kokoro-creative` — character crea al personaje,
  creative lo integra en la pieza publicitaria
