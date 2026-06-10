# Epic E46: Parrilla 2.0 — Metodología Zelva44

> **Status:** IN PROGRESS
> **Created:** 2026-06-09
> **Origin:** Documento "Como Crear Una Parrilla Zelva44 Para Kokoro"
> **Depends on:** E39 (CUR), E40 (Parrilla Fase C)

## Objective

La parrilla actual (`/kokoro-parrilla` + `kokoro-parrilla-method.md`)
define 6 fases (A-F) pero carece de la profundidad táctica que el caso
real Zelva44 reveló. E46 incorpora 6 patrones battle-tested:

1. **4-layer pre-review** — performance, visuales, estrategia, feedback CMO
2. **Trigger events vs atributos** — no basta listar features
3. **4-column output** — hook, guion visual, caption, revisión interna
4. **Unique mechanism per piece** — si dos piezas comparten mecanismo, una sobra
5. **Quality criteria** — 8 reglas de aprobación antes de entregar
6. **Repeatable workflow** — 10 pasos replicables para cualquier invitado

**Value:** La parrilla deja de ser un template genérico y se convierte en
un sistema que produce contenido operable: el creativo sabe qué grabar,
el media buyer sabe qué probar, el CMO ve que se respetó su criterio.

## Stories (6 planned)

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| S46.1 | 4-Layer Pre-Review Protocol | M | Documentar el protocolo de revisión previa: performance real de Meta, arte visual real, estrategia comercial, feedback del CMO. Si falta una capa, la parrilla sale genérica. |
| S46.2 | Trigger Events vs Attributes | M | Metodología para convertir atributos fríos en trigger events de vida/mentalidad. Con ejemplos Zelva44: "44 residencias" → "no se siente como torre llena de gente". |
| S46.3 | 4-Column Output System | M | Sistema de separación estricta: hook visible (0-3s), guion visual (producción), caption público, revisión interna. Sin mezclar capas. |
| S46.4 | Unique Mechanism Rule | S | Regla: cada pieza debe tener un mecanismo distinto. Mapa de territorios sin repetición. Si dos piezas comparten mecanismo, una sobra. |
| S46.5 | Quality Gates (8 reglas) | S | Checklist de calidad: ¿cualquier torre podría firmarla? ¿frases vagas? ¿falta precio? ¿mismo ángulo que otra? ¿guion incompleto? ¿caption con notas internas? |
| S46.6 | Upgrade `/kokoro-parrilla` Command | L | Reescribir el comando y knowledge file con la metodología completa. Integrar las 5 stories anteriores en un flujo cohesivo. |

**Total:** 6 stories, 16 SP

## Scope

### In scope (MUST)
- Documentar el protocolo de 4-layer pre-review
- Metodología trigger events con ejemplos reales
- Sistema de 4-column output con separación estricta
- Regla de unique mechanism + mapa de territorios
- 8 quality gates con criterios de aprobación/rechazo
- Upgrade completo de `/kokoro-parrilla` y `kokoro-parrilla-method.md`
- Workflow de 10 pasos replicable para cualquier invitado

### In scope (SHOULD)
- Ejemplos multi-idioma (Chicano rules: inglés que no suene traducido)
- Reglas de posicionamiento no-negociables por invitado
- Testimonios simulados con disclaimer legal

### Out of scope
- Automatización de generación de copy
- Integración con MCP para datos de performance
- UI de parrilla
- Calendarización automática

## Done Criteria

### Per story
- [ ] 4-layer protocol documented with Zelva44 examples
- [ ] Trigger event methodology with before/after examples
- [ ] 4-column system documented; each column has clear boundaries
- [ ] Unique mechanism rule with territory map template
- [ ] 8 quality gates with pass/fail criteria
- [ ] `/kokoro-parrilla` upgraded; `kokoro-parrilla-method.md` rewritten

### Epic complete
- [ ] Un operador puede seguir los 10 pasos y producir una parrilla operable
- [ ] El output tiene hook, guion, caption y revisión separados
- [ ] Cada pieza tiene un mecanismo distinto
- [ ] Las 8 quality gates son verificables (no opinables)
- [ ] Merged to main

## Dependencies

```
S46.1 (pre-review)
  ↓
S46.2 (triggers) ──┐
S46.3 (4-column)  ─┤
S46.4 (mechanism) ─┤
S46.5 (gates) ────┘
  ↓
S46.6 (upgrade command + knowledge)
```

## Architecture

| Decision | Rationale |
|----------|-----------|
| 4-column output es ESTRICTO | Si se mezclan, el equipo produce mal. Cada columna tiene un consumidor distinto |
| Trigger events, no atributos | Un atributo describe el producto. Un trigger event describe al comprador en un momento de decisión |
| Unique mechanism por pieza | Sin esta regla, la parrilla produce refritos. Mismo copy con palabras cambiadas |

## Risks

| Risk | Mitigation |
|------|------------|
| Metodología muy específica de Zelva44 | Abstraer los patrones (trigger events, 4-column, unique mechanism) — los ejemplos son Zelva44, la estructura es universal |
| `/kokoro-parrilla` ya es un archivo grande (8KB) | S46.6 reescribe de cero, no parchea |
| Curva de aprendizaje para operadores | Los quality gates son binarios (pasa/no pasa) — no requieren criterio experto |

## Parking Lot

- Automatizar quality gates con script de validación
- Generar territory map automáticamente desde buyer personas
- Integrar con `/kokoro-cur` (Fase C) para que CUR alimente los trigger events
