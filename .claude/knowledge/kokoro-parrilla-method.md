# /kokoro-parrilla-method — Metodologia del Pipeline Parrilla (6 Fases)

> Metodologia completa del pipeline Parrilla de Contenido Comercial.
> 6 fases encadenadas con gates entre fases, loop de feedback v1→v2,
> y entrega de xlsx de 3 hojas.
>
> "No construyes una parrilla — cultivas un ecosistema de angulos."

## Principio fundacional

La Parrilla de Contenido Comercial no es un calendario editorial. Es un
**mapa de cobertura de angulos** sobre el cual se siembran 12 piezas de
contenido que cubren los clusters del corpus del invitado. Cada decision
en la parrilla se fundamenta en una Base de Aprendizaje — no en opinion.

## Las 6 Fases

### Fase 0 — Tracking Check (verificacion de medicion)

**Skill:** `/kokoro-tracking-check`

Antes de cualquier analisis, verifica que el tracking digital esta sano.
Si el tracking miente, todos los datos posteriores son ruido.

**Gate:** Si hay CRITICOS → WAIT. No pasar a Fase A hasta reparacion.
Si GO → continuar.

**Output:** gap-list priorizada + GO/WAIT verdict

---

### Fase A — Inteligencia base

**Skills humanas:** `/kokoro-listen`, `/kokoro-research`, `/kokoro-audit`

Analisis del contexto del invitado:
- Escucha de su audiencia (transcripts, redes, reviews)
- Investigacion de mercado y competencia
- Auditoria de sitio web y presencia digital

**Gate:** Output debe contener al menos 3 insights de audiencia utilizables
para la parrilla. Si no, volver a escuchar.

**Output:** brief de inteligencia (contexto del invitado, insights de audiencia,
panorama competitivo)

---

### Fase B — Alma de marca

**Skills humanas:** `/kokoro-onboard`, lectura de landing/website

Conexion con la identidad del invitado:
- Voz, tono y personalidad de marca
- Promesa central y diferenciacion
- Buyer personas y segmentos

**Gate:** Output debe incluir al menos 2 buyer personas definidas con
necesidades especificas. Si no, volver a indagar.

**Output:** brief de marca (voz, personalidad, buyer personas, promesa central)

---

### Fase C — CUR (Contenido Util Relevante)

**Skills humanas:** metodologia CUR → `/kokoro-cur`

Definicion de los pilares de contenido:
- Que contenido es UTIL para la audiencia
- Que contenido es RELEVANTE para el negocio
- Donde se cruzan ambos → sweet spot de la parrilla

**Gate:** Output debe producir al menos 3 pilares de contenido validados
contra los insights de Fase A. Si no, ajustar pilares.

**Output:** matriz CUR (pilares de contenido, temas por pilar, formatos sugeridos)

---

### Fase D — Feed Audit (auditoria del corpus Meta Ads)

**Skill:** `/kokoro-feed-audit`

Audita el corpus activo de Meta Ads por angulo y cluster:
- Que angulos estan cubiertos
- Que angulos estan ausentes
- Que anti-patrones de senal se detectan

**Gate:** corpus.json debe tener angles_absent con al menos 2 entradas
(angulos por explorar). Si todos los angulos estan cubiertos, el invitado
tiene un corpus completo y la parrilla se enfoca en profundizar clusters.

**Output:** `corpus.json` con angles_covered, angles_absent, antipatterns

---

### Fase E — Propuesta v1 + loop feedback

**Skill:** `/kokoro-parrilla` (orquestador)

Sintesis de las fases previas en una propuesta de parrilla:

1. **v1 strawman** — primera version de la parrilla (12 piezas) basada en
   los inputs de Fases A-D
2. **Feedback elevation** — el operador eleva la parrilla al CMO/invitado
   para feedback dirigido. Cada pieza de feedback se convierte en una
   regla global (no en un cambio puntual)
3. **v2 (max 2 pasadas)** — segunda version incorporando las reglas
   elevadas del feedback. Maximo 2 pasadas de feedback (v1 strawman →
   feedback → v2). Si hay mas de 2 rondas, el exceso se parquea para
   el piloto.

**Gate:** Maximo 2 pasadas. Si el feedback requiere mas, parquear para
post-piloto.

**Output:** brief de parrilla v1 (strawman) o v2 (post-feedback)

---

### Fase F — Parrilla xlsx + verificacion pre-delivery

**Skill:** `/kokoro-parrilla` (orquestador)

Generacion del xlsx final y verificacion:

1. **Generar xlsx** con `scripts/generate-parrilla-xlsx.py` — 3 hojas:
   - Hoja 1: Reglas Globales + Cuello del Funnel (preamble)
   - Hoja 2: Parrilla 12 piezas (12 filas con columnas definidas)
   - Hoja 3: Bases de Aprendizaje (≥15 citas verificables)

2. **Verificacion pre-delivery** (deterministica, NO LLM):
   1. Vocabulario commodity — grep contra [precio, descuento, cliente, gratis, barato, comprar, vender, gastar]
   2. Vocabulario binario — grep contra [ganador, perdedor, funciono, no funciono, el mejor, el peor]
   3. Referencias internas — grep contra lista provista por usuario
   4. Hoja 3 minima — assert len(rows) >= 15
   5. Citas verificables — assert columna Fuente no vacia en cada fila
   6. Fechas absolutas — regex contra fechas relativas
   7. Typos nombres propios — comparar contra lista confirmada

3. **Si hay fail** → el xlsx NO se entrega. Reportar al operador.
4. **Si pasa** → entregar xlsx + verification-report.md

**Gate:** Verificacion 7 checks debe pasar. Si no, no entregar.

**Output:** `parrilla-{slug}-v{N}-piloto-{YYYY-MM}.xlsx` + `verification-report.md`

---

## Esquema del xlsx

### Hoja 1 — Reglas Globales + Cuello del Funnel

- Principio fundacional (1 parrafo)
- Tabla de 7-9 reglas globales (ID R1..R9)
- Declaracion explicita del cuello del funnel
- Parking lot post-piloto

### Hoja 2 — Parrilla (12 filas)

Columnas en orden:
`# | Nombre AT | Dia/Semana | Formato | Pilar | Buyer Persona | Texto en pieza | Copy caption | Guion/Idea visual | Que NO hacer | CTA`

### Hoja 3 — Bases de Aprendizaje (≥15 filas)

Columnas:
`# | Decision de la parrilla | Por que (fundamentacion) | Evidencia / cita literal | Fuente`

Filename: `marketing/content/parrillas/parrilla-{slug}-v{N}-piloto-{YYYY-MM}.xlsx`

---

## Conexion con otras skills

- `/kokoro-validate` — *"La parrilla que entregaste es una hipotesis
  fundamentada — candidata a `/kokoro-validate` para destilar plan de
  validacion."* (PAT-L-079: soft coupling textual)
- `/kokoro-experiment` — *"...y a `/kokoro-experiment` cuando el primer
  resultado del piloto entre."*
- `/kokoro-quality-gates.md` — gates de calidad que este pipeline satisface
  antes de entrega

## Anti-patrones del pipeline

- **Saltarse Fase 0** — nunca construir parrilla sin tracking verificado
- **Saltarse gates** — cada gate existe por una razon; no avanzar sin
  cumplir criterios
- **Mas de 2 pasadas de feedback** — el exceso se parquea, no se incorpora
- **Entregar xlsx sin verificacion** — los 7 checks son obligatorios
- **Usar LLM como juez** — la verificacion es deterministica (grep, regex,
  listas explicitas)
- **Vocabulario binario** — prohibido en cualquier fase del pipeline
