#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_HOME="${KOKORO_CONFIG_HOME:-${XDG_CONFIG_HOME:-$HOME/.config}/kokoro}"
ENV_FILE="${KOKORO_META_ADS_ENV_FILE:-$CONFIG_HOME/meta-ads.env}"

if ! command -v uv >/dev/null 2>&1; then
    echo "Meta Ads connector requires uv: https://docs.astral.sh/uv/" >&2
    exit 2
fi

exec uv run --project "$SCRIPT_DIR" kokoro-meta-ads-launch --env-file "$ENV_FILE"
