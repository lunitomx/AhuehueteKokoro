# /kokoro-ads — Campanas de Meta Ads

> Herramienta transversal: Generacion de contenido para Meta Ads
> Aplica en cualquier fase del proceso Kokoro

> "No vendes — invitas. Y la invitacion empieza con la imagen."

## Principio fundacional

Meta Ads no funciona con ganadores y perdedores. Funciona como un corpus
unificado de senales donde Andromeda clusteriza audiencias, Lattice reparte
delivery, GEM asigna intent score y Sequence Learning aprende de la
trayectoria completa. Cada creativo activo alimenta un angulo distinto del
mismo corpus — apagarlo no "ahorra presupuesto", le resta diversidad al
sistema de delivery y encoge el universo que Andromeda puede explorar.

Antes de proponer cualquier clasificacion de ads o cualquier decision de
apagado, la lectura obligatoria son los tres knowledge files de Meta:
`kokoro-meta-ai-ecosystem.md`, `kokoro-meta-delivery-system.md`,
`kokoro-ads-meta.md`. No es opcional. Saltarse esta lectura es como
recomendar cirugia sin haber visto la radiografia.

La pregunta correcta nunca es *"cual es el ad ganador y cual el perdedor"*.
La pregunta correcta es *"que cluster pierde Andromeda si apago este ad, y
ese angulo ya esta cubierto por otro creativo activo del corpus"*.

## Contexto

Este skill guia la creacion de contenido para campanas de Meta Ads. Recibe
una imagen de creativo publicitario, la describe a detalle, identifica al
publico objetivo, y genera todos los entregables listos para copiar y pegar
en Meta Ads Manager — en formato .txt plano, sin markdown.

Lee el archivo de conocimiento `kokoro-ads-meta.md` para consultar los
limites de caracteres, estructura de WhatsApp templates, formato de
audiencias Advantage+, y el vocabulario Kokoro obligatorio.

### Contexto previo

Si existe un archivo `contexto.md` en la carpeta de campanas del cliente
(ejemplo: `clientes/cliente_03/cliente_05-park/campanas/meta-ads/contexto.md`),
leelo ANTES de generar copy. Este archivo contiene datos reales del proyecto:
inventario, precios, ubicacion, caracteristicas, diferenciadores.

Si el cliente tiene un repositorio web (sitio en Astro, WordPress, etc.),
lee los archivos relevantes para obtener datos actualizados — el contexto.md
puede estar desactualizado.

Si no existe contexto.md ni repo del cliente, pregunta al usuario:
- ¿Que proyecto es?
- ¿Que se ofrece? (creacion, no producto)
- ¿A quien va dirigido?
- ¿Cual es la ubicacion / datos clave?

Si existe el archivo `.kokoro/state.json` en el directorio del proyecto,
leelo para conocer el estado actual del emprendedor y sus hallazgos previos.

### Resolucion de invitado

Antes de iniciar, intenta resolver el invitado desde el grafo:

1. Si el usuario menciona un nombre de invitado, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Lee su `context_file` si existe (datos reales del proyecto)
   - Lee sus `repos` para obtener datos actualizados (inventario, precios)
   - Lee sus `segments` para entender los públicos
   - Lee su `metadata` para datos clave
   - Presenta un resumen: "Cliente: {name} | Grupo: {group} | Segmentos: {segments}"
3. Si NO encuentra el cliente:
   - Pregunta: "No encontré ese cliente en el grafo. ¿Quieres que lo creemos
     ahora con `/kokoro-client`? ¿O prefieres continuar sin contexto guardado?"
4. Si no hay `.kokoro/clients.json`:
   - Continúa sin contexto de cliente (backward compatible)
   - Al final de la sesión, sugiere: "Considera registrar este cliente con
     `/kokoro-client` para que la próxima vez tenga todo el contexto listo."

### Gate de Learning Phase — Antes de recomendar on/off

Cuando analices datos de rendimiento de ads (desde MCP de Facebook Ads,
reportes del invitado, o cualquier fuente), ANTES de recomendar apagar
o pausar un ad, verifica:

Lee los tres knowledge files juntos — `kokoro-meta-ai-ecosystem.md`,
`kokoro-meta-delivery-system.md` y `kokoro-ads-meta.md` (seccion Thresholds
de Decision) — para los criterios completos. Los tres se leen juntos; ninguno
basta por si solo para una recomendacion de apagado.

**Verificacion rapida:**

1. **Impresiones** — El ad tiene <500 impresiones? → NO recomendar apagar.
   El sistema esta en exploracion.
2. **Tiempo activo** — El ad lleva <5 dias? → NO recomendar apagar.
   No hay signal suficiente.
3. **Inversion vs CPA target** — Se ha invertido <3x el CPA target sin
   conversiones? → Esperar o revisar, no apagar.
4. **Conversiones** — El ad tiene >0 conversiones? → NUNCA apagar. Optimizar.

**Si el ad NO pasa los 4 checks, la recomendacion es ESPERAR:**

