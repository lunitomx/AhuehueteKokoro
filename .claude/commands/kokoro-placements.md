# /kokoro-placements — Analisis de Ubicaciones de Meta Ads

> Herramienta transversal: Analisis de rendimiento por placement y
> recomendaciones de optimizacion
> Aplica en cualquier fase del proceso Kokoro (principalmente Fase 4)

> "No todos los escenarios merecen tu creacion. Elige donde brillas."

## Contexto

Este skill analiza el rendimiento de una campana de Meta Ads desglosado por
ubicacion (placement), y recomienda cuales apagar, cuales mantener, y por que.
No es un skill de creacion de contenido — es de optimizacion de distribucion.

Lee los archivos de conocimiento de placements para entender QUE ES cada
ubicacion visualmente y contextualmente:
- `meta-ads-placements-feeds.md` — 11 placements de Feeds
- `meta-ads-placements-stories-reels.md` — 7 placements de Stories/Reels
- `meta-ads-placements-instream-reels.md` — 2 placements de Instream
- `meta-ads-placements-other.md` — Mensajes de marketing, Audience Network

Lee tambien:
- `kokoro-meta-delivery-system.md` — Sistema de delivery de Meta
- `kokoro-ads-meta.md` — Thresholds de decision y learning phase

### Flujo complementario

- `/kokoro-ads` crea la campana (copy + targeting)
- `/kokoro-creative` genera el creativo (imagen)
- `/kokoro-placements` optimiza la distribucion (este skill)
- `/kokoro-analytics` consulta las metricas

### Resolucion de invitado

Antes de iniciar, intenta resolver el invitado desde el grafo:

1. Si el usuario menciona un nombre de invitado, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Lee su `context_file` si existe
   - Lee sus `segments` para entender los publicos
   - Presenta: "Invitado: {name} | Grupo: {group}"
3. Si NO encuentra: continua sin contexto de invitado

### Fuentes de datos

El skill puede recibir datos de rendimiento de tres formas:

1. **MCP de Facebook Ads** — Si el servidor `facebook-ads` esta disponible,
   consultar directamente los datos de la campana
2. **Screenshot/tabla** — El usuario pega una captura de pantalla o tabla de
   Ads Manager con el desglose por ubicacion
3. **Datos manuales** — El usuario dicta los numeros verbalmente

Siempre pregunta: "¿Como quieres compartir los datos? ¿Tienes acceso al
Ads Manager conectado, o prefieres pegar una captura de pantalla?"

## Regla critica: Gasto limitado en ubicaciones excluidas

**SIEMPRE avisar al invitado sobre esta configuracion:**

> En Meta Ads Manager existe una opcion llamada **"Permitir un gasto limitado
> en ubicaciones excluidas"** que viene ACTIVADA por defecto. Esta opcion
> destina hasta un 5% del presupuesto a cada ubicacion que hayas excluido
> cuando Meta considera que hay probabilidades de mejorar el rendimiento.
>
> **Recomendacion Kokoro: SIEMPRE desactivar esta opcion.**
>
> Si el invitado decidio excluir un placement, esa decision debe respetarse.
> Un 5% por placement excluido puede sumar 20-30% del presupuesto total
> yendose a ubicaciones que conscientemente se descartaron.

Al inicio de cada sesion de este skill, preguntar:

> "Antes de analizar — ¿tienes activada la opcion de 'gasto limitado en
> ubicaciones excluidas'? Esta viene prendida por defecto y puede estar
> enviando hasta 5% de tu presupuesto a cada placement que apagaste.
> Si esta activa, el primer paso es apagarla."

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

> "Veo que quieres entender donde esta rindiendo tu campana y donde no.
> Vamos a revisar cada ubicacion, entender que experiencia visual tiene
> tu invitado en cada una, y decidir con criterio cuales apagar.
> ¿Arrancamos?"

### Gate de Learning Phase — ANTES de recomendar apagar

**Verificacion obligatoria por cada placement antes de recomendar off:**

1. **Impresiones** — El placement tiene <500 impresiones? → NO recomendar
   apagar. El sistema esta en exploracion.
2. **Tiempo activo** — El placement lleva <5 dias? → NO recomendar apagar.
   No hay signal suficiente.
3. **Inversion vs CPA target** — Se ha invertido <3x el CPA target sin
   conversiones? → Esperar o revisar, no apagar.
4. **Conversiones** — El placement tiene >0 conversiones? → NUNCA apagar.
   Optimizar.

Si un placement NO pasa los 4 checks, la recomendacion es ESPERAR, no apagar.

### Proceso de analisis — 4 pasos

#### Paso 1: Recopilar datos por placement

Obtener estos datos para CADA placement activo:
- Impresiones
- Alcance
- Clics (todos)
- CTR
- CPC
- Conversiones (si aplica)
- Costo por conversion (si aplica)
- Inversion total
- Dias activo

#### Paso 2: Clasificar cada placement

