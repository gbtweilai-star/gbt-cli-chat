#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m gbt_cli_chat info
PYTHONPATH=src python -m gbt_cli_chat check --payload '{}'
PYTHONPATH=src python -m gbt_cli_chat run   --payload '{}'
