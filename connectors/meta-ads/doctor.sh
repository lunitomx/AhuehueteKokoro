#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_HOME="${KOKORO_CONFIG_HOME:-${XDG_CONFIG_HOME:-$HOME/.config}/kokoro}"
ENV_FILE="${KOKORO_META_ADS_ENV_FILE:-$CONFIG_HOME/meta-ads.env}"

exec python3 "$SCRIPT_DIR/src/kokoro_meta_ads/doctor.py" \
    --env-file "$ENV_FILE" \
    --json
