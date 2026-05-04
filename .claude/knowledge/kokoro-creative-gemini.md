# Gemini Image Generation — Referencia Tecnica para /kokoro-creative

> Skill: `/kokoro-creative`
> Herramienta transversal: aplica en cualquier fase

> "La imagen no decora — posiciona. Cada pixel comunica quien eres."

## Proposito

Referencia tecnica para el skill `/kokoro-creative`. Documenta la API de
Gemini para generacion de imagenes, la estructura JSON que controla los
creativos, las reglas de texto en espanol, y los tamanos requeridos por
Meta Ads.

## API de Gemini — Generacion de Imagenes

### Modelos Disponibles

| Modelo | ID API | Calidad | Costo aprox |
|--------|--------|---------|-------------|
| Nano Banana Pro | `nano-banana-pro-preview` | Alta (recomendado) | ~$0.13 USD/img |
| Nano Banana 2 | `gemini-3.1-flash-image-preview` | Alta | ~$0.05 USD/img |
| Nano Banana | `gemini-2.5-flash-image` | Buena | ~$0.04 USD/img |

Modelo por defecto: `nano-banana-pro-preview`

### Endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}
```

### Request Body — Una imagen de entrada (logo)

```json
{
  "contents": [{
    "parts": [
      {"inline_data": {"mime_type": "image/png", "data": "{logo_base64}"}},
      {"text": "{prompt_con_json_spec}"}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

### Request Body — Multiples imagenes de entrada (logo + QR, logo + foto, etc.)

La API acepta multiples `inline_data` parts en el mismo request. Cada imagen
se referencia en el prompt por orden ("first uploaded image", "second uploaded
image"). Validado con logo + QR code en tarjetas de presentacion.

```json
{
  "contents": [{
    "parts": [
      {"inline_data": {"mime_type": "image/png", "data": "{logo_base64}"}},
      {"inline_data": {"mime_type": "image/png", "data": "{qr_base64}"}},
      {"text": "First image is the logo. Second image is the QR code. Use both EXACTLY..."}
    ]
  }],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"]
  }
}
```

Casos de uso para multiples imagenes:
- Logo + QR code (tarjetas de presentacion)
- Logo + foto de producto (catálogos)
- Logo + foto de ponente (creativos de eventos)

### Response

La imagen generada viene en `candidates[0].content.parts[N].inlineData.data`
como base64. Decodificar y guardar como PNG/JPEG.

### Autenticacion

API key en variable de entorno `GEMINI_API_KEY` (archivo `.env` en raiz del
proyecto). NUNCA hardcodear la key en el codigo.

## Tamanos de Creativos para Meta Ads

### Los 3 tamanos obligatorios

| Nombre | Ratio | Pixeles | Uso en Meta |
|--------|-------|---------|-------------|
| Cuadrado | 1:1 | 1080x1080 | Feed Facebook + Instagram |
| Vertical | 9:16 | 1080x1920 | Stories + Reels + WhatsApp Status |
| Horizontal | 1.91:1 | 1200x628 | Desktop + ubicaciones secundarias |

Prioridad: Cuadrado (caballo de batalla) > Vertical (mayor alcance) > Horizontal (soporte)

## Formatos Adicionales

### Tarjeta de Presentacion

| Nombre | Ratio | Pixeles | Uso |
|--------|-------|---------|-----|
| Tarjeta frente | 3.5:2 | 1050x600 | Impresion — frente de tarjeta |
| Tarjeta reverso | 3.5:2 | 1050x600 | Impresion — reverso de tarjeta |

Las tarjetas se generan como par (frente + reverso). El frente lleva el
gancho/hook y datos de contacto. El reverso es minimalista — QR, telefono,
nombre, logo.

Si el invitado tiene QR, subirlo a `clientes/{grupo}/assets/` y enviarlo
como segunda imagen en el request (ver seccion de multiples imagenes).

### Adaptaciones por tamano

- **Vertical**: Composicion diferente — logo arriba, foto centro, info abajo.
  Respetar safe zones: evitar top 14% (status bar) y bottom 20% (CTA area).
- **Horizontal**: Split layout — foto a la izquierda (55-60%), panel de texto
  a la derecha (40-45%). Composicion mas cinematica.
- **Cuadrado**: Composicion estandar — foto domina top 65%, texto en bottom 35%.

## Estructura JSON para Creativos

### Estructura Base

```json
{
  "prompt_instruction": "Descripcion general de lo que se necesita",
  "text_critical_rules": {
    "rule_1": "Acentos en espanol obligatorios",
    "rule_2": "Nombres propios exactos",
    "rule_3": "Sin elementos decorativos no especificados",
    "rule_4": "Texto legible y correcto"
  },
  "scene": {
    "type": "tipo de fotografia",
    "setting": "descripcion del ambiente",
    "perspective": "angulo de camara",
    "subjects": [{"role": "", "description": "", "position": ""}],
    "props": "elementos en escena",
    "mood": "tono emocional"
  },
  "lighting": {
    "primary": "luz principal",
    "secondary": "luz de relleno",
    "interaction": "como interactua la luz con la escena"
  },
  "color_scheme": {
    "primary": "color principal de marca + hex",
    "secondary": "color secundario + hex",
    "environment_palette": "tonos del ambiente",
    "contrast": "relacion de contraste"
  },
  "text_overlays": {
    "layout": "distribucion del texto en la imagen",
    "elements": [{"text": "", "style": "", "position": ""}],
    "bottom_bar": {
      "left_block": {"background": "", "text_color": "", "content": ""},
      "right_block": {"background": "", "text_color": "", "content": ""}
    }
  },
  "brand_guidelines": {
    "logo": "descripcion detallada del logo",
    "fonts": "tipografias",
    "overall_feel": "sensacion general"
  },
  "technical": {
    "dimensions": "tamano en pixeles",
    "format": "tipo de formato",
    "text_ratio": "menos del 20% para Meta Ads compliance",
    "quality": "nivel de calidad"
  }
}
```

## Estilo Visual — Preguntar SIEMPRE

El modelo genera fondo blanco plano por defecto. Eso produce disenos sin
personalidad. SIEMPRE preguntar al usuario que estilo visual quiere:

### Opciones de estilo

1. **Diseño con fondo de color** (recomendado para tarjetas, flyers):
   Fondo en color de marca (gradient o solido) con patrones geometricos
   sutiles, ondas abstractas, o texturas ligeras. Texto en blanco.
   Ejemplo: tarjeta Mercadopago con fondo navy + ondas azul claro.

2. **Fotografico** (recomendado para Meta Ads):
   Foto lifestyle o clinica como elemento principal. Texto superpuesto
   con barras de color de marca para legibilidad.
   Ejemplo: creativos Baby Balance con foto de mama/bebe o fisioterapeuta.

3. **Minimalista sobre blanco** (solo cuando el usuario lo pide):
   Fondo blanco limpio, solo texto y logo. Solo usar cuando el usuario
   explicitamente pide algo limpio/simple.

Si el usuario no especifica, preguntar:
> "¿Como imaginas el estilo visual? Con fondo de color y diseño grafico,
> con fotografia, o minimalista sobre blanco?"

NUNCA generar fondo blanco plano sin preguntar — el resultado se ve
"sin diseño" y el usuario lo rechazara.

### Instrucciones para fondo con diseño

Cuando el estilo sea "fondo de color", incluir en el JSON:

```json
"scene": {
  "type": "graphic design",
  "background": "Solid or gradient background in brand primary color ({hex}).
    Add subtle geometric patterns, abstract wave shapes, or light mesh
    gradients in brand secondary color ({hex}) for visual depth.
    NOT flat — needs visual interest and texture.",
  "mood": "Premium, professional, modern fintech/education/[industry] aesthetic"
}
```

Referencia de estilos que funcionan bien:
- Ondas abstractas (estilo fintech: Stripe, Nubank, Mercadopago)
- Gradientes mesh (estilo tech: Apple, Linear)
- Patrones geometricos sutiles (estilo educacion premium)

## Reglas Criticas para Texto en Espanol

Los modelos de generacion de imagen tienden a omitir diacriticos. Para
mitigarlo:

1. Agregar seccion `text_critical_rules` al JSON con reglas explicitas
2. En el prompt wrapper, repetir: "All Spanish text MUST include proper
   accents: Estimulacion (o con acento), anos (n con tilde)"
3. Listar CADA palabra con acento que debe aparecer en la imagen
4. Aceptar que ~10% de las veces el modelo omitira acentos — esto se
   corrige en 30 segundos en Canva

## Regla de Logo

El modelo tiende a "reinterpretar" logos en vez de copiarlos. Para forzar
el uso del logo real:

**Instruccion obligatoria en el prompt:**

```
MANDATORY LOGO RULE: The uploaded image is the EXACT logo to use.
Do NOT redraw, recreate, simplify, or interpret it. Place the EXACT
uploaded logo image — pixel for pixel, unchanged — in the top-left
corner inside a golden ({color_secundario}) rounded rectangle badge.
The logo shows [descripcion del logo]. Reproduce it EXACTLY.
```

Siempre adjuntar el logo como `inline_data` (base64 PNG) en el primer
part del request.

## Vocabulario Kokoro en Creativos

Aplican las mismas sustituciones que en `/kokoro-ads`:

| Nunca | Siempre |
|-------|---------|
| precio | inversion |
| producto | creacion |
| gratis | cortesia / de regalo |
| descuento | condiciones especiales |
| cliente | invitado |

## Nomenclatura de Archivos Generados

```
clientes/{grupo}/campanas/meta-ads/generated-{NN}-{publico}-{tamano}.png
```

Donde:
- `{NN}` = numero del creativo (01, 02, 03...)
- `{publico}` = slug del publico (mamas, profesionales, brokers...)
- `{tamano}` = cuadrado, vertical, horizontal

Los JSON de especificacion se guardan como:
```
clientes/{grupo}/campanas/meta-ads/json-imagen-{NN}-{publico}.json
```

## Limites y Consideraciones

- **Rate limits tier gratuito**: ~10-15 imagenes/dia. Con billing: ~1000/min.
- **Tamano del request**: El logo en base64 suma ~200KB al request. Normal.
- **Tiempo de generacion**: 20-60 segundos por imagen con Nano Banana Pro.
- **Calidad**: ~90-95% publicable. El 5% restante son acentos y alineacion
  fina que se corrigen en Canva en 2 minutos.
