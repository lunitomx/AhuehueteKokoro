# Scout — Reconocimiento de Artefactos

> Knowledge file para `/kokoro-scout` y `/kokoro-mirror`.

## Qué escanea

El directorio del proyecto en busca de artefactos Kokoro:
- `.kokoro/clients.json` — grafo de invitados
- `.claude/commands/` — skills instalados
- `.claude/knowledge/` — archivos de referencia
- `work/epics/` — épicas activas

## Mirror mode

`/kokoro-mirror` relee el perfil del scout y lo presenta como
espejo — "esto es lo que Kokoro ve en tu proyecto".
