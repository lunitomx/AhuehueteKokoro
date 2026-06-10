# Learning State Detector — Google Ads

> Knowledge file para S45.2. Infiere `learning_state` automáticamente
> desde datos del MCP de Google Ads. Usado por `/kokoro-gads` y
> `/kokoro-close` al persistir session_log.

## Decision Tree

```
¿MCP disponible?
├── NO → learning_state = null (no inventar)
└── SÍ → fetch campaign performance data
    │
    ├── campaign active < learning_window?
    │   ├── Search/Display: < 14 days → "learning"
    │   └── PMax: < 28 days → "learning"
    │   (razón: campaña en período de aprendizaje de Smart Bidding)
    │
    ├── conversions_window < threshold?
    │   ├── Search/Display: conversions_14d < 30 → "learning"
    │   └── PMax/Shopping: conversions_28d < 50 → "learning"
    │   (razón: volumen insuficiente para que Smart Bidding optimice)
    │
    ├── spend > 0 AND conversions_window == 0?
    │   └── SÍ → "needs_attention" (razón: inversión sin conversiones)
    │
    ├── cpa_change > +30%?
    │   └── SÍ → "needs_attention" (razón: CPA subió X% vs período anterior)
    │
    ├── impressions dropped >50% without budget change?
    │   └── SÍ → "needs_attention" (razón: delivery colapsado sin causa aparente)
    │
    └── else → "stable" (razón: CPA estable dentro de ±15%)
```

## Thresholds por Campaign Type

| Campaign Type | Learning Window | Conversion Threshold | Period |
|:-------------:|:--------------:|:--------------------:|:------:|
| Search | 14 días | 30 | 14 días |
| Display | 14 días | 30 | 14 días |
| Performance Max | 28 días | 50 | 28 días |
| Shopping | 14 días | 50 | 28 días |
| Other | 14 días | 30 | 14 días |

| Métrica | Umbral | → State |
|---------|:------:|:-------:|
| Impressions change (sin budget change) | > -50% | needs_attention |
| CPA change (período actual vs anterior) | > +30% | needs_attention |
| CPA change (período actual vs anterior) | ±15% con conversiones ≥ threshold | stable |

## Output Contract

```json
{
  "learning_state": "learning",
  "reason": "Search campaign active 9 days — Smart Bidding aún en período de aprendizaje (mínimo 14 días)",
  "source": "mcp",
  "detected_at": "2026-06-09"
}
```

## Fallback

Si el MCP de Google Ads no está configurado o no responde:
- `learning_state` se omite del session_log
- No se muestra estado falso en kokoro-open
- El operador puede establecerlo manualmente

## Override Manual

Misma regla que S45.1: el valor manual tiene prioridad.
`source: "manual"` para trazabilidad.
