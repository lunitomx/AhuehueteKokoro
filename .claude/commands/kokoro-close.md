# /kokoro-close — Cerrar Sesion con Invitado

> Herramienta transversal: Cierre de trabajo con un invitado
> Aplica en cualquier fase del proceso Kokoro

> "Lo que no se registra, se olvida. Y lo que se olvida, se repite."

## Contexto

Este skill cierra una sesion de trabajo con un invitado. Captura que se
hizo, que se aprendio, actualiza el perfil si hay datos nuevos, y propone
el siguiente paso. Es el complemento de `/kokoro-open`.

Lee el archivo de conocimiento `kokoro-session-log.md` para consultar el
schema del historial de sesiones.

### Resolucion de invitado

1. Si se trabajo con un invitado durante la sesion (mencionado en
   conversacion o resuelto por /kokoro-open), usarlo directamente
2. Si no esta claro, preguntar: "¿Con que invitado cerramos hoy?"
3. Resolver desde `.kokoro/clients.json` con `find_by_name`

## Instrucciones para la sesion

### Proceso — 5 pasos EN ORDEN

1. IDENTIFICAR que se hizo
2. EXTRAER hallazgos
3. ACTUALIZAR perfil si hay datos nuevos
4. PROPONER siguiente paso
5. PERSISTIR todo

### Paso 1: Identificar que se hizo

Revisa la conversacion actual e identifica:
- **Que skills se usaron** (kokoro-creative, kokoro-ads, etc.)
- **Que se produjo** (creativos, copy, diagnostico, canvas, etc.)
- **Tipo de trabajo** (creative, ads, strategy, research, etc.)

Si no es obvio, pregunta brevemente:

> "Antes de cerrar, un resumen rapido: ¿que logramos hoy con {name}?"

Construye el **summary** — 1-2 lineas concretas de lo que se hizo.
No genericas ("se trabajo en marketing") sino especificas
("6 creativos Baby Balance, 2 publicos x 3 tamanos").

### Paso 2: Extraer hallazgos

Los hallazgos son lo que se APRENDIO del invitado, su publico, o su
mercado durante la sesion. No son tareas completadas — son insights.

Revisa la conversacion y extrae:
- Descubrimientos sobre el publico ("mamas responden a dolor X")
- Aprendizajes sobre el mercado ("competidores no ofrecen Y")
- Validaciones ("el gancho Z funciono / no funciono")
- Datos nuevos del negocio ("tiene 4 cursos activos, no 3")

Si no hay hallazgos claros, preguntar:

> "¿Que aprendimos de {name} hoy que no sabiamos antes?"

Los hallazgos se guardan como lista de strings cortos y directos.

### Paso 3: Actualizar perfil si hay datos nuevos

Revisa si durante la sesion se aprendio algo que deberia actualizarse
en el perfil del invitado:

- **Segmentos nuevos** → agregar a `segments`
- **Datos de contacto** → agregar a `metadata`
- **Formaciones / creaciones nuevas** → actualizar `metadata`
- **Colores de marca** → actualizar `metadata["colores_marca"]`

Solo actualizar si hay datos NUEVOS y CONCRETOS. No actualizar por
actualizar.

### Paso 4: Proponer siguiente paso

Basandote en lo que se hizo hoy y lo que queda pendiente, propone
UNA accion concreta para la proxima sesion:

> "La proxima vez con {name}: {accion concreta porque razon}."

Ejemplos buenos:
- "Lanzar la campana Baby Balance en Meta Ads con los creativos generados"
- "Hacer diagnostico con /kokoro-diagnose — aun no se por que el negocio no crece"
- "Crear landing page para el taller con los copies que generamos"

Ejemplos malos:
- "Seguir trabajando en marketing" (vago)
- "Revisar los resultados" (sin especificar que resultados)

### Paso 5: Persistir todo

Construye la entrada del session_log y guardala:

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
    "type": "{type}",
    "skill": "{skill_principal}",
    "client_id": client.id,
    "summary": "{summary}",
    "hallazgos": [{hallazgos}],
    "artifacts": [{artifacts}],
    "next_action": "{next_action}"
}

client.metadata["session_log"].insert(0, entry)

# Rotar si excede 20
if len(client.metadata["session_log"]) > 20:
    client.metadata["session_log"] = client.metadata["session_log"][:20]

# Actualizar timestamps
client.updated = datetime.now(tz=timezone.utc)
registry.updated = client.updated
save_registry(project, registry)
```

Despues de persistir, confirmar al usuario:

```
## Sesion cerrada con {name}

| Campo | Detalle |
|-------|---------|
| Fecha | {date} |
| Tipo | {type} |
| Resumen | {summary} |
| Hallazgos | {N} insights guardados |
| Artifacts | {N} archivos registrados |

### Proxima sesion
{next_action}

Usa `/kokoro-open {name}` la proxima vez para retomar donde quedamos.
```

## Notas para Claude

- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- Usa "invitado" no "cliente", "creacion" no "producto"
- El cierre debe ser BREVE — 2 minutos maximo
- No pidas al usuario que dicte un resumen largo — infiere de la conversacion
- Si la conversacion fue corta o no hubo hallazgos significativos, esta
  bien guardar una entrada minima (solo date, type, summary, next_action)
- IMPORTANTE: Siempre proponer next_action — es el valor principal del cierre
- IMPORTANTE: Siempre persistir con save_registry — no dejar cambios sin guardar
- IMPORTANTE: Los hallazgos son del INVITADO, no del proceso. "Aprendimos
  que el publico de Crescer responde a X" es un hallazgo. "Usamos
  kokoro-creative" no lo es
- Responde en el idioma del usuario
- Si se usaron varios skills durante la sesion, registrar el principal en
  `skill` y mencionar los otros en el `summary`
