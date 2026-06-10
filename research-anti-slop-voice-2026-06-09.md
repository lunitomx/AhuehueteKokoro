# Investigación: Anti-AI-Slop y Clonación de Voz Escrita

> RaiSE Research — 2026-06-09
> Triangulación: GitHub API + documentación de proyectos + Kokoro existente

---

## Resumen Ejecutivo

**Anti-AI-Slop en español:** No existe una herramienta dedicada. El mejor
approach es adaptar `jalaalrd/anti-ai-slop-writing` (⭐146, 50+ banned words,
35+ banned phrases) traduciendo los patrones al español. El precedente
checo (`nowork-ai/anti-ai-slop-cz`, ⭐10) demuestra que la adaptación
idiomática es viable y efectiva.

**Clonación de voz escrita:** `Ab-Romia/Style-Echo-AI-Humanizer` (⭐4) es
el approach correcto: VoicePrint aprende de muestras de escritura real y
aplica el estilo a cualquier output. Pequeño pero arquitectónicamente
correcto. Kokoro ya tiene una base sólida con `hallmark` (anti-slop
design) y `humanizer` (humanización de texto).

---

## Parte 1: Anti-AI-Slop Tools

### Hallazgo 1.1 — `jalaalrd/anti-ai-slop-writing` (LÍDER)

| Campo | Dato |
|-------|------|
| ⭐ | 146 |
| Fuente | GitHub API + README |
| Idioma | Inglés (universal) |
| Compatibilidad | Claude Code, Codex, Cursor, Gemini CLI, 8+ agents |
| Confianza | **Alta** — proyecto activo, documentación detallada |

**Qué hace:** 50+ banned words, 35+ banned phrases, 16 banned openers,
10 structural patterns, punctuation tells, formatting leaks, accuracy
failures. Basado en investigación de Carnegie Mellon (2025), Wikipedia
"Signs of AI Writing", y análisis de Buffer (52M posts).

**Adaptación al español requeriría:**
- Traducir banned words (delve→profundizar, tapestry→tapiz, vibrant→vibrante)
- Identificar patrones específicos del español (gerundios abusivos,
  "sin lugar a dudas", "es importante destacar", conectores académicos)
- Ajustar structural patterns (rule of three en español, hedging patterns)

### Hallazgo 1.2 — `adenaufal/anti-slop-writing` (PRECEDENTE MULTILINGÜE)

| Campo | Dato |
|-------|------|
| ⭐ | 75 |
| Fuente | GitHub API + README |
| Idioma | Bahasa Indonesia + English (bilingüe) |
| Confianza | **Alta** — demuestra que la adaptación idiomática funciona |

**Qué aporta:** Versión "lite" para contextos de caracteres limitados
(ChatGPT Custom Instructions). Instalación por plataforma documentada
(Claude Code, ChatGPT, Gemini, Copilot, API, local LLM).

**Relevancia para Kokoro:** El approach bilingüe (idioma nativo + English)
es exactamente lo que Kokoro necesita (español + English).

### Hallazgo 1.3 — `nowork-ai/anti-ai-slop-cz` (PRECEDENTE CHECO)

| Campo | Dato |
|-------|------|
| ⭐ | 10 |
| Fuente | GitHub API |
| Idioma | Checo |
| Confianza | **Media** — prueba de concepto |

**Qué demuestra:** Adaptar anti-slop a un idioma no-inglés es viable.
Reglas específicas por idioma (čeština tiene sus propios tells de AI).

### Hallazgo 1.4 — Español: vacío detectado

**No existe herramienta anti-AI-slop en español en GitHub.** Búsquedas
con `español`, `spanish`, `castellano` no arrojaron resultados relevantes.
Esto es una **oportunidad**: Kokoro puede ser el primer skill anti-slop
en español para agentes AI.

---

## Parte 2: Clonación de Voz Escrita (Writing Style Clone)

### Hallazgo 2.1 — `Ab-Romia/Style-Echo-AI-Humanizer` (ARQUITECTURA CORRECTA)

