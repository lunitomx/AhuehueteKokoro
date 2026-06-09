# Epic Design: Google Ads negative keyword lifecycle

## Affected Surface (Gemba)

| Module/File | Current State | Changes |
|-------------|---------------|---------|
| Google Ads connector action surface | Actualmente expone operación de altas (`add`) para negativas | Agregar ruta de acción para baja/limpieza con manejo explícito de estado |
| Negative keyword state model | No parece existir estado persistente para negativas | Incluir `state` (`active`, `removed`) por entidad de negativa en respuestas y auditoría |
| Execution response contract | Retorno orientado a altas | Mantener estructura simétrica en borrados para trazabilidad por IDs y resultados |
| Docs/usage examples | Incompleto para `delete` | Añadir caso de uso de limpieza y ejemplos de invocación y resultados |
| Test matrix | Cubría `add` y/o flujos de error de adición | Añadir escenarios de eliminación y estados en tests unit/integración |

## Target Components

| Component | Responsibility | Key Interface |
|-----------|---------------|---------------|
| Connector action parser | Interpretar intención de mutación (`add` vs `delete`) para negativas | `action` + `resource` + `payload` |
| Negative keyword processor | Resolver coincidencia por texto y estado objetivo | `normalize`, `match`, `apply_state` |
| Audit/event logger | Generar evento con mismo formato de trazabilidad usado en adiciones | `record_event(action="negative_keyword.delete", ...)` |
| Response formatter | Devolver IDs y resultado por candidato | `action_result(success|partial|failed)` |
| Usage docs | Describir contrato operativo de limpieza | `kokoro-gads` o comando equivalente |

## Key Contracts

### Connector delete contract (target)

Input:
- `action`: `delete` (en el dominio de negativas)
- `target_type`: `negative_keyword`
- `text`: texto de palabra clave negativa
- `match_type`: al menos `EXACT`, `PHRASE`, `BROAD` (si aplica en la API real)
- `ad_group_id` o equivalente de scope operativo
- `scope`: `dry_run` opcional

Behavior:
- Identifica negativas activas compatibles por texto/criterio de coincidencia.
- Si encuentra coincidencias activas, intenta cambiar estado a `removed` o ejecutar operación equivalente de borrado.
- Si no encuentra coincidencias o ya están removidas, responde estado parcial explicando `not_found` / `already_removed`.

Response contract:
- `action`: `negative_keyword.delete`
- `status`: `success` / `partial` / `failed`
- `requested`: número de criterios solicitados
- `removed`: lista de IDs/criterios removidos o estados cambiados
- `not_found` o `already_removed`: lista informativa
- `errors`: errores de API o permisos por ID
- `audit_event_id`: id del registro de bitácora

### Audit contract
- Debe incluir al menos:
  - `connector`, `action`, `payload_hash` (no datos sensibles), `outcome`, `actor`, `timestamp`
- `add` y `delete` deben compartir formato base para comparación histórica.

## Architecture

No requiere nuevo stack ni ADR adicional. Enfocado en extensión de contrato y simetría de gobernanza operacional dentro del conector existente.

### Migration Path
1. Habilitar `delete` con bandera/fallback para no romper clientes existentes.
2. Mantener `add` sin cambios de firma pública.
3. Desplazar estados de negativas a explícitamente visibles: `active` y `removed`.
4. Validar compatibilidad con flujos actuales antes de documentar como estable.

## Risks

| Riesgo | L/I | Mitigación |
|--------|:---:|------------|
| La API del conector/Google Ads requiere un payload distinto al supuesto | Medio/Alto | Hacer investigación de schema en S41.1 y congelar contrato con pruebas de contrato reales |
| Removals no idempotentes generan errores repetidos | Medio/Medio | Implementar `already_removed` y respuestas de estado parcial con detalle claro |
| Pérdida de trazabilidad entre `add` y `delete` | Medio/Bajo | Enforce un contrato único de respuesta + auditoría sin campos nuevos exclusivos |

## Open Questions
- ¿La plataforma soporta estado explícito `removed` o solo hard-delete? Si no, definir estado lógico de log local.
- ¿La operación debe aceptar lote de textos o un solo texto por invocación?
- ¿Qué `match_type` está disponible en el entorno objetivo y cómo se normaliza de forma estable?