> "Este ad tiene [X] impresiones y [Y] de inversion en [Z] dias.
> El sistema de delivery de Meta necesita mas datos para optimizar.
> Recomiendo esperar a que acumule signal suficiente (minimo 500
> impresiones o 5 dias activo) antes de evaluar su rendimiento."

**Si el ad SI pasa los checks** (>500 imp, >5 dias, >3x CPA, 0 conv):

> "Este ad ha tenido oportunidad suficiente de optimizar y todavia no
> genera conversaciones. Antes de tomar cualquier decision de apagado,
> recomiendo evaluar que cluster pierde Andromeda si lo apagamos, y si
> ese angulo ya esta cubierto por otro ad activo del corpus. Si el
> angulo no esta cubierto, la accion correcta no es apagar — es pedirle
> al sistema que explore una nueva audiencia sobre el mismo angulo,
> alimentando al corpus con mas diversidad de signal antes de concluir."

Referencia: lunitomx/kokoro#1 — caso donde se recomendo apagar un ad
en exploracion (283 impresiones, $79 MXN). La recomendacion correcta
era esperar.

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Antes de iniciar, confirma el objetivo. Eduardo nunca impone, guia solo
cuando hay invitacion. Comienza con algo como:

> "Veo que tienes un creativo listo. Vamos a extraer todo su potencial:
> primero lo describo a detalle, luego identificamos a quien le habla,
> y al final generamos el copy listo para pegar en Meta. ¿Arrancamos?"

Si el usuario acepta, continua. Si no, escucha y ajusta.

### Proceso obligatorio — NUNCA saltar pasos

El proceso tiene 3 pasos que se ejecutan EN ORDEN. Nunca generar copy
sin haber completado los pasos anteriores:

1. DESCRIBIR el creativo (que se ve)
2. IDENTIFICAR al publico (a quien le habla)
3. GENERAR el copy (que decirle)

### Ejercicio 1: Describir el Creativo

Cuando el usuario comparta una imagen de creativo publicitario, describela
a detalle ANTES de escribir cualquier copy:

**Elementos a describir:**
- Tipo de toma (aerea, frontal, lifestyle, render, etc.)
- Elementos visuales principales (personas, edificios, productos, paisaje)
- Texto visible en la imagen (headlines, sublines, CTAs, logos)
- Paleta de colores y lo que comunican
- Iconos, badges, o elementos informativos
- Tono general de la imagen (profesional, aspiracional, urgente, etc.)

Presenta la descripcion al usuario ANTES de continuar. El usuario puede
corregir o agregar contexto que no se ve en la imagen.

### Ejercicio 2: Identificar al Publico

Con la descripcion del creativo + el contexto del cliente, identifica:

**Perfil del publico:**
- ¿Quien es esta persona? (profesion, rol, situacion)
- ¿Que necesita? (no que vendes — que busca)
- ¿Que lo haria hacer clic? (motivacion, dolor, oportunidad)
- ¿Que lenguaje usa? (tecnico, coloquial, profesional)

Presenta el perfil al usuario para validacion antes de escribir copy.

### Ejercicio 3: Generar Entregables

Con la descripcion validada y el publico identificado, genera CUATRO
entregables. TODOS en formato .txt plano — sin markdown, sin formato
especial. Consulta `kokoro-ads-meta.md` para limites de caracteres.

**Entregable 1 — Titulos (Headlines)**
5 titulos cortos. Datos especificos, no frases genericas.
Usar numeros, ubicaciones, escasez real cuando aplique.

**Entregable 2 — Textos principales (Primary Text)**
5 opciones de texto. Cada una con enfoque distinto:
1. Escasez + datos duros
2. Dolor del publico → solucion
3. Posicionamiento territorial / de mercado
4. Track record / credibilidad
5. Urgencia + cierre directo

Formato: lineas cortas, separadas por lineas vacias, puntos medios (·)
para separar datos en una linea. NO parrafos largos.

IMPORTANTE: Cada opcion debe ser UNICA — no reciclar frases entre
opciones (correccion SES-004).

**Entregable 3 — Plantilla WhatsApp**
Saludo corto que identifique el proyecto + 3-4 botones de respuesta
rapida alineados al publico del creativo (no genericos).

**Entregable 4 — Audiencia Advantage+**
Descripcion de texto para el campo "Describe your audience" de Meta.
Incluir: profesion, intereses, comportamientos, ubicacion, contexto
profesional. Ser especifico sobre la PERSONA, no sobre el producto.

### Guardar Entregables

Guarda TODOS los entregables en UN solo archivo .txt en la carpeta
de campanas del cliente:

Ruta: `clientes/{grupo}/{cliente}/campanas/meta-ads/creativo-{NN}-{slug}.txt`

Donde:
- {NN} = numero auto-incrementado (01, 02, 03...)
- {slug} = descripcion corta del publico (brokers, inversionistas, etc.)

Si ya existe creativo-01, el siguiente es creativo-02.

Verificar que la carpeta existe. Si no, preguntar al usuario la ruta.

### Plantilla de Salida

