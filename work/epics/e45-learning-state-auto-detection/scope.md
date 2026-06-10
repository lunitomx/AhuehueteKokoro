# Epic E45: Learning State Auto-Detection

> **Status:** IN PROGRESS
> **Created:** 2026-06-09
> **Origin:** E43 parking lot
> **Depends on:** E42 (Google Ads Learning), E43 (Meta Ads Learning)

## Objective

Hoy `learning_state` es manual: el operador decide si una campaña está
en `learning`, `stable` o `needs_attention`. E45 lo automatiza usando
datos reales de los MCP de Meta Ads y Google Ads.

**Value:** El learning loop deja de depender de que el operador recuerde
actualizarlo. Cada sesión de `/kokoro-open` trae el estado real inferido
de los datos, no la última opinión humana.

## How It Works

### Meta Ads Detection

| Condición | → learning_state |
|-----------|:----------------:|
| Campaña activa <7 días | `learning` |
| <50 conversiones en últimos 7 días | `learning` |
| >50 conversiones, CPA estable (±15% vs semana anterior) | `stable` |
| CPA subió >30% vs semana anterior | `needs_attention` |
| Spend >0, 0 conversiones en 7 días | `needs_attention` |
| Campaña pausada >7 días | `needs_attention` |

### Google Ads Detection

| Condición | → learning_state |
|-----------|:----------------:|
| Campaña activa <14 días (Search/Display) o <28 días (PMax) | `learning` |
| <30 conversiones en últimos 14 días (Search) | `learning` |
| >30 conversiones, CPA estable (±15%) | `stable` |
| CPA subió >30% vs período anterior | `needs_attention` |
| Impresiones cayeron >50% sin cambio de budget | `needs_attention` |

### Fallback

Si el MCP no está disponible (runtime sin conexión), el learning_state
se omite en vez de inventarse. El operador puede establecerlo manualmente
como hoy.

## Stories (3 planned)

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| S45.1 | Meta Ads Learning State Detector | M | Inferir learning_state desde datos de Meta Ads MCP (campaign performance, spend, conversions, CPA trend) |
| S45.2 | Google Ads Learning State Detector | M | Inferir learning_state desde datos de Google Ads MCP (campaign age, conversions, CPA stability, impression trend) |
| S45.3 | Integrate into Open/Close + Documentation | S | Inyectar auto-detection en kokoro-open (surface) y kokoro-close (persist). Documentar thresholds. Actualizar learning record schema si es necesario. |

**Total:** 3 stories, 7 SP

## Scope

### In scope (MUST)
- Definir thresholds de detección para Meta Ads y Google Ads
- Detector lee datos de MCP cuando está disponible
- learning_state inferido se persiste en session_log al cerrar
- kokoro-open muestra el estado inferido (no solo el manual)
- Fallback limpio cuando MCP no está disponible

### In scope (SHOULD)
- Explicar al operador POR QUÉ se infirió ese estado (transparencia)
- Permitir override manual si el operador discrepa

### Out of scope
- Cambiar thresholds en runtime (van hardcodeados en esta épica)
- UI de configuración de thresholds
- Alertas proactivas (eso es otra épica)

## Done Criteria

- [ ] Meta Ads: learning_state inferido automáticamente desde MCP
- [ ] Google Ads: learning_state inferido automáticamente desde MCP
- [ ] kokoro-open muestra el estado inferido con explicación
- [ ] kokoro-close persiste el estado inferido en session_log
- [ ] Fallback: sin MCP → sin learning_state (no inventa)
- [ ] Operador puede hacer override manual

## Dependencies

```
S45.1 (Meta detector) ──┐
                         ├── S45.3 (integrate + docs)
S45.2 (Google detector) ─┘
```

## Risks

| Risk | Mitigation |
|------|------------|
| MCP no disponible en todos los runtimes | Fallback: omitir, no inventar |
| Thresholds no universales (varían por industria) | Usar thresholds conservadores; el override manual cubre edge cases |
| Meta Ads MCP cambia API | Detector lee fields estándar (spend, conversions, cpa); son estables |
