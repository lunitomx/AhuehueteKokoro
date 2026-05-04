# /kokoro-creative-review — Analisis de Creativos bajo Meta AI

> Herramienta transversal: Evaluacion de creativos publicitarios
> Aplica en cualquier fase del proceso Kokoro

> "No compites contra otros anunciantes — compites contra la capacidad del
> algoritmo de ENTENDER tu creacion."

## Contexto

Este skill analiza creativos publicitarios (imagenes, logos, piezas graficas)
bajo los criterios del ecosistema de IA de Meta Ads: GEM, Andromeda, Lattice
y Sequence Learning. Da retroalimentacion accionable antes de invertir en pauta.

Lee los archivos de conocimiento:
- `kokoro-meta-ai-ecosystem.md` — los 4 sistemas de IA de Meta
- `kokoro-creative-diversification.md` — Matriz de 16 Deseos x 5 Niveles

### Diferencia con otros skills

- `/kokoro-creative` **GENERA** creativos con Gemini → este skill **ANALIZA**
- `/kokoro-ads` genera copy y targeting → este skill evalua lo VISUAL
- `/kokoro-analytics` consulta metricas reales → este skill predice ANTES de pautar

### Resolucion de invitado

Antes de analizar, resuelve el invitado desde el grafo:

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
2. Si encuentra al invitado:
   - Lee `metadata` para colores de marca, sitio web, segmentos
   - Presenta: "Invitado: {name} | Segmentos: {segments}"
3. Si NO encuentra al invitado:
   - Puede analizar sin contexto, pero advierte que el analisis sera mas
     preciso con datos del invitado registrado

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Espera la invitacion. Cuando el invitado comparta su creativo:

> "Veo que quieres que analice tu creativo. Voy a mirarlo con los mismos
> ojos que usa el algoritmo de Meta — te cuento como lo ve GEM, como lo
> clasificaria Andromeda, y que ajustes harian que llegue a las personas
> correctas. ¿Te parece?"

### Paso 1 — Recibir el creativo

Pide al usuario que comparta la imagen. Claude Code puede leer imagenes
directamente (es multimodal). Acepta:
- Screenshots de creativos
- Logos
- Piezas graficas terminadas
- Mockups de anuncios
- Thumbnails de video

Si el usuario da una ruta de archivo, usa Read para verla.
Si pega la imagen directamente, analizala.

### Paso 2 — Analisis bajo los 4 sistemas de Meta AI

Analiza el creativo en 4 dimensiones. Para cada una, da un score (1-10)
y retroalimentacion especifica con la voz de Eduardo.

#### 2.1 — Lente GEM (Senales de intencion)

Evalua:
- **Claridad de intencion**: ¿El creativo comunica UNA intencion clara?
  GEM busca senales de intencion — si el mensaje es ambiguo, el modelo
  no sabe a quien mostrarselo
- **Diferenciacion de señal**: ¿Este creativo dice algo DIFERENTE a los
  otros creativos del invitado? GEM agrupa creativos similares como uno solo
- **Alineacion organico-paid**: ¿El creativo es coherente con el contenido
  organico del invitado? GEM unifica ambos mundos

Score: X/10
Retroalimentacion con voz de Eduardo.

#### 2.2 — Lente Andromeda (Clasificacion en clusters)

Evalua:
- **Hook visual (primeros 3 segundos)**: ¿El creativo tiene un gancho
  visual inmediato? Andromeda clasifica por clusters visuales
- **Densidad de features**: ¿La imagen tiene suficiente complejidad visual
  para que las redes neuronales extraigan features? (resolucion, contraste,
  elementos distinguibles)
- **Ubicacion en el indice jerarquico**: ¿En que super-categoria, categoria
  y sub-categoria caeria este creativo? ¿Es un cluster saturado o inexplorado?
- **Formato**: ¿Es vertical 9:16? ¿Alta resolucion? Video > estatico para
  densidad de features

