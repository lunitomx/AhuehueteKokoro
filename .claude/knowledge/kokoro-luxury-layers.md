---
knowledge_id: "kokoro-luxury-layers"
purpose: "Luxury-specific augmentation for base Kokoro skills when positioning_tier = luxury"
sources:
  - "lux-assessment.md"
  - "lux-scarcity.md"
  - "lux-quality-symbolism.md"
  - "lux-experience.md"
  - "lux-communication.md"
  - "lux-pricing.md"
  - "lux-growth.md"
consumed_by: ["base kokoro skills when client positioning_tier = luxury"]
---

# Kokoro Luxury Layers

> When `positioning_tier = luxury` in the client profile, each base Kokoro skill
> gains additional considerations. This file documents the luxury-specific layer
> for each skill. No base skill is modified — this is additive context only.

**Activation rule:** Check `ClientProfile.metadata["positioning_tier"]`. If the
value is `"luxury"` (or `"premium"` for selective principles), apply the
considerations below in addition to the base skill flow.

**If no tier is set:** Suggest running `/kokoro-luxury-assess` before proceeding,
but do not block the session.

---

## /kokoro-diagnose — Luxury Layer

> Before diagnosing anchors and blind spots, assess WHERE the business sits
> on the F-S-E positioning triangle.

### Considerations

1. **Run the F-S-E positioning check first.** Before the Speed Boat exercise,
   ask: "Is your differentiation primarily functional, symbolic, or emotional?"
   A luxury business whose anchors are functional (cost, features) has a
   positioning incoherence that must be surfaced. [lux-assessment]

2. **Evaluate the Dream Equation.** During the diagnosis, assess:
   `Deseabilidad = 1 / (Puertas x Visibilidad Comun)`. If the invitado has
   too many access points or too much common visibility, that IS the anchor
   — even if they don't see it. [lux-scarcity]

3. **Check for commoditization signals.** Red flags for luxury businesses:
   frequent discounts, price wars, loss of wait lists, mass distribution.
   These indicate a drift from luxury toward premium/mass that the diagnosis
   must name explicitly. [lux-assessment]

4. **Assess symbolic architecture health.** Which of the 8 Symbolic Pillars
   are active (founding myth, icons, rituals, cult objects)? Missing pillars
   are structural weaknesses, not just marketing gaps. [lux-quality-symbolism]

### Key Shift

Standard diagnosis finds operational anchors. Luxury diagnosis must also find
**positioning incoherence** — the gap between luxury aspiration and actual
market behavior.

---

## /kokoro-canvas — Luxury Layer

> A Lean Canvas for luxury operates under structural constraints that
> standard and premium businesses don't face.

### Considerations

1. **Channels block: hyper-selective distribution.** Instead of "where do you
   reach your invitado," the question becomes: "Through how FEW doors do you
   choose to be accessible?" Use the Selectivity Ratio: ultra-luxury < 50
   access points, high luxury < 200, core luxury < 600. [lux-scarcity]

2. **Revenue streams: Veblen-compatible pricing.** The pricing model must
   support systematic price increases over time. Revenue projections should
   assume ascending prices, not stable or declining — luxury ALWAYS increases
   prices. [lux-pricing]

3. **Unfair advantage: symbolic architecture.** The moat for luxury is NOT
   features or cost efficiency — it is the founding myth, cult objects, rituals,
   and icons that cannot be replicated. Map which symbolic pillars constitute
   the real unfair advantage. [lux-quality-symbolism]

4. **Cost structure: vertical integration.** Luxury requires control over
   production (artisanal processes, quality at source). The cost structure
   must account for this — outsourcing erodes luxury legitimacy.
   [lux-quality-symbolism]

5. **Key metrics: add Demand Gap Index.** Beyond standard traction metrics,
   luxury needs `(Demand - Supply) / Demand >= 30%`. If demand is not exceeding
   supply, the scarcity engine is broken. [lux-scarcity]

### Key Shift

Standard canvas optimizes for reach and conversion. Luxury canvas optimizes for
**controlled access and symbolic value** — fewer doors, higher meaning per door.

---

## /kokoro-finance — Luxury Layer

> Financial evaluation for luxury inverts the standard logic: pricing power
> comes from perceived value, not from cost structure.

### Considerations

1. **Replace cost-plus with value-based pricing.** Never calculate price as
   cost + margin. Price is determined by: intangible attributes, symbolic value,
   brand mystique, hyper-personalization, and scarcity. The question is "what
   value do I create?" not "what does it cost me?" [lux-pricing]

2. **Apply the Veblen Effect test.** Ask: "If you raised your investment by
   20%, would demand increase?" If yes, the invitado is in Veblen territory
   and should plan systematic price increases. If no, the symbolic foundation
   needs strengthening before pricing changes. [lux-pricing]

3. **Benchmark against luxury, not mass.** The reference price should be the
   most basic creation of an established luxury brand in the same category —
   not the mass-market equivalent. Being at 4-20x above mass is the minimum;
   being at the same level as mass destroys legitimacy. [lux-pricing]

