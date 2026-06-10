# Epic E46: Parrilla 2.0 — Content Grid Engine

> **Status:** IN PROGRESS
> **Created:** 2026-06-09
> **Origin:** Metodología de parrilla de contenido (patrones universales)
> **Depends on:** E39 (CUR), Fase C de la parrilla

## Objective

La parrilla actual (`/kokoro-parrilla` + `kokoro-parrilla-method.md`)
es un esqueleto de 6 fases sin profundidad táctica. E46 la convierte en
un **motor de parrilla** que funciona para cualquier negocio — desde un
restaurante hasta una inmobiliaria, desde un SaaS hasta un consultor.

**Value:** Kokoro no entrega templates. Kokoro guía al emprendedor a
descubrir SU propia parrilla: qué decir, a quién, con qué mecanismo,
cómo saber si funciona.

## Principios de Diseño

1. **No templates.** El output es específico del negocio, no genérico.
2. **La data manda.** La parrilla nace de lo que ya funcionó y falló,
   no de lo que "debería" funcionar.
3. **Separación estricta.** Lo que ve la audiencia ≠ lo que necesita
   el equipo para producir.
4. **Cada pieza tiene un porqué.** Si dos piezas hacen lo mismo, una sobra.
5. **Gates, no opiniones.** Cada decisión se valida contra criterios
   verificables.

## Stories (6 planned)

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| S46.1 | Pre-Review Protocol | M | Antes de crear, revisar 4 capas: qué funcionó/falló en data real, qué dice la estrategia del negocio, qué feedback existe. Si falta una capa, la parrilla sale genérica. |
| S46.2 | Trigger Discovery Engine | M | Metodología para pasar de "lo que mi negocio tiene" a "lo que mi audiencia está viviendo cuando decide". No es copywriting — es psicología de decisión. |
| S46.3 | Output Separation System | M | 4 columnas con propósito distinto: lo que la audiencia ve en 2 segundos, lo que el equipo necesita para producir, lo que se publica, lo que se revisa internamente. |
| S46.4 | Territory Mapping | S | Cada pieza ocupa un territorio distinto. Mapa visual de territorios para evitar refritos. Si dos piezas comparten mecanismo, el mapa lo detecta. |
| S46.5 | Quality Gates | S | 8 criterios binarios de aprobación. ¿Esto lo podría decir cualquier negocio del mismo rubro? ¿El primer segundo justifica detenerse? ¿El equipo puede producirlo sin preguntar? |
| S46.6 | Engine Integration | L | Unificar S46.1–S46.5 en un flujo cohesivo. Reescribir `/kokoro-parrilla` y `kokoro-parrilla-method.md` como un motor, no como un template. |

**Total:** 6 stories, 16 SP

## Scope

### In scope (MUST)
- Protocolo de pre-review: qué datos mirar, cómo extraer patrones
- Metodología de trigger discovery: del atributo al evento mental
- Sistema de output separation: 4 columnas con propósito y consumidor
- Territory mapping: cómo detectar que dos piezas se solapan
- 8 quality gates con criterios de aprobación/rechazo
- Flujo unificado en `/kokoro-parrilla` que guía al operador paso a paso

### In scope (SHOULD)
- Ejemplos genéricos multi-industria (servicios, producto físico, SaaS, real estate)
- La parrilla sirve tanto para un solopreneur como para un equipo con creativo y media buyer

### Out of scope
- Generación automática de copy o creativos
- Integración con APIs de Meta/Google
- Calendarización o scheduling
- UI visual de la parrilla

## Done Criteria

### Per story
- [ ] Pre-review protocol: el operador sabe qué datos revisar antes de crear
- [ ] Trigger discovery: el operador puede convertir un atributo en un evento mental
- [ ] Output separation: las 4 columnas están documentadas con propósito y anti-patrones
- [ ] Territory mapping: existe un template de mapa de territorios
- [ ] Quality gates: 8 criterios binarios, verificables sin criterio experto
- [ ] `/kokoro-parrilla` unificado: el operador sigue el flujo y produce parrilla operable

### Epic complete
- [ ] Un emprendedor sin experiencia en marketing puede seguir el flujo y obtener una parrilla
- [ ] La parrilla producida tiene mecanismos distintos por pieza
- [ ] El output separa claramente lo público de lo interno
- [ ] Las quality gates son verificables por cualquier persona del equipo
- [ ] Merged to main

## Dependencies

```
S46.1 (pre-review: qué mirar antes de crear)
  ↓
S46.2 (triggers: del atributo a la decisión) ──┐
S46.3 (separation: 4 columnas) ────────────────┤
S46.4 (territories: sin solapamiento) ─────────┤
S46.5 (gates: aprobación binaria) ─────────────┘
  ↓
S46.6 (engine: unificar todo en el comando)
```

## Architecture

| Decisión | Por qué |
|----------|---------|
| El motor es un guía, no un generador | Kokoro no reemplaza al emprendedor — lo eleva |
| 4 columnas con propósito distinto | Cada columna tiene un consumidor. Mezclarlas produce confusión |
| Territorios, no plantillas | Un template produce refritos. Un mapa de territorios obliga a pensar |
| Gates binarios, no opiniones | "¿Esto lo podría decir otro negocio?" se responde sí/no. No requiere experiencia |

## Riesgos

| Riesgo | Mitigación |
|--------|------------|
| La metodología es abstracta sin ejemplos | Cada story incluye ejemplos genéricos de al menos 2 industrias distintas |
| El operador se salta el pre-review | El comando no avanza sin confirmar que las 4 capas fueron revisadas |
| Territory mapping es difícil de explicar | Se entrega un template visual (tabla) que hace el solapamiento obvio |