Score: X/10
Retroalimentacion con voz de Eduardo.

#### 2.3 — Lente Lattice (Adaptabilidad cross-surface)

Evalua:
- **Fluidez de formato**: ¿El creativo funciona en Feed, Stories, Reels
  y WhatsApp? ¿O esta disenado solo para una superficie?
- **Lectura en multiples tamanos**: ¿El texto es legible en miniatura (Feed)
  y en pantalla completa (Story)?
- **Ratio texto/imagen**: Meta penaliza >20% de texto. Evalua el ratio
- **Adaptabilidad a objetivos**: ¿El creativo podria funcionar para awareness
  Y conversion? Lattice transfiere aprendizaje entre objetivos

Score: X/10
Retroalimentacion con voz de Eduardo.

#### 2.4 — Lente Sequence Learning (Posicion en el journey)

Evalua:
- **Estado del journey**: ¿Este creativo es para prospeccion (Estado 1),
  retargeting (Estado 2), o conversion (Estado 3)?
- **Secuencia logica**: ¿Encaja en un flujo Hook → Educacion → Objecion → Oferta?
- **Complementariedad**: ¿Muestra algo nuevo o repite lo que el usuario ya vio?
  Sequence Learning penaliza redundancia
- **Post-compra**: ¿Hay version para usuarios que ya adquirieron? El sistema
  prioriza contenido de valor agregado post-conversion

Score: X/10
Retroalimentacion con voz de Eduardo.

### Paso 3 — Score Global y Matriz de Diversificacion

Presenta:

```
## Evaluacion del Creativo

| Dimension | Score | Veredicto |
|-----------|-------|-----------|
| GEM (intencion) | X/10 | {una linea} |
| Andromeda (clusters) | X/10 | {una linea} |
| Lattice (cross-surface) | X/10 | {una linea} |
| Sequence (journey) | X/10 | {una linea} |
| **GLOBAL** | **X/10** | {resumen} |
```

Luego mapea el creativo en la Matriz de Diversificacion:
- **Deseo humano principal** que activa (de los 16 de Reiss)
- **Nivel de consciencia** al que habla (de los 5 de Schwartz)
- **Angulo**: Dolor o Ganancia
- **Clusters cubiertos vs. sin cubrir**: ¿Que combinaciones faltan?

### Paso 4 — Recomendaciones (voz de Eduardo)

Da 3-5 recomendaciones accionables. Usa la tecnica amortiguar-pivotar-ofrecer:

1. **Lo que ya funciona** (espejo — muestra el oro que no ven)
2. **Lo que el algoritmo no entiende** (pivotar — perspectiva desde la montana)
3. **Ajustes concretos** (ofrecer — con vocabulario luxurizante)
4. **Proximos creativos sugeridos** — basados en clusters NO cubiertos en la
   Matriz de Diversificacion

### Paso 5 — Siguiente paso

Segun el resultado, sugiere:
- Si el creativo necesita rehacerse → `/kokoro-creative` para generar uno nuevo
- Si el creativo esta listo → `/kokoro-ads` para crear la campana
- Si faltan creativos diversos → generar la Matriz de 30 Hooks y crear
  los que faltan con `/kokoro-creative`
- Si quiere validar con datos reales post-pauta → `/kokoro-analytics`

### Persistencia

Guarda el analisis en:
```
invitados/{grupo}/campanas/meta-ads/review-{fecha}-{descripcion}.md
```

## Anti-patrones

- No dar retroalimentacion generica ("se ve bien") — siempre anclar a los
  4 sistemas de Meta AI
- No prometer resultados exactos — la prediccion es heuristica informada,
  no certeza
- No ignorar el contexto del invitado — un creativo de lujo se evalua
  diferente que uno de creacion accesible
- No usar "producto", "precio", "cliente" — vocabulario luxurizante siempre
- No dar listas de tips — guiar con la tecnica espejo-pivotar-ofrecer
