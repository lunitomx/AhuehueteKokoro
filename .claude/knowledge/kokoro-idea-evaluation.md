# Evaluación de Ideas v1

> El puntaje ordena la mesa. La persona elige qué se sirve.

La regla canónica vive en `runtime/ideas.py` (`EVALUATION_DIMENSIONS`,
`INVERTED_DIMENSIONS`, `evaluation_score`, `validate_brief` y los reducers
`idea_evaluated`, `idea_selected`, `idea_briefed`, `idea_tested`). Si este
archivo y el código no coinciden, el código manda.

Cómo entra una idea al banco está en `kokoro-idea-bank.md`.

## Para qué sirve

Un banco lleno no sirve si todas las ideas pesan igual. La evaluación da seis
lecturas comparables, un puntaje para ordenar y un camino claro hasta la
prueba: seleccionar, preparar el brief, probar y aprender.

## Contrato

### Dimensiones (`EVALUATION_DIMENSIONS`), enteros de 1 a 5

| Dimensión | Pregunta | Se invierte |
|---|---|---|
| `strategic_fit` | ¿Empuja la Montaña del Mañana del invitado? | No |
| `evidence_strength` | ¿Qué tan sólida es la fuente? | No |
| `novelty` | ¿Abre algo que aún no se ha probado? | No |
| `production_cost` | ¿Cuánto cuesta producirla? | Sí |
| `speed_to_learn` | ¿Qué tan rápido da una lectura? | No |
| `risk` | ¿Qué puede salir mal con la marca o la persona? | Sí |

`score` = suma de las seis. Las invertidas cuentan como `6 − valor`. Rango
de 6 a 30. Ejemplo: `{5, 3, 4, 2, 4, 2}` → 5 + 3 + 4 + 4 + 4 + 4 = **24**.

### Eventos

| Evento | Payload | Desde → hacia |
|---|---|---|
| `idea_evaluated` | `idea_id`, `evaluation`, `rationale` | `raw` o `evaluated` → `evaluated` |
| `idea_selected` | `idea_id`, `selected_by: "human"`, `selector_ref` (slug), `reason` | `evaluated` → `selected` |
| `idea_briefed` | `idea_id`, `brief` | `selected` → `briefed` |
| `idea_tested` | `idea_id`, `test_ref`, `outcome`, `validation_id?`, `learning_record_id?` | `briefed` o `tested` → `tested` o `learned` |
| `idea_archived` | `idea_id`, `reason` | cualquier abierto → `archived` |

### Brief (`BRIEF_FIELDS`)

| Campo | Regla |
|---|---|
| `objective` | Qué buscamos |
| `audience` | A qué persona |
| `format` | Pieza, canal, duración |
| `learning_goal` | Qué queremos aprender |
| `measurement` | Cómo lo leemos |
| `next_step` | El siguiente paso concreto |
| `hypothesis_id` | Opcional; la `HYP-…` debe existir |

## Reglas

1. **El puntaje no decide.** Solo ordena `open_ideas` de mayor a menor. Una
   idea de 18 puede ser la correcta si la persona tiene una razón.
2. **Reevaluar está permitido.** Una idea `evaluated` puede recibir otra
   evaluación; el puntaje se recalcula. Una idea ya seleccionada no.
3. **Siempre con razón.** `rationale` es obligatorio. Seis números sin razón
   no se registran.
4. **Solo una persona selecciona.** `selected_by` debe ser `"human"` y
   `selector_ref` un slug. Kokoro propone; no elige.
5. **El brief conecta con la vara.** Si la prueba busca un veredicto, el brief
   lleva `hypothesis_id` y la vara vive en el contrato de hipótesis.
6. **`learned` exige respaldo.** `idea_tested` con `validation_id` o
   `learning_record_id` mueve la idea a `learned`. Sin respaldo, queda en
   `tested`.
7. **El respaldo guarda su estado.** `backed_by` copia el estado de la
   validación o del CLR. Un `inconclusive` también es aprendizaje.
8. **Observado ≠ inferido ≠ validado.** «Tuvo 40 leads» es `observed`.
   «La idea funciona» necesita una validación contra su vara.

## Ejemplo

Invitado `cliente_01`. Dos ideas abiertas, datos ficticios.

| Idea | Fit | Evidencia | Novedad | Costo | Velocidad | Riesgo | Score |
|---|---|---|---|---|---|---|---|
| `IDEA-031` tablero de portales | 5 | 3 | 4 | 2 | 4 | 2 | 24 |
| `IDEA-032` webinar de cierre fiscal | 4 | 2 | 3 | 4 | 2 | 2 | 19 |

1. `/kokoro-idea-evaluate` registra ambas con su razón. El banco las ordena
   31, 32.
2. `equipo_01` selecciona `IDEA-031`: «es la de menor inversión y aprende en
   dos semanas».
3. `/kokoro-idea-brief` registra el brief con `hypothesis_id: HYP-020`.
4. Tras la prueba, `idea_tested` con `validation_id: VAL-020` (`validated`)
   mueve la idea a `learned`.
5. `IDEA-032` se archiva: «el cierre fiscal ya pasó; volver en marzo».

## Anti-patrones

- **Ganar por puntaje.** «Tiene 24, se hace» quita la decisión a la persona.
- **Inflar `evidence_strength`.** Una frase de Kokoro (`kokoro_inference`)
  no es evidencia fuerte.
- **Brief sin medición.** Si no hay `measurement`, no hay prueba.
- **Cerrar como aprendida sin validación.** Queda `tested` y se dice así.

## Comandos y runtime

- `/kokoro-idea-evaluate` puntúa, explica y propone; registra con permiso.
- `/kokoro-idea-brief` prepara el brief después de la selección humana.
- `/kokoro-hypothesis` y `/kokoro-hypothesis-validate` dan la vara y el
  veredicto.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence check  --kind idea_evaluation --input-file scores.json   # devuelve score
K evidence check  --kind idea_brief      --input-file brief.json
K evidence append --type idea_evaluated --input-file eval.json --idempotency-key idea-031-eval
K evidence append --type idea_selected  --input-file sel.json  --idempotency-key idea-031-sel
K evidence append --type idea_briefed   --input-file br.json   --idempotency-key idea-031-brief
K evidence append --type idea_tested    --input-file test.json --idempotency-key idea-031-test
```

`sel.json`: `{"idea_id": "IDEA-031", "selected_by": "human",
"selector_ref": "equipo_01", "reason": "…"}`. Todo en `.kokoro/`; nada se
promueve solo.
