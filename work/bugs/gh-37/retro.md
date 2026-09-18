## Retrospective: gh-37

### Summary

- **Root cause:** el entrypoint `.agents/skills/kokoro` se diseñó para un
  checkout (resolución posicional) y se declaró como instalable, sin guarda de
  preflight ni comando de recuperación.
- **Fix approach:** resolución explícita de la raíz del paquete, guarda
  ejecutable (`preflight.sh`) que falla con el comando soportado, docs que
  enrutan a la vía auditada y test de contrato en CI.
- **Classification:** Interface / S2-Medium / Design / Missing.

### Process Improvement

**Prevention:** que `kokoro-package.yaml` no pueda declarar un `*_entrypoint`
sin un guard ejecutable hermano y sin una aserción de contrato en
`tests/agents_entrypoint_contract.sh`. La convención queda ahora en el propio
test: cualquier entrypoint futuro se verifica igual.

**Pattern:** Bug Type=Interface + Origin=Design → cuando un artefacto se declara
"instalable" sin definir su contrato de instalación, el modo de fallo es
silencioso (el instalador reporta éxito). Todo entrypoint necesita una guarda
que resuelva o se detenga con la acción soportada.

### Heutagogical Checkpoint

1. **Learned:** el repo público tiene tres vías de instalación (checkout,
  instalador auditado, instalador de skills de terceros) y solo dos estaban
  cubiertas; la tercera se apoyaba en un router cuyo contrato nunca se escribió.
  También aprendí que el privacy scan corre sobre *todo* el árbol, incluidos los
  artefactos RaiSE, y que los commits del bugfix van al repo público.
2. **Process change:** los artefactos de bug deben redactarse desde el primer
  commit sin marcadores del árbol privado; el gate de privacidad se corre antes
  de cada commit del pipeline, no al final.
3. **Framework improvement:** separar en el test de contrato los bloques
  "router", "guarda ejecutable" y "docs" permitió que T2 cerrara con evidencia
  parcial (13/13) sin fingir verde completo mientras T3 seguía pendiente.
4. **Capability gained:** convertir una guarda en prosa para un LLM en una
  guarda **ejecutable** verificable con `HOME` aislado, de modo que la regresión
  se prueba de verdad y no por grep.

### Patterns

- **Added:** PAT-49 (technical — entrypoint resuelve por ruta explícita o falla
  con el comando soportado), PAT-50 (process — artefactos de bugfix en repo
  público deben pasar el privacy scan).
- **Reinforced:** ninguno evaluado (no se cargaron patrones de comportamiento en
  el arranque de esta sesión).

### Evidencia

| Gate | Resultado |
|---|---|
| `bash tests/agents_entrypoint_contract.sh` | 17/17 OK |
| `python3 install/privacy_scan.py .` | OK |
| `install/install.sh` + `install/verify.sh` en HOME aislado | `Kokoro verify OK.` (89 wrappers) |
| Reproducción original (copia aislada) | guarda sale 1 y nombra `install/install.sh` |

### Addendum post-CI

El primer run de CI del PR #39 falló en el paso del contrato: el workflow
exporta `KOKORO_CLAUDE_HOME` en `$GITHUB_ENV`, así que el caso C (paquete en
`$HOME/.claude/kokoro`) resolvía primero el `KOKORO_CLAUDE_HOME` heredado del
runner y salía 1. Fix: el test ahora limpia explícitamente `KOKORO_HOME`,
`KOKORO_PACKAGE_HOME` y `KOKORO_CLAUDE_HOME` en los cuatro entornos simulados,
verificado reproduciendo el env de CI en local.

**Lección:** un test que hereda variables de entorno del runner no es
determinista; el verde local no garantiza el verde en CI. La guarda del router
en sí no cambió: el defecto estaba en la prueba.

