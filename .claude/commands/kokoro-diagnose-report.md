# /kokoro-diagnose-report — Reporte, Puntaje, y Accion

> Sub-skill de /kokoro-diagnose — NO invocar directamente
> Input: `.kokoro/diagnostics/anclas.md`, `.kokoro/diagnostics/ranking.md`
> Produce: Diagnostico final + actualizacion de `.kokoro/state.json`

## Contexto

Consolida los hallazgos del Mapa de Anclas y Ranking de Claridad en un reporte
estructurado con puntaje, resumen, plan de accion, y persistencia
en state.json.

## Instrucciones

### Paso 1 — Consolidar Hallazgos

Leer ambos archivos de diagnostico: anclas.md y ranking.md.
Integrar los hallazgos en un mapa unificado de dimensiones.

### Paso 2 — Presentar Reporte

Presentar al emprendedor el reporte completo:

```
## Diagnostico de {nombre del negocio}

### Mapa de Anclas
**Vientos (fortalezas):**
- {lista de vientos identificados}

**Anclas (obstaculos):**
- {lista de anclas priorizadas — la mas pesada primero}

**Rocas (riesgos):**
- {lista de riesgos identificados}

### Ranking de Claridad
**Vision clara:**
- {lo que sabe con certeza}

**Vision borrosa:**
- {lo que necesita validar}

**Puntos ciegos:**
- {lo que no veia}

### Mapa de Hallazgos

| Dimension | Hallazgo | Prioridad | Accion |
|-----------|----------|-----------|--------|
| Viento | {fortaleza clave} | Alta | Potenciar |
| Ancla | {obstaculo critico} | Alta | Cortar |
| Roca | {riesgo principal} | Media | Mitigar |
| Punto ciego | {area invisible} | Alta | Explorar |

### Plan de Accion (proximas 2 semanas)
1. {accion prioritaria — ancla mas pesada}
2. {accion de validacion — punto borroso mas critico}
3. {accion de exploracion — punto ciego mas relevante}

### Siguiente paso
Cuando completes estas acciones, usa `/kokoro-mountain` para definir
tu Montana del Manana — la vision a 3 anos de tu negocio.
```

Preguntar: "¿Resuena este diagnostico? ¿Falta algo?"

### Paso 3 — Persistencia

Actualizar `.kokoro/state.json` con los hallazgos. Si no existe,
crear la estructura primero (`kokoro init` o manualmente).

Registrar cada hallazgo como nodo estructurado:

- **Tipo `problema`**: Cada ancla, roca o punto ciego identificado
  - id: `PRO-001`, `PRO-002`, etc.
  - source_skill: `kokoro-diagnose`
  - content: descripcion del hallazgo
  - metadata: `{"categoria": "ancla|roca|punto_ciego", "prioridad": "alta|media|baja"}`

Marca el skill como completado en la fase 1 con un resumen de una linea.

Ejemplo:
```json
{
  "id": "PRO-001",
  "type": "problema",
  "content": "No tiene claridad sobre sus costos reales",
  "source_skill": "kokoro-diagnose",
  "created": "2026-03-24T00:00:00Z",
  "metadata": {"categoria": "punto_ciego", "prioridad": "alta"}
}
```

Confirmar: "Diagnostico guardado en state.json."

## Notas para Claude

- Integra TODOS los hallazgos de ambos ejercicios — no omitas ninguno
- El mapa de hallazgos debe tener al menos 4 filas (viento, ancla, roca, punto ciego)
- El plan de accion debe ser accionable esta semana, no teorico
- state.json debe tener nodes y skill completions correctamente estructurados
