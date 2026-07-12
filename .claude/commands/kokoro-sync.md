# /kokoro-sync — Publicar Kokoro al repositorio público

> Pipeline completo de distribución: scoutea diferencias, sincroniza extension/,
> actualiza README, commitea y publica al repositorio público.

> "Lo que no se distribuye, no existe."

## Contexto

Kokoro se desarrolla en **RaizAncestral** (repositorio privado) y se distribuye
a través de **AhuehueteKokoro** (repositorio público en GitHub).

Este skill orquesta el pipeline completo de publicación para que cada cambio
llegue al repositorio público sin fricción.

## Cuándo usarlo

- Después de crear, modificar o eliminar un skill en `.claude/commands/`
- Después de cambiar archivos de conocimiento en `.claude/knowledge/`
- Antes de querer compartir cambios con usuarios del repo público
- Cuando quieras verificar qué skills están fuera de sincronía

## Cuándo NO usarlo

- Para cambios urgentes que solo afectan al repo privado — no hace falta
- Si solo cambiaste archivos de RaizAncestral que no están en `extension/`
  (work/, governance/, tests/, etc.)

## Instrucciones

### 1. Verificar estado actual

Ejecuta el scout para ver qué skills están desincronizados:

```bash
./scripts/publish-kokoro.sh --scout
```

Esto **no modifica nada**. Solo muestra qué archivos cambiaron.

### 2. Publicar pipeline completo

```bash
./scripts/publish-kokoro.sh
```

Esto ejecuta los 5 pasos:
1. **SCOUT** — detecta skills nuevos, modificados y eliminados
2. **SYNC** — copia los cambios a `extension/`
3. **README** — verifica que la tabla del README tenga los skills nuevos
4. **COMMIT** — crea un commit descriptivo en RaizAncestral
5. **PUBLISH** — corre `sync-to-ahuehuetemx.sh` hacia AhuehueteKokoro

### 3. Dry run (ensayar sin ejecutar)

```bash
./scripts/publish-kokoro.sh --dry-run
```

Muestra todo lo que haría sin modificar nada.

### 4. Solo publicar (si ya sincronizaste)

```bash
./scripts/publish-kokoro.sh --publish
```

Salta los pasos 1-4 y solo corre el sync a AhuehueteKokoro.

## Arquitectura

```
RaizAncestral/                          AhuehueteKokoro/
├── .claude/commands/   ───sync──→      ├── .claude/commands/  (68 skills)
├── .claude/knowledge/  ───sync──→      ├── .claude/knowledge/ (58 archivos)
├── .claude/skills/     ───sync──→      ├── .claude/skills/    (11 skills)
├── extension/          ──canonical──→  ├── AGENTS.md
│   ├── README.md                        ├── README.md
│   ├── AGENTS.md                        ├── SETUP-CLAUDE-DESKTOP.md
│   └── .claude/                         └── .gitignore
│
├── scripts/
│   ├── publish-kokoro.sh     ← ORQUESTADOR (este skill)
│   └── sync-to-ahuehuetemx.sh ← DISTRIBUIDOR
│
└── .github/workflows/
    └── publish-kokoro.yml    ← AUTO (push a dev)
```

## Automatización

Este pipeline también se ejecuta automáticamente via GitHub Action cada que
haces push a `dev`. Si prefieres control manual, usa este skill.

## Salida esperada

```
══════════════════════════════════════════════
  Kokoro Publisher — Orquestador de Publicación
══════════════════════════════════════════════

  Origen:  .../RaizAncestral
  Destino: .../RaizAncestral/extension

[1/5]🔍 Scouteando diferencias...
  📂 Commands:
    ~ modificado: kokoro-placements.md
  📂 Knowledge:
    ✓ Sin cambios
  ...

[2/5]📦 Sincronizando a extension/...
  ✓ Sincronizado

[3/5]📝 Actualizando README.md...
  ✓ README ya tiene todos los skills documentados

[4/5]💾 Commit en RaizAncestral...
  ✓ Commit creado

[5/5]🚀 Publicando a AhuehueteKokoro...
  ✓ Pushed to origin

══════════════════════════════════════════════
  ¡Pipeline completado!
══════════════════════════════════════════════
```
