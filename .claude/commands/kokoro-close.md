# /kokoro-close - Cerrar sesion con Memory v2

Cierra una sesion escribiendo continuidad durable en
`.kokoro/shared/events/`. Memory v2 es el camino primario y el ledger es
inmutable y append-only.

## Camino primario Memory v2

1. Confirma el `actor_id`, `organization_id` y `business_ids` del scope
   resuelto al abrir. Rechaza cualquier negocio no autorizado antes de
   escribir.
2. Construye un `SessionCloseInput` con `session_id`, resumen, provenance y
   timestamp, y captura por separado `decisions`, `evidence`, `outcomes` y
   `next_steps`.
3. Ejecuta `close_session(project, close_input, repository_visibility=...)`.
   Cada registro conserva scope, confidence, provenance y evidencia.
4. Rebuild de vistas es derivado y no modifica el ledger. Reintentar el mismo
   payload es idempotente; reutilizar `session_id` con otro payload produce
   `EventConflict` y no sobrescribe ningun evento.
5. Presenta el resultado, las decisiones, evidencia, resultados y proximo paso.
   Si no hay evidencia o capacidad suficiente, dejalo como incertidumbre y
   propone la pregunta que falta.

La implementacion equivalente es:

```python
from pathlib import Path
from kokoro.memory.session import SessionCloseInput, close_session

close_session(
    Path("."),
    SessionCloseInput(
        session_id="{session_id}",
        actor_id="{actor_id}",
        organization_id="{organization_id}",
        business_ids=["{business_id}"],
        summary="{summary}",
        decisions=[],
        evidence=[],
        outcomes=[],
        next_steps=[],
        source_ref="{source_ref}",
    ),
    repository_visibility="private",
)
```

Nunca borres, edites, sobrescribas o recortes eventos, sesiones ni historial.
Las correcciones se agregan como nuevos eventos con `supersedes`.

## Compatibilidad v1

`.kokoro/clients.json`, `contexto.md` y `metadata.session_log` son solo
fuentes de migracion lossless. Pueden permanecer sin cambios mientras se
agregan eventos v2; no son fuente activa de continuidad y no se ejecutan
`load_registry`, `save_registry` ni escrituras sobre `session_log` desde este
flujo.

## Contrato de cierre

El cierre debe desafiar la decision con evidencia, alternativas, señales que la
refutarian, capacidad, riesgo financiero y paz mental. No cierres si falta un
dato esencial: registra la incertidumbre y el siguiente paso que la resolveria.
