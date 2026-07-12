# /kokoro-patrones - Patrones entre negocios

Consulta Memory v2 para comparar aprendizajes entre negocios seleccionados por
la persona. La fuente canonica es `.kokoro/shared/events/`; nunca uses un
patron sin citar evidencia del ledger.

## Flujo activo

1. Resuelve `actor_id`, organizacion y scope. Pide una seleccion explicita de
   al menos dos negocios y rechaza cualquier negocio no autorizado.
2. Busca eventos de evidencia reales dentro de los negocios seleccionados.
   Cada negocio debe estar representado; no rellenes huecos con una inferencia.
3. Presenta cada candidato con resumen, `event_id`, provenance, confidence,
   refs de evidencia, contraevidencia y senales que lo refutarian.
4. Mantiene el estado `candidate`. No lo presentes como hecho ni lo promuevas
   sin confirmacion humana explicita.
5. Si la persona confirma, agrega un evento de confirmacion que supersede al
   candidato; el historial original permanece intacto.

## Contrato de salida

```text
Patron candidato: {summary}
Negocios seleccionados: {business_ids}
Evidencia: {event_id/ref + provenance}
Confidence: {confidence}
Contraevidencia: {refs}
Senales que refutarian: {signals}
Estado: candidate | confirmed
```

Si no hay dos negocios autorizados o evidencia suficiente, devuelve una
incertidumbre verificable y no inventes un patron.
