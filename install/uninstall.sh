#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

CLAUDE_HOME="$(kokoro_claude_home)"
PACKAGE_HOME="$(kokoro_package_home "$CLAUDE_HOME")"
COMMANDS_TARGET="$CLAUDE_HOME/commands"
CODEX_HOME_PATH="$(kokoro_codex_home)"
CODEX_SKILL_DIR="$CODEX_HOME_PATH/skills/kokoro"

removed=0
preserved=0

if [ -d "$COMMANDS_TARGET" ]; then
    while IFS= read -r wrapper; do
        if grep -q '^kokoro_owned: true$' "$wrapper"; then
            rm -f "$wrapper"
            echo "Removed wrapper: $(kokoro_display_path "$wrapper")"
            removed=$((removed + 1))
        else
            echo "Preserved non-Kokoro command: $(kokoro_display_path "$wrapper")"
            preserved=$((preserved + 1))
        fi
    done < <(find "$COMMANDS_TARGET" -maxdepth 1 -type f -name 'kokoro*.md' | sort)
fi

if [ -f "$CODEX_SKILL_DIR/SKILL.md" ]; then
    if grep -q '^kokoro_owned: true$' "$CODEX_SKILL_DIR/SKILL.md"; then
        rm -rf "$CODEX_SKILL_DIR"
        echo "Removed Codex skill: $(kokoro_display_path "$CODEX_SKILL_DIR")"
        removed=$((removed + 1))
    else
        echo "Preserved non-Kokoro Codex skill: $(kokoro_display_path "$CODEX_SKILL_DIR")"
        preserved=$((preserved + 1))
    fi
fi

if [ -f "$PACKAGE_HOME/package.yaml" ] && grep -q '^package: kokoro$' "$PACKAGE_HOME/package.yaml"; then
    rm -rf "$PACKAGE_HOME"
    echo "Removed package home: $(kokoro_display_path "$PACKAGE_HOME")"
    removed=$((removed + 1))
elif [ -e "$PACKAGE_HOME" ]; then
    echo "Preserved package home without Kokoro marker: $(kokoro_display_path "$PACKAGE_HOME")"
    preserved=$((preserved + 1))
fi

echo "Kokoro uninstall complete. removed=$removed preserved=$preserved"
