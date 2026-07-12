# /kokoro-consultor - Contrato de razonamiento

Usa Memory v2 para desafiar una decision antes de presentarla como recomendada.
La fuente canonica es `.kokoro/shared/events/`; una nota conversacional no
sustituye el registro durable.

## Camino activo Memory v2

Confirma el actor, la organizacion y los negocios autorizados. Pregunta y
registra todos estos campos antes de cerrar la revision:

- **Evidencia:** citas verificables con `ref` y, cuando sea posible, excerpt.
- **Alternativas:** al menos dos rutas comparables, incluida la de no actuar.
- **Senales que refutarian:** observaciones concretas que harian cambiar la
  recomendacion.
- **Capacidad:** tiempo, energia, equipo y limites operativos disponibles.
- **Riesgo financiero:** inversion expuesta, limite de perdida y condicion de
  pausa.
- **Paz mental:** costo humano aceptable y senal de que la decision deja de ser
  sostenible.

No confundas una preferencia con evidencia. Si falta un campo, registra la
incertidumbre y no recomiendes avanzar.

La implementacion agrega un evento inmutable con provenance, confidence y
scope:

```python
from pathlib import Path
from kokoro.memory.reasoning import (
    ConsultantReasoningInput,
    record_reasoning_review,
)

record_reasoning_review(
    Path("."),
    ConsultantReasoningInput(
        review_id="{review_id}",
        decision_id="{decision_id}",
        actor_id="{actor_id}",
        organization_id="{organization_id}",
        business_ids=["{business_id}"],
        challenge="{challenge}",
        evidence=[...],
        alternatives=["{option_a}", "{option_b}"],
        disconfirming_signals=["{signal}"],
        capacity="{capacity}",
        financial_risk="{financial_risk}",
        peace_of_mind="{peace_of_mind}",
        source_ref="{source_ref}",
    ),
    repository_visibility="private",
)
```

Repetir el mismo payload es idempotente. Reutilizar `review_id` con otro
payload produce `EventConflict`; nunca sobrescribas ni borres el evento
original.
