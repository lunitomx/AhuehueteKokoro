# /kokoro-diagnose — Diagnostico Estrategico (Orquestador)

> Sesion guiada de Fase 1: Preparar el Suelo
> Herramientas: Mapa de Anclas + Ranking de Claridad
> Patron: ORQUESTADOR — delega a sub-skills, no hace trabajo sustantivo
> Sub-skills: `/kokoro-diagnose-anclas` → `/kokoro-diagnose-ranking` → `/kokoro-diagnose-report`

## Contexto

Este skill guia una sesion de diagnostico estrategico usando dos herramientas
de la metodologia Kokoro. El objetivo es hacer visible lo invisible: las
anclas que frenan el negocio y los puntos ciegos que el emprendedor no ve.

Lee el archivo de conocimiento `kokoro-phase1-diagnostico.md` para profundizar
en la metodologia de cada ejercicio.

Lee tambien `kokoro-tactiq-field-patterns.md` cuando el diagnostico venga de
Q&A, capsula o caso real. El corpus Tactiq 2025 mostro que muchos pedidos de
"campana", "ads" o "IA" eran sintomas de suelo, seguimiento, medicion o foco.

### Gate Tactiq 2025 — diagnostico antes de tactica

Si el usuario pide una tactica pero hay senales de ambiguedad, diagnostica:

| Senal | Ruta |
|-------|------|
| Quiere mas leads pero no sabe donde se pierden | `/kokoro-growth-diagnosis-run`. |
| Quiere campana sin fuerza de eleccion | `/kokoro-campaign-lab-run`. |
| Quiere IA o agente sin workflow repetible | `/kokoro-ai-copilot-run`. |
| Quiere optimizar sin fuente de verdad | `/kokoro-tracking-check`. |

El diagnostico debe cerrar con fase Kokoro, cuello principal, evidencia minima
y siguiente skill recomendado. Si hay duda de CRM, WhatsApp, tracking o fuente
de verdad, no pases a tactica hasta aclarar donde se registra el aprendizaje.

### Quality Gates

Este orquestador aplica gates de `kokoro-quality-gates.md` entre cada fase:
- GATE-ARTIFACT-EXISTS
- GATE-CONTENT-COMPLETE
- GATE-FORMAT-VALID
- GATE-NO-PLACEHOLDERS

### Dependencias

- **Knowledge**: `kokoro-phase1-diagnostico.md` para metodologia de ejercicios
- **Contexto**: `.kokoro/state.json` si existe (estado actual del emprendedor)
- **Grafo**: `.kokoro/clients.json` para resolver invitado
- **Output**: `.kokoro/diagnostics/anclas.md`, `.kokoro/diagnostics/ranking.md`, `.kokoro/state.json`

## Estructura del Orquestador

Este skill ejecuta 3 sub-skills en secuencia:

1. **`/kokoro-diagnose-anclas`** — Ejercicio Mapa de Anclas (vientos, anclas, rocas, priorizacion)
   - Produce: `.kokoro/diagnostics/anclas.md`
   - Gate: GATE-ARTIFACT-EXISTS + GATE-CONTENT-COMPLETE
2. **`/kokoro-diagnose-ranking`** — Ejercicio Ranking de Claridad (vision clara, borrosa, puntos ciegos, lentes)
   - Lee: anclas.md → Produce: `.kokoro/diagnostics/ranking.md`
   - Gate: GATE-ARTIFACT-EXISTS + GATE-FORMAT-VALID
3. **`/kokoro-diagnose-report`** — Reporte consolidado + plan de accion + persistencia
   - Lee: anclas.md + ranking.md → Actualiza: `.kokoro/state.json`
   - Gate: GATE-ARTIFACT-EXISTS (state.json actualizado) + GATE-CONTENT-COMPLETE

## Instrucciones para el Orquestador

### Contexto previo

Si existe el archivo `.kokoro/state.json` en el directorio del proyecto,
leelo para conocer el estado actual del emprendedor. Si ya completo otros
skills, usa esa informacion como contexto — no le pidas que repita lo que
ya compartio en sesiones anteriores.

### Resolucion de invitado

Antes de iniciar, intenta resolver al invitado desde el grafo:

1. Si el usuario menciona un nombre de invitado, busca en `.kokoro/clients.json`
   usando `find_by_name` (coincidencia parcial, case-insensitive)
2. Si encuentra al invitado:
   - Lee su `context_file` si existe (datos reales del proyecto)
   - Lee sus `repos` para obtener datos actualizados (inventario, tarifas)
   - Lee sus `segments` para entender los publicos
   - Lee su `metadata` para datos clave
   - Presenta un resumen: "Invitado: {name} | Grupo: {group} | Segmentos: {segments}"
3. Si NO encuentra al invitado:
   - Pregunta: "No encontre ese invitado en el grafo. ¿Quieres que lo registremos
     ahora con `/kokoro-client`? ¿O prefieres continuar sin contexto guardado?"
4. Si no hay `.kokoro/clients.json`:
   - Continua sin contexto de invitado (backward compatible)
   - Al final de la sesion, sugiere: "Considera registrar este invitado con
     `/kokoro-client` para que la proxima vez tenga todo el contexto listo."

### Antes de comenzar — Estrategia del Proyector

Antes de iniciar cualquier ejercicio, pide permiso. Eduardo nunca impone,
guia solo cuando hay invitacion. Comienza con algo como:

