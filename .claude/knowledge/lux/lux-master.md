---
knowledge_id: "lux-master"
purpose: "Unified luxury framework synthesis — cross-module master reference for router skill"
sources: ["notas-eduardo/Arquitectura_Completa_del_Lujo"]
consumed_by: ["/kokoro-luxury"]
---

# Lux by Kokoro Master — Arquitectura Integral del Lujo

> A unified framework for understanding, building, and scaling luxury brands
> with coherence, purpose, and strategic power.

## The Architecture

Luxury is not a set of scattered tactics. It is an **integrated system** where
every element — from initial positioning to pricing strategy — reinforces a
central purpose: creating lasting symbolic value that justifies exceptional
prices and generates genuine loyalty.

> "La coherencia es la base para generar confianza desde el primer segundo,
> un activo invaluable que, una vez perdido, es casi imposible de recuperar."

## The 5 Parts of the Architecture

### Part 1: El Mapa Fundamental
**Module:** `lux-assessment.md`

The three universes of value: Mass Market, Premium, Luxury. The fundamental
decision is architectural — it defines your entire operations model.

**Key framework:** Triangulo Funcional-Simbolico-Emocional (F-S-E)
- F-driven upward = Premium
- S/E-driven upward = Luxury
- No successful hybrids exist — coherence requires absolute clarity

### Part 2: Diferenciacion y Construccion de Valor
**Modules:** `lux-assessment.md` + `lux-quality-symbolism.md`

Premium vs Luxury is the critical distinction. Plus: the 8 Pillars of Symbolic
Architecture — the invisible foundation of every luxury brand.

**8 Pilares:**
1. Mito Fundacional — Genesis narrative
2. Leyenda — Collective meaning propagation
3. Iconos y Simbolos — Visual anchoring system
4. Objetos de Culto — Identity materialization
5. Rituales — Intentional experience choreographies
6. Liturgias — Collective community synchronization
7. Lugares de Culto — Spatialization of meaning
8. Shopper Journey — Symbolic initiation path

### Part 3: Los Superpoderes del Lujo
**Modules:** `lux-scarcity.md` + `lux-quality-symbolism.md` + `lux-experience.md`

Three superpowers that create desire:

| Superpower | Creates | Key metric |
|------------|---------|-----------|
| **Escasez** | Desire through controlled limitation | Demand Gap Index >= 30% |
| **Calidad** | Justification for exceptional pricing | Quality Perception Index |
| **Experiencia** | Emotional memory and advocacy | Experience Memory Rate >= 70% |

**Dream Equation:**
```
Deseabilidad = 1 / (Puertas x Visibilidad Comun)
```

### Part 4: Construccion de la Marca
**Module:** `lux-communication.md`

Communication that elevates — visual codes, artification, vocabulary strategy.

**Key frameworks:**
- Paleta 60/30/10 (color strategy)
- Silencio Visual (less is luxury)
- Artificacion Scale (7 levels of art integration)
- Vocabulario Luxurizante (word substitution table)

**The formula:**
```
Known by many + Accessible by few + Admired by all = Luxury
```

### Part 5: Escala y Rentabilidad
**Modules:** `lux-pricing.md` + `lux-growth.md`

Pricing as philosophy and growth without dilution.

**Pricing:**
- Veblen Effect: price increase → desirability increase
- 3 Principles: no cost-plus, always increase, never discount
- Value-Based Pricing is the only valid approach

**Growth:**
- 3 strategies: geographic expansion, portfolio management, brand stretching
- Luxury Pyramid (5 levels from Ultra High-End to Everyday Luxury)
- 3 Golden Rules of stretching

## Cross-Module Decision Tree

Use this when routing invitados to the right module:

```
START
  |
  v
Has the invitado been assessed? (positioning_tier in profile)
  |
  NO --> /kokoro-luxury-assess
  |
  YES --> Is tier "luxury" or "premium"?
    |
    NO (standard) --> "Luxury modules don't apply. Consider /kokoro-diagnose"
    |
    YES --> What does the invitado need?
      |
      +-- "I want to understand my positioning" --> /kokoro-luxury-assess
      +-- "I need to create scarcity/exclusivity" --> /kokoro-luxury-scarcity
      +-- "I need to elevate quality/symbolism" --> /kokoro-luxury-quality
      +-- "I need to design experiences" --> /kokoro-luxury-experience
      +-- "I need to elevate my communication" --> /kokoro-luxury-communication
      +-- "I need pricing strategy" --> /kokoro-luxury-pricing
      +-- "I need to grow without diluting" --> /kokoro-luxury-growth
      +-- "I'm not sure / show me everything" --> Present module menu
```

## Module Interaction Map

```
Assessment ─────────── gates access to all modules
     |
     v
Scarcity ←──────────→ Pricing (Dream Equation affects pricing power)
     |                    |
     v                    v
Quality ←──────────→ Communication (quality story drives communication)
     |                    |
     v                    v
Experience ←─────────→ Growth (experiences scale through pyramid levels)
```

No module operates in isolation. Every decision in one area impacts the others.
The master skill should always check: "Does this recommendation maintain
coherence across all modules?"

## Implementation Priority

For a brand new to luxury positioning:

| Phase | Module | Why first |
|-------|--------|-----------|
| 1 | Assessment | Must know where you stand before moving |
| 2 | Quality + Symbolism | Foundation — can't fake luxury without substance |
| 3 | Communication | How you tell the story determines perception |
| 4 | Scarcity | Control access once you have something worth restricting |
| 5 | Experience | Design memorable moments once brand is established |
| 6 | Pricing | Set price after value is fully communicated |
| 7 | Growth | Scale only after all other modules are solid |

## Anti-patterns (Cross-module)

- **Skipping assessment** — Applying luxury tactics to a standard business
- **Module isolation** — Working on pricing without considering scarcity
- **Tactics without foundation** — Doing exclusive events without quality substance
- **Growth before coherence** — Scaling before all modules are aligned
- **Copying luxury brands** — Imitating Hermes aesthetics without Hermes substance
