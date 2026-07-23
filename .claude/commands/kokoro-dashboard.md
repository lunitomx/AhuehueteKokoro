# /kokoro-dashboard — Vista desde la Montana

> Herramienta transversal: genera un dashboard visual privado desde un payload
> sanitizado de Kokoro.

> "No es un tablero para mirar numeros. Es una vista para entender donde esta
> vivo el negocio y cual es el siguiente acto correcto."

## Contexto

Este skill convierte el trabajo de Kokoro en un artefacto visual: una
**Vista desde la Montana** que muestra etapa actual, senales, campanas,
contenido de confianza, seguimiento y siguiente accion.

Lee antes:

- `kokoro-curriculum-five-levels.md` para Raiz, Semilla, Brote, Ramas, Fruto.
- `kokoro-meta-delivery-system.md` si el dashboard
  toca Ramas, Flywheel, follow-up o contenido de enamoramiento.
- `kokoro-share-readiness.md` si el usuario quiere publicar o compartir el
  dashboard fuera de su espacio privado.

## Gate E51 — dashboard privado por defecto

Nunca generes un dashboard visual desde respuestas crudas de MCP, transcripts,
tokens, account IDs, customer IDs, paths privados o screenshots reales sin
sanitizar.

El dashboard debe nacer de un payload compatible con el contrato E51:

- `subject`
- `stage`
- `stages`
- `signals`
- `campaigns`
- `trust_assets`
- `follow_up`
- `next_action`

Si falta esa estructura, primero crea el resumen sanitizado. Si el usuario pide
publicarlo, detente y ejecuta una revision tipo `/kokoro-share-readiness`.

## Gate E52 — workspace local, no hosting

Si el usuario quiere que el dashboard sea una experiencia recurrente o "tipo
producto", no lo vendas como hosting. Inicializa primero el workspace local:

`kokoro dashboard-workspace init --target {proyecto} --project-name "{nombre}"`

Esto crea `.kokoro/dashboard/` con:

- `payloads/` para JSON sanitizado,
- `snapshots/` para historiales privados,
- `exports/` para bundles curados despues de share-readiness,
- `assets/` para visuales locales/offline,
- `manifest.json` declarando `hosting: none`.

El workspace vive en la maquina/proyecto del usuario. No requiere login,
servidor, billing, multi-tenant storage ni sincronizacion remota.

## Gate S52.5 — export curado, no publicacion automatica

Si el usuario quiere compartir un dashboard fuera de su workspace privado, usa
un bundle local curado, no el snapshot privado directo:

`kokoro dashboard-workspace export --target {proyecto} --share-readiness-ok`

Antes de ejecutar, confirma que ya se hizo `/kokoro-share-readiness`. El export
rechaza payloads con `subject.privacy_level: private`; para usuarios reales debe
existir primero un payload `curated-public`.

El bundle queda en `exports/` dentro del workspace local. No sube archivos, no
crea galeria publica, no manda datos a hosting y no convierte el dashboard en
SaaS.

## Proceso

### Paso 1: Diagnosticar etapa

Determina si la lectura principal es:

| Etapa | Senal |
|---|---|
| Raiz | Falta diagnostico, claridad, modelo economico o verdad del negocio. |
| Semilla | Falta segmento, promesa, creacion, modelo o evidencia de viabilidad. |
| Brote | Hay validacion, PESCAR, experimentos o campanas de aprendizaje. |
| Ramas | Hay pauta, contenido, Flywheel, storytelling, retargeting o seguimiento. |
| Fruto | Solo soporte operativo o brecha conocida hasta tener fuente formal M5. |

### Paso 2: Crear payload sanitizado

Resume solo lo que pueda vivir en un dashboard privado:

- lectura estrategica,
- evidencia agregada,
- campanas como experimentos,
- gaps de confianza,
- estado de seguimiento,
- siguiente accion.

No incluyas IDs de cuentas, tokens, rutas privadas, transcripts crudos ni
respuestas completas de plataformas.

### Paso 3: Renderizar artefacto

Si estas operando en el repo con CLI disponible, usa:

`kokoro dashboard --input {payload.json} --output {directorio_salida}`

Para preparar un espacio local recurrente antes de generar dashboards reales:

`kokoro dashboard-workspace init --target {proyecto} --project-name "{nombre}"`

Si no hay CLI disponible, entrega el payload y la indicacion de render para que
el operador lo ejecute.

### Paso 4: Presentar lectura

Devuelve la ubicacion del artefacto y una lectura breve.

## Plantilla de Salida

```
## Vista desde la Montana — {invitado}

| Seccion | Estado |
|---|---|
| Etapa actual | {Raiz/Semilla/Brote/Ramas/Fruto} |
| Payload sanitizado | {creado/validado} |
| Artefacto HTML | {ruta o pendiente} |
| Privacidad | {privado/sintetico/curated-public} |

### Lectura Kokoro

{2-4 lineas: que esta vivo, que esta bloqueado, que no debe escalar todavia}

### Siguiente accion correcta

{accion primaria}

### No incluido

- Respuestas crudas de plataformas.
- Account IDs, tokens o rutas privadas.
- Raw transcripts.
- Publicacion sin share-readiness.

### Siguiente paso

- `/kokoro-scorecard` para actualizar metricas.
- `/kokoro-rhythm` para convertir la vista en ritual semanal.
- `/kokoro-share-readiness` si se quiere publicar una version curada.
```

## Notas

- Usa "invitado", "creacion" e "inversion".
- No vendas el dashboard como Fruto/Modulo 5 completo.
- La promesa es claridad visual y accion consciente, no vigilancia permanente.
