# Google Ads Learning Record — Canonical Schema

> Definido en E42 S42.1. Este es el schema canónico para entradas de
> aprendizaje de Google Ads dentro del Session Log de Kokoro.

## Purpose

Define un `LearningRecord` explícito para que cada sesión de Google Ads
deje una traza reusable: qué se revisó, qué se aprendió, y qué sigue.
El invitado que regresa no reinicia desde cero — Kokoro lee el historial
y propone foco.

## Schema

### Core fields (required, all Kokoro sessions)

| Field | Type | Description |
|-------|------|-------------|
| `date` | `string` (YYYY-MM-DD) | Fecha de la sesión |
| `type` | `string` | Tipo de trabajo. Para Google Ads: `"gads"` |
| `client_id` | `string` | ID del invitado en el grafo |
| `summary` | `string` | Qué se hizo (1-2 líneas, concreto) |

### Core fields (optional, all Kokoro sessions)

| Field | Type | Description |
|-------|------|-------------|
| `skill` | `string` | Skill que generó la entrada (ej: `/kokoro-google-ads-run`) |
| `hallazgos` | `string[]` | Qué se aprendió del invitado, su audiencia, su mercado |
| `artifacts` | `string[]` | Paths relativos a reportes, exports, o entregables |
| `next_action` | `string` | Qué hacer la próxima sesión con este invitado |

### Google Ads fields (all optional, additive)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `platform` | `string` | `"google_ads"` | Plataforma de origen del aprendizaje |
| `campaign_type` | `string` | `"search"`, `"display"`, `"pmax"`, `"shopping"`, `"other"` | Tipo de campaña revisada |
| `learning_state` | `string` | `"learning"`, `"stable"`, `"needs_attention"` | Madurez del aprendizaje para esta cuenta/campaña |
| `task_group` | `string` | free text | Grupo de tareas (ej: "keywords", "bidding", "creatives") |
| `task` | `string` | free text | Tarea específica dentro del grupo |
| `cadence` | `string` | `"72h"`, `"weekly"`, `"monthly"`, `"90d"` | Ritmo de revisión recomendado |
| `landing_page` | `string` | URL or path | Landing page activa durante la revisión |
| `asset_group` | `string` | free text | Grupo de assets en uso |
| `change_made` | `string` | free text | Cambio realizado en esta sesión |
| `reason` | `string` | free text | Por qué se hizo el cambio |

## Example

```json
{
  "date": "2026-06-09",
  "type": "gads",
  "skill": "/kokoro-google-ads-run",
  "client_id": "cliente_demo",
  "summary": "Revisión Search last_30_days — términos, pacing, negativas",
  "hallazgos": [
    "Las consultas informativas atraen clics pero aún no convierten",
    "El grupo de anuncios sigue en etapa de aprendizaje",
    "Términos de marca tienen CTR 3x pero conversión similar a genéricos"
  ],
  "artifacts": [
    "reports/google-ads/2026-06-09-cliente_demo.md"
  ],
  "next_action": "Revisar términos de búsqueda en 72h y preparar ajustes de negativas",
  "platform": "google_ads",
  "campaign_type": "search",
  "learning_state": "learning",
  "task_group": "keywords",
  "task": "search_term_audit",
  "cadence": "72h",
  "change_made": "Agregadas 12 negativas BROAD para términos informativos",
  "reason": "Consultas sin intención comercial diluyen el presupuesto"
}
```

## Backward Compatibility

- All Google Ads fields are **optional** — entries without them remain valid.
- Existing `session_log` entries with `platform`, `campaign_type`, and
  `learning_state` are already compatible.
- The schema adds `task_group`, `task`, `cadence`, `landing_page`,
  `asset_group`, `change_made`, and `reason` as new optional fields.
- No existing field is renamed, removed, or made required.

## Storage

The Learning Record lives inside `ClientProfile.metadata["session_log"]`
as defined in `kokoro-session-log.md`. No separate storage, no migration.

```python
# Insert at position 0 (most recent first)
client.metadata["session_log"].insert(0, entry)

# Rotate if exceeds 20 entries
if len(client.metadata["session_log"]) > 20:
    client.metadata["session_log"] = client.metadata["session_log"][:20]
```

## Mapping to Learning Dashboard

El `kokoro-learning-dashboard.md` consume este schema:

| Dashboard Capa | Campos que alimenta |
|----------------|---------------------|
| **Plan** | `task_group`, `task`, `cadence`, `landing_page` |
| **Ejecución** | `summary`, `artifacts`, `change_made`, `reason`, `asset_group` |
| **Aprendizaje** | `hallazgos`, `learning_state`, `next_action` |

## Anti-patterns

- **No inventar `learning_state`** — si no está claro, omitir.
- **No duplicar el perfil del invitado** — el Learning Record es historial
  de interacciones, no ficha técnica.
- **No guardar datos de cuenta** — customer IDs, budgets, y credenciales
  viven en el runtime privado, no en el session_log.
- **No omitir `next_action`** — es el valor principal del cierre.
- **No mezclar múltiples campañas en una entrada** — una entrada por
  revisión. Si se revisaron Search y PMax en la misma sesión, dos entradas.

## Related

- `kokoro-session-log.md` — storage, ubicación, reglas de escritura/lectura
- `kokoro-learning-dashboard.md` — modelo de Plan/Ejecución/Aprendizaje
- `/kokoro-google-ads-run` — orquestador ejecutivo que produce estas entradas
- `/kokoro-open` — lee el session_log para proponer foco al invitado
- `/kokoro-close` — escribe el session_log al cerrar sesión
