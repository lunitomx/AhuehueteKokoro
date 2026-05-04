# Personajes Hiper-Realistas — Referencia Tecnica para /kokoro-character

> Skill: `/kokoro-character`
> Herramienta transversal: aplica en cualquier fase

> "Un personaje bien construido no es una foto — es una historia que se lee en los ojos."

## Proposito

Referencia tecnica para el skill `/kokoro-character`. Documenta el prompt base
para generacion de avatares hiper-realistas, las variables de personalizacion,
la API de Gemini, y las reglas de composicion.

## Prompt Base — Plantilla Maestra

Este JSON es la base de TODOS los personajes. Las variables entre `{llaves}`
se reemplazan segun los datos recopilados del usuario.

```json
{
  "description": "A hyper-realistic close-up portrait of {subject_description}, with detailed facial features that appear lifelike. The skin texture should show pores, subtle wrinkles, and natural imperfections like {skin_details}. The eyes must have a glossy, reflective look, capturing light with sharp details in the iris ({eye_color} eyes), and the eyelashes should be clearly visible. The eyebrows should be well-defined but natural, with individual hair strands visible. The lighting should be soft but dramatic, highlighting the high points of the face like the cheekbones, nose bridge, and lips. The shadows should be deep to create dimension, especially around the eyes and under the chin. The lips should have a slight gloss, with natural texture visible. The hair should have individual strands — {hair_description} — with natural shine, and should be styled in a way that reflects light naturally. {background_description}",
  "composition": "{composition_description}",
  "expression": "{expression_description}",
  "clothing": "{clothing_description}",
  "lighting": "{lighting_preset}",
  "style": "Ultra-realistic, with a cinematic quality, focusing on details like skin texture, facial hair, and lighting effects that mimic real-world photography. The overall tone should be natural and lifelike, emphasizing the character's human features.",
  "resolution": "8K",
  "focus": "Sharp focus on the eyes and face, ensuring all details are captured crisply. The rest of the face and hair should be slightly blurred but still maintain a high level of detail.",
  "lens": "{lens_preset}",
  "camera_angle": "{camera_angle_preset}",
  "aspect_ratio": "{aspect_ratio}"
}
```

## Variables de Personalizacion

### subject_description

Descripcion completa del sujeto. Construir a partir de:

| Campo | Ejemplo | Obligatorio |
|-------|---------|-------------|
| Genero | a woman, a man, a non-binary person | Si |
| Edad aprox | in their late 20s, around 45 years old | Si |
| Etnia/rasgos | with Latin American features, East Asian features, dark skin | Si |
| Contexto | who is a yoga instructor, a tech entrepreneur, a chef | No |

Ejemplo completo:
```
a woman in her early 30s with Latin American features who is a wellness entrepreneur
```

### skin_details

Imperfecciones naturales que agregan realismo:

| Opcion | Prompt |
|--------|--------|
| Joven (20s) | freckles and a light natural blush |
| Medio (30-40s) | subtle laugh lines and light freckles |
| Maduro (50+) | expression lines, subtle age spots, and natural weathering |
| Atletico | sun-kissed glow with light freckles |
| Default | freckles or subtle scars |

### eye_color

Opciones: brown, dark brown, hazel, green, blue, gray, amber

### hair_description

Construir con: color + textura + largo + estilo

Ejemplos:
- `dark brown wavy hair, shoulder-length, with natural highlights`
- `black straight hair pulled back in a professional bun`
- `salt-and-pepper curly hair, close-cropped`
- `auburn hair with loose curls falling past the shoulders`
- `shaved head with a short fade`

### background_description

| Preset | Prompt |
|--------|--------|
| Desenfocado neutro (default) | The background should be blurred with soft neutral tones, with the focus entirely on the person, ensuring the character's face takes the center stage. |
| Estudio | The background is a clean studio backdrop in {color}, with subtle gradient lighting. |
| Ambiente natural | The background shows a softly blurred {environment} — suggesting context without competing with the subject. |
| Marca | The background is a solid {brand_color} with subtle gradient, placing the character in a branded context. |

### composition_description

