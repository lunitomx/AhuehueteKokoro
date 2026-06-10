# Learning State Detector — Meta Ads

> Knowledge file para S45.1. Infiere `learning_state` automáticamente
> desde datos del MCP de Meta Ads. Usado por `/kokoro-ads` y
> `/kokoro-close` al persistir session_log.

## Decision Tree

```
¿MCP disponible?
├── NO → learning_state = null (no inventar)
└── SÍ → fetch campaign performance data
    │
    ├── campaign active < 7 days?
    │   └── SÍ → "learning" (razón: campaña en período inicial)
    │
    ├── conversions_7d < 50?
    │   └── SÍ → "learning" (razón: volumen de conversiones insuficiente
    │              para que Meta optimice con confianza)
    │
    ├── spend > 0 AND conversions_7d == 0?
    │   └── SÍ → "needs_attention" (razón: inversión sin retorno)
    │
    ├── cpa_change_7d > +30%?
    │   └── SÍ → "needs_attention" (razón: CPA subió X% vs semana anterior)
    │
    └── else → "stable" (razón: CPA estable dentro de ±15%)
```

## Thresholds

| Métrica | Umbral | → State |
|---------|:------:|:-------:|
| Campaign age | < 7 días | learning |
| Conversions (7d) | < 50 | learning |
| Conversions (7d) | ≥ 50 AND CPA ±15% | stable |
| CPA change (7d vs prev 7d) | > +30% | needs_attention |
| Spend > 0, conversions = 0 (7d) | — | needs_attention |

## Output Contract

```json
{
  "learning_state": "stable",
  "reason": "CPA estable: $12.40 esta semana vs $11.80 semana anterior (+5.1%)",
  "source": "mcp",
  "detected_at": "2026-06-09"
}
```

## Campo learning_state en session_log

El campo ya existe en el schema del learning record. La única adición
es que ahora puede ser poblado automáticamente.

| learning_state | Significado |
|:--------------:|-------------|
| `learning` | La campaña aún no tiene datos suficientes para optimizar |
| `stable` | La campaña tiene volumen y CPA estable — período de cosecha |
| `needs_attention` | Algo cambió: CPA subió, conversiones cayeron, o gasta sin retorno |
| `null` | MCP no disponible — no se infiere nada |

## Fallback

Si el MCP de Meta Ads no está configurado o no responde:
- `learning_state` se omite del session_log (no se escribe el campo)
- No se muestra "learning" ni "stable" falso en kokoro-open
- El operador puede establecerlo manualmente si lo desea

## Override Manual

El valor manual tiene prioridad sobre el automático:
- Si el operador escribe `learning_state: "stable"` en el session_log,
  el detector NO lo modifica
- El source se marca como "manual" para trazabilidad
- En la siguiente sesión, si no hay override nuevo, el detector vuelve
  a inferir desde MCP

## Ejemplo en kokoro-ads

```python
# Al cerrar sesión de Meta Ads
from kokoro.learning_state import detect_meta_ads_state

if mcp_available:
    result = detect_meta_ads_state(campaign_id)
    if result:
        entry["learning_state"] = result["learning_state"]
        entry["learning_state_reason"] = result["reason"]
        entry["learning_state_source"] = result["source"]
```

## Relación con S45.2

S45.2 implementa el mismo contrato para Google Ads con thresholds
específicos de esa plataforma (Search 14 días, PMax 28 días, etc.).
La interfaz de output es idéntica: `{learning_state, reason, source}`.
