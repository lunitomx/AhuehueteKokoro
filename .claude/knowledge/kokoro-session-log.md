# Session Log — Esquema y Guia para /kokoro-open y /kokoro-close

> Referencia tecnica para el historial de sesiones por invitado.
> Usado por: `/kokoro-open`, `/kokoro-close`, `/kokoro-ads`, `/kokoro-creative`

> "Cada sesion deja una huella. Kokoro recuerda para que Eduardo no repita."

## Proposito

Define el esquema de datos para el historial de sesiones que Kokoro mantiene
por cada invitado. Vive en `ClientProfile.metadata["session_log"]` — una
lista plana de entradas ordenadas por fecha descendente.

## Ubicacion

```
.kokoro/clients.json → clients[N].metadata.session_log
```

No requiere cambios al modelo Pydantic. `metadata` es `dict[str, Any]`.

## Schema

```json
{
  "session_log": [
    {
      "date": "2026-03-27",
      "type": "creative",
      "skill": "/kokoro-creative",
      "client_id": "crescer",
      "summary": "6 creativos Baby Balance — 2 publicos x 3 tamanos",
      "hallazgos": [
        "Publico mamas responde a dolor 'no se si mi bebe va bien'",
        "Fotos lifestyle > clinicas para segmento mamas"
      ],
      "artifacts": [
        "campanas/meta-ads/creativo-01-mamas.txt",
        "campanas/meta-ads/creativo-02-profesionales.txt"
      ],
      "next_action": "Lanzar campana en Meta Ads con los creativos generados"
    }
  ]
}
```

## Campos

| Campo | Tipo | Requerido | Descripcion |
|-------|------|:---------:|-------------|
| date | string (YYYY-MM-DD) | si | Fecha de la sesion |
| type | string | si | Tipo de trabajo realizado |
| skill | string | no | Skill que genero la entrada |
| client_id | string | si | ID del invitado en el grafo |
| summary | string | si | Que se hizo (1-2 lineas, concreto) |
| hallazgos | list[string] | no | Que se aprendio del invitado, su publico, su mercado |
| artifacts | list[string] | no | Paths relativos a clientes/{grupo}/ |
| next_action | string | no | Que hacer la proxima vez con este invitado |

### Valores validos para `type`

| type | Cuando usarlo |
|------|---------------|
| creative | Generacion de imagenes con /kokoro-creative |
| ads | Copy y campanas con /kokoro-ads |
| strategy | Diagnostico, canvas, fuerzas, poda, finanzas |
| research | Investigacion de mercado con /kokoro-research |
| launch | Lanzamiento con /kokoro-launch |
| experiment | Experimentos 3x3x3 con /kokoro-experiment |
| onboarding | Registro inicial o conexion de plataformas |
| general | Trabajo que no encaja en las categorias anteriores |

### Valores validos para `skill`

Cualquier skill de Kokoro: `/kokoro-creative`, `/kokoro-ads`,
`/kokoro-diagnose`, `/kokoro-canvas`, `/kokoro-pescar`, etc.
Si el trabajo fue manual (sin skill), omitir el campo.

## Reglas de Escritura

### Quien escribe

- `/kokoro-close` — siempre (es su funcion principal)
- `/kokoro-ads` — al final de generar entregables
- `/kokoro-creative` — al final de generar imagenes
- Otros skills — cuando se integren (S15.4)

### Como escribir una entrada

```python
from pathlib import Path
from datetime import datetime, timezone
from kokoro.clients.store import load_registry, save_registry

project = Path(".")
registry = load_registry(project)
client = registry.find_by_id("crescer")

# Inicializar session_log si no existe
if "session_log" not in client.metadata:
    client.metadata["session_log"] = []

# Crear nueva entrada
entry = {
    "date": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
    "type": "creative",
    "skill": "/kokoro-creative",
    "client_id": client.id,
    "summary": "6 creativos Baby Balance — 2 publicos x 3 tamanos",
    "hallazgos": [
        "Publico mamas responde a dolor 'no se si mi bebe va bien'"
    ],
    "artifacts": [
        "campanas/meta-ads/creativo-01-mamas.txt"
    ],
    "next_action": "Lanzar campana en Meta Ads"
}

# Insertar al inicio (mas reciente primero)
client.metadata["session_log"].insert(0, entry)

# Rotar si excede 20 entradas
if len(client.metadata["session_log"]) > 20:
    client.metadata["session_log"] = client.metadata["session_log"][:20]

# Persistir
client.updated = datetime.now(tz=timezone.utc)
registry.updated = client.updated
save_registry(project, registry)
```

### Limite de entradas

Maximo 20 entradas por invitado. Al agregar la entrada 21, la mas antigua
se descarta automaticamente. 20 sesiones es contexto suficiente.

### Paths de artifacts

Siempre relativos a `clientes/{grupo}/`. No paths absolutos.

Ejemplo: si el archivo esta en
`clientes/crescer/campanas/meta-ads/creativo-01.txt`,
el artifact se registra como `campanas/meta-ads/creativo-01.txt`.

## Reglas de Lectura

### /kokoro-open lee asi

1. Cargar registry con `load_registry(project)`
2. Resolver invitado con `find_by_name(query)` o `find_by_id(id)`
3. Leer `client.metadata.get("session_log", [])`
4. Mostrar las ultimas 3-5 entradas como contexto
5. Extraer `next_action` de la entrada mas reciente como propuesta de foco

### Formato de presentacion

```
## Sesion con {name}

Ultima sesion: {date} — {summary}
Hallazgos: {hallazgos como bullets}
Pendiente: {next_action}

¿Continuamos con esto o tienes otra prioridad hoy?
```

## Anti-patrones

- **No crear archivos separados por sesion** — todo vive en metadata
- **No guardar conversaciones completas** — solo resumen y hallazgos
- **No guardar datos que ya estan en el perfil** — el session_log es
  historial de interacciones, no duplicacion del perfil
- **No guardar entradas vacias** — si no hubo hallazgos ni artifacts,
  al menos el summary debe ser sustancial
- **No omitir next_action** — /kokoro-close SIEMPRE debe proponer
  siguiente paso. Es el valor principal del cierre
