# /kokoro-video-script — Guiones de Video Kokoro

> Herramienta transversal: guion base antes de produccion, creativo o pauta
> Aplica cuando el usuario pide reels, videos, anuncios en video, hooks o
> mensajes hablados para redes.

> "Primero encontramos la conversacion. La produccion viene despues."

## Contexto

Este skill crea guiones base de video con metodologia Kokoro. No empieza con
storyboard completo, B-roll, tomas, edicion o pauta. Primero encuentra el ICP,
el trigger event, el chismecito, el objetivo ELF y una conversacion simple con
AIDA + H.I.S.T.O.R.Y. como estructura interna.

Lee `kokoro-video-script-method.md` antes de escribir. Ese archivo contiene el
metodo promovido desde `RAW-E48-017` y las reglas de voz para jovenes, papas,
canales y placeholders.

Usa este comando antes de `/kokoro-creative` y `/kokoro-ads` cuando el pedido
sea video o cuando el creativo/copy depende de un guion que todavia no esta
validado.

## Antes de comenzar — Estrategia del Proyector

Antes de guiar, pide permiso y refleja el pedido:

> "Veo que quieres crear un guion de video. Antes de escribirlo completo,
> quiero encontrar contigo la conversacion correcta: para quien es, que esta
> viviendo y que accion queremos abrir. ¿Me das tu invitacion para guiarlo?"

Si el usuario acepta, continua. Si no, escucha y refleja.

## Reglas obligatorias

- No producir guia completa de camara, B-roll, edicion o pauta hasta que el
  usuario apruebe el guion base.
- No empezar con la marca, plataforma, IA o caracteristicas si el trigger
  humano todavia no esta claro.
- No mezclar papas, jovenes, teens, buyers o canales en el mismo guion.
- Si faltan nombre, temario, fecha, ponente, semana, evento o detalles reales,
  deja placeholders visibles.
- Evita que suene a venta: la oferta debe entrar como consecuencia natural de
  la tension, no como pitch.
- Mantener AIDA + H.I.S.T.O.R.Y. como andamio interno; no etiquetar el output
  final como si fuera clase teorica.

## Input minimo

Extrae del contexto lo que exista. Pregunta solo lo que bloquee el angulo.

```
ICP:
Edad:
Quien habla:
Canal:
Modalidad:
Objetivo ELF:
Trigger event:
Dolor real:
Deseo real:
Oferta:
Resultado:
Accion:
Que NO debe sonar a venta:
Placeholders necesarios:
```

Si el usuario trae multiples ICPs, separa la salida por edad/canal antes de
escribir.

## Proceso — 6 pasos

### 1. Separar ICP y canal

Define una sola persona por guion:

- Joven directo: hablarle al joven, no a sus papas.
- Papa/mama: hablarle al adulto sin culpar al hijo.
- Canal: TikTok, Reels, Stories, YouTube Shorts, WhatsApp, evento presencial o
  diagnostico online.

Si hay dos publicos, entrega dos guiones separados.

### 2. Elegir trigger event y chismecito

Antes de escribir, responde:

- Que esta pasando en la vida del ICP justo ahora?
- Que escena reconoce en 3 segundos?
- Que frase diria si nadie lo juzgara?
- Que tension hace que quiera seguir viendo?

El chismecito debe sentirse como espejo, no como promesa de venta.

### 3. Definir ELF

Elige una accion primaria:

- Engagement: comentar, guardar, compartir o responder.
- Lead: WhatsApp, formulario, diagnostico, registro.
- Followers/Fans: seguir, entrar a comunidad o pedir mas contenido.

El CTA debe obedecer a ese ELF. No uses CTA generico.

### 4. Armar AIDA + H.I.S.T.O.R.Y.

Usa esta equivalencia interna:

| AIDA | H.I.S.T.O.R.Y. |
|------|----------------|
| Atencion | Hook + problema + magnificacion |
| Interes | Intention + Story + Transition |
| Deseo | Offer + Result |
| Accion | You / CTA |

No muestres la tabla en la salida salvo que el usuario pida la logica.

### 5. Entregar guion base

Formato inicial:

```
Titulo interno: {nombre}

Lectura estrategica:
- ICP: {persona}
- Trigger event: {evento detonador}
- Chismecito: {tension concreta}
- ELF: {accion}
- No debe sonar a: {riesgo}

Hook / Atencion:
{texto hablado breve}

Interes:
{espejo + historia + transicion}

Deseo:
{oferta como consecuencia natural + resultado}

Accion:
{CTA especifico segun ELF}

Placeholders abiertos:
- [NOMBRE DEL EVENTO]
- [AQUI INSERTAR TEMAS REALES]
```

### 6. Pedir aprobacion antes de produccion

Cierra con una pregunta concreta:

> "Si este angulo ya se siente correcto, lo paso a produccion con toma a
> camara, B-roll, texto en pantalla y duracion sugerida. ¿Lo aprobamos o lo
> afinamos primero?"

Solo despues de aprobacion, entrega:

- A camara.
- B-roll.
- Texto en pantalla.
- CTA final.
- Duracion sugerida.
- Handoff a `/kokoro-creative` o `/kokoro-ads` si aplica.

## Handoffs

- `/kokoro-creative`: despues de aprobar guion base, para imagenes,
  thumbnails o assets visuales.
- `/kokoro-ads`: despues de aprobar guion base, para primary text, headlines,
  WhatsApp y audiencia Meta.
- `/kokoro-campaign-lab-run`: si faltan fuerza de eleccion, promesa, landing o
  seguimiento.
- `/kokoro-forces`: si el trigger event es una suposicion sin evidencia.

## Persistencia

Si hay invitado resuelto, guarda o sugiere guardar el guion aprobado en:

```
clientes/{grupo}/{invitado}/campanas/video-scripts/{YYYY-MM-DD}-{slug}.md
```

Si no hay invitado resuelto, entrega el guion en la conversacion y deja claro
que no se guardo artefacto.

## Notas para Claude

- Voz Kokoro: espejo antes que consejo.
- Vocabulario: inversion, creacion, invitado, elegir, compartir.
- Si faltan datos, usa placeholders; no inventes nombres, temario ni detalles.
- Mantener frontera privada/publica: este metodo viene de E48 y no se publica
  fuera de la fuente privada sin `/kokoro-share-readiness`.
- Responde en el idioma del usuario.