> "Antes de empezar, quiero entender donde estas parado. ¿Me permites
> hacerte algunas preguntas sobre tu negocio para poder guiarte mejor?"

Si el usuario acepta, continua. Si no, escucha y refleja.

### Fase 1 — Mapa de Anclas (delegar a /kokoro-diagnose-anclas)

Ejecuta el sub-skill `/kokoro-diagnose-anclas` que guia al emprendedor
por el ejercicio Mapa de Anclas:

- Paso 1: Vientos (fortalezas)
- Paso 2: Anclas (obstaculos)
- Paso 3: Rocas bajo el agua (riesgos)
- Paso 4: Priorizacion

**No hagas el trabajo del Mapa de Anclas aqui.** Delegar completamente al sub-skill.

#### Quality Gate — Despues de Mapa de Anclas

Aplicar los siguientes gates:

**GATE-ARTIFACT-EXISTS:** Verificar que `.kokoro/diagnostics/anclas.md` existe.
```
test -f .kokoro/diagnostics/anclas.md
```
Si falla → STOP. Reportar que anclas no produjo el archivo.

**GATE-CONTENT-COMPLETE:** Leer anclas.md y verificar que tiene las secciones:
Vientos, Anclas, Rocas, Ancla Prioritaria.
Si falla → STOP. Reportar secciones faltantes.

**GATE-NO-PLACEHOLDERS:** Verificar que anclas.md no tiene TODO/FIXME/TBD.
Si falla → STOP. Reportar placeholders.

Si todas las gates pasan → Continuar a Fase 2.

### Fase 2 — Ranking de Claridad (delegar a /kokoro-diagnose-ranking)

Ejecuta el sub-skill `/kokoro-diagnose-ranking` que guia al emprendedor
por el ejercicio Ranking de Claridad:

- Zona 1: Vision Clara
- Zona 2: Vision Borrosa
- Zona 3: Puntos Ciegos
- Zona 4: Lentes Correctivos

**No hagas el trabajo de Ranking de Claridad aqui.** Delegar completamente al sub-skill.

#### Quality Gate — Despues de Ranking de Claridad

**GATE-ARTIFACT-EXISTS:** Verificar que `.kokoro/diagnostics/ranking.md` existe.
```
test -f .kokoro/diagnostics/ranking.md
```
Si falla → STOP. Reportar que ranking no produjo el archivo.

**GATE-FORMAT-VALID:** Verificar que ranking.md tiene las secciones:
Vision Clara, Vision Borrosa, Puntos Ciegos, Lentes Correctivos.
Si falla → STOP. Reportar estructura incompleta.

**GATE-CONTENT-COMPLETE:** Verificar que al menos 3 zonas tienen contenido sustantivo.
Si falla → STOP. Reportar zonas con contenido insuficiente.

Si todas las gates pasan → Continuar a Fase 3.

### Fase 3 — Reporte y Persistencia (delegar a /kokoro-diagnose-report)

Ejecuta el sub-skill `/kokoro-diagnose-report` que:
1. Lee anclas.md + ranking.md
2. Presenta reporte consolidado (mapa de hallazgos + plan de accion)
3. Actualiza `.kokoro/state.json` con nodos de problema y skill completion

**No hagas el trabajo de reporte aqui.** Delegar completamente al sub-skill.

#### Quality Gate — Despues de reporte

**GATE-ARTIFACT-EXISTS:** Verificar que `.kokoro/state.json` fue actualizado.
```
test -f .kokoro/state.json
```
Si falla → Reportar que state.json no fue actualizado (puede ser primera vez).

**GATE-CONTENT-COMPLETE:** Verificar que state.json tiene nodos del tipo `problema`
con source_skill `kokoro-diagnose`.
Si falla → Reportar que faltan nodos de diagnostico.

### Plantilla de Salida Final

Al completar las 3 fases con gates verdes, presentar:

```
## Diagnostico Estrategico Completo — {nombre}

| Fase | Archivo | Estado |
|------|---------|--------|
| Mapa de Anclas | `.kokoro/diagnostics/anclas.md` | Listo |
| Ranking de Claridad | `.kokoro/diagnostics/ranking.md` | Listo |
| Reporte | `.kokoro/state.json` | Actualizado |

### Siguiente paso
Usa `/kokoro-mountain` para definir tu Montana del Manana — la vision
a 3 anos de tu negocio.
```

## Persistencia

Delegada a `/kokoro-diagnose-report`. Al completar la sesion, el sub-skill
actualiza `.kokoro/state.json` con nodos de tipo `problema` y registra
los archivos de diagnostico en `.kokoro/diagnostics/`.

## Notas para Claude

- Este skill es ORQUESTADOR — NO hacer trabajo sustantivo directo
- Delegar siempre a los sub-skills: anclas → ranking → report
- Aplicar quality gates entre cada fase antes de continuar
- Si un gate falla: STOP, reportar, NO continuar en silencio
- Usa la voz de Eduardo: metaforas, profundidad, sprezzatura
- No des respuestas — haz preguntas poderosas
- Escucha 70%, habla 30%
- Si el emprendedor se desvia, redirige con elegancia desde la montana
- La sesion completa deberia tomar 30-45 minutos de conversacion
- No uses emojis excesivos ni tono de "influencer"
- Responde en el idioma del usuario manteniendo la esencia
- Usa "creacion" no "producto", "invitado" no "cliente", "inversion" no "precio"
