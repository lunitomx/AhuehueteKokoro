# Scope — gh-37

**Issue:** [lunitomx/AhuehueteKokoro#37](https://github.com/lunitomx/AhuehueteKokoro/issues/37)
**Título:** bug: Codex skill installer installs an unusable Kokoro router
**Rama:** `bug/gh-37/unusable-codex-router` (desde `origin/main` @ `8a42601`)
**Fecha:** 2026-09-17

## WHAT

Un instalador de skills de terceros que copia únicamente
`.agents/skills/kokoro/SKILL.md` reporta éxito y deja un router Kokoro que no
puede resolver ninguna de sus raíces declaradas. El usuario ve una skill
instalada que no puede atender ni la primera petición.

## WHEN

Al instalar solo la skill desde el repo público con un instalador estándar de
skills, p. ej.:

```sh
python3 install-skill-from-github.py --repo lunitomx/AhuehueteKokoro --path .agents/skills/kokoro
```

Condiciones: `KOKORO_HOME` sin definir, el SKILL.md fuera de un paquete
instalado y fuera de un checkout de Kokoro.

## WHERE

- `.agents/skills/kokoro/SKILL.md` — resolución de raíz **posicional**
  (pasos 1–3) y manejo de fallo genérico (paso 6).
- `kokoro-package.yaml` — declara `codex_entrypoint: .agents/skills/kokoro/SKILL.md`
  como entrypoint, pero nada garantiza que el resto del paquete viaje con él.

## EXPECTED

Una copia aislada del SKILL.md debe:

1. Detectar que no puede resolver el paquete (sin `KOKORO_HOME`, sin paquete
   instalado, sin checkout) y **detenerse**.
2. Nombrar el comando soportado y auditable de instalación completa
   (`install/install.sh`) en vez de una acción vaga ("Kokoro verify/update").
3. No simular capacidad: no debe intentar atender la petición con comandos o
   conocimiento inexistentes.

## Done when

- [ ] Existe una prueba automatizada que, sobre una copia aislada del SKILL.md,
      falla con el router actual y pasa con el router corregido.
- [ ] El router instalado emite un mensaje de fallo que incluye el comando
      exacto de instalación soportado.
- [ ] El README/guía de instalación dirige a los instaladores de skills de
      terceros hacia la ruta auditada (`install/install.sh`).
- [ ] `install/verify.sh` sigue pasando en una instalación completa.

## Reproducción (evidencia)

```text
Contenido instalado (copia aislada):
  <skill-root>/skills/kokoro/SKILL.md

KOKORO_HOME='<unset>'
  FALTA IDENTITY_kokoro.md
  FALTA .claude/commands/kokoro.md
  FALTA .claude/knowledge

ocurrencias de 'install/install.sh' en el router: 0
ocurrencias de 'verify': 1  (texto vago: "Kokoro verify/update", sin ruta)
```

## Fuera de alcance

- #38 (target `.agents` del instalador auditado) — se resuelve en la rama
  `fix/agents-skill-install-target`, no aquí.
- Publicar el paquete o tocar el árbol privado de origen en esta fase.

## TRIAGE

```
TRIAGE:
  Bug Type:    Interface
  Severity:    S2-Medium
  Origin:      Design
  Qualifier:   Missing
```

**Justificación**

| Dimensión | Valor | Por qué |
|---|---|---|
| Bug Type | **Interface** | El fallo está en el contrato entre el instalador de skills de terceros y el paquete Kokoro: se copia un entrypoint cuyo contrato exige archivos que no viajan con él. |
| Severity | **S2-Medium** | Bloquea por completo esa vía de instalación, pero existe workaround confirmado (`install/install.sh`) y no hay pérdida de datos ni exposición de credenciales. |
| Origin | **Design** | El diseño del entrypoint `.agents/skills/kokoro` nunca fue autosuficiente ni fallaba con un mensaje accionable; no es un error de código aislado. |
| Qualifier | **Missing** | Falta la guarda de resolución de paquete y falta el mensaje con el comando soportado; el contenido existente es correcto en sí mismo. |

**Tracker:** GitHub issue (no Jira). El proyecto Jira `KOKORO` no tiene issues y
este repo público se gobierna en GitHub, así que los 4 campos custom de Jira
(`customfield_13267/12090/13269/13270`) **no aplican**; la clasificación queda
en este artefacto versionado como fuente de verdad.
