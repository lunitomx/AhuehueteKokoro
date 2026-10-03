# Iteración Creativa v1

> Cambiar a propósito, preservar lo que funciona, leer la señal con
> honestidad.

La regla canónica vive en `runtime/creative.py` (`ITERATION_FAMILIES`,
`signal_distance`, `validate_iteration`, `validate_learning_record`) y sus tres
eventos. Si este archivo y el código no coinciden, el código manda.

Cómo se elige qué pieza iterar está en `kokoro-creative-winner-selection.md`.

## Para qué sirve

Una creación que ya funciona no se reinventa desde una hoja en blanco. Se
itera: se declara qué se preserva, qué familia cambia y qué esperamos
aprender. Así un anuncio deja de ser solo un asset y se vuelve una unidad de
conocimiento.

## Contrato

### Las 16 familias (`ITERATION_FAMILIES`)

| Familia | Qué cambia |
|---|---|
| `hook` | Los primeros segundos o la primera línea |
| `headline` | El titular |
| `body_copy` | El texto de apoyo |
| `offer` | La propuesta y sus condiciones especiales |
| `cta` | La invitación a actuar |
| `proof` | La prueba: dato, caso, demostración |
| `angle` | El ángulo: desde qué tensión o deseo se habla |
| `persona` | A qué persona se le habla |
| `visual_subject` | Qué o quién aparece |
| `visual_style` | Cómo se ve: luz, color, tratamiento |
| `format` | Imagen, video, carrusel |
| `length` | Duración o extensión |
| `audio` | Voz, música, sonido |
| `placement` | Adaptación a una ubicación |
| `audience` | Segmentación |
| `landing` | La página a la que llega la persona |

Cada cambio declara su alcance (`CHANGE_SCOPES`): `element` (un elemento
puntual) o `concept` (la familia completa).

### Iteration Brief (`ITER-`)

| Campo | Regla |
|---|---|
| `id` | `ITER-…` |
| `guest` | Slug del invitado |
| `base_creative_ref` | La pieza base (referencia relativa) |
| `hypothesis_id` | Opcional; si existe, debe estar en el ledger |
| `changes` | Al menos uno: `{family, scope, description}` |
| `preserve` | Familias que no se tocan (Preservation Contract) |
| `core_idea_changed` | `true` o `false`, obligatorio |
| `learning_goal` | Qué queremos aprender |
| `success_metric` | Contra qué se mide |
| `privacy_class` | Solo `team` |
| `origin` | Opcional: comando, run y eventos de origen |

El ledger añade `signal_distance`, `signal_reading`, `controlled_test` y
`status`: `planned` → `approved` / `rejected` / `needs_changes` → `learned`.

### Signal Distance (`SIGNAL_LEVELS`)

| Nivel | Cuándo | Lectura |
|---|---|---|
| 1 | Una familia, un solo cambio de alcance `element` | Lectura limpia |
| 2 | Una familia (varios cambios o alcance `concept`) | Lectura controlada |
| 3 | Dos familias | Solo direccional |
| 4 | Tres o más familias, o `core_idea_changed: true` | Creación nueva, no iteración |

Solo los niveles 1 y 2 cuentan como prueba controlada (`controlled_test`).

### Creative Learning Record (`CLR-`)

| Campo | Regla |
|---|---|
| `id` | `CLR-…` |
| `guest`, `iteration_id` | Mismo invitado que la iteración |
| `epistemic_state` | `observed`, `inferred`, `validated`, `invalidated`, `inconclusive`, `insufficient` |
| `validation_id` | Obligatorio para los 4 estados de resolución |
| `lesson` | La lección en una oración |
| `evidence_refs` | Referencias de apoyo |
| `privacy_class` | Solo `team` |

## Reglas

1. **Preservation Contract.** Una familia en `preserve` no puede aparecer en
   `changes`. Si aparece, se rechaza: «preservation contract conflict».
2. **La distancia la calcula el runtime.** Nadie declara su nivel a mano.
3. **Revisión humana.** `creative_iteration_reviewed` solo acepta
   `reviewed_by: "human"` y un `reviewer_ref` en slug. Decide `approved`,
   `rejected` o `needs_changes`, desde `planned` o `needs_changes`.
4. **El aprendizaje espeja su validación.** Un CLR necesita una iteración
   `approved`. Si trae `validation_id`, su `epistemic_state` debe ser igual al
   estado actual de esa validación. Una validación `stale` no respalda un CLR
   nuevo: primero se revalida.
5. **Sin prueba controlada no hay veredicto.** Nivel 3 o 4 no puede registrar
   `validated` ni `invalidated`. Queda `observed` o `inferred`.
6. **Al registrar el CLR**, la iteración pasa a `learned`.
7. **Observado ≠ inferido ≠ validado.** «Subió el CTR» es `observed`. «Subió
   por el gancho» es `inferred` mientras no haya validación.
8. **Grounding antes de publicar.** Los textos de la iteración pasan por
   GATE-GROUNDED (`kokoro-grounding-standard.md`).

## Ejemplo

Invitado `cliente_01`. La pieza base `creativos/cliente_01/portales-v1` lidera
en citas. Datos ficticios.

```json
{"iteration": {
  "id": "ITER-003", "guest": "cliente_01",
  "base_creative_ref": "creativos/cliente_01/portales-v1",
  "hypothesis_id": "HYP-020",
  "changes": [{"family": "hook", "scope": "element",
               "description": "Abrir con la pantalla de 10 portales en vez del rostro"}],
  "preserve": ["offer", "proof", "cta", "persona", "format"],
  "core_idea_changed": false,
  "learning_goal": "Saber si el gancho visual sube la retención a 3 segundos",
  "success_metric": "Retención a 3 segundos contra la base de la cuenta",
  "privacy_class": "team"
}}
```

Nivel 1, prueba controlada. `equipo_01` la aprueba. Tras el sprint,
`VAL-020` resulta `validated`, y `CLR-003` registra `validated` con
`validation_id: VAL-020` y la lección.

Contraejemplo: `ITER-004` cambia `hook`, `persona`, `offer` y
`visual_subject`. Nivel 4: es una creación nueva. Su CLR solo puede decir
`observed` («consiguió 18 citas») o `inferred`.

## Anti-patrones

- **Cambiarlo todo y llamarlo prueba.** Cuatro familias no aíslan nada.
- **Preservar en el texto, cambiar en la pieza.** El contrato se declara en
  `preserve` y el runtime lo vigila.
- **Lección sin validación.** «El gancho funciona» sin `VAL-…` es una opinión.
- **Autoaprobación.** Un agente propone iteraciones; una persona las revisa.

## Comandos y runtime

- `/kokoro-iterate` lee la señal, redacta el brief, corre el check y pide
  revisión humana. Después registra el CLR.
- `/kokoro-creative` y `/kokoro-creative-review` producen y revisan la pieza.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence check  --kind iteration --input-file iter.json   # devuelve signal_distance y controlled_test
K evidence append --type creative_iteration_planned  --input-file ev.json  --idempotency-key iter-003
K evidence append --type creative_iteration_reviewed --input-file rev.json --idempotency-key iter-003-rev
K evidence check  --kind learning_record --input-file clr.json
K evidence append --type creative_learning_recorded  --input-file clr-ev.json --idempotency-key clr-003
cat .kokoro/shared/views/evidence/creative.yaml
```

`rev.json`: `{"iteration_id": "ITER-003", "reviewed_by": "human",
"reviewer_ref": "equipo_01", "decision": "approved", "notes": "…"}`.
`clr-ev.json` envuelve `{"learning_record": { … }}`.
