# Vigencia del Contexto v1

> Lo que sabemos del invitado tiene fecha. Nombrarla es honestidad, no
> burocracia.

La regla canónica vive en `runtime/freshness.py` (`ARTIFACT_FIELDS`,
`report`, `gate_context_fresh` y los eventos `context_refreshed` y
`context_marked_stale`) y en `evidence.validate_freshness`. Si este archivo y
el código no coinciden, el código manda.

El bloque Freshness v1 y sus clases están en `kokoro-evidence-model.md`. La
cascada entre artefactos está en `kokoro-dependency-staleness.md`. Las
validaciones viejas están en `kokoro-revalidation.md`.

## Para qué sirve

Un mapa de Customer Forces de agosto, un mensaje de septiembre y una landing
de octubre son contexto vivo. Si nadie dice cuándo se revisaron, Kokoro
recomienda sobre conocimiento viejo como si fuera de hoy. Este contrato
registra cada artefacto vivo con su fecha y su clase. También dice si sirve
para explorar o para decidir.

## Contrato

### Artefacto vivo (`context_refreshed` envuelve `artifact`)

| Campo | Regla | Ejemplo |
|---|---|---|
| `id` | Mayúsculas, guion y sufijo | `FORCES-2026-08` |
| `guest` | Slug del invitado | `cliente_01` |
| `kind` | Slug corto en minúsculas | `forces` |
| `title` | Nombre legible | `Customer Forces de despachos` |
| `source_ref` | Relativo al workspace; nunca absoluto | `.kokoro/shared/guests/cliente_01/forces.md` |
| `freshness` | Bloque Freshness v1 completo | ver abajo |
| `supersedes` | Opcional; id de otro artefacto que este reemplaza | `FORCES-2026-05` |

Payload del evento: `{artifact, material_change (true o false), summary}`.

### Bloque `freshness`

| Campo | Regla |
|---|---|
| `generated_on` | Fecha de la versión. No puede ir hacia atrás en un refresh. |
| `freshness_class` | `fast` (≤ 30 días), `medium` (≤ 90), `slow` (≤ 365) o `event_driven` |
| `refresh_by` | Obligatorio salvo en `event_driven` |
| `depends_on` | Ids de artefactos, hipótesis o validaciones |
| `invalidated_by` | Eventos que lo vencen. Obligatorio en `event_driven`. |
| `last_material_change` | Opcional. En un refresh material sin este campo se usa `generated_on`. |

### Estados del nodo (`NODE_STATUSES`) y recomendación del reporte

| Estado | Significa | Recomendación |
|---|---|---|
| `current` | Al día | (si `refresh_by` pasó: `refresh`) |
| `potentially_stale` | Algo de arriba está viejo | `check_upstream_first` |
| `stale_by_dependency` | Algo de arriba cambió después de su última revisión | `review_against_upstream` |
| `stale` | Una persona lo marcó viejo | `refresh` |
| `superseded` | Otro artefacto lo reemplazó | `repoint_dependents` |

### GATE-CONTEXT-FRESH

| Uso | `current` | `potentially_stale` | `stale`, `stale_by_dependency`, `superseded`, vencido o desconocido |
|---|---|---|---|
| `explore` | Pass | Partial | Partial |
| `decide` | Pass | Partial | **Blocked** |

Sin ids, el gate queda Skipped: no se usó contexto guardado.

## Reglas

1. **Registrar es refrescar.** La primera vez que llega un artefacto se
   registra con `context_refreshed`. No cuenta como cambio material.
2. **Material o no.** Un refresh con `material_change: true` avisa a todo lo
   que depende de él. Con `false`, solo confirma que sigue vigente y no avisa
   a nadie.
3. **Refrescar limpia lo propio.** Todo refresh deja el nodo en `current` y
   marca que se revisó hoy contra lo de arriba.
4. **Marcar viejo a mano.** `context_marked_stale` con `trigger: "manual"` o
   con uno de los eventos de `invalidated_by`. Otro texto se rechaza. Solo se
   marca un artefacto `current`.
5. **Rechazos del runtime.** Mover el artefacto a otro invitado, refrescar uno
   `superseded`, regresar `generated_on`, usar el id de una validación («use
   /kokoro-revalidate») o cerrar un ciclo de dependencias.
6. **El calendario no muta nada.** El reporte lee `today` y dice `fresh`,
   `expired` o `event_driven`, con `days_to_refresh`. El estado no cambia
   solo.
7. **Explorar sí, decidir no.** Con contexto viejo se puede conversar si se
   dice. Para recomendar una inversión, el gate en `decide` no debe quedar
   Blocked.
8. **Dependencias sin registro.** Un id en `depends_on` que no está en el
   grafo aparece como `untracked`. Para decidir con él, primero se registra.

## Ejemplo

Invitado `cliente_01`. Hoy es 3 de octubre. Datos ficticios.

| Artefacto | Clase | `generated_on` | `refresh_by` | Estado | Calendario |
|---|---|---|---|---|---|
| `FINANCE-2026-06` | `medium` | 2026-06-20 | 2026-09-18 | `current` | `expired` |
| `FORCES-2026-08` | `medium` | 2026-08-10 | 2026-11-08 | `current` | `fresh`, 36 días |

`/kokoro-refresh` lista `FINANCE-2026-06` con `refresh`. La persona quiere
comparar dos ofertas: el gate en `decide` con `FINANCE-2026-06` queda
Blocked («FINANCE-2026-06: expired»). Kokoro lo dice y propone revisar las
finanzas antes de hablar de inversión.

La persona revisa: los números no cambiaron. Se registra un refresh con
`material_change: false` y `generated_on: 2026-10-03`. El gate pasa.

## Anti-patrones

- **Renovar la fecha sin mirar.** Un refresh es una revisión real, no un
  cambio de fecha.
- **Todo `slow`.** El runtime rechaza un `refresh_by` mayor que el límite de
  la clase.
- **Marcar `material_change: false` para no avisar.** Si cambió el contenido,
  es material.
- **Callar lo viejo en modo explorar.** Partial obliga a decirlo.

## Comandos y runtime

- `/kokoro-refresh` corre el reporte, explica cada recomendación y registra
  refrescos con permiso. Nunca refresca solo.
- La receta `freshness-review` (semanal sugerida) solo lee.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence check  --kind artifact --input-file artifact.json
K evidence append --type context_refreshed    --input-file ev.json    --idempotency-key forces-2026-08-r2
K evidence append --type context_marked_stale --input-file stale.json --idempotency-key forces-2026-08-stale
K freshness report --guest cliente_01 --today 2026-10-03          # mutates: false
K freshness gate --ids FINANCE-2026-06,FORCES-2026-08 --use decide --today 2026-10-03
cat .kokoro/shared/views/evidence/freshness.yaml
```

Todo vive en `.kokoro/` del workspace. No hay cron, hooks ni refresco
automático.
