<!-- kokoro-managed: do not edit, will be overwritten by kokoro init -->
# Meta Ads — Especificaciones y Vocabulario Kokoro

> Skill: `/kokoro-ads`
> Herramienta transversal: aplica en cualquier fase

> "La forma de comunicar define tu categoria mas que la creacion misma."

## Proposito

Referencia tecnica para el skill `/kokoro-ads`. Documenta los limites de
caracteres de Meta Ads, la estructura de plantillas WhatsApp Business, el
formato de audiencias Advantage+, el vocabulario Kokoro obligatorio para
copy publicitario, y las reglas de formato de salida.

## Meta Ads — Limites de Caracteres

### Titulares (Headlines)

- Maximo: 40 caracteres
- Recomendado: 25 caracteres (lo que se muestra sin corte)
- Mejores practicas:
  - Datos especificos: numeros, ubicaciones, escasez real
  - Beneficio directo, no descripcion del producto
  - Vocabulario Kokoro (ver tabla abajo)
  - Sin signos de exclamacion excesivos
  - Sin MAYUSCULAS completas (parece spam)

### Texto Principal (Primary Text)

- Visible antes de "Ver mas": 125 caracteres
- Maximo total: 2000 caracteres
- Mejores practicas:
  - Primera linea = hook (lo unico que se ve sin expandir)
  - Lineas cortas separadas por lineas vacias
  - Puntos medios (·) para separar datos en una linea
  - Numeros y datos especificos, no frases vagas
  - Sin parrafos largos — formato de lectura movil
  - Cada opcion de texto debe ser UNICA — no reciclar frases entre opciones

### Descripcion (Description)

- Maximo: 30 caracteres
- Solo visible en algunos placements (feed, no stories)
- Usar para refuerzo de CTA o dato clave

### Formato de Imagen

- Feed: 1080 x 1080 px (cuadrado)
- Stories / Reels: 1080 x 1920 px (vertical)
- Ratio de texto en imagen: menos del 20% para mejor alcance

## WhatsApp Business — Estructura de Plantilla

### Componentes

1. **Mensaje de saludo**: corto, identifica el proyecto, establece propuesta
   de valor. Maximo 1024 caracteres pero se recomienda menos de 160.

2. **Botones de respuesta rapida**: 3-4 botones maximo
   - Cada boton: maximo 20 caracteres
   - Orientados a accion, no a caracteristicas
   - Mapeados a la intencion del invitado (no del vendedor)
   - Ejemplos buenos: "Agendar visita", "Ver disponibilidad", "Conocer inversiones"
   - Ejemplos malos: "Producto A", "Producto B", "Info general"

### Reglas de Aprobacion

- Sin emojis excesivos en el saludo
- Sin urgencia falsa ("ULTIMA OPORTUNIDAD")
- Sin variables no resueltas
- Tono profesional pero cercano

## Advantage+ — Descripcion de Audiencia

### Formato

Campo de texto libre para Meta AI targeting. No son demograficos
tradicionales — es una descripcion de la PERSONA.

### Estructura Recomendada

```
[Profesion / Rol] que [comportamiento o situacion]. Interesados en
[intereses relevantes]. Ubicados en [zona geografica]. Con experiencia
en [contexto profesional]. Buscan [necesidad o motivacion].
```

### Mejores Practicas

- Ser especifico sobre la PERSONA, no sobre el producto
- Incluir: profesion, intereses, comportamientos, ubicacion, contexto profesional
- Incluir: titulos de puesto, industria, nivel de experiencia
- No incluir: descripcion del producto, caracteristicas, precios
- Pensar: "¿quien es esta persona un martes a las 10am?"
- Longitud recomendada: 150-300 caracteres

## Vocabulario Kokoro para Ads

El vocabulario define la categoria. Estas sustituciones son OBLIGATORIAS
en todo copy generado por `/kokoro-ads`:

| Nunca uses | Usa en su lugar |
|------------|-----------------|
| precio | **inversion** |
| producto | **creacion** |
| gratis | **cortesia** / **de regalo** |
| descuento | **condiciones especiales** |
| cliente | **invitado** / **persona** |
| comprar | **adquirir** / **elegir** |
| barato | **accesible** |
| vender | **compartir** / **invitar** |
| problema | **oportunidad** / **reto** |
| gastar | **invertir** |

### En Ingles

