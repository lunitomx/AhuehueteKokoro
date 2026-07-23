"""Load local Meta credentials as data, then start the MCP server."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from kokoro_meta_ads.doctor import REQUIRED_ENVIRONMENT, merged_environment


def main() -> None:
    """Launch the server after a safe, allowlisted credential-file merge."""
    parser = argparse.ArgumentParser(prog="kokoro-meta-ads-launch")
    parser.add_argument("--env-file", type=Path, required=True)
    args = parser.parse_args()

    environment = merged_environment(os.environ, args.env_file)
    for key in REQUIRED_ENVIRONMENT:
        if key in environment:
            os.environ[key] = environment[key]

    from kokoro_meta_ads.server import main as server_main

    server_main()


if __name__ == "__main__":
    main()
