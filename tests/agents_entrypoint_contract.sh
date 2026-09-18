#!/usr/bin/env bash
#
# Contract test for the .agents/skills/kokoro entrypoint — issue #37.
#
# Bug: an installer that copies only .agents/skills/kokoro/SKILL.md leaves a
# router that cannot resolve identity, commands or knowledge, and that never
# names the supported install command.
#
# This test fails on the pre-fix router and passes on the corrected one.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$REPO_ROOT/.agents/skills/kokoro"
ROUTER="$SKILL_DIR/SKILL.md"
PREFLIGHT="$SKILL_DIR/preflight.sh"
README="$REPO_ROOT/README.md"
PORTABLE_DOC="$REPO_ROOT/docs/releases/e49-portable-install.md"
SUPPORTED_CMD="install/install.sh"

failures=0

fail() { printf 'FAIL: %s\n' "$*" >&2; failures=$((failures + 1)); }
pass() { printf 'ok:   %s\n' "$*"; }

rel() { printf '%s' "${1#"$REPO_ROOT"/}"; }

contains() { # file literal label
    local file="$1" literal="$2" label="$3"
    if [ -f "$file" ] && grep -qF -- "$literal" "$file"; then
        pass "$label"
    else
        fail "$label — falta '$literal' en $(rel "$file")"
    fi
}

echo "=== 1. contrato estático del router ==="
contains "$ROUTER" "KOKORO_HOME" "router respeta KOKORO_HOME"
contains "$ROUTER" "~/.claude/kokoro" "router conoce el package home instalado"
contains "$ROUTER" "IDENTITY_kokoro.md" "router verifica la identidad del paquete"
contains "$ROUTER" "preflight.sh" "router invoca la guarda de preflight"
contains "$ROUTER" "$SUPPORTED_CMD" "router nombra el comando soportado"
contains "$ROUTER" "not a valid installation" "router declara inválida la copia aislada"

echo
echo "=== 2. guarda de preflight (HOME aislado) ==="
if [ ! -f "$PREFLIGHT" ]; then
    fail "falta la guarda ejecutable $(rel "$PREFLIGHT")"
else
    work="$(mktemp -d)"
    trap 'rm -rf "$work"' EXIT

    # --- Caso A: copia aislada, sin paquete ni checkout ---------------------
    isolated_home="$work/home-a"
    mkdir -p "$isolated_home" "$work/skills/kokoro"
    cp "$ROUTER" "$work/skills/kokoro/SKILL.md"
    cp "$PREFLIGHT" "$work/skills/kokoro/preflight.sh"
    chmod +x "$work/skills/kokoro/preflight.sh"

    out_a="$(HOME="$isolated_home" KOKORO_HOME= KOKORO_PACKAGE_HOME= \
        "$work/skills/kokoro/preflight.sh" 2>&1)"
    rc_a=$?

    if [ "$rc_a" -eq 1 ]; then
        pass "copia aislada → sale 1"
    else
        fail "copia aislada → se esperaba exit 1, se obtuvo $rc_a"
    fi
    if printf '%s' "$out_a" | grep -qF -- "$SUPPORTED_CMD"; then
        pass "copia aislada → el mensaje nombra $SUPPORTED_CMD"
    else
        fail "copia aislada → el mensaje no nombra $SUPPORTED_CMD"
    fi

    # --- Caso B: KOKORO_HOME apunta a un paquete válido ---------------------
    fake_pkg="$work/pkg-b"
    mkdir -p "$fake_pkg"
    : > "$fake_pkg/IDENTITY_kokoro.md"

    out_b="$(HOME="$isolated_home" KOKORO_HOME="$fake_pkg" \
        "$work/skills/kokoro/preflight.sh" 2>&1)"
    rc_b=$?

    if [ "$rc_b" -eq 0 ]; then
        pass "KOKORO_HOME válido → sale 0"
    else
        fail "KOKORO_HOME válido → se esperaba exit 0, se obtuvo $rc_b"
    fi
    if printf '%s' "$out_b" | grep -qF -- "$fake_pkg"; then
        pass "KOKORO_HOME válido → imprime la raíz resuelta"
    else
        fail "KOKORO_HOME válido → no imprime la raíz resuelta"
    fi

    # --- Caso C: layout instalado en el HOME --------------------------------
    home_c="$work/home-c"
    mkdir -p "$home_c/.claude/kokoro"
    : > "$home_c/.claude/kokoro/IDENTITY_kokoro.md"

    out_c="$(HOME="$home_c" KOKORO_HOME= KOKORO_PACKAGE_HOME= \
        "$work/skills/kokoro/preflight.sh" 2>&1)"
    rc_c=$?

    if [ "$rc_c" -eq 0 ]; then
        pass "paquete en ~/.claude/kokoro → sale 0"
    else
        fail "paquete en ~/.claude/kokoro → se esperaba exit 0, se obtuvo $rc_c"
    fi

    # --- Caso D: checkout contenedor (el propio repo) -----------------------
    out_d="$(HOME="$isolated_home" KOKORO_HOME= KOKORO_PACKAGE_HOME= \
        "$PREFLIGHT" 2>&1)"
    rc_d=$?

    if [ "$rc_d" -eq 0 ]; then
        pass "checkout contenedor → sale 0"
    else
        fail "checkout contenedor → se esperaba exit 0, se obtuvo $rc_d"
    fi
    if printf '%s' "$out_d" | grep -qF -- "$REPO_ROOT"; then
        pass "checkout contenedor → imprime la raíz del repo"
    else
        fail "checkout contenedor → no imprime la raíz del repo"
    fi
fi

echo
echo "=== 3. docs enrutan a la vía auditada ==="
contains "$README" "instalador de skills" "README advierte sobre instaladores de skills"
contains "$README" "$SUPPORTED_CMD" "README nombra el comando soportado"
contains "$PORTABLE_DOC" "instalador de skills" "guía portable advierte sobre instaladores de skills"
contains "$PORTABLE_DOC" "$SUPPORTED_CMD" "guía portable nombra el comando soportado"

echo
if [ "$failures" -gt 0 ]; then
    printf '%d comprobación(es) fallaron.\n' "$failures" >&2
    exit 1
fi

echo "Contrato del entrypoint .agents/skills/kokoro OK."
