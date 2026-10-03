# Vigencia por Dependencia v1

> Cuando cambia la raíz, las ramas no se secan solas. Pero hay que mirarlas.

La regla canónica vive en `runtime/freshness.py` (`statuses`,
`check_dependencies`, `RECOMMENDATIONS`). Si este archivo y el código no
coinciden, el código manda.

El registro de artefactos está en `kokoro-context-freshness.md`. Las
validaciones que dependen de algo están en `kokoro-revalidation.md`.

## Para qué sirve

Si cambian las Customer Forces, el mensaje construido sobre ellas puede
quedar mal apuntado, y la landing construida sobre el mensaje también. El
grafo de dependencias dice qué revisar después de un cambio, en qué orden y
con qué urgencia. No cambia nada solo.

## Contrato

Las aristas salen de `freshness.depends_on` de cada nodo. Los nodos son
artefactos vivos y validaciones registradas.

| Concepto | Regla del runtime |
|---|---|
| `changed_sequence` | Momento del último cambio material. Lo mueven un refresh material, `context_marked_stale`, un `supersedes` (en el viejo) y `validation_expired`. |
| `verified_sequence` | Momento de la última revisión del nodo. Lo pone cada refresh. |
| `stale_by_dependency` | Un upstream directo cambió después de la última revisión del nodo. |
| `potentially_stale` | Un upstream directo no está `current`, pero no cambió después de la revisión. |
| `untracked` | Un id de `depends_on` que no existe en el grafo. |
| Ciclo | Rechazado: «freshness dependencies form a cycle through X». |

Recomendaciones por tipo de nodo:

| Estado | Artefacto | Validación |
|---|---|---|
| `stale` | `refresh` | `revalidate` |
| `stale_by_dependency` | `review_against_upstream` | `expire_then_revalidate` |
| `potentially_stale` | `check_upstream_first` | `check_upstream_first` |
| `superseded` | `repoint_dependents` | (no aplica) |
| vencido por calendario | `refresh` | `expire_then_revalidate` |

El reporte ordena: `stale`, `stale_by_dependency`, `superseded`,
`potentially_stale`.

## Reglas

1. **Solo un salto marca `stale_by_dependency`.** El hijo directo de lo que
   cambió queda `stale_by_dependency`. El nieto queda `potentially_stale`:
   tal vez no le afecta.
2. **Se revisa de arriba hacia abajo.** Primero el upstream, después lo que
   depende de él. Por eso el nieto dice `check_upstream_first`.
3. **Revisar no es cambiar.** Si el mensaje se revisa y sigue bien, un
   refresh con `material_change: false` lo deja `current` sin avisar a la
   landing.
4. **Cambiar sí avisa.** Si el mensaje cambia, un refresh material deja a la
   landing en `stale_by_dependency`.
5. **Reemplazar avisa.** Un artefacto nuevo con `supersedes` deja al viejo
   `superseded` y a sus dependientes `stale_by_dependency`. Hay que
   reapuntarlos al id nuevo.
6. **Sin ciclos.** Un artefacto no puede depender de algo que depende de él.
7. **Nadie refresca en cascada.** Kokoro muestra la lista; la persona decide
   cada revisión.

## Ejemplo

Invitado `cliente_01`. Tres artefactos `medium`, `generated_on: 2026-08-10`,
`refresh_by: 2026-11-08`. Datos ficticios.

```
FORCES-2026-08  →  MESSAGE-2026-08  →  LANDING-2026-08
(Customer Forces)  (mensaje central)   (landing de citas)
```

1. **Registro.** Los tres entran con `context_refreshed`. Los tres quedan
   `current`.
2. **Revisión sin cambio.** FORCES se refresca con `material_change: false`.
   Nada cascada; los tres siguen `current`.
3. **Cambio real.** Las entrevistas de septiembre muestran una ansiedad nueva:
   miedo a multas del SAT. FORCES se refresca con `material_change: true`.

| Nodo | Estado | Razón | Recomendación |
|---|---|---|---|
| `FORCES-2026-08` | `current` | | |
| `MESSAGE-2026-08` | `stale_by_dependency` | FORCES-2026-08 changed after MESSAGE-2026-08 was last verified | `review_against_upstream` |
| `LANDING-2026-08` | `potentially_stale` | MESSAGE-2026-08 is stale_by_dependency | `check_upstream_first` |

4. **Gate del 3 de octubre.** LANDING: Partial en `explore` y en `decide`.
   MESSAGE: Partial en `explore`, Blocked en `decide`.
5. **Revisar el mensaje.** Se reescribe y se refresca con cambio material.
   MESSAGE queda `current`. Ahora LANDING queda `stale_by_dependency`.
6. **Revisar la landing.** Se ajusta y se refresca. Todo `current`.

Variante con reemplazo: en lugar de refrescar, se registra `FORCES-2026-10`
con `supersedes: FORCES-2026-08`. El viejo queda `superseded`
(`repoint_dependents`) y MESSAGE queda `stale_by_dependency`. MESSAGE se
registra de nuevo con `depends_on: ["FORCES-2026-10"]`.

Marcar a mano: si FORCES declara `invalidated_by: ["cambio de ley fiscal"]`,
el trigger «cambio de oferta» se rechaza. «manual» o «cambio de ley fiscal»
funcionan, y FORCES queda `stale` (`refresh`).

## Anti-patrones

- **Saltar al nieto.** Ajustar la landing antes de revisar el mensaje.
- **Refrescar todo en bloque.** Cada refresh afirma que alguien lo revisó.
- **Dejar el id viejo en `depends_on`.** Tras un reemplazo, el dependiente
  sigue señalando un nodo `superseded`.
- **Dependencias de adorno.** Un `depends_on` sin relación real llena el
  reporte de ruido.

## Comandos y runtime

- `/kokoro-refresh` muestra la cascada y propone el orden de revisión.
- `/kokoro-revalidate` atiende las validaciones del grafo.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K freshness report --guest cliente_01 --today 2026-10-03
K freshness gate --ids MESSAGE-2026-08,LANDING-2026-08 --use decide --today 2026-10-03
K evidence append --type context_refreshed --input-file forces.json --idempotency-key forces-2026-08-m1
```

Todo vive en `.kokoro/` del workspace. No hay cron, hooks ni cascada
automática.
