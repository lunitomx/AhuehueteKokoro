#!/usr/bin/env bash

set -euo pipefail

kokoro_realpath() {
    local target="$1"
    if command -v python3 >/dev/null 2>&1; then
        python3 -c 'import os,sys; print(os.path.abspath(os.path.expanduser(sys.argv[1])))' "$target"
    else
        case "$target" in
            ~/*) printf '%s\n' "$HOME/${target#~/}" ;;
            /*) printf '%s\n' "$target" ;;
            *) printf '%s\n' "$(pwd)/$target" ;;
        esac
    fi
}

kokoro_script_dir() {
    cd "$(dirname "${BASH_SOURCE[1]}")" && pwd
}

kokoro_source_root() {
    local script_dir="$1"
    local root
    root="$(cd "$script_dir/.." && pwd)"

    if [ ! -d "$root/.claude/commands" ] && [ ! -d "$root/commands" ]; then
        echo "Kokoro setup error: package source does not contain Kokoro commands: $root" >&2
        exit 2
    fi

    printf '%s\n' "$root"
}

kokoro_source_commands_dir() {
    local root="$1"
    if [ -d "$root/.claude/commands" ]; then
        printf '%s\n' "$root/.claude/commands"
    else
        printf '%s\n' "$root/commands"
    fi
}

kokoro_source_knowledge_dir() {
    local root="$1"
    if [ -d "$root/.claude/knowledge" ]; then
        printf '%s\n' "$root/.claude/knowledge"
    else
        printf '%s\n' "$root/knowledge"
    fi
}

kokoro_source_manifest() {
    local root="$1"
    if [ -f "$root/kokoro-package.yaml" ]; then
        printf '%s\n' "$root/kokoro-package.yaml"
    else
        printf '%s\n' "$root/package.yaml"
    fi
}

kokoro_claude_home() {
    kokoro_realpath "${KOKORO_CLAUDE_HOME:-$HOME/.claude}"
}

kokoro_package_home() {
    local claude_home="$1"
    kokoro_realpath "${KOKORO_PACKAGE_HOME:-$claude_home/kokoro}"
}

kokoro_codex_home() {
    kokoro_realpath "${KOKORO_CODEX_HOME:-${CODEX_HOME:-$HOME/.codex}}"
}

kokoro_config_home() {
    kokoro_realpath "${KOKORO_CONFIG_HOME:-${XDG_CONFIG_HOME:-$HOME/.config}/kokoro}"
}

kokoro_meta_ads_env_file() {
    local config_home="$1"
    kokoro_realpath "${KOKORO_META_ADS_ENV_FILE:-$config_home/meta-ads.env}"
}

kokoro_display_path() {
    local path="$1"
    case "$path" in
        "$HOME"/*) printf '~/%s\n' "${path#"$HOME"/}" ;;
        *) printf '%s\n' "$path" ;;
    esac
}

kokoro_copy_dir() {
    local src="$1"
    local dst="$2"

    if [ ! -d "$src" ]; then
        echo "Kokoro setup error: missing source directory: $src" >&2
        exit 2
    fi

    rm -rf "$dst"
    mkdir -p "$dst"
    cp -R "$src/." "$dst/"
}

kokoro_same_path() {
    [ "$(kokoro_realpath "$1")" = "$(kokoro_realpath "$2")" ]
}

kokoro_forbidden_prefix() {
    printf 'rai'
}

kokoro_count_forbidden_named_paths() {
    local root="$1"
    local prefix
    prefix="$(kokoro_forbidden_prefix)"

    if [ ! -e "$root" ]; then
        printf '0\n'
        return
    fi

    find "$root" -name "$prefix-*" -print 2>/dev/null | wc -l | tr -d ' '
}
