# Kokoro Learning Record — Canonical Schema

> Definido en E42 S42.1 y extendido en E43 S43.1. Schema canónico para
> entradas de aprendizaje de Google Ads y Meta Ads dentro del Session Log.

## Purpose

Define un `LearningRecord` explícito para que cada sesión deje una traza
reusable: qué se revisó, qué se aprendió, y qué sigue. El invitado que
regresa no reinicia desde cero — Kokoro lee el historial y propone foco.

## Schema

### Core fields (required, all Kokoro sessions)

| Field | Type | Description |
|-------|------|-------------|
| `date` | `string` (YYYY-MM-DD) | Fecha de la sesión |
| `type` | `string` | Tipo de trabajo. `"gads"` para Google Ads, `"ads"` para Meta Ads |
| `client_id` | `string` | ID del invitado en el grafo |
| `summary` | `string` | Qué se hizo (1-2 líneas, concreto) |

### Core fields (optional, all Kokoro sessions)

| Field | Type | Description |
|-------|------|-------------|
| `skill` | `string` | Skill que generó la entrada |
| `hallazgos` | `string[]` | Qué se aprendió del invitado, su audiencia, su mercado |
| `artifacts` | `string[]` | Paths relativos a reportes, exports, o entregables |
| `next_action` | `string` | Qué hacer la próxima sesión con este invitado |

### Shared platform fields (optional, both platforms)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `platform` | `string` | `"google_ads"`, `"meta_ads"` | Plataforma de origen |
| `learning_state` | `string` | `"learning"`, `"stable"`, `"needs_attention"` | Madurez del aprendizaje |

### Google Ads fields (all optional, additive)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `campaign_type` | `string` | `"search"`, `"display"`, `"pmax"`, `"shopping"`, `"other"` | Tipo de campaña |
| `task_group` | `string` | free text | Grupo de tareas |
| `task` | `string` | free text | Tarea específica |
| `cadence` | `string` | `"72h"`, `"weekly"`, `"monthly"`, `"90d"` | Ritmo de revisión |
| `landing_page` | `string` | URL or path | Landing activa |
| `asset_group` | `string` | free text | Grupo de assets |
| `change_made` | `string` | free text | Cambio realizado |
| `reason` | `string` | free text | Por qué el cambio |

### Meta Ads fields (all optional, additive)

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `campaign_objective` | `string` | `"conversion"`, `"traffic"`, `"awareness"`, `"leads"`, `"engagement"`, `"app_installs"`, `"sales"` | Objetivo de la campaña |
| `audience_type` | `string` | `"advantage_plus"`, `"custom"`, `"lookalike"`, `"saved"`, `"broad"` | Tipo de audiencia |
| `placements` | `string[]` | `"feed"`, `"stories"`, `"reels"`, `"instream"`, `"search"`, `"messages"`, `"in-article"`, `"apps"` | Placements activos |
| `creative_count` | `number` | integer | Número de creativos en el corpus activo |
| `corpus_angle` | `string` | free text | Ángulo que este creativo cubre en el corpus unificado |
| `campaign_type` | `string` | `"catalog"`, `"traffic"`, `"leads"`, `"engagement"`, `"app_promotion"`, `"calls"` | Tipo de campaña en Meta |
| `cadence` | `string` | `"72h"`, `"weekly"`, `"monthly"`, `"90d"` | Ritmo de revisión |
| `asset_group` | `string` | free text | Grupo de assets o carpeta de creativos |
| `change_made` | `string` | free text | Cambio realizado en esta sesión |
| `reason` | `string` | free text | Por qué se hizo el cambio |

> **Nota:** `campaign_type`, `cadence`, `asset_group`, `change_made`,
> y `reason` son compartidos con Google Ads pero con valores específicos
> de cada plataforma.

## Examples

### Google Ads entry

```json
{
  "date": "2026-06-09",
  "type": "gads",
  "skill": "/kokoro-google-ads-run",
  "client_id": "cliente_demo",
  "summary": "Revisión Search last_30_days — términos, pacing, negativas",
  "hallazgos": ["Las consultas informativas atraen clics pero aún no convierten"],
  "artifacts": ["reports/google-ads/2026-06-09-cliente_demo.md"],
  "next_action": "Revisar términos en 72h y preparar ajustes de negativas",
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

### Meta Ads entry

```json
{
  "date": "2026-06-09",
  "type": "ads",
  "skill": "/kokoro-ads",
  "client_id": "cliente_demo",
  "summary": "6 creativos Baby Balance — 2 públicos x 3 tamaños",
  "hallazgos": [
    "Público mamás responde a dolor 'no sé si mi bebé va bien'",
    "Fotos lifestyle > clínicas para segmento mamás"
  ],
  "artifacts": [
    "campanas/meta-ads/creativo-01-mamas.txt",
    "campanas/meta-ads/creativo-02-profesionales.txt"
  ],
  "next_action": "Lanzar campaña en Meta Ads con los creativos generados",
  "platform": "meta_ads",
  "campaign_objective": "conversion",
  "audience_type": "advantage_plus",
  "placements": ["feed", "stories", "reels"],
  "creative_count": 6,
  "corpus_angle": "mamás primerizas — dolor emocional",
  "campaign_type": "traffic",
  "cadence": "weekly",
  "learning_state": "stable",
  "change_made": "Nuevo corpus de 6 creativos para Baby Balance",
  "reason": "Segmento mamás sin cobertura previa en el corpus"
}
```

## Backward Compatibility

- All platform fields are **optional** — entries without them remain valid.
- Existing `session_log` entries are unaffected.
- No existing field is renamed, removed, or made required.
- Entries with `platform: "meta_ads"` coexist with `platform: "google_ads"`
  in the same `session_log` array.

## Storage

The Learning Record lives inside `ClientProfile.metadata["session_log"]`
as defined in `kokoro-session-log.md`. No separate storage, no migration.

```python
client.metadata["session_log"].insert(0, entry)
if len(client.metadata["session_log"]) > 20:
    client.metadata["session_log"] = client.metadata["session_log"][:20]
```

## Mapping to Learning Dashboard

| Dashboard Capa | Campos que alimenta |
|----------------|---------------------|
| **Plan** | `task_group`, `task`, `cadence`, `landing_page`, `campaign_objective`, `audience_type`, `placements` |
| **Ejecución** | `summary`, `artifacts`, `change_made`, `reason`, `asset_group`, `creative_count`, `corpus_angle` |
| **Aprendizaje** | `hallazgos`, `learning_state`, `next_action` |

## Anti-patterns

- **No inventar `learning_state`** — si no está claro, omitir.
- **No duplicar el perfil del invitado** — el Learning Record es historial.
- **No guardar datos de cuenta** — IDs, budgets, credenciales viven en runtime privado.
- **No omitir `next_action`** — es el valor principal del cierre.
- **No mezclar plataformas en una entrada** — si se revisaron Google Ads
  y Meta Ads en la misma sesión, dos entradas separadas.

## Related

- `kokoro-session-log.md` — storage, ubicación, reglas de escritura/lectura
- `kokoro-learning-dashboard.md` — modelo de Plan/Ejecución/Aprendizaje
- `kokoro-client-learning-guide.md` — guía del invitado
- `/kokoro-google-ads-run` — orquestador Google Ads
- `/kokoro-ads` — skill táctico Meta Ads
- `/kokoro-open` / `/kokoro-close` — leer/escribir session_log
