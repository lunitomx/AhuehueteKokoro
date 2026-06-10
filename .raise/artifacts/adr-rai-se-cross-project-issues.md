# ADR: RaiSE Cross-Project Issue Contamination

> **Issue:** `eLuna-002`
> **Date:** 2026-06-09
> **Status:** Open
> **Severity:** Medium — false positives en scanners de integridad

## Context

RaiSE mantiene una base de datos SQLite global en `~/.rai/raise.db` (7.4MB)
que almacena datos de los 120+ proyectos registrados en `developer.yaml`.
Al sincronizar issues desde Jira, los briefs de épicas se cachean en la
tabla `issue_cache` sin un campo `project_id`.

Cuando un scanner de integridad busca "epics en draft sin evidencia completa",
encuentra issues de TODOS los proyectos mezclados — produciendo falsos
positivos como:

```
E3, E5, E7, E8, E9, E36, E38, E39, E40, E41, E45
```

En un proyecto que solo tiene E41, E42, E43 cerradas.

## Evidencia

Schema actual de `issue_cache`:

```sql
CREATE TABLE issue_cache (
    key        TEXT PRIMARY KEY,
    summary    TEXT NOT NULL DEFAULT '',
    fetched_at TEXT NOT NULL
    -- ❌ sin project_id
);
```

El resto de las tablas SÍ tienen `project_id`:

| Tabla | project_id |
|-------|:----------:|
| sessions | ✅ |
| missions | ✅ |
| patterns | ✅ |
| artifacts | ✅ |
| pipeline_runs | ✅ |
| graph_nodes | ✅ |
| ledger_entries | ✅ |
| **issue_cache** | ❌ |

## Decisión propuesta

### Opción A: Agregar project_id a issue_cache (mínimo)

```sql
ALTER TABLE issue_cache ADD COLUMN project_id TEXT NOT NULL DEFAULT '';
```

El sync de Jira debe filtrar por `project_id = {CWD}` al consultar issues.
Esto resuelve el problema inmediato sin cambiar la arquitectura de DB.

### Opción B: Per-project DB (ideal a largo plazo)

Migrar de `~/.rai/raise.db` global a `.raise/rai/raise.db` por proyecto.
Cada proyecto tiene su propia DB — imposible la contaminación cruzada.
Requiere migración de datos existentes (7.4MB, 120+ proyectos).

### Recomendación

**Opción A ahora, Opción B en roadmap.** La Opción A es un cambio mínimo
(1 columna + filtro en queries). La Opción B requiere planificación de
migración.

## Consequences

- **Positivo:** Los scanners de integridad solo reportan issues del proyecto activo.
- **Positivo:** El developer.yaml ya lista todos los proyectos — el `project_id` puede resolverse automáticamente.
- **Negativo:** La Opción B requiere downtime de migración y posiblemente un script de particionado.

## Related

- `eLuna-001`: Google Ads Learning System (closed — backlog actualizado)
- `developer.yaml`: lista 120+ proyectos con paths
- `~/.rai/raise.db`: 7.4MB, 20+ tablas, schema v32
