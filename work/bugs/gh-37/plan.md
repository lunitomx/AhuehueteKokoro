# Plan — gh-37

**Issue:** [lunitomx/AhuehueteKokoro#37](https://github.com/lunitomx/AhuehueteKokoro/issues/37)
**Rama:** `bug/gh-37/unusable-codex-router`
**Enfoque elegido (GATE 2):** B — router con resolución explícita + guarda de
preflight ejecutable + comando soportado, docs hacia la vía auditada y test de
contrato.

## Estrategia

La guarda se vuelve **ejecutable** (`preflight.sh`) para que el fix sea
verificable de forma determinista, no solo por prosa. El router la invoca como
primer paso y mantiene un fallback en prosa para harnesses que no ejecutan
scripts.

## Tasks

### T1: Regression test (RED)
- Crear `tests/agents_entrypoint_contract.sh` con tres bloques:
  1. **Contrato estático del router**: `.agents/skills/kokoro/SKILL.md` contiene
     `KOKORO_HOME`, `~/.claude/kokoro`, `IDENTITY_kokoro.md`, una sección de
     preflight, el comando `install/install.sh` y la frase que declara inválida
     la copia aislada.
  2. **Guarda ejecutable** (3 entornos simulados con `HOME` aislado):
     - copia aislada sin paquete → `preflight.sh` sale **1** y su mensaje
       contiene `install/install.sh`;
     - `KOKORO_HOME` con `IDENTITY_kokoro.md` → sale **0** e imprime la raíz;
     - layout instalado `$HOME/.claude/kokoro/IDENTITY_kokoro.md` → sale **0**.
  3. **Docs**: `README.md` y `docs/releases/e49-portable-install.md` enrutan a
     los instaladores de skills de terceros hacia `install/install.sh`.
- Verify: `bash tests/agents_entrypoint_contract.sh` → **FALLA** (prueba que el
  bug existe).
- Commit: `test(gh-37): add regression test for the .agents router contract`

### T2: Router con guarda y comando soportado (GREEN)
- Reescribir `.agents/skills/kokoro/SKILL.md` con la precedencia explícita:
  `KOKORO_HOME` → `~/.claude/kokoro` → raíz del checkout contenedor.
- Añadir `.agents/skills/kokoro/preflight.sh` (ejecutable) que resuelve la raíz
  y, si no existe, imprime el comando soportado y sale 1.
- Verify: `bash tests/agents_entrypoint_contract.sh` → **PASA**.
- Commit: `fix(gh-37): make the .agents router resolve the package or fail clearly`

### T3: Docs de la vía soportada
- `README.md` y `docs/releases/e49-portable-install.md`: sección que explica que
  copiar solo `SKILL.md` con un instalador de terceros **no** es una instalación
  válida y enruta a `./install/install.sh`.
- Verify: bloque 3 del test de contrato + `python3 install/privacy_scan.py .`.
- Commit: `docs(gh-37): route third-party skill installers to the audited installer`

### T4: Integración en CI y verificación end-to-end
- Añadir el test de contrato como paso del workflow
  `.github/workflows/kokoro-privacy.yml`.
- Verify (local, HOME aislado): `bash install/install.sh` +
  `"$KOKORO_CLAUDE_HOME/kokoro/install/verify.sh"` → `Kokoro verify OK.`
- Commit: `test(gh-37): run the .agents entrypoint contract in CI`

## Criterios de Done (del scope)

| Criterio | Task |
|---|---|
| Prueba automatizada que falla hoy y pasa corregida | T1 + T2 |
| Mensaje de fallo con el comando exacto soportado | T2 |
| Docs enrutan a la ruta auditada | T3 |
| `install/verify.sh` sigue pasando | T4 |

## Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| Duplicar/ chocar con la rama `fix/agents-skill-install-target` (#38) | #37 no toca `install/install.sh`; el router del repo es un archivo distinto. Se documenta la dependencia en el cierre. |
| Prosa que un harness no ejecuta | Fallback en prosa dentro del propio router; el test cubre ambos. |
| Romper el caso "checkout" | T1 caso 3 y `install/verify.sh` en T4 lo cubren. |
