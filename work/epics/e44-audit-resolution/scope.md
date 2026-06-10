# Epic E44: Audit Resolution — Kodawari

> **Status:** COMPLETE
> **Created:** 2026-06-09
> **Trigger:** Auditoría técnica 2026-06-09 (B+, 17 hallazgos)

## Objective

Resolver todos los hallazgos de la auditoría técnica. Dos objetivos
paralelos: (1) eliminar deuda de higiene acumulada y (2) construir
las defensas anti-slop + voice-print que la investigación identificó
como gap estratégico.

**Value:** Un repo limpio proyecta confianza. Una voz blindada contra
AI-slop proyecta humanidad. Ambos son el mismo principio Kokoro:
sprezzatura — elegancia sin esfuerzo aparente.

## Stories (7 planned)

| ID | Story | Size | Cubre hallazgos |
|----|-------|:----:|-----------------|
| S44.1 | Extraer IDENTITY.md canónico | M | A1 — drift AGENTS/CLAUDE |
| S44.2 | Knowledge files para 17 comandos huérfanos | L | A2 — superficie sin documentar |
| S44.3 | Quick wins: zombie E34, .xlsx, SETUP, sesiones | S | A3, S2, C2, O2 |
| S44.4 | Mover work/ fuera de commands/ | S | A4 — estructura huérfana |
| S44.5 | .env.example + CI link checker | S | O3, T1 |
| S44.6 | TOC en archivos >15KB | S | C3 — navegabilidad |
| S44.7 | Anti-slop español + VoicePrint Eduardo | L | Investigación — gap estratégico |

**Total:** 7 stories, 20 SP

## Scope

### In scope (MUST)
- Extraer identidad Kokoro a IDENTITY.md sin romper AGENTS.md ni CLAUDE.md
- Documentar los 17 comandos sin knowledge file
- Eliminar E34 zombie, .xlsx binario, sesiones vacías
- Actualizar SETUP-CLAUDE-DESKTOP.md con counts reales
- Mover .claude/commands/work/ → work/epics-archive/
- Crear .env.example
- Agregar TOC a archivos >15KB
- Crear skill anti-slop en español
- Formalizar VoicePrint de Eduardo

### In scope (SHOULD)
- GitHub Action: markdown link checker

### Out of scope
- Reescribir AGENTS.md o CLAUDE.md completos
- Migrar RaiSE skills a otro lado
- Tests automatizados de markdown
- Dashboard o UI

## Done Criteria

### Per story
- [ ] IDENTITY.md es la fuente canónica de voz/vocabulario/arquetipos
- [ ] 17 knowledge files creados, cada comando referencia al menos uno
- [ ] E34, .xlsx, sesiones vacías eliminados; SETUP actualizado
- [ ] work/ reubicado fuera de .claude/commands/
- [ ] .env.example existe; CI opcional documentado
- [ ] Archivos >15KB tienen TOC
- [ ] anti-slop-es SKILL.md existe; VoicePrint documentado

### Epic complete
- [ ] 0 hallazgos Medium abiertos del audit
- [ ] 0 hallazgos Low abiertos del audit
- [ ] Merged to main

## Dependencies

```
S44.3 (quick wins, sin dependencias)
S44.4 (mover work/)
S44.1 (IDENTITY.md)
S44.2 (knowledge files) ← puede paralelizarse con S44.7
S44.5 (.env.example + CI)
S44.6 (TOC) ← puede paralelizarse con S44.7
S44.7 (anti-slop + voice) ← puede paralelizarse con S44.2
```

## Architecture Note

S44.1 NO fusiona AGENTS.md con CLAUDE.md. Extrae la identidad compartida
(voz, vocabulario, arquetipos, metodología) a un archivo canónico que
ambos referencian. Cada runtime conserva su entry point con instrucciones
específicas de carga de skills.

```
IDENTITY.md          ← Voz, vocabulario, arquetipos (fuente única)
AGENTS.md            ← "Lee IDENTITY.md" + instrucciones Codex
CLAUDE.md            ← "Lee IDENTITY.md" + instrucciones Claude
```

## Risks

| Risk | Mitigation |
|------|------------|
| Extraer identidad rompe referencias en runtime | Ambos entry points conservan su estructura; solo se mueve contenido compartido |
| 17 knowledge files es mucho volumen | Priorizar por batch: sub-comandos primero, core methodology después, transversales al final |
| Anti-slop español sin precedentes | Basarse en `jalaalrd/anti-ai-slop-writing` (⭐146) como plantilla; adaptar patrones al español |

## Parking Lot

- Integrar anti-slop + voice en un pipeline automático (post-E44)
- VoicePrint runtime: medir longitud de oración, densidad metafórica, ratio pregunta/afirmación
