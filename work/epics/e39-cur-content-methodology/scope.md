# Epic E39: CUR — Contenido Útil Relevante (Parrilla Fase C)

> **Status:** COMPLETE
> **Created:** 2026-06-09
> **Deuda desde:** E40 (referenciada como "herramienta futura E39")

## Objective

Crear el skill humano `/kokoro-cur` para la Fase C de la parrilla de
contenido. CUR guía al operador a definir pilares de contenido que sean
útiles para la audiencia Y relevantes para el negocio — el sweet spot
donde la parrilla genera valor real.

**Value:** La parrilla de contenido tiene 6 fases. Las fases A, B, D, E, F
tienen skills implementados. La Fase C lleva meses como "herramienta futura
E39". Cerrar este gap completa el pipeline de la parrilla.

## Stories (3 planned)

| ID | Story | Size | Description |
|----|-------|:----:|-------------|
| S39.1 | CUR Knowledge File | M | Crear `kokoro-cur-method.md`: metodología, pilares, sweet spot, ejemplos |
| S39.2 | /kokoro-cur Command | M | Crear el comando que guía al operador paso a paso en la sesión |
| S39.3 | Integrate into Parrilla | S | Actualizar `kokoro-parrilla.md` y `kokoro-parrilla-method.md`: quitar "futura E39", enlazar skill real |

**Total:** 3 stories, 7 SP

## Scope

### In scope (MUST)
- Definir metodología CUR con criterios claros de utilidad y relevancia
- Crear comando `/kokoro-cur` que guíe al operador
- Gate: al menos 3 pilares de contenido validados contra insights de Fase A
- Output: matriz CUR (pilares, temas por pilar, formatos sugeridos)
- Integrar en el pipeline de la parrilla como Fase C

### In scope (SHOULD)
- Ejemplos de pilares CUR para distintos tipos de negocio
- Anti-patrones comunes (contenido que parece útil pero no lo es)

### Out of scope
- Automatización con IA (es un skill humano)
- Integración con Meta Ads o calendarización
- UI o dashboard

## Done Criteria

- [x] `/kokoro-cur` existe como comando y guía al operador
- [x] `kokoro-cur-method.md` documenta la metodología completa
- [x] `kokoro-parrilla.md` referencia el skill real (no "futura E39")
- [x] Gate de 3 pilares implementado en el comando

## Dependencies

Ninguna. CUR es autónomo — se alimenta de los insights de Fase A (Buyer
Personas) y Fase B (Alma de Marca) pero no depende de código de otras fases.

## Risks

| Risk | Mitigation |
|------|------------|
| CUR es subjetivo por naturaleza | El gate de 3 pilares + validación contra insights asegura calidad mínima |
| Skill "humano" difícil de testear | El output es una matriz estructurada — validable por completitud |
