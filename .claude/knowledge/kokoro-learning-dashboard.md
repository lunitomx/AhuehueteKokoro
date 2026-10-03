# Learning Dashboard — Guía para Invitados

> Tu historial de aprendizaje en Kokoro: qué sabemos, qué falta saber y qué
> decisión sigue.

## 1) Qué es

El Learning Dashboard es la vista de lo que Kokoro sabe de un invitado y por
qué lo sabe. Tiene dos fuentes:

- **Memoria viva (E60)** — el ledger de evidencia del proyecto
  (`.kokoro/shared/events/evidence/`) y sus vistas en
  `.kokoro/shared/views/evidence/`. Guarda preguntas abiertas, hipótesis,
  validaciones, vigencia del contexto, ideas, learning traces e iteraciones
  creativas.
- **session_log** — el registro de sesiones por invitado dentro de
  `metadata.session_log`. Es el histórico que Kokoro ya usaba (sección 13).

No es una base de datos nueva ni una app separada. Las vistas se reconstruyen
del ledger con `evidence rebuild`; borrarlas no pierde nada.

**No abandonar `session_log` hasta completar la migración.** Mientras un
invitado no tenga ledger, el dashboard se arma solo con `session_log`, y cada
sección de memoria viva dice "sin datos todavía".

Cuando vuelves a abrir un invitado, Kokoro recuerda lo que se hizo, lo
aprendido, lo que sigue abierto y el siguiente paso.

## 2) Cómo se arma

Todo es lectura. Ningún comando de esta lista escribe en el ledger:

```bash
python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" evidence summary --target <proyecto>
python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" freshness report --target <proyecto>
python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" client show --id <id-del-invitado>
```

| # | Sección | Fuente |
|---|---------|--------|
| 3 | Estado actual | `evidence summary` + último `session_log` |
| 4 | Preguntas abiertas | vista `open-loops` |
| 5 | Hipótesis activas | vista `hypotheses` |
| 6 | Experimentos | `state.json` (nodos `EXP-…`) + vista `validations` |
| 7 | Validaciones recientes | vista `validations` |
| 8 | Conocimiento por vencer | `freshness report` + vista `freshness` |
| 9 | Banco de ideas | vista `idea-bank` |
| 10 | Iteraciones creativas | vista `creative` |
| 11 | Learning traces pendientes | vista `learning` |
| 12 | Siguiente decisión | `next_action` del último `session_log` + secciones 4–11 |

## 3) Estado actual

Una foto en cinco líneas: fase del invitado, último trabajo, número de loops
abiertos, validaciones vencidas y artefactos que piden atención. Sale de
`evidence summary`.

Ejemplo: "Fase 3. Última sesión: reporte de experimento. 4 loops abiertos,
1 revalidación vencida, 2 artefactos por revisar."

## 4) Preguntas abiertas

Los open loops activos, ordenados por prioridad. Cada uno con su origen
(sesión, scorecard, experimento) y su estado. Se capturan con
`/kokoro-loop-capture` y se ordenan con `/kokoro-loop-rollup`.

## 5) Hipótesis activas

Hipótesis creadas o aprobadas que todavía no tienen validación. Cada una con
su predicción y su barra precomprometida. Se crean con `/kokoro-hypothesis`.

## 6) Experimentos

Sprints 3x3x3 diseñados, en curso o completados, con la hipótesis que prueban
(`source_hypothesis_id`). Vienen de `/kokoro-experiment`.

## 7) Validaciones recientes

Validaciones de los últimos 90 días con su estado: `validated`,
`invalidated`, `inconclusive` o `insufficient`. `evidence summary` da la
proporción invalidada e inconclusa. Una proporción invalidada alta no es mala
noticia: dice que el invitado está aprendiendo rápido.

## 8) Conocimiento por vencer

Artefactos y validaciones que no están `current`: vencidos por calendario
(`refresh_by`), potencialmente vencidos, vencidos por dependencia o
reemplazados. Cada uno con la recomendación del reporte (`refresh`,
`review_against_upstream`, `revalidate`, etc.). Siguiente paso:
`/kokoro-refresh` o `/kokoro-revalidate`. Kokoro recomienda; la persona
decide.