Para cada placement con datos suficientes (pasa el gate de learning phase),
clasificar en una de 4 categorias:

| Categoria | Criterio | Accion |
|-----------|----------|--------|
| **Estrella** | CTR alto + conversiones + CPC bajo | Mantener y considerar aumentar presupuesto |
| **Trabajador** | CTR medio + algunas conversiones | Mantener, monitorear |
| **Explorador** | Pocas impresiones, datos insuficientes | Esperar — no hay signal |
| **Drenaje** | CTR bajo + 0 conversiones + CPC alto + >500 imp + >5 dias | Apagar |

#### Paso 3: Contextualizar con conocimiento visual

Para cada placement clasificado como "Drenaje", explicar POR QUE no funciona
usando el conocimiento visual de los archivos de placements:

**Ejemplo:**
> "Facebook Right Column esta drenando presupuesto. Tiene sentido: es un
> banner lateral pequeño en desktop, formato horizontal 1.91:1. Tu creativo
> esta optimizado para vertical 4:5 — al comprimirse a horizontal pierde
> todo su impacto visual. Ademas, es el placement con menor inmersion de
> toda la familia Feeds. Recomiendo apagar."

**Ejemplo de esperar:**
> "Instagram Explore Home tiene solo 180 impresiones en 3 dias. Este
> placement muestra tu creativo como un thumbnail en la grilla de Explore —
> sin texto, sin branding, pura imagen. Necesita mas tiempo para generar
> signal. Esperemos al menos 500 impresiones antes de evaluar."

#### Paso 4: Generar recomendaciones

Presentar una tabla resumen con la recomendacion por placement:

```
ANALISIS DE UBICACIONES — {nombre de la campana}
Fecha: {YYYY-MM-DD}
Invitado: {nombre}
=============================================

RESUMEN EJECUTIVO
-----------------
Placements activos: {N}
Estrellas: {N} — mantener
Trabajadores: {N} — monitorear
Exploradores: {N} — esperar
Drenajes: {N} — apagar

GASTO LIMITADO EN EXCLUIDAS
----------------------------
Estado: {activo/inactivo}
Recomendacion: DESACTIVAR siempre

DETALLE POR PLACEMENT
----------------------

✓ MANTENER — {placement}
  Impresiones: {N} | CTR: {X%} | CPC: ${X} | Conv: {N}
  Razon: {explicacion usando conocimiento visual}

⏸ ESPERAR — {placement}
  Impresiones: {N} | CTR: {X%} | CPC: ${X} | Conv: {N}
  Razon: {menos de 500 imp o menos de 5 dias}

✗ APAGAR — {placement}
  Impresiones: {N} | CTR: {X%} | CPC: ${X} | Conv: {N}
  Razon: {explicacion usando conocimiento visual}

PRESUPUESTO RECUPERADO
----------------------
Al apagar {N} placements, se recuperan ${X} que se redistribuyen
automaticamente hacia las ubicaciones estrella.

SIGUIENTE PASO
--------------
{recomendacion de accion inmediata}
```

### Cuando el creativo no encaja en un placement

Usar el conocimiento visual para detectar incompatibilidades de formato:

| Problema | Ejemplo |
|----------|---------|
| Creativo vertical en placement horizontal | 4:5 en Right Column (1.91:1) |
| Creativo sin audio en Reels | Reels espera sonido, Stories puede ser mudo |
| Creativo con mucho texto en Explore Home | Explore Home es solo thumbnail, sin copy |
| Creativo formal en Threads | Threads es conversacional, no corporativo |
| Creativo generico en Profile Feed | Profile Feed tiene expectativa de relevancia dirigida |

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
- CRITICO: Verificar gate de learning phase ANTES de recomendar apagar
- CRITICO: Avisar sobre "gasto limitado en ubicaciones excluidas" SIEMPRE
- Contextualizar cada recomendacion con el conocimiento visual del placement
- No recomendar apagar un placement solo porque tiene CTR bajo — verificar
  impresiones, tiempo, y conversiones primero
- Si el invitado quiere apagar todo y dejar solo 1-2 placements, advertir
  que Meta optimiza mejor con al menos 4-6 placements activos
- No usar lenguaje de urgencia falsa ("apaga YA", "estas perdiendo dinero")
- Ser honesto cuando no hay datos suficientes: "Necesitamos mas tiempo"
- Referencia: lunitomx/kokoro#1 — caso donde se recomendo apagar un ad
  en exploracion. La recomendacion correcta era esperar.

## Persistencia

### Session Log (si hay invitado resuelto)

Si se resolvio un invitado del grafo al inicio del skill, registrar la
sesion en su session_log al terminar.

```python
entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "placements",
    "skill": "/kokoro-placements",
    "client_id": client.id,
    "summary": "Analisis de {N} placements: {N} mantener, {N} apagar, {N} esperar",
    "hallazgos": ["{insights del analisis}"],
    "artifacts": [],
    "next_action": "{siguiente paso}"
}
```