4. **Evaluate pricing power indicators.** Key signals: wait lists (demand
   exceeds supply), secondary market premiums (resale > retail), zero need
   for discounts, and price-driven desirability increases.
   [lux-pricing, lux-scarcity]

5. **Gift > Discount rule.** If a luxury invitado needs to move inventory,
   the strategy is to elevate value (gift additional creations) — never
   admit the value wasn't real by discounting. Discounts are the second
   kryptonite of luxury after massification. [lux-pricing]

### Key Shift

Standard finance asks "how do I become profitable?" Luxury finance asks
"how do I walk FROM profitability?" — pricing as philosophy, not mathematics.

---

## /kokoro-pescar — Luxury Layer

> PESCAR for luxury shifts from persuasion to seduction. The communication
> doesn't sell — it awakens desire through mystery and symbolic resonance.

### Considerations

1. **P (Problema) becomes aspiration, not pain.** Luxury invitados don't buy
   to solve problems — they buy for what it REPRESENTS. Reframe the trigger:
   "What desire does your creation awaken?" not "What problem does it solve?"
   [lux-assessment, lux-communication]

2. **E (Estrategia): seduce, don't explain.** Communication must evoke and
   suggest, never explain features or compare directly. Mass explains, premium
   differentiates, luxury seduces. Use the Artification Scale to elevate
   content through art integration. [lux-communication]

3. **C (Contenido): apply luxury visual codes.** All content must follow:
   Paleta 60/30/10 for color, Silencio Visual (white space as intention, not
   absence), centralidad visual, strategic B&W, emotional/symbolic language
   over technical. [lux-communication]

4. **A (Accion): invitation, not CTA.** Replace direct calls-to-action with
   invitational access. "Apply for access" > "Buy now." "Request an
   appointment" > "Add to cart." The action itself must signal exclusivity.
   [lux-scarcity, lux-communication]

5. **R (Resultado): measure desire, not just conversion.** Add luxury-specific
   metrics: Demand Gap Index, wait list length, Experience Memory Rate (>= 70%
   spontaneous recall at 72h), secondary market price signals.
   [lux-scarcity, lux-experience]

### Key Shift

Standard PESCAR builds awareness-to-conversion. Luxury PESCAR builds
**mystery-to-desire** — the invitado must feel chosen, not targeted.

---

## /kokoro-launch — Luxury Layer

> Luxury launches are not events of maximum exposure. They are ceremonies
> of controlled revelation — slow-burn, invitation-only, designed for scarcity.

### Considerations

1. **Strategic scarcity from day one.** Never launch with full availability.
   Use the Demand Gap principle: produce less than projected demand by at least
   30%. Wait lists, limited editions, and invitational access create desire
   that open availability destroys. [lux-scarcity]

2. **Slow-burn launch (Apnea Comercial).** Replace the standard 4-week
   pre-launch sequence with a longer arc of mystery. Reveal elements gradually
   — the creation is not fully shown until the inner circle has experienced
   it. Luxury whispers; mass shouts. [lux-scarcity, lux-communication]

3. **Invitation-only first wave.** The first access goes to a curated inner
   circle — existing loyal invitados, cultural influencers (as genuine users,
   not paid ambassadors), or strategic early adopters. The launch itself is
   an exclusive experience. [lux-experience]

4. **Landing page as symbolic space.** The landing page must follow luxury
   visual codes: Silencio Visual, Paleta 60/30/10, price revealed only after
   full value transmission. No "limited time offer" urgency — luxury urgency
   comes from genuine scarcity, not countdown timers. [lux-communication]

5. **Post-launch: discontinuity option.** Plan in advance which editions or
   variants will be strategically discontinued to maintain the Dream Equation.
   Patek Philippe discontinued their best-seller at $33k — it surged to
   $150-200k on secondary market. [lux-scarcity]

### Key Shift

Standard launch maximizes first-week exposure. Luxury launch maximizes
**first-week exclusivity** — fewer people experience it initially, but the
ripple effect of desire is far more powerful.

---

## /kokoro-factory — Luxury Layer

> The Customer Factory for luxury is not a volume machine. It is a curation
> engine that selects who enters and controls how many proceed.

### Considerations

1. **Hyper-selective distribution.** The "Adquirir" step in the factory is
   inverted: instead of maximizing reach, minimize access points. Use the
   Door Matrix (open vs close decisions) where revenue per door matters more
   than total doors. Closing an underperforming door is ALWAYS better than
   keeping it with discounts. [lux-scarcity]

2. **Customer curation at acquisition.** The factory must include a
   qualification step: not everyone who wants in gets in. Application
   processes, invitational access, referral requirements. The brand CHOOSES
   its invitados — the "Say-No Brand" model. [lux-scarcity]

3. **Retention through symbolic belonging.** Retention is not driven by
   discounts or loyalty points — it is driven by tribe membership. Use the
   Tribe-Fire Canvas: shared rituals, curated gatherings, content of value,
   and collective memory. The invitado stays because they BELONG, not because
   they get a deal. [lux-experience]

