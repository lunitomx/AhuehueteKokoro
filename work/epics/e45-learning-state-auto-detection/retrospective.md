---
epic_id: E45
title: Learning State Auto-Detection
status: complete
completed: 2026-06-09
stories:
  S45.1: Meta Ads Detector — Done
  S45.2: Google Ads Detector — Done
  S45.3: Integrate + Documentation — Done
---

# E45 Retrospective: Learning State Auto-Detection

## Summary

E45 eliminó la dependencia humana del learning_state. Ahora Kokoro infiere
automáticamente si una campaña está en learning, stable o needs_attention
usando datos reales del MCP. Si el MCP no está disponible, no inventa —
omite el campo. El operador conserva poder de override manual.

## What Shipped

| Story | Result |
|-------|--------|
| S45.1 | Meta Ads detector: 5 thresholds, decision tree, fallback null |
| S45.2 | Google Ads detector: per-campaign-type thresholds (5 types), impressions drop detection |
| S45.3 | Integration: kokoro-open muestra razón, schema actualizado con source+reason |

## Done Criteria

| Criteria | Status |
|----------|:------:|
| Meta Ads: learning_state inferido desde MCP | ✅ |
| Google Ads: learning_state inferido desde MCP | ✅ |
| kokoro-open muestra estado con explicación | ✅ |
| kokoro-close persiste en session_log | ✅ |
| Fallback null (no inventa) | ✅ |
| Operador override manual | ✅ |
