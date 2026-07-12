# /kokoro-open - Abrir sesion con Memory v2

Abre una sesion con un actor confirmado y carga solo el contexto autorizado.
Memory v2 es el camino primario y `.kokoro/shared/events/` es la fuente
canonica append-only.

## Camino primario Memory v2

1. Resuelve el actor con `open_session(project, actor_hint=...)`. Si hay mas
   de una coincidencia, pide `confirmed_actor_id`; no adivines.
2. Resuelve el `scope` del actor y, si aplica, el `business_id` solicitado.
   Si la identidad o autorizacion no es verificable, detente sin leer datos.
3. Deriva y presenta la vista autorizada de:
   - `.kokoro/shared/views/context.md`
   - `.kokoro/shared/views/open-loops.yaml`
   - `.kokoro/shared/views/patterns.yaml`
4. El resultado debe mostrar organizacion, negocios autorizados, integrantes,
   responsabilidades, autoridad/proceso de decision y memoria pertinente.
   Cita `event_id`, provenance, confidence y evidencia cuando se presente un
   hallazgo.
5. Pregunta si la persona quiere ser guiada y espera confirmacion antes de
   proponer trabajo. No inventes un foco ni expongas otro negocio.

La implementacion equivalente es:

```python
from pathlib import Path
from kokoro.memory.session import open_session

opened = open_session(
    Path("."),
    actor_hint="{actor_hint}",
    confirmed_actor_id="{confirmed_actor_id}",
    business_id="{business_id}",
)
```

La vista materializada compartida puede reconstruirse desde el ledger, pero la
apertura usa una derivacion filtrada por actor y scope y no reemplaza la vista
global en disco.

## Compatibilidad v1

`.kokoro/clients.json`, `contexto.md` y `metadata.session_log` son fuentes de
migracion unidireccional. Solo se consultan para detectar material pendiente de
migrar a Memory v2; no son la fuente de continuidad, no se editan y no se
eliminan. La migracion conserva la fuente original y agrega eventos v2.

## Bienvenida

Si la identidad o el consentimiento faltan, usa el flujo de bienvenida para
capturar integrantes, responsabilidad, autoridad/proceso de decision y
consentimiento. Confirma la sintesis con la persona antes de continuar.