4. **Revenue per invitado > volume.** The factory KPIs must shift from
   "how many invitados" to "how much value per invitado." LTV grows through
   ascending price tiers (Luxury Pyramid: everyday luxury -> core -> high ->
   ultra), not through increasing unit count. [lux-growth, lux-pricing]

### Key Shift

Standard factory optimizes throughput. Luxury factory optimizes
**selectivity and depth** — fewer invitados, deeper relationships, higher
lifetime value per person.

---

## /kokoro-mafia — Luxury Layer

> A luxury Oferta Mafia doesn't just remove objections — it creates a sense
> of being chosen for something few will ever access.

### Considerations

1. **Real exclusivity, not manufactured urgency.** The Mafia Offer for luxury
   must be backed by genuine scarcity: limited production, invitational access,
   artisanal constraints. "Only 50 available" must mean exactly 50, not a
   marketing tactic. Authenticity is the foundation. [lux-scarcity,
   lux-quality-symbolism]

2. **Rituals of access.** The acquisition process itself becomes a ritual:
   application, waiting period, personal communication, ceremonial delivery.
   The Initiatic Journey (8 Symbolic Pillars) transforms the purchase from
   transaction to transformation. [lux-quality-symbolism]

3. **Symbolic power as value driver.** The offer's irresistibility comes not
   from a low price or bonus stack, but from what the creation REPRESENTS:
   founding myth, cult object status, belonging to a tribe. Map which of the
   8 Symbolic Pillars the offer activates. [lux-quality-symbolism]

4. **Price communicates identity.** In luxury, the investment IS part of the
   value proposition — not an objection to overcome. The Mafia Offer should
   never reduce the price to make it "irresistible." Instead, it should make
   the value so symbolically rich that the price feels inevitable.
   [lux-pricing]

5. **Multi-sensory experience packaging.** The offer should include
   experiential elements designed using the 4-D Multisensory framework:
   sight, sound, scent, touch. Delivery itself is a ceremony, not logistics.
   [lux-experience]

### Key Shift

Standard Mafia Offer makes it irrational to refuse by removing risk. Luxury
Mafia Offer makes it irrational to refuse by making exclusion feel like a
**loss of identity and belonging**.

---

## /kokoro-funnel — Luxury Layer

> The luxury funnel does not convert — it seduces. Each stage is a ritual
> of deepening connection, not a step toward a transaction.

### Considerations

1. **Conciencia as cultural presence, not ads.** Luxury awareness is built
   through cultural positioning: art patronage (Artification Scale), symbolic
   events (Fendi on Fontana di Trevi), editorial presence, and word-of-mouth
   from the inner circle. The brand is KNOWN by many but ACCESSIBLE by few.
   [lux-communication, lux-experience]

2. **Consideracion as seduction, not comparison.** The invitado doesn't compare
   features — they are drawn into a symbolic universe. Social proof is not
   "1000+ happy customers" but "George Clooney is a genuine enthusiast" (user
   role, not ambassador role). The brand's power must exceed any individual
   endorser. [lux-communication]

3. **Decision as ceremonial commitment.** The purchase moment is ritualized:
   personal consultation, curated presentation, atmospheric environment. Price
   is communicated AT THE END, after full value transmission. Use round prices,
   no currency symbol when possible, price opacity in physical spaces.
   [lux-pricing, lux-quality-symbolism]

4. **Experiencia as multisensory immersion.** Post-purchase is not "onboarding"
   — it is an initiation. Design using the 4-D Multisensory framework and the
   Fuego de Campamento (Campfire) stages: Spark, Fuel, Circle, Embers. Target
   Experience Memory Rate >= 70% at 72 hours. [lux-experience]

5. **Lealtad as tribe membership.** Loyalty is not a points program — it is
   belonging to an exclusive tribe. Use the Tribe-Fire Canvas: shared rituals,
   curated invitado selection, content of value (artisan masterclasses, not
   discount codes), and collective memory. [lux-experience]

### Key Shift

Standard funnel measures conversion rates. Luxury funnel measures
**desire intensity and tribal belonging** — the invitado doesn't "convert,"
they are welcomed into a world.

---

## Quick Reference Matrix

| Base Skill | Primary Luxury Shift | Key Metric Addition | Source Modules |
|---|---|---|---|
| /kokoro-diagnose | + F-S-E positioning check | Commoditization signals | assessment, scarcity |
| /kokoro-canvas | + Scarcity and distribution constraints | Demand Gap Index >= 30% | scarcity, growth, pricing |
| /kokoro-finance | + Value-based pricing, Veblen | Secondary market premium | pricing, scarcity |
| /kokoro-pescar | + Seduction codes, visual silence | Experience Memory Rate | communication, scarcity |
| /kokoro-launch | + Slow-burn, invitation-only | Wait list conversion | scarcity, communication, experience |
| /kokoro-factory | + Hyper-selective distribution | Revenue per door | scarcity, experience, growth |
| /kokoro-mafia | + Real exclusivity, symbolic power | Symbolic Pillar activation | quality-symbolism, scarcity |
| /kokoro-funnel | + Seduction funnel, ritual stages | Tribal belonging NPS | communication, experience |