## 9) Banco de ideas

Conteo de ideas por estado (`raw`, `evaluated`, `selected`, `briefed`,
`tested`, `learned`, `archived`) y las que esperan una decisión humana para
pasar a `selected`. Ver `/kokoro-idea-harvest`, `/kokoro-idea-evaluate` y
`/kokoro-idea-brief`.

## 10) Iteraciones creativas

Iteraciones planeadas y revisadas, con la proporción que cambió una sola
variable. Los Creative Learning Records muestran qué aprendió cada prueba.
Una pieza que destaca aparece como "candidato a iterar" solo si pasó el
`GATE-PERFORMANCE-SIGNAL` contra la línea base de la cuenta. Ver
`/kokoro-iterate`.

## 11) Learning traces pendientes

Correcciones y aprendizajes capturados que esperan revisión humana. Cada uno
con su alcance (`output`, `guest`, `team`, `skill`, `system`). Promover,
rechazar o aplicar es siempre decisión de una persona (`/kokoro-learn`,
`kokoro-learning-promotion.md`).

## 12) Siguiente decisión

Una sola decisión, en palabras reales, con lo que depende de ella. Se elige
entre el `next_action` del último `session_log` y lo que piden las secciones
4–11. Si dos compiten, gana la que tiene contexto vencido o una revalidación
pendiente: decidir sobre contexto vencido sale caro.

## 13) session_log — cómo leerlo

Cada entrada de `metadata.session_log` incluye, como mínimo:

- `date`: fecha de la sesión.
- `type`: tipo de trabajo (`gads`, `creative`, `ads`, etc.).
- `summary`: lo hecho (1-2 líneas).
- `hallazgos`: aprendizajes concretos sobre la audiencia, el mercado o el resultado.
- `next_action`: el siguiente paso sugerido.

Cuando aplica Google Ads, también puede incluir:

- `platform`: `google_ads`
- `campaign_type`: `search`, `display`, `pmax`, `shopping`, `other`
- `learning_state`: `learning`, `stable`, `needs_attention`
- `task_group`: `insight`, `optimization`, `launch`
- `task`: tarea concreta de ese bloque
- `cadence`: `72h`, `weekly`, `monthly`, `90d`
- `landing_page`, `asset_group`, `change_made`, `reason`

Regla práctica:
- Si viene `learning_state`, úsalo para decidir si seguimos probando (`learning`) o si estabilizamos (`stable`) o si hay correcciones urgentes (`needs_attention`).

Un `hallazgo` del `session_log` no es una validación. Si vale la pena
conservarlo, se propone como learning trace con `/kokoro-learn` o como open
loop con `/kokoro-loop-capture`.

## 14) Flujo de control en 3 capas

### Capa de plan

- Qué se va a trabajar (contexto y objetivo de la sesión).

### Capa de ejecución

- Qué se produjo y se registró (`artifacts`, entregables, cambios recomendados o ejecutados).

### Capa de aprendizaje

- Qué se aprendió y cuál es el siguiente paso natural (`hallazgos` + `next_action`).
- Qué queda en la memoria viva: loops, validaciones, learning traces.

## 15) Diferencias clave entre documentos

- **session_log**: resumen histórico de sesiones por invitado.
- **ledger de evidencia**: registro append-only de preguntas, hipótesis, validaciones, vigencia, ideas y aprendizajes. Es la fuente de las secciones 4–11.
- **validation plan**: cómo se piensa y valida una hipótesis.
- **experiment report**: resultados concretos de pruebas y decisiones.

Usa los cuatro como una secuencia: plan -> ejecutar -> validar -> aprender -> repetir.

## 16) Atribución de método

Esta metodología de aprendizaje y mejora iterativa toma base de **LeanStack** y de los principios de estructuración de hipótesis de **Ash Maurya** (`Lean Stack` / `Problem-Solution-Fit`).
