# E49 Portable Install Release

## Qué cambia

Kokoro ya no depende de que Claude Code o Codex se abran dentro del repo clonado.
El paquete público ahora incluye instalador global, verificador, actualizador y
desinstalador.

## Cómo instalar

```bash
git clone https://github.com/lunitomx/AhuehueteKokoro.git
cd AhuehueteKokoro
./install/install.sh
```

Después de instalar, puedes abrir otro proyecto y usar Kokoro:

```bash
cd ~/mi-proyecto
claude
/kokoro
```

## Qué instala

- `~/.claude/kokoro/` con identidad, comandos y conocimiento de Kokoro.
- `~/.claude/commands/kokoro*.md` como wrappers globales para Claude Code.
- `~/.codex/skills/kokoro/SKILL.md` como router global para Codex.

## Verificación

```bash
~/.claude/kokoro/install/verify.sh
```

El verificador comprueba identidad, comandos, conocimiento, wrappers de Claude,
skill de Codex y ausencia de superficies privadas en el paquete instalado.

## Desinstalar

```bash
./install/uninstall.sh
```

El desinstalador solo elimina archivos marcados como propiedad de Kokoro y deja
intactos los comandos propios del usuario.
