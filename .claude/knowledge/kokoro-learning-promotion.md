# Promoción de Aprendizaje y Rutinas v1

> Lo que se aprende sube despacio, con nombre y con razón. Lo que se repite
> se escribe como receta, no como reloj.

La regla canónica vive en `runtime/learning.py` (`_check_basis` y los eventos
`learning_trace_promoted`, `learning_trace_rejected`,
`learning_trace_applied`) y en `runtime/routines.py` (`validate_recipe`,
`BUILTIN_RECIPES`). Si este archivo y el código no coinciden, el código
manda.

La captura de traces está en `kokoro-learning-traces.md`.

## Para qué sirve

Una trace capturada es local. Para que cambie cómo trabaja un equipo o un
comando, una persona la promueve con una base declarada. Después, un cambio
revisado la aplica. Kokoro nunca se reescribe a sí mismo. Las rutinas siguen
la misma lógica: son recetas que una persona corre cuando elige, no tareas
programadas.

## Contrato

### Promoción (`learning_trace_promoted`)

| Campo | Regla |
|---|---|
| `trace_id` | Trace en estado `captured` |
| `promoted_by` | Siempre `"human"` |
| `approver_ref` | Slug de quien aprueba |
| `to_scope` | Igual o más amplio que el alcance actual; nunca más estrecho |
| `basis` | `explicit_rule`, `repetition`, `performance` o `confirmed` |
| `basis_refs` | Referencias que sostienen la base |
| `reason` | Por qué se promueve |

| Base | Qué exige el runtime |
|---|---|
| `explicit_rule` | La trace trae `explicit_rule` |
| `repetition` | Al menos 2 traces más en `basis_refs` (3 en total). Ninguna puede ser la misma, `rejected` ni `superseded` |
| `performance` | Exactamente una validación en `basis_refs`, con estado actual `validated` |
| `confirmed` | La confirmación de la persona; sin chequeo extra |

Además: un `to_scope` de `team`, `skill` o `system` exige `explicit_rule` en
la trace. `skill` y `system` exigen `feedback_source: user` y `skill_ref`.

### Otros eventos

| Evento | Payload | Desde |
|---|---|---|
| `learning_trace_rejected` | `trace_id`, `reason` | `captured` o `promoted` |
| `learning_trace_applied` | `trace_id`, `change_ref` (commit, PR o ruta relativa), `reviewed_by: "human"` | `promoted` |

### Receta de rutina (`RECIPE_FIELDS`)

| Campo | Regla |
|---|---|
| `name` | Slug kebab-case |
| `purpose` | Para qué |
| `cadence_suggestion` | `daily`, `weekly`, `biweekly`, `monthly`, `on_demand`, `event_driven`. Solo sugerencia |
| `reads`, `writes` | Rutas `.kokoro/shared/…` o `.kokoro/local/…` (privada, fuera de git) |
| `requires_action_permission` | `true` obligatorio si `writes` no está vacío |
| `required_connectors` | `meta_ads`, `google_ads`, `ga4`, `search_console`, `crm` |
| `privacy_scope` | `team` o `personal`. Una receta `team` no escribe en `.kokoro/local/` |
| `command` | Un comando `/kokoro-…` |

## Reglas

1. **Nada se valida por conveniencia.** La base `performance` exige una
   validación `validated` vigente. Un buen mes sin hipótesis no cuenta.
2. **Tres no es coincidencia.** `repetition` pide tres traces. El runtime
   cuenta; la persona juzga si de verdad dicen lo mismo.
3. **Promover no edita.** `learning_trace_applied` registra un cambio que ya
   pasó revisión humana (un PR, un commit). El runtime nunca toca comandos,
   skills, knowledge ni `CLAUDE.md`.
4. **Rechazar también enseña.** Una trace `rejected` queda con su razón.
5. **Una rutina no escribe reglas.** Una receta que escribe en `skills`,
   `commands`, `agents`, `knowledge`, `.claude/` o `CLAUDE.md` se rechaza.
6. **Una rutina no se programa.** Kokoro no instala cron, hooks ni agentes en
   segundo plano. `routine list` responde `scheduled: false`.
7. **Escribir pide permiso.** Toda receta que escribe pide
   `requires_action_permission: true`. Al correrla se pregunta antes.

### Recetas incluidas

| Receta | Comando | Cadencia sugerida | Escribe |
|---|---|---|---|
| `freshness-review` | `/kokoro-refresh` | weekly | No |
| `loop-rollup` | `/kokoro-loop-rollup` | weekly | Sí, con permiso |
| `revalidation-queue` | `/kokoro-revalidate` | monthly | No |
| `idea-harvest` | `/kokoro-idea-harvest` | weekly | Sí, con permiso |
| `creative-signal-read` | `/kokoro-iterate` | weekly (`meta_ads`) | No |
| `learning-review` | `/kokoro-learn` | biweekly | Sí, con permiso |
| `weekly-scorecard` | `/kokoro-rhythm` | weekly | No |

## Ejemplo

Equipo que trabaja con `cliente_01`, `cliente_02` y `cliente_03`. Datos
ficticios.

1. Tres traces de alcance `output`, una por invitado. En las tres la persona
   corrige lo mismo: «no abras con una estadística; abre con la escena».
2. La tercera, `TRACE-021`, trae `explicit_rule: "En /kokoro-launch, abrir
   con una escena antes de un dato"`, `feedback_source: user` y `skill_ref:
   /kokoro-launch`.
3. `equipo_01` promueve `TRACE-021` a `skill` con `basis: repetition` y
   `basis_refs: ["TRACE-017", "TRACE-019"]`.
4. Alguien abre un PR que ajusta `/kokoro-launch`. Otra persona lo revisa y
   lo fusiona.
5. Se registra `learning_trace_applied` con `change_ref: "PR #52"` y
   `reviewed_by: "human"`.

Intento rechazado: promover `TRACE-012` (alcance `guest`) a `output`.
«promotion cannot narrow a trace's scope».

## Anti-patrones

- **Autopromoción.** Kokoro propone; una persona promueve.
- **Aplicar sin revisión.** Un cambio a un comando sin PR revisado no se
  registra como aplicado.
- **Rutina como cron.** «Corre cada lunes a las 8» no existe; la cadencia es
  una sugerencia.
- **Receta que escribe en silencio.** Sin `requires_action_permission: true`,
  el runtime la rechaza.

## Comandos y runtime

- `/kokoro-learn` muestra las traces pendientes y registra la decisión de la
  persona.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence append --type learning_trace_promoted --input-file promo.json --idempotency-key trace-021-promo
K evidence append --type learning_trace_rejected --input-file rej.json   --idempotency-key trace-018-rej
K evidence append --type learning_trace_applied  --input-file app.json   --idempotency-key trace-021-app
K routine list                                   # scheduled: false
K routine show --name learning-review
K routine check --input-file receta.json         # valida una receta propia
```

Todo vive en `.kokoro/` del workspace. No hay cron, hooks ni promoción
automática.
