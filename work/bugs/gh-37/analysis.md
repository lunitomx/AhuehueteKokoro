# Analysis — gh-37

**Issue:** [lunitomx/AhuehueteKokoro#37](https://github.com/lunitomx/AhuehueteKokoro/issues/37)
**Rama:** `bug/gh-37/unusable-codex-router`
**Método:** 5 Whys (cadena causal única) + verificación de hipótesis competidoras
**Clasificación (triage):** Interface / S2-Medium / Design / Missing

## Señales disponibles

| Señal | Presente | Método que sugiere |
|---|---|---|
| Stack trace / error con ubicación | No (fallo de comportamiento, no excepción) | — |
| Cambio que lo introdujo | Sí (`e3b2f0c`, `c2b325a`, `4984c87`) | git log por archivo |
| Causa única sospechada | Sí | **5 Whys** |
| Causa evidente en reproducción | Parcial | 5 Whys + hipótesis |

Método elegido: **5 Whys**, apoyado en el historial de los commits que
introdujeron el entrypoint. Tier rai-debug: **S**.

## 5 Whys

```
Problema: una copia aislada de .agents/skills/kokoro/SKILL.md no puede
resolver identidad, comandos ni conocimiento (0/3 raíces).

1. ¿Por qué?  Porque el router resuelve la raíz del paquete POR POSICIÓN
              (KOKORO_HOME → paquete contenedor → checkout) y en la copia
              aislada ninguna de las tres aplica.
              Evidencia: SKILL.md pasos 1–3; reproducción → 3/3 FALTA.

2. ¿Por qué?  Porque el router se escribió para vivir DENTRO del checkout,
              donde la posición siempre resuelve sola.
              Evidencia: `e3b2f0c fix(install): expose Kokoro Codex entrypoint`
              (29 jun, con `tests/test_integrity.py`); README solo documenta
              `./install/install.sh`, nunca un instalador de skills de terceros.

3. ¿Por qué?  Porque el manifest declaró ESE MISMO archivo como
              `codex_entrypoint` instalable, sin un contrato que garantice que
              el resto del paquete viaje con él.
              Evidencia: `kokoro-package.yaml:7`;
              `install/install.sh:188-190` copia el dir a
              `$PACKAGE_HOME/.agents/skills/kokoro` (anidado, ver #38).

4. ¿Por qué?  Porque no hay guarda de preflight ni mensaje accionable: el
              paso 6 dice "run Kokoro verify/update" sin nombrar ningún
              comando soportado ni ruta.
              Evidencia: `grep -c 'install/install.sh' SKILL.md` → 0;
              'verify' aparece 1 vez, como texto vago.

5. ¿Por qué?  (RAÍZ) Porque el diseño del entrypoint `.agents/skills/kokoro`
              nunca definió su contrato de instalación: asumió resolución
              posicional y no distinguió "checkout" de "skill instalada por un
              tercero". Por eso el modo de fallo es silencioso y sin salida.
```

## Hipótesis competidoras (eliminadas)

| Hipótesis | Test | Resultado | Conclusión |
|---|---|---|---|
| H1: el router está corrupto o desactualizado | `git log --follow` + lectura completa + `verify.sh` | Contenido coherente, `kokoro_owned: true`, verify lo revisa | **Eliminada** |
| H2: el instalador auditado no instala ninguna skill | Inspección de `install.sh` + `~/.codex/skills/kokoro/SKILL.md` | Sí la instala (y tras #38 también en `~/.agents`) | **Eliminada** (el fallo es de la vía de terceros) |
| H3: los harnesss `.agents` no descubren la skill | Catálogo de skills de la sesión DSH actual | `kokoro` **sí** aparece, descubierta desde `.agents/skills/kokoro` del proyecto | **Eliminada** |
| H4: el problema es solo #38 (target faltante) | `git diff origin/main..fix/agents-skill-install-target` | #38 no toca el router del repo; la copia aislada seguiría rota | **Eliminada** como causa de #37 |

## Causa raíz

> El entrypoint `.agents/skills/kokoro` se diseñó para un checkout (resolución
> posicional) y se declaró como entrypoint instalable, sin guarda de preflight
> ni comando de recuperación. Una instalación que copie solo el `SKILL.md`
> queda muda: no puede resolver el paquete ni sabe qué hacer al respecto.

Es accionable y explica todos los síntomas: copia aislada sin raíces, ausencia
de mensaje útil y aparente "éxito" del instalador de terceros.

## Enfoques de fix (para GATE 2)

| # | Enfoque | Alcance | Trade-off |
|---|---|---|---|
| **A** | Solo docs: README/guía advierten que la vía de terceros es inválida | `README.md`, `docs/releases/e49-portable-install.md` | Mínimo, pero **no arregla el router**: quien ya lo instaló sigue con una skill muda. No cumple "Done when". |
| **B** | **Router con resolución explícita + guarda + comando soportado, y docs que enrutan a la vía auditada, con test de contrato** | `.agents/skills/kokoro/SKILL.md`, `README.md`, `docs/releases/e49-portable-install.md`, `tests/` | Cubre las 3 sugerencias del issue; reusa la forma del router generado que #38 ya produce (ruta absoluta del paquete). Añade un test de contrato estático. |
| **C** | Empaquetar identidad+comandos+conocimiento dentro de `.agents/skills/kokoro` | todo el paquete | Autosuficiencia real, pero duplica ~200 archivos y rompe la separación public/package. Sobre-ingeniería para S2. |

**Recomendado: B.** Ataca la causa raíz (contrato de instalación indefinido),
es consistente con la forma que #38 ya introduce, y deja una prueba que evita
la regresión. A sola no cumple; C no se justifica para S2-Medium.

## Contrato del router corregido (borrador para Fase 4/5)

1. `KOKORO_HOME` si está definido.
2. Si no, `~/.claude/kokoro/IDENTITY_kokoro.md` (ruta absoluta del paquete
   instalado, forma que ya emite `write_router_skill()`).
3. Si no, la raíz del checkout contenedor (caso desarrollo).
4. Si ninguna resuelve: **STOP** y mostrar el comando soportado exacto
   (`git clone … && cd AhuehueteKokoro && ./install/install.sh`), declarando
   explícitamente que copiar solo el `SKILL.md` no es una instalación válida.
