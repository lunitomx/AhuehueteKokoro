# Contrato de Hipótesis v1

> Una hipótesis es una pregunta con una vara fijada antes de mirar el
> resultado. No es una respuesta, ni una corazonada con formato.

La regla canónica vive en `runtime/evidence.py` (`validate_hypothesis`,
`bar_digest` y los dos gates) y en `runtime/evidence_ledger.py`
(`hypothesis_created`, `hypothesis_approved`). Si este archivo y el código no
coinciden, el código manda y este archivo es el error.

Los estados epistémicos y la provenance están en `kokoro-evidence-model.md`.
De dónde nace una hipótesis está en `kokoro-open-questions.md`.

## Para qué sirve

Separa la apuesta del resultado. **Observado ≠ inferido ≠ hipótesis ≠
validado.** Nada llega a `validated` por conveniencia: solo una validación
registrada contra una vara precomprometida y aprobada por una persona.

Sin este contrato, la vara se escribe después de ver los números y cualquier
resultado parece un éxito.

## Contrato

Campos que escribe quien crea la hipótesis:

| Campo | Regla | Ejemplo |
|---|---|---|
| `id` | `HYP-…` o `HIP-…` | `HYP-014` |
| `source_loop_id` | Opcional. `LOOP-…` en estado `promoted`. | `LOOP-007` |
| `origin` | Texto. Obligatorio si no hay `source_loop_id`: el comando que la creó. | `/kokoro-hypothesis` |
| `guest` | Slug del invitado, nunca un nombre real. | `cliente_01` |
| `prediction` | Qué esperamos que pase, observable. | `El encabezado de portales consigue 1.3x citas` |
| `decision_at_stake` | Qué decisión cambia con el resultado. | `Qué mensaje encabeza la campaña de noviembre` |
| `evidence_plan.sources` | Al menos una fuente. | `["meta_ads", "crm"]` |
| `evidence_plan.disconfirming_read` | La lectura que la haría falsa. Obligatoria. | `B consigue igual o menos citas que A` |
| `evidence_plan.unavailable_sources` | Opcional. Lo que no podremos ver. | `["cobro a 60 días"]` |
| `precommitted_bar` | Los 4 criterios: `validated`, `invalidated`, `inconclusive`, `insufficient`. | ver Ejemplo |
| `experiment_id` | Opcional. `EXP-…` | `EXP-014` |
| `supersedes` | Opcional. La hipótesis que este rediseño reemplaza. | `HYP-013` |
| `redesign_reason` | Obligatorio con `supersedes`. | `La muestra de 20 leads era chica` |

Campos que pone el ledger, nunca la entrada:

| Campo | Significado |
|---|---|
| `status` | `proposed` → `approved` → `resolved`, o `superseded` |
| `bar_sha256` | Huella de los 4 criterios de la vara |
| `approved_by`, `approver_ref`, `approved_at` | Quién aprobó (siempre `human`) y cuándo |
| `validation_ids` | Validaciones registradas contra esta hipótesis |
| `superseded_by`, `resolved_at` | Rediseño que la reemplazó; fecha de resolución |

## Reglas

1. **Falsable (GATE-HYPOTHESIS-FALSIFIABLE).** Exige `disconfirming_read` y
   `precommitted_bar.invalidated`. Los criterios `validated` e `invalidated`
   no pueden ser el mismo texto. Si falla, el gate queda Blocked.
2. **Vara precomprometida (GATE-EVIDENCE-BAR-PRECOMMITTED).** Los 4 criterios
   existen antes de mirar datos. Falta uno: Blocked.
3. **Huella de la vara.** `bar_sha256` es el SHA-256 del JSON canónico de los
   4 criterios. `evidence check --kind hypothesis` la devuelve sin escribir.
4. **Aprobación humana.** `hypothesis_approved` solo acepta
   `approved_by: "human"`, un `approver_ref` en forma de slug y el mismo
   `bar_sha256`. Solo se aprueba desde `proposed`. Kokoro no se aprueba solo.
5. **Validar exige aprobación.** `validation_recorded` pide una hipótesis
   `approved` y la misma huella. Si cambia: «evidence bar changed after
   commitment; record a redesign first». Si hay `experiment_id`, debe coincidir.
