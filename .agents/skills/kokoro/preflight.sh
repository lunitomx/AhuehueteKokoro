#!/usr/bin/env bash
#
# Kokoro entrypoint guard — issue #37.
#
# Resolves the Kokoro package root for the .agents/skills/kokoro router and
# fails loudly when the skill was installed without the package.
#
# Exit 0: the first line of stdout is the resolved package root.
# Exit 1: no package resolved; prints the supported install command.

set -uo pipefail

SUPPORTED_INSTALL='git clone https://github.com/lunitomx/AhuehueteKokoro.git && cd AhuehueteKokoro && ./install/install.sh'

has_package() {
    [ -n "${1:-}" ] && [ -f "$1/IDENTITY_kokoro.md" ]
}

resolve() {
    local candidate

    candidate="${KOKORO_HOME:-}"
    if has_package "$candidate"; then printf '%s\n' "$candidate"; return 0; fi

    candidate="${KOKORO_PACKAGE_HOME:-}"
    if has_package "$candidate"; then printf '%s\n' "$candidate"; return 0; fi

    candidate="${KOKORO_CLAUDE_HOME:-$HOME/.claude}/kokoro"
    if has_package "$candidate"; then printf '%s\n' "$candidate"; return 0; fi

    # Checkout case: walk up from this script looking for IDENTITY_kokoro.md.
    local dir
    dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/IDENTITY_kokoro.md" ]; then printf '%s\n' "$dir"; return 0; fi
        dir="$(dirname "$dir")"
    done
    if [ -f "/IDENTITY_kokoro.md" ]; then printf '%s\n' "/"; return 0; fi

    return 1
}

if root="$(resolve)"; then
    printf '%s\n' "$root"
    exit 0
fi

cat >&2 <<EOF
Kokoro entrypoint error: no Kokoro package could be resolved.

This SKILL.md was installed without the Kokoro package, so the router cannot
read identity, commands or knowledge. Copying this file alone is not a valid
installation.

Install Kokoro with the audited installer:

  $SUPPORTED_INSTALL

Then re-run this guard: it must print the package root and exit 0.
EOF
exit 1