| Campo | Dato |
|-------|------|
| ⭐ | 4 |
| Fuente | GitHub API |
| Enfoque | VoicePrint — aprende de muestras de escritura |
| Confianza | **Media** — proyecto pequeño pero arquitectura sólida |

**Concepto clave:** VoicePrint analiza muestras de escritura real de una
persona y extrae: longitud de oración, vocabulario característico,
patrones de puntuación, muletillas, estructura de párrafos, tono
emocional. Luego aplica ese perfil a cualquier texto generado por AI.

**Aplicación a Kokoro:** Eduardo ya tiene un perfil de voz documentado
(SOUL.md, AGENTS.md, CLAUDE.md). VoicePrint podría formalizarse como
parte del sistema de identidad de Kokoro.

### Hallazgo 2.2 — `rudra496/StealthHumanizer`

| Campo | Dato |
|-------|------|
| ⭐ | 43 |
| Fuente | GitHub API |
| Enfoque | Multi-proveedor (35), multi-estilo (6), multi-idioma (16+) |
| Confianza | **Alta** |

**Relevancia:** 16+ idiomas sugiere que el español está cubierto.
Enfoque en "bypass detection" más que en clonación de estilo. Útil
como complemento, no como solución principal de voz.

### Hallazgo 2.3 — Kokoro ya tiene base

| Skill existente | Propósito | Cobertura |
|-----------------|-----------|:---------:|
| `hallmark` | Anti-AI-slop para diseño web | Diseño visual |
| `humanizer` | Humanizar texto (quitar AI-isms) | Texto general |
| `voice-dna` | Guía de escritura para voz humana | Voz |
| SOUL.md | Identidad completa de Eduardo | Personalidad |

**Gap detectado:** Estas herramientas están dispersas. No hay un sistema
unificado de "voice cloning" que tome muestras de Eduardo, extraiga un
VoicePrint, y lo aplique consistentemente a todo output.

---

## Recomendaciones para Kokoro

### Corto plazo (esta épica)

1. **Skill `anti-ai-slop-es`**: Adaptar `jalaalrd/anti-ai-slop-writing` al
   español. Traducir banned words, agregar patrones específicos del español,
   y validar contra textos generados por Claude/DeepSeek en español.

2. **VoicePrint de Eduardo**: Formalizar el perfil de voz en un documento
   estructurado (no solo prosa) con métricas medibles: longitud promedio
   de oración, densidad metafórica, ratio pregunta/afirmación, vocabulario
   característico.

### Mediano plazo

3. **Sistema unificado anti-slop + voice**: Integrar `anti-ai-slop-es` +
   VoicePrint + `hallmark` + `humanizer` en un pipeline que todo output
   de Kokoro atraviese antes de llegar al usuario.

---

## Fuentes

| Fuente | Tipo | Confianza |
|--------|------|:---------:|
| GitHub API search (`anti+slop+ai+writing`) | Primaria | Alta |
| GitHub API search (`ai+text+humanizer+writing+style`) | Primaria | Alta |
| `jalaalrd/anti-ai-slop-writing` README | Primaria | Alta |
| `adenaufal/anti-slop-writing` README | Primaria | Alta |
| Carnegie Mellon AI detection research (2025) — referenciado por jalaalrd | Secundaria | Media |
| Wikipedia "Signs of AI Writing" — referenciado por adenaufal | Secundaria | Alta |
| `.claude/skills/hallmark/SKILL.md` | Primaria | Alta |
| `SOUL.md` (identidad Kokoro) | Primaria | Alta |

---

## Niveles de Confianza

| Hallazgo | Confianza | Razón |
|----------|:---------:|-------|
| `jalaalrd` es el líder en anti-slop | Alta | ⭐146, documentación detallada, multi-agente |
| No existe anti-slop en español | Alta | 3 búsquedas, cero resultados |
| Adaptación idiomática es viable | Alta | Precedentes: checo, indonesio, chino |
| VoicePrint es el approach correcto | Media | Proyecto pequeño (⭐4) pero arquitectura sólida |
| Kokoro tiene base dispersa | Alta | 4 skills existentes, sin integración |