| Never use | Use instead |
|-----------|-------------|
| price | **investment** |
| product | **creation** |
| free | **complimentary** / **as a gift** |
| discount | **special conditions** |
| customer / client | **guest** / **person** |
| buy | **choose** / **select** |
| cheap | **accessible** |
| sell | **share** / **invite** |
| problem | **opportunity** / **challenge** |
| spend | **invest** |

## Reglas de Formato de Salida

### Formato Obligatorio

- TODOS los entregables en archivos `.txt` plano
- SIN formato markdown (sin `**`, sin `##`, sin `|tablas|`)
- Usar lineas vacias y separadores `====` / `----` para estructura
- Los archivos deben poder copiarse y pegarse directamente en Meta Ads Manager
- Cada seccion de entregable separada por encabezados con `====`

### Nomenclatura de Archivos

```
clientes/{grupo}/{cliente}/campanas/meta-ads/creativo-{NN}-{slug}.txt
```

Donde:
- `{NN}` = numero auto-incrementado (01, 02, 03...)
- `{slug}` = descripcion corta del publico (brokers, inversionistas, etc.)
- Si ya existe `creativo-01`, el siguiente es `creativo-02`

### Estructura del Archivo .txt

```
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
```

## Thresholds de Decision — Cuando Apagar o Pausar un Ad

Para el contexto completo del sistema de delivery de Meta (fases, mecanica
de Andromeda/GEM/Lattice, resets de learning phase, budget minimos), ver
`kokoro-meta-delivery-system.md`.

Esta seccion es una referencia rapida de decision para el skill `/kokoro-ads`.

### Tabla de Decision

| Situacion | Threshold | Accion |
|-----------|-----------|--------|
| Ad en exploracion (<500 impresiones, <3 dias) | Cualquier metrica | ESPERAR — datos insuficientes |
| Ad en learning temprano (<500 imp, 3-5 dias) | <1x CPA invertido | ESPERAR — sin signal |
| Ad en learning (500-2000 imp, 5-7 dias, 0 conv) | 1-2x CPA | REVISAR copy/targeting, no apagar |
| Ad en learning (500-2000 imp, 5-7 dias, 0 conv) | 2-3x CPA | SOFT PAUSE — revisar antes de reactivar |
| Ad con signal suficiente (>2000 imp, >5 dias, 0 conv) | >3x CPA | HARD KILL — no convierte |
| Ad con conversiones, <5 dias | Cualquier CPA | ESPERAR — hay signal positiva |
| Ad en optimizacion (>7 dias, conversiones) | CPA >30% arriba del target | OPTIMIZAR — ajustar, no apagar |

### Regla de Oro

> **NUNCA recomendar apagar un ad que no ha salido de learning phase.**
> Si las impresiones son <500 o el tiempo activo es <5 dias, la accion
> default es ESPERAR. El sistema de delivery de Meta necesita volumen
> minimo para optimizar. Apagar antes de tiempo es desperdiciar la
> inversion en datos que nunca llegaron a madurar.

### Referencia cruzada

Para el sistema completo de delivery (fases, resets, budget minimos),
ver `kokoro-meta-delivery-system.md`.

## Anti-patrones

### Formato

- **No markdown en archivos de salida** — Meta Ads Manager renderiza asteriscos
  y hashes como texto literal. Nunca uses `**`, `##`, ni `|tablas|` en los .txt
- **No emojis** — salvo que el invitado los solicite explicitamente
- **No copiar-pegar entre variaciones** — cada opcion de texto debe ser unica
  y con enfoque distinto (correccion SES-004)

### Contenido

- **No "10 tips para..."** — Eduardo no da tips, guia procesos
- **No hacks, growth hacking, monetizar, escalar rapido** — vocabulario prohibido
- **No urgencia falsa** — "ULTIMO DIA!!!" destruye credibilidad
- **No escasez artificial** — solo usar escasez cuando es real y verificable
- **No promesas sin proceso** — "duplica tus ventas en 30 dias" esta prohibido
- **No copy centrado en el vendedor** — centrar siempre en el invitado

### Proceso

- **No generar copy sin describir el creativo primero** — el copy nace de la
  imagen, no al reves (feedback_meta_ads_process.md)
- **No saltar la identificacion de publico** — el copy habla AL publico del
  creativo, no a un publico generico
- **No ignorar el contexto del invitado** — leer contexto.md o preguntar datos
  antes de generar cualquier entregable