6. **Rediseño por `supersedes`.** Para cambiar la vara se crea una hipótesis
   nueva con `supersedes` y `redesign_reason`. La anterior debe estar
   `proposed` o `approved` y pasa a `superseded`. La nueva empieza en
   `proposed` y necesita su propia aprobación.
7. **Después de resolver no hay `supersedes`.** Una hipótesis `resolved` no se
   rediseña. Si el resultado fue `inconclusive` o `insufficient`, la siguiente
   apuesta nace de un loop nuevo (`validation.new_loops`) o con `origin`.
8. **Del loop a la hipótesis.** Con `source_loop_id`, el loop debe estar
   `promoted`. Un rediseño puede colgar del mismo loop si reemplaza una
   hipótesis de ese loop.
9. **Nada de secretos ni datos privados.** Contenido con forma de secreto se
   rechaza. Las personas se nombran por slug.

## Ejemplo

Invitado `cliente_01`, despachos contables. Datos ficticios.

```json
{"hypothesis": {
  "id": "HYP-014",
  "source_loop_id": "LOOP-007",
  "guest": "cliente_01",
  "prediction": "El encabezado de portales consigue al menos 1.3x las citas del de seguimiento",
  "decision_at_stake": "Qué mensaje encabeza la campaña de noviembre",
  "evidence_plan": {
    "sources": ["meta_ads", "crm"],
    "disconfirming_read": "Portales consigue igual o menos citas que seguimiento"
  },
  "precommitted_bar": {
    "validated": "Portales >= 1.3x citas con 25 o más leads por variante en 14 días",
    "invalidated": "Portales <= 1.0x citas con 25 o más leads por variante",
    "inconclusive": "Entre 1.0x y 1.3x, o citas y show apuntan en sentidos opuestos",
    "insufficient": "Menos de 25 leads en alguna variante al cerrar la ventana"
  },
  "experiment_id": "EXP-014"
}}
```

1. `K evidence check --kind hypothesis` devuelve `ok: true` y la huella.
2. La persona `equipo_01` lee la vara y aprueba con esa huella.
3. A los 10 días alguien propone bajar a 1.2x. La vara ya está comprometida:
   se registra `HYP-015` con `supersedes: HYP-014` y la razón, y se aprueba
   otra vez. La versión vieja queda en el ledger como `superseded`.

## Anti-patrones

- **Mover la vara.** Bajar de 1.3x a 1.1x al ver 1.15x. El ledger lo rechaza.
- **Vara escrita después.** Si los criterios llegan junto con los números, no
  hay hipótesis: hay un reporte con un adjetivo.
- **Sin lectura que la refute.** «Veremos qué pasa» no es `disconfirming_read`.
- **Aprobación de la IA.** Solo una persona aprueba. Un agente propone.
- **Rediseñar lo resuelto.** Un `insufficient` pide una apuesta nueva, no
  reescribir la vieja.
- **Nombres reales en `approver_ref`.** Siempre slug.

## Comandos y runtime

- `/kokoro-hypothesis` redacta la hipótesis y su vara, corre el check y pide
  aprobación humana.
- `/kokoro-hypothesis-validate` registra el resultado contra la vara.
- `/kokoro-validate` y `/kokoro-experiment` siguen siendo el plan y el sprint
  3x3x3. Este contrato les da su forma en el ledger.

```bash
K() { python3 "$KOKORO_PACKAGE_HOME/runtime/kokoro.py" "$@"; }
K evidence check  --kind hypothesis --input-file hyp.json        # sin escribir; devuelve bar_sha256
K evidence append --type hypothesis_created  --input-file ev.json --idempotency-key hyp-014
K evidence append --type hypothesis_approved --input-file ok.json --idempotency-key hyp-014-ok
cat .kokoro/shared/views/evidence/hypotheses.yaml
```

`ok.json`: `{"hypothesis_id": "HYP-014", "approved_by": "human",
"approver_ref": "equipo_01", "bar_sha256": "<huella del check>"}`.
Todo vive en el workspace `.kokoro/`; nada se escribe en el paquete.
