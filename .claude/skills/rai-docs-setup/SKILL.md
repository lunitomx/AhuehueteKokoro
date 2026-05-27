---
allowed-tools:
- Bash(rai:*)
- Bash([ -n:*)
description: 'Configure the docs adapter for all RaiSE skills in one session — docs
  adapter config complete. Currently supports Confluence.

  '
license: MIT
metadata:
  raise.adaptable: 'true'
  raise.fase: '0'
  raise.frequency: once
  raise.gate: ''
  raise.next: rai-backlog-setup
  raise.prerequisites: ''
  raise.version: 1.1.0
  raise.visibility: public
  raise.work_cycle: utility
name: rai-docs-setup
---

# Docs Setup

## Purpose

Configure `.raise/docs.yaml` para un espacio de Confluence en una sola sesión conversacional — al terminar el usuario sabe cómo está mapeado su espacio y cómo publicar el primer artefacto. Currently supported backend: Confluence.

## Mastery Levels (ShuHaRi)

- **Shu**: Follow all steps in order; show routing map and rai docs write demo at the end
- **Ha**: Run steps 0–3 directly; show routing map and verify
- **Ri**: `rai adapter setup confluence --site {site} --instance {instance} --space {space} --yes --structure raise && rai docs search "{space}"`

## When to use this skill

| Need | Skill |
|------|-------|
| Configure **docs adapter** (Confluence space, routing) | **This skill** (`rai-docs-setup`) |
| Configure **backlog adapter** (Jira, custom fields, statuses) | `rai-backlog-setup` |
| Configure both at once (legacy) | `rai-adapter-setup` *(deprecated)* |

Use this skill after `rai init`, when setting up the docs adapter, or when `/rai-doctor` reports missing docs adapter config.

**When to skip:** `rai docs search "test"` returns results without error — adapter already configured. Use `--overwrite` to regenerate.

## Context

**Prerequisites:** `CONFLUENCE_URL` + `CONFLUENCE_API_TOKEN` + `CONFLUENCE_USERNAME` must exist in `~/.rai/.env` or `.env` in the project root. `rai init` complete.

## Steps

### Step 0: Credential Gate

Check that all three credentials are present. Never print or log their values.

```bash
[ -n "$CONFLUENCE_URL" ] || {
  echo "CONFLUENCE_URL no está seteada."
  echo "Opciones:"
  echo "  1. Llena .env.example y cópialo a .env en el proyecto: CONFLUENCE_URL=https://tu-instancia.atlassian.net"
  echo "  2. O agrégala globalmente en ~/.rai/.env para todos los worktrees"
  exit 1
}
[ -n "$CONFLUENCE_API_TOKEN" ] || {
  echo "CONFLUENCE_API_TOKEN no está seteada."
  echo "Opciones:"
  echo "  1. Llena .env.example y cópialo a .env en el proyecto: CONFLUENCE_API_TOKEN=tu-token"
  echo "  2. O agrégala globalmente en ~/.rai/.env para todos los worktrees"
  exit 1
}
[ -n "$CONFLUENCE_USERNAME" ] || {
  echo "CONFLUENCE_USERNAME no está seteada."
  echo "Opciones:"
  echo "  1. Llena .env.example y cópialo a .env en el proyecto: CONFLUENCE_USERNAME=tu-email"
  echo "  2. O agrégala globalmente en ~/.rai/.env para todos los worktrees"
  exit 1
}
```

If any check fails: stop and present the message above. Do NOT ask the user to type the token in the chat. Do NOT suggest running `source`. `rai` loads credentials automatically from `.env` in the project (higher priority) or `~/.rai/.env` as global fallback — `rai init` ya genera `.env.example` con las vars necesarias.

**Nota:** Si el shell reporta MISSING pero las vars están en `.env`, está bien — `rai` las carga directamente sin necesidad de `export`.

<verification>
`CONFLUENCE_URL`, `CONFLUENCE_API_TOKEN`, and `CONFLUENCE_USERNAME` are present in the environment OR exist in `.env`/`~/.rai/.env`. Skill proceeds.
</verification>

### Step 1: Collect Connection Parameters

Ask in order — do not bundle into a single prompt:

1. **Site** — "¿Cuál es tu Confluence site? (ej. `miempresa.atlassian.net` para Cloud, o `confluence.miempresa.com` para self-hosted)"

   Derive `{instance}` automatically from the first subdomain: `ferrodza.atlassian.net` → `ferrodza`. No need to ask.

2. **Space key** — "¿Cuál es la clave de tu espacio? La encuentras en la URL: `…/wiki/spaces/{CLAVE}/…`"

### Step 2: Elegir estructura de páginas

Antes de preguntar, explica lo que cambia:

> "¿Cómo quieres organizar los artefactos en Confluence?
>
> **[1] Estructura RaiSE** *(recomendado)*
>    27 tipos mapeados en 7 secciones — las páginas padre se crean solas la primera vez:
>    - **Epics** → briefs, scopes, diseños, docs
>    - **Stories** → scope, design, plan, cierre
>    - **Bugs** → scope, análisis, plan, retro
>    - **Sessions** → diarios, retrospectivas
>    - **Architecture** → ADRs, domain model, system design
>    - **Research** → research, proposals
>    - **Developer Docs** → vision, PRD, guardrails, backlog
>
> **[2] Mínima**
>    Solo 2 rutas genéricas: `adr` y `developer`. Útil si quieres definir tu propia estructura."

- **[1]** → add `--structure raise` to the command
- **[2]** → continue without preset

### Step 3: Run Setup

```bash
# Con estructura RaiSE (recomendado):
rai adapter setup confluence --site {site} --instance {instance} --space {space} --yes --structure raise

# Sin preset:
rai adapter setup confluence --site {site} --instance {instance} --space {space} --yes
```

The CLI auto-discovers the page tree and validates credentials against the live API — if credentials are wrong, fails here with a clear error.

Use `--overwrite` if the adapter is already configured and the developer wants to regenerate.

<verification>
CLI output shows "Discovering spaces..." and found `{space}`. Config written to `.raise/docs.yaml`.
</verification>

### Step 4: Mostrar el mapa de rutas

Después del setup, lee `.raise/docs.yaml` y presenta el mapa en formato legible. Agrupa por `parent_title`:

```
✓ Tu espacio {space} está mapeado en {N} secciones:

  Epics          → epic-brief, epic-scope, epic-design, epic-docs
  Stories        → story, story-scope, story-design, story-plan
  Bugs           → bugfix-scope, bugfix-analysis, bugfix-plan, bugfix-retro
  Sessions       → session-diary, retrospective, mission-retro
  Architecture   → adr, architecture-domain-model, architecture-index,
                   architecture-module, architecture-system-context, architecture-system-design
  Research       → research, proposal
  Developer Docs → project-vision, project-prd, project-guardrails, project-backlog

Las páginas padre se crean automáticamente la primera vez que publiques a cada sección.
```

Explica brevemente: cuando una skill publica un artefacto (ej. `session-diary`), el CLI busca la página padre configurada (`Sessions`), la crea si no existe, y publica ahí. El usuario nunca tiene que crear la estructura manualmente.

### Step 5: Demo de rai docs write

Muestra cómo publicar el primer artefacto:

```bash
# Publicar desde un archivo existente:
rai docs write session-diary \
  --title "Mi primera sesión" \
  --file .raise/sessions/hoy.md

# Publicar desde stdin (útil en pipes y scripts):
echo "# Contenido" | rai docs write session-diary \
  --title "Mi primera sesión" \
  --stdin \
  --output-path .raise/sessions/hoy.md
```

**Sobre `--output-path`:** necesario cuando la ruta en `docs.yaml` no tiene `local_dir` configurado (el caso por defecto). Sin él, el CLI no sabe dónde guardar la copia local y falla. Siempre inclúyelo cuando publiques desde stdin.

Explica: el tipo de artefacto (`session-diary`, `adr`, `research`, etc.) es lo que determina dónde va la página en Confluence — no hay que especificar la página padre manualmente.

### Step 6: Verify

```bash
rai doctor
rai docs search "{space}"
```

Show both outputs. Confirm that `rai doctor` reports no adapter errors and `rai docs search` returns results from the configured space.

Confirm routing is complete:
- With `--structure raise`: the setup output shows "✓ Injecting RaiSE routing preset (27 artifact types)"
- Without preset: at minimum `adr` and `developer` routes are present

Declare setup complete.

<verification>
`rai doctor` passes. `rai docs search "{space}"` returns ≥1 result. Routing count confirmed (27 with preset, ≥2 without).
</verification>

## Output

| Artifact | Destination |
|----------|-------------|
| Docs adapter config | `.raise/docs.yaml` |
| Routing map | Shown in conversation (Step 4) |
| Write demo | Shown in conversation (Step 5) |

## Quality Checklist

- [ ] Credential gate passed — `CONFLUENCE_URL`, `CONFLUENCE_API_TOKEN`, and `CONFLUENCE_USERNAME` present (or in `.env`)
- [ ] NEVER print, log, or request the value of a credential in the conversation
- [ ] NEVER suggest running `source` — credentials are loaded automatically by `rai`
- [ ] NEVER ask the user to type a token in the chat
- [ ] Asked site and space conversationally (2 questions) — instance derived automatically
- [ ] Showed both structure options with concrete examples BEFORE asking
- [ ] Called `rai adapter setup confluence` with `--site`, `--instance`, `--space`, `--yes` (no TTY)
- [ ] Presented routing map grouped by section after setup (Step 4)
- [ ] Showed `rai docs write` demo with `--output-path` note (Step 5)
- [ ] `rai doctor` reports no adapter errors after setup
- [ ] `rai docs search "{space}"` returns ≥1 result
- [ ] Routing count confirmed: 27 with `--structure raise`, ≥2 without

## References

- CLI help: `rai adapter setup confluence --help`, `rai docs write --help`
- Diagnostics: `/rai-doctor`
- Complement: `/rai-backlog-setup` (backlog adapter)
- Deprecated: `/rai-adapter-setup` (combined setup — use dedicated skills instead)
