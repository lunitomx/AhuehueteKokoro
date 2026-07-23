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
CONFIG_HOME="$(kokoro_config_home)"
META_ADS_ENV_FILE="$(kokoro_meta_ads_env_file "$CONFIG_HOME")"
errors=0

fail() {
    echo "Kokoro verify error: $*" >&2
    errors=$((errors + 1))
}

require_file() {
    local file="$1"
    [ -f "$file" ] || fail "missing file: $file"
}

require_dir() {
    local dir="$1"
    [ -d "$dir" ] || fail "missing directory: $dir"
}

require_file "$PACKAGE_HOME/package.yaml"
require_file "$PACKAGE_HOME/IDENTITY_kokoro.md"
require_file "$PACKAGE_HOME/AGENTS.md"
require_file "$PACKAGE_HOME/CLAUDE.md"
require_dir "$PACKAGE_HOME/commands"
require_dir "$PACKAGE_HOME/knowledge"
require_file "$PACKAGE_HOME/commands/kokoro.md"
require_file "$PACKAGE_HOME/runtime/kokoro.py"
require_dir "$PACKAGE_HOME/connectors/meta-ads"
require_file "$PACKAGE_HOME/connectors/meta-ads/run.sh"
require_file "$PACKAGE_HOME/connectors/meta-ads/doctor.sh"
require_file "$PACKAGE_HOME/connectors/meta-ads/pyproject.toml"
require_file "$PACKAGE_HOME/install/privacy_scan.py"
require_file "$META_ADS_ENV_FILE"

python3 "$PACKAGE_HOME/runtime/kokoro.py" doctor >/dev/null || fail "Kokoro runtime doctor failed"
"$PACKAGE_HOME/connectors/meta-ads/doctor.sh" >/dev/null || fail "Meta Ads connector doctor failed"
if ! python3 "$PACKAGE_HOME/install/privacy_scan.py" "$PACKAGE_HOME"; then
    fail "release privacy scan failed"
fi

wrapper_count=0
if [ -d "$COMMANDS_TARGET" ]; then
    while IFS= read -r wrapper; do
        wrapper_count=$((wrapper_count + 1))
        grep -q '^kokoro_owned: true$' "$wrapper" || fail "wrapper is missing Kokoro ownership marker: $wrapper"
        grep -q '^kokoro_package_home:' "$wrapper" || fail "wrapper is missing package home: $wrapper"

        source_name="$(grep '^kokoro_source:' "$wrapper" | head -1 | sed 's/^kokoro_source: *"//; s/"$//')"
        if [ -z "$source_name" ]; then
            fail "wrapper is missing source metadata: $wrapper"
        elif [ ! -f "$PACKAGE_HOME/$source_name" ]; then
            fail "wrapper source does not exist: $PACKAGE_HOME/$source_name"
        fi
    done < <(find "$COMMANDS_TARGET" -maxdepth 1 -type f -name 'kokoro*.md' | sort)
fi

[ "$wrapper_count" -gt 0 ] || fail "no Kokoro Claude wrappers found in $COMMANDS_TARGET"

require_file "$CODEX_SKILL_DIR/SKILL.md"
if [ -f "$CODEX_SKILL_DIR/SKILL.md" ]; then
    grep -q '^kokoro_owned: true$' "$CODEX_SKILL_DIR/SKILL.md" || fail "Codex skill missing ownership marker"
    grep -q '^kokoro_package_home:' "$CODEX_SKILL_DIR/SKILL.md" || fail "Codex skill missing package home"
fi

for path in "$PACKAGE_HOME" "$COMMANDS_TARGET" "$CODEX_SKILL_DIR"; do
    count="$(kokoro_count_forbidden_named_paths "$path")"
    [ "$count" = "0" ] || fail "forbidden package path names found under $path"
done

for private_dir in .raise .rai .kokoro clients clientes private exports reports generated deliverables; do
    [ ! -e "$PACKAGE_HOME/$private_dir" ] || fail "private/runtime directory copied into package: $PACKAGE_HOME/$private_dir"
done

while IFS= read -r sensitive_file; do
    fail "sensitive or OS file copied into package: $sensitive_file"
done < <(
    find "$PACKAGE_HOME" -type f \( \
        -name '.DS_Store' -o \
        -name '*.csv' -o \
        -name '*.xls' -o \
        -name '*.xlsx' -o \
        -name '.env*' -o \
        -name 'client_secret_*.json' \
    \) -print 2>/dev/null
)

if [ "$errors" -gt 0 ]; then
    exit 1
fi

echo "Kokoro verify OK."
echo "Package root: $(kokoro_display_path "$PACKAGE_HOME")"
echo "Claude wrappers: $wrapper_count"
echo "Codex skill: $(kokoro_display_path "$CODEX_SKILL_DIR")"
echo "Meta Ads connector: optional"
