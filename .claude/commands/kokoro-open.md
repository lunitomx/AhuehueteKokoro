# /kokoro-open — Abrir Sesion con Invitado

> Herramienta transversal: Inicio de trabajo con un invitado
> Aplica en cualquier fase del proceso Kokoro

> "Antes de sembrar, recuerda que sembraste la ultima vez."

## Contexto

Este skill abre una sesion de trabajo con un invitado. Carga su perfil
del grafo, muestra el historial de sesiones recientes, y propone un foco
para hoy basado en lo que quedo pendiente.

Lee el archivo de conocimiento `kokoro-session-log.md` para consultar el
schema del historial de sesiones.

### Resolucion de invitado

1. Si el usuario menciona un nombre, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Carga su perfil completo
   - Lee `metadata["session_log"]` si existe
   - Presenta contexto y propone foco
3. Si NO encuentra al invitado:
   - Pregunta: "No encontre a ese invitado en el grafo. ¿Quieres que lo
     registremos con `/kokoro-client`?"
4. Si no hay `.kokoro/clients.json`:
   - "Aun no hay invitados registrados. Usa `/kokoro-client` para
     crear el primero."

## Instrucciones para la sesion

### Antes de comenzar — Estrategia del Proyector

Si el usuario no menciona un invitado especifico, pregunta:

> "¿Con quien trabajamos hoy?"

Si menciona al invitado, procede directamente.

### Paso 1: Cargar perfil del invitado

Lee `.kokoro/clients.json` y resuelve al invitado. Extrae:

- **name** — nombre del invitado
- **group** — grupo o paraguas
- **description** — esencia del negocio
- **segments** — a quien atiende
- **industry** — sector
- **metadata** — datos clave (colores, sitio web, etc.)

### Paso 2: Cargar historial de sesiones

Lee `metadata["session_log"]` (o `[]` si no existe).

Si hay sesiones anteriores, mostrar las **ultimas 3** en formato resumido.

Si no hay sesiones anteriores, es primera vez con este invitado.

### Paso 3: Presentar contexto

**Si tiene historial (sesiones previas):**

```
## Sesion con {name}

{description}
Segmentos: {segments}

### Ultimas sesiones

| Fecha | Tipo | Que se hizo |
|-------|------|-------------|
| {date_1} | {type_1} | {summary_1} |
| {date_2} | {type_2} | {summary_2} |
| {date_3} | {type_3} | {summary_3} |

### Hallazgos recientes
{hallazgos de la sesion mas reciente como bullets}

### Foco propuesto
{next_action de la sesion mas reciente}

¿Continuamos con esto o tienes otra prioridad hoy?
```

**Si es primera vez:**

```
## Primera sesion con {name}

{description}
Segmentos: {segments}
Industria: {industry}

Es la primera vez que trabajamos con {name}. Algunas opciones
para arrancar:

1. `/kokoro-diagnose` — Diagnostico estrategico (si es un negocio
   que necesita claridad)
2. `/kokoro-ads` — Campana de Meta Ads (si ya tiene algo que
   comunicar)
3. `/kokoro-creative` — Crear material visual (si necesita creativos)
4. `/kokoro-canvas` — Lean Canvas (si necesita modelar el negocio)

¿Que necesita {name} hoy?
```

### Paso 4: Esperar direccion

No avances sin la confirmacion del usuario. Presenta las opciones y
espera. Eduardo no impone — guia solo cuando hay invitacion.

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- Usa "invitado" no "cliente", "creacion" no "producto"
- La apertura debe ser breve — 30 segundos de lectura maximo
- No repitas datos que el usuario ya sabe — se conciso
- Si el invitado tiene muchos datos en metadata, muestra solo lo relevante
  para la sesion, no TODO
- Responde en el idioma del usuario
- IMPORTANTE: Siempre leer clients.json ANTES de presentar cualquier cosa
- IMPORTANTE: Si hay next_action, proponerlo como foco — no inventar otro

## Persistencia

Este skill NO escribe nada. Solo lee. La escritura la hace `/kokoro-close`
al cerrar la sesion.
