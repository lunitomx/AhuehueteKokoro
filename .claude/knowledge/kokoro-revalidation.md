# Revalidación v1

> Lo validado también envejece. Revalidar no es repetir el sello: es volver a
> medir contra la misma vara.

La regla canónica vive en `runtime/evidence_ledger.py`
(`validation_recorded`, `validation_expired`, `_check_revalidation`) y en
`runtime/freshness.py` (estados y recomendaciones). Si este archivo y el código
no coinciden, el código manda.

Freshness v1 y los 9 estados están en `kokoro-evidence-model.md`. La parte de
dependencias está en `kokoro-dependency-staleness.md`.

## Para qué sirve

Un resultado de campaña de octubre no describe enero. Sin revalidación, un
`validated` viejo se cita en un plan nuevo «porque ya se probó». Este contrato
dice cuándo un resultado deja de contar y cómo se renueva sin hacer trampa.

## Contrato

Toda validación lleva un bloque `freshness` obligatorio:

| Campo | Regla | Ejemplo |
|---|---|---|
| `generated_on` | Día en que se resolvió. | `2026-10-16` |
| `freshness_class` | `fast`, `medium`, `slow` o `event_driven`. | `fast` |
| `refresh_by` | Máximo 30 / 90 / 365 días después. No aplica a `event_driven`. | `2026-11-14` |
| `depends_on` | Ids de los que depende: artefactos, hipótesis, validaciones. | `["FORCES-2026-10"]` |
| `invalidated_by` | Eventos que la vencen antes. Obligatorio en `event_driven`. | `["cambio de oferta"]` |

Eventos:

| Evento | Payload | Efecto |
|---|---|---|
| `validation_expired` | `validation_id`, `reason` | `current_state` pasa a `stale`. Sus dependientes quedan `stale_by_dependency`. |
| `validation_recorded` con `revalidates` | Validación completa + `revalidates: VAL-…` | Nueva validación. La vieja sigue `stale` como historia. |

## Reglas

1. **Tres formas de quedar viejo.** Por calendario (`refresh_by` pasó), por
   dependencia (un upstream cambió materialmente) o a mano
   (`validation_expired`). Ver la tabla de recomendaciones.
2. **El calendario no cambia el estado solo.** El reporte marca `expired` y
   recomienda `expire_then_revalidate`. El paso a `stale` es un evento
   `validation_expired` con razón. Kokoro no expira nada por su cuenta.
3. **Cualquier resolución puede expirar.** `validated`, `invalidated`,
   `inconclusive` e `insufficient` pasan a `stale`. Un `stale` no vuelve a
   `validated` directo.
4. **Revalidar es una validación nueva.** Lleva id nuevo y
   `revalidates: VAL-…`. La hipótesis debe estar `resolved` y la anterior
   debe ser `stale` y de esa misma hipótesis.
5. **Misma vara.** La revalidación repite el `bar_sha256` de la hipótesis. Si
   la vara ya no sirve, se abre una hipótesis nueva desde un loop nuevo; una
   hipótesis resuelta no acepta `supersedes`.
6. **El resultado puede cambiar.** Lo que fue `validated` puede salir
   `invalidated` al revalidar. Eso es aprendizaje, no fracaso.
7. **Reapuntar dependientes.** Lo que dependía de `VAL-010` sigue apuntando ahí.
   Se registra de nuevo con `depends_on: ["VAL-011"]` cuando una persona lo
   revise.
8. **Decidir con algo viejo está bloqueado.** GATE-CONTEXT-FRESH en modo
   `decide` bloquea una validación `stale`, `stale_by_dependency` o vencida.
   En modo `explore` queda Partial: se puede conversar, diciendo que es viejo.

| Situación de la validación | Estado en el grafo | Recomendación del reporte |
|---|---|---|
| `refresh_by` pasó, sin evento | `current` + `calendar: expired` | `expire_then_revalidate` |
| Un upstream cambió materialmente | `stale_by_dependency` | `expire_then_revalidate` |
| Un upstream está viejo, sin cambio propio | `potentially_stale` | `check_upstream_first` |
| Ya se registró `validation_expired` | `stale` | `revalidate` |

## Ejemplo

Invitado `cliente_01`. `VAL-010` validó `HYP-010` el 5 de octubre: el mensaje
de portales consiguió 1.4x citas. Clase `fast`, `refresh_by: 2026-11-04`,
`depends_on: ["FORCES-2026-10"]`.

1. El 10 de noviembre, `/kokoro-refresh` lista `VAL-010` con
   `calendar: expired` y `expire_then_revalidate`.
2. La persona confirma. Se registra `validation_expired` con la razón
   «pasaron 30 días; la campaña cambió de temporada».
3. `/kokoro-revalidate` arma el plan: misma vara, nueva ventana de 14 días.
4. Resultado: 1.35x con 31 y 23 citas. Se registra `VAL-011` con
   `revalidates: VAL-010`, `state: validated` y freshness nueva.
5. El mensaje que dependía de `VAL-010` se registra otra vez apuntando a
   `VAL-011`.

## Anti-patrones

- **Renovar la fecha.** Cambiar `refresh_by` sin medir otra vez no es revalidar.
- **Revalidar con otra vara.** Si la vara cambió, es otra hipótesis.
- **Borrar el viejo.** El ledger es append-only; `VAL-010` queda como historia.
- **Citar un `stale`.** «Se validó en octubre» no sostiene una decisión hoy.
- **Clase equivocada.** Un resultado de campaña como `slow` para no revisarlo
  en un año. El runtime rechaza un `refresh_by` mayor al límite de la clase.

## Comandos y runtime

- `/kokoro-refresh` muestra qué venció; nunca expira ni revalida solo.
- `/kokoro-revalidate` propone la expiración, arma el plan y registra la
  validación nueva con aprobación humana.
- La receta `revalidation-queue` (mensual sugerida) solo lee: lista y propone.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K freshness report --guest cliente_01 --today 2026-11-10                 # solo lectura
K evidence append --type validation_expired  --input-file exp.json --idempotency-key val-010-exp
K evidence check  --kind validation --input-file val-011.json            # sin escribir
K evidence append --type validation_recorded --input-file ev.json  --idempotency-key val-011
K freshness gate --ids VAL-011 --use decide --today 2026-11-12
```

`exp.json`: `{"validation_id": "VAL-010", "reason": "…"}`. `ev.json` envuelve:
`{"validation": { …, "revalidates": "VAL-010" }}`. Todo en `.kokoro/` del
workspace. No hay cron, hooks ni revalidación automática.