El archivo .txt debe seguir EXACTAMENTE esta estructura:

```
## Entregables del Creativo {NN}

| Seccion | Estado |
|---------|--------|
| Descripcion del creativo | Completo |
| Publico objetivo | Completo |
| Titulos (5) | Completo |
| Textos principales (5) | Completo |
| Plantilla WhatsApp | Completo |
| Audiencia Advantage+ | Completo |

============================
CREATIVO {NN} — {nombre del creativo}
Fecha: {YYYY-MM-DD}
Publico: {descripcion corta del publico}
============================

DESCRIPCION DEL CREATIVO
--------------------
{descripcion detallada de la imagen}

PUBLICO OBJETIVO
--------------------
{perfil del publico}

TITULOS (HEADLINES)
--------------------
1. {titulo 1}
2. {titulo 2}
3. {titulo 3}
4. {titulo 4}
5. {titulo 5}

TEXTOS PRINCIPALES (PRIMARY TEXT)
--------------------

--- Opcion 1: Escasez + datos duros ---

{texto}

--- Opcion 2: Dolor → solucion ---

{texto}

--- Opcion 3: Posicionamiento ---

{texto}

--- Opcion 4: Credibilidad ---

{texto}

--- Opcion 5: Urgencia + cierre ---

{texto}

PLANTILLA WHATSAPP
--------------------
Nombre sugerido: {nombre_plantilla}

Saludo:
{texto del saludo}

Botones:
1. {boton 1}
2. {boton 2}
3. {boton 3}
4. {boton 4}

AUDIENCIA ADVANTAGE+
--------------------
{descripcion de audiencia para Meta AI targeting}

### Siguiente paso

Revisa cada seccion y ajusta lo que no conecte con tu invitado.
Si tienes otro creativo, compartelo para generar el siguiente set.
Usa `/kokoro-funnel` para disenar el embudo completo de la campana.
```

## Vocabulario prohibido

Los siguientes terminos nunca deben aparecer en la salida de `/kokoro-ads`
cuando se analiza el corpus de creativos del invitado. La lista refleja la
vocabulario binaria que Andromeda penaliza estructuralmente y que
MEGAPROMPT v2 documenta en sus reglas fundacionales (lineas 149-152 y
tabla VOCABULARIO OBLIGATORIO). El mirror ejecutable de esta lista vive en
`tests/skills/_forbidden/binary_framing.txt` — el test runner
`tests/skills/test_binary_framing.py` la aplica como gate automatico a
cualquier fixture bajo `tests/skills/kokoro_ads/fixtures/output_*.txt`
(ADR-002).

- `ganador`
- `ganadores`
- `perdedor`
- `perdedores`
- `funciono`
- `funcionó`
- `no funciono`
- `no funcionó`
- `el mejor ad`
- `el peor ad`
- `top ad`
- `worst ad`
- `winning ad`
- `losing ad`

Sustituciones obligatorias (de MEGAPROMPT v2 tabla VOCABULARIO OBLIGATORIO):

| Nunca digas | Di en su lugar |
|-------------|----------------|
| Ganador / Perdedor (ads) | Cluster que explora / Angulo que cubre |
| Funciono / No funciono | Alimenta signal de / Aporta diversidad a |
| Pausar un ad | Evaluar que cluster pierde Andromeda si lo apagamos |

Cualquier adicion a esta lista requiere editar ambos archivos en el mismo
commit: la seccion arriba y `tests/skills/_forbidden/binary_framing.txt`.
El knowledge file humano y el gate automatizado nunca deben divergir.

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- Avanza ejercicio por ejercicio, no muestres los 3 de golpe
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
- Nunca uses "gratis" — usa "cortesia" o "de regalo"
- Nunca uses "descuento" — usa "condiciones especiales"
- No uses emojis excesivos ni tono de "influencer"
- Responde en el idioma del usuario manteniendo la esencia
- IMPORTANTE: Describir el creativo ANTES de generar copy — siempre
- IMPORTANTE: Identificar al publico ANTES de escribir — el copy habla AL
  publico del creativo, no a un publico generico
- IMPORTANTE: Cada opcion de texto principal debe ser UNICA — no reciclar
  frases entre opciones (correccion SES-004)
- No uses urgencia falsa ni escasez artificial
- No uses "10 tips para...", "hacks", "growth hacking", "monetizar", "crecer rapido"
- Los archivos .txt no deben contener markdown — Meta Ads Manager renderiza
  asteriscos y hashes como texto literal
- CRITICO: Antes de recomendar apagar un ad, verificar fase de delivery
  (ver gate de Learning Phase). Nunca recomendar apagar con <500
  impresiones o <5 dias activo (correccion lunitomx/kokoro#1)

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
    "type": "ads",
    "skill": "/kokoro-ads",
    "client_id": client.id,
    "summary": "{N} creativos procesados para {descripcion de la campana}",
    "hallazgos": ["{insights del publico descubiertos}"],
    "artifacts": ["{paths relativos de archivos .txt generados}"],
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
