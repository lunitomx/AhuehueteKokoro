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

### Paso 1B — Oportunidades a explorar

Si hay fricciones operativas con evidencia, propone como máximo tres
oportunidades para explorar. Cada una debe conservar su evidencia, riesgo y lo
que falta por aclarar:

| Campo | Regla |
|-------|-------|
| Oportunidad | Describe el cambio que valdría la pena investigar, no una promesa. |
| Impacto esperado | Alto, medio, bajo o `Pendiente`, explicado con la evidencia disponible. |
| Esfuerzo estimado | Alto, medio, bajo o `Pendiente`; no es una cotización. |
| Confianza | Alta, media o baja según la calidad de la evidencia. |
| Riesgos y dependencias | Límites, permisos, personas o sistemas que habría que revisar. |
| Por aclarar | Datos que impedirían decidir con honestidad. |
| Siguiente paso | Una conversación, validación o experimento; nunca una ejecución automática. |

Si faltan datos esenciales, conserva `Pendiente` y formula la pregunta que los
resolvería. No inventes cifras, no presentes una prioridad como autorización y
no traduzcas esta propuesta en ROI, presupuesto o una promesa de resultado.

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

### Oportunidades a explorar

| Oportunidad | Impacto esperado | Esfuerzo estimado | Confianza | Evidencia | Riesgos y dependencias | Por aclarar | Siguiente paso |
|-------------|------------------|-------------------|-----------|-----------|------------------------|-------------|----------------|
| {oportunidad} | {alto/medio/bajo/Pendiente} | {alto/medio/bajo/Pendiente} | {alta/media/baja} | {hecho o patrón} | {riesgos} | {preguntas} | {validación o experimento} |

Estas son propuestas para conversar, no instrucciones de ejecución. No
modifiques cuentas, campañas, CRM, calendarios ni otras herramientas desde el
diagnóstico.

### Plan de Accion (proximas 2 semanas)
1. {accion prioritaria — ancla mas pesada}
2. {accion de validacion — punto borroso mas critico}
3. {accion de exploracion — punto ciego mas relevante}

### Siguiente paso
Cuando completes estas acciones, usa `/kokoro-mountain` para definir
tu Montana del Manana — la vision a 3 anos de tu negocio.
```

Preguntar: "¿Resuena este diagnóstico y estas de acuerdo en guardarlo como
contexto para continuar después? ¿Falta algo?"

### Paso 3 — Persistencia

Sólo actualiza el contexto local si la persona da una confirmación afirmativa,
actual y específica. Si responde de forma ambigua o no confirma, entrega el
reporte como borrador y no escribas archivos de contexto.

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
- Presenta como máximo tres oportunidades y conserva visibles sus límites.