| Preset | Prompt |
|--------|--------|
| Retrato centrado (default) | The portrait should be centered, with the face facing directly towards the camera. Tight framing from upper chest to just above the head. |
| Tres cuartos | Three-quarter view with the subject slightly turned, creating depth. Framed from mid-chest up. |
| Perfil editorial | Side profile with dramatic lighting, editorial magazine quality. |
| Ambiental | Wider framing showing the subject in their environment, face still the focal point. |

### expression_description

| Preset | Prompt |
|--------|--------|
| Neutral confiado (default) | A neutral expression with quiet confidence — relaxed jaw, slight intensity in the eyes, as if listening attentively. |
| Sonrisa sutil | A subtle, genuine smile — not forced — with warmth in the eyes. The kind of smile that makes you feel welcomed. |
| Determinado | A determined expression with focused eyes and slightly set jaw. Communicates resolve without aggression. |
| Amigable | An open, approachable expression with a warm smile showing teeth naturally. Eyes crinkled slightly with genuine warmth. |
| Pensativo | A thoughtful expression, eyes slightly narrowed, as if considering an important idea. Lips relaxed, head tilted slightly. |
| Serio profesional | A composed, professional expression. Direct gaze, neutral mouth, conveying authority and competence. |

### clothing_description

| Preset | Prompt |
|--------|--------|
| Casual premium | Wearing a well-fitted {color} crew-neck sweater in soft cashmere, suggesting effortless style. |
| Profesional | Wearing a tailored {color} blazer over a clean white shirt, projecting professional authority. |
| Creativo | Wearing a relaxed linen shirt in {color}, slightly open at the collar, suggesting creative freedom. |
| Deportivo | Wearing a fitted athletic top in {color}, suggesting health and vitality. |
| Personalizado | {user_description} |

### lighting_preset

| Preset | Prompt |
|--------|--------|
| Dramatico suave (default) | Soft and diffused lighting from a 45-degree angle above and to the side, creating gentle shadows under the cheekbones and jawline. Natural light effects on the face, with reflective highlights on the skin, eyes, and lips. |
| Golden hour | Warm golden hour lighting from the side, casting a warm glow on the skin. Deep amber highlights on the cheekbones and hair, with soft shadows adding warmth and dimension. |
| Estudio Rembrandt | Classic Rembrandt lighting — key light at 45 degrees creating a triangle of light on the shadow-side cheek. Dramatic but flattering, emphasizing bone structure. |
| Luz natural frontal | Soft, even frontal lighting as if near a large window. Minimal shadows, clean and approachable. Subtle catchlights in both eyes. |
| Cinematico | Moody cinematic lighting with strong contrast. Side-lit with a cool fill, creating depth and atmosphere. Film-like color grading. |

### lens_preset

| Preset | Prompt |
|--------|--------|
| Retrato clasico (default) | 85mm lens, providing natural bokeh effect for background blur and maintaining a realistic depth of field. |
| Intimo | 50mm lens, slightly wider perspective creating an intimate, documentary feel. |
| Editorial | 135mm lens, strong compression and creamy bokeh for editorial magazine quality. |
| Ambiental | 35mm lens, wider perspective showing more environment while keeping the subject prominent. |

### camera_angle_preset

| Preset | Prompt |
|--------|--------|
| Frontal (default) | Straight-on angle, slightly tilted downward to give the impression of depth and dimension. |
| Ligeramente elevado | Slightly elevated angle (about 15 degrees above eye level), creating a subtle editorial quality. |
| A nivel de ojos | Perfectly eye-level, direct and confrontational in an engaging way. |
| Ligeramente bajo | Slightly low angle, conveying authority and presence. |

### aspect_ratio

| Uso | Ratio | Pixeles |
|-----|-------|---------|
| Redes sociales cuadrado | 1:1 | 1080x1080 |
| Historia/Reel | 9:16 | 1080x1920 |
| Feed horizontal | 16:9 | 1920x1080 |
| Retrato editorial | 4:5 | 1080x1350 |
| Avatar / profile pic | 1:1 | 512x512 |
| Tarjeta de presentacion | 3.5:2 | 1050x600 |

Default: 1:1 a 1080x1080

## API de Gemini — Generacion

### Modelo

Usar `nano-banana-pro-preview` (mejor calidad para retratos).

### Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent?key={api_key}
```

### Request — Sin imagen de referencia

Para personajes nuevos (sin foto base):

```json
{
  "contents": [{
    "parts": [
      {"text": "{prompt_completo}"}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

### Request — Con imagen de referencia

Si el usuario sube una foto de referencia (para capturar un estilo, pose, o
como base de un personaje):

```json
{
  "contents": [{
    "parts": [
      {"inline_data": {"mime_type": "image/png", "data": "{reference_base64}"}},
      {"text": "Use this reference image ONLY for style/pose inspiration. Generate a NEW hyper-realistic character based on the following spec — do NOT copy the face from the reference.\n\n{prompt_completo}"}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

IMPORTANTE: Cuando se usa referencia, dejar CLARO en el prompt que es solo
inspiracion, no copia. No queremos generar deepfakes de personas reales.

### Response

La imagen viene en `candidates[0].content.parts[N].inlineData.data` como
base64. Decodificar y guardar como PNG.

## Construccion del Prompt Final

El prompt que se envia a Gemini se construye concatenando todas las secciones
del JSON en un texto narrativo coherente. Orden:

1. **description** — abre con la descripcion del sujeto y detalles faciales
2. **expression** — estado emocional y expresion
3. **clothing** — vestimenta
4. **composition** — encuadre y composicion
5. **lighting** — iluminacion
6. **style** — estilo general (siempre hiper-realista)
7. **resolution** — 8K
8. **focus** — enfoque en ojos y rostro
9. **lens** — lente y bokeh
10. **camera_angle** — angulo de camara
11. **aspect_ratio** — mencionado al inicio: "Generate an image at {ratio}"

### Ejemplo de prompt final ensamblado

```
Generate a hyper-realistic portrait at 1:1 aspect ratio (1080x1080 pixels).

A hyper-realistic close-up portrait of a woman in her early 30s with Latin
American features who is a wellness entrepreneur, with detailed facial features
that appear lifelike. The skin texture should show pores, subtle wrinkles, and
natural imperfections like subtle laugh lines and light freckles. The eyes must
have a glossy, reflective look, capturing light with sharp details in the iris
(dark brown eyes), and the eyelashes should be clearly visible. [...]

Expression: A subtle, genuine smile — not forced — with warmth in the eyes.
The kind of smile that makes you feel welcomed.

Clothing: Wearing a relaxed linen shirt in warm terracotta, slightly open at
the collar, suggesting creative freedom.

Composition: The portrait should be centered, with the face facing directly
towards the camera. Tight framing from upper chest to just above the head.

Lighting: Soft and diffused lighting from a 45-degree angle above and to the
side, creating gentle shadows under the cheekbones and jawline. [...]

Style: Ultra-realistic, with a cinematic quality, focusing on details like skin
texture and lighting effects that mimic real-world photography.

Resolution: 8K. Sharp focus on the eyes and face.
Lens: 85mm with natural bokeh.
Camera: Straight-on angle, slightly tilted downward.
```

## Nomenclatura de Archivos

### Sin invitado (uso general)

```
characters/{proyecto}/character-{NN}-{nombre_corto}.png
characters/{proyecto}/json-character-{NN}-{nombre_corto}.json
```

Ejemplo:
```
characters/social-room/character-01-wellness-coach.png
characters/social-room/json-character-01-wellness-coach.json
```

### Con invitado

```
clientes/{grupo}/assets/character-{NN}-{nombre_corto}.png
clientes/{grupo}/assets/json-character-{NN}-{nombre_corto}.json
```

## Consideraciones Eticas

- NUNCA generar retratos de personas reales identificables
- Si el usuario pide "hazme un avatar de [persona famosa]", rechazar
  con elegancia: la creacion de personajes es para personas ficticias
  o representaciones arquetipicas
- Las fotos de referencia son solo para estilo/pose, nunca para copiar rostros
- Incluir en metadata del JSON: `"type": "ai-generated-character"`
- Si el personaje se usara en publicidad, recordar que Meta exige que las
  imagenes generadas por IA se marquen como tal

## Limites y Costos

- ~$0.13 USD / imagen con Nano Banana Pro (~$2.50 MXN)
- Rate limits tier gratuito: ~10-15 imagenes/dia
- Tiempo de generacion: 20-60 segundos por imagen
- Calidad: ~95% publicable para retratos (mejor que para diseño grafico)
