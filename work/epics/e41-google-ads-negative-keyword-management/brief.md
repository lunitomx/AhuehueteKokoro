# Epic Brief: Google Ads negative keyword lifecycle

## Hypothesis
Para equipos que operan Google Ads diariamente y usan el conector de Kokoro,
la falta de acción para quitar keywords negativas existentes rompe la trazabilidad diaria y evita corregir segmentación sin rehacer grupos completos.

Agregar soporte de eliminación/limpieza de negativas con estado gestionado (`active`/`removed`) y respuesta auditada permitirá recuperar control operativo sin perder evidencia de decisión.

## Success Metrics
- **Leading:** Se documenta y prueba al menos un flujo end-to-end de eliminación por texto + criterio de coincidencia.
- **Lagging:** El tiempo para deshacerse de una negativa obsoleta baja de forma mensurable en el playbook operativo (sin afectar la trazabilidad de cambios).

## Appetite
M — 5-7 historias (sin incluir pruebas de contrato entre runtime y proveedor)

## Scope Boundaries
### In (MUST)
- Habilitar acción de `delete`/`remove` en connector para negativas existentes.
- Soportar manejo de estado (`active`, `removed`) por grupo de anuncios.
- Mantener respuesta/registro con traza equivalente al flujo de `add` (IDs afectados, confirmación y resultado).
- Actualizar documentación de uso con ejemplos de limpieza.

### In (SHOULD)
- Agregar validaciones de idempotencia (clave por texto + criterio de coincidencia).
- Agregar pruebas de regresión para escenarios de "no existe", "ya removida" y "parcialmente removida".

### No-Gos
- Cambiar estrategia de negocio del keyword management global de Google Ads.
- Añadir limpieza de positivos o reglas de audiencia (fuera del conector de negativas).
- Soporte de otras plataformas de anuncios en este epic.

### Rabbit Holes
- Dibujar un re-diseño completo del conector sin mapear primero contratos actuales.
- Reemplazar toda la capa del conector por un wrapper nuevo sin evidencia de compatibilidad.

## Problem and Issue Link
- Issue: `#1` — [feat(google-ads): add delete support for negative keywords in connector](https://github.com/lunitomx/AhuehueteKokoro/issues/1)
