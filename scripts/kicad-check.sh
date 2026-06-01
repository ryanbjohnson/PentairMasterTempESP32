#!/usr/bin/env bash
set -euo pipefail

PROJECT_BASE="${1:-pcb/mastertemp_esp32/mastertemp_esp32}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v kicad-cli >/dev/null 2>&1; then
  echo "kicad-cli was not found on PATH. Install KiCad or use the VS Code dev container." >&2
  exit 127
fi

mkdir -p reports

echo "KiCad CLI:"
kicad-cli version

echo "Running schematic ERC..."
kicad-cli sch erc "${PROJECT_BASE}.kicad_sch" --format json --output reports/erc.json --exit-code-violations

echo "Running PCB DRC..."
kicad-cli pcb drc "${PROJECT_BASE}.kicad_pcb" --format json --output reports/drc.json

echo "Running PCB schematic parity report..."
kicad-cli pcb drc "${PROJECT_BASE}.kicad_pcb" --format json --schematic-parity --output reports/drc-parity.json

if [[ "${STRICT_KICAD_DRC:-0}" == "1" ]]; then
  echo "STRICT_KICAD_DRC=1: rerunning PCB DRC with violation exit code..."
  kicad-cli pcb drc "${PROJECT_BASE}.kicad_pcb" --format json --schematic-parity --output reports/drc-strict.json --exit-code-violations
fi

echo "Reports written to reports/erc.json, reports/drc.json, and reports/drc-parity.json"
