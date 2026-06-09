# Epic E41 Scope: Google Ads Negative Keyword Lifecycle

> **Status:** COMPLETE
> **Created:** 2026-06-08

## Objective

Agregar una operación de eliminación/limpieza de negatives en el conector de Google Ads que sea trazable y consistente con `add`, con soporte de estado (`active`, `removed`) y respuesta de auditoría operativa.

**Value:** Permite recuperar gobernanza diaria sin rehacer grupos de anuncios; mejora la calidad de segmentación y reduce riesgo de restricciones heredadas.

## Stories (4 planned)

| ID | Story | Size | Status | Description |
|----|-------|:----:|:------:|-------------|
| S41.1 | Contract Discovery for Negative Keywords | M | Done | Levantar estado actual del conector, acciones soportadas y formato de payload/respuesta para negativos existentes. |
| S41.2 | Action Contract for Delete | M | Done | Diseñar y formalizar contrato de entrada/salida para `negative_keyword.delete` manteniendo compatibilidad con `add`. |
| S41.3 | Implement Delete Operation | L | Planned | Implementar adapter local de eliminación por texto/criterio usando discovery del MCP oficial. |
| S41.4 | Audit + Docs + Regression Coverage | M | Done | Alinear respuesta de bitácora con `add`, agregar ejemplos y pruebas para casos reales de operación. |

**Total:** 4 stories, 4 points (aprobado para empezar).

## Scope

### In scope (MUST)
- Resolver acción `delete`/`remove` para negativas.
- Gestionar estado `active`/`removed` en respuesta y registro.
- Retornar resultado con IDs/criterios afectados, incluyendo errores parciales.
- Documentar ejemplo de uso para limpieza diaria y recuperación de errores.
- Capturar evidencia de auditoría equivalente a operaciones de `add`.

### In scope (SHOULD)
- Cobertura de pruebas por lote y operación de idempotencia.
- Soporte explícito de modo `dry_run` si ya existe en la acción de `add`.
- Validación de privacidad de datos sensibles en logs.

### Out of scope
- Cambios de UI o consola externa.
- Cambios a métodos de decisión de bidding/offline scoring.
- Limpieza automática sin intervención operativa explícita.

## Done Criteria

### Per story
- [ ] Contratos y tests de integración del conector actualizados para negativos.
- [ ] Flujo de delete implementado con `dry behavior` coherente con API real.
- [ ] Pruebas de regresión para `not_found`, `already_removed`, y `partial_success`.
- [ ] Documentación y ejemplo publicados en comando/conector correspondiente.

### Epic complete
- [ ] Se puede eliminar una negativa existente por texto + criterio.
- [ ] Flujo de bitácora registra eventos de eliminación con estructura equivalente a add.
- [ ] Issue #1 puede cerrarse con evidencia de validación.
- [ ] No hay regresión en acción `add` de negativas.

## Dependencies

```
S41.1 (gemba + contract check)
  ↓
S41.2 ─────────────────────┐
  ↓                       │
S41.3                    │
  ↓                       │
S41.4 (docs + pruebas + audit parity)
```

## Architecture

| Decision | ADR | Summary |
|----------|-----|---------|
| Extend existing connector action contract vs new operation endpoint | N/A | Se prefiere extensión compatible para evitar ruptura de cliente |
| Use logical removed state when hard-delete is unavailable | N/A | Mantiene auditoría y reversibilidad operativa |

## Risks

| Risk | L/I | Mitigation |
|------|:---:|------------|
| API real difiere del supuesto de `match_type` | H/M | Diseñar contrato en S41.1 con inspección directa y versionarlo |
| Remover por texto ambiguo en distintos grupos | M/M | Requerir `scope` explícito y retorno de coincidencias detallado |
| Sin telemetría de borrados previa | L/H | Expandir test y docs de auditoría; validar no ruptura con `add` |

## Implementation Plan

### Story Sequence

| Order | Story | Size | Dependencies | Milestone | Rationale |
|:-----:|-------|:----:|--------------|-----------|-----------|
| 1 | S41.1 | M | None | M1 | Sin contrato real no hay implementación segura de delete |
| 2 | S41.2 | M | S41.1 | M1 | Necesario definir input/output antes de código |
| 3 | S41.3 | L | S41.2 | M2 | Implementación del valor principal |
| 4 | S41.4 | M | S41.3 | M3 | Cierra trazabilidad, auditoría y estabilidad de producto |

### Milestones

| Milestone | Stories | Target | Success Criteria |
|-----------|---------|--------|------------------|
| **M1: Contract-ready** | S41.1, S41.2 | Día 1-2 | Contrato documentado y aprobado; no ruptura de `add` |
| **M2: Delete implemented** | S41.3 | Día 3-4 | Delete funcional por texto/criterio con estado y resultados |
| **M3: Audit parity** | S41.4 | Día 4-5 | Bitácora y documentación alineadas con criterio de add |

### Progress Tracking

| Story | Size | Status | Actual | Velocity | Notes |
|-------|:----:|:------:|:------:|:--------:|-------|
| S41.1 | M | Done | 2h | — | API real no está en checkout público; issue/doc evidencia registrada como `code-path-gap` |
| S41.2 | M | Done | 1h 30m | — | Contrato local definido porque la surface oficial de Google Ads MCP es read-only |
| S41.3 | L | Done | 2h | — | Adapter contract + 3 file updates; runtime path deferred to private workspace |
| S41.4 | M | Done | 45m | — | Audit, docs y regresión definidos; contract parity con add confirmada |

## Parking Lot

- Soporte de limpieza masiva transaccional por lotes grandes (`>100`) → futuro epic si aparece caso de rendimiento.
- UI de revisión antes de borrar → deferido a una integración de operación.
