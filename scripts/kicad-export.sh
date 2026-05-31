#!/usr/bin/env bash
set -euo pipefail

PROJECT_BASE="${1:-pcb/mastertemp_esp32/mastertemp_esp32}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v kicad-cli >/dev/null 2>&1; then
  echo "kicad-cli was not found on PATH. Install KiCad or use the VS Code dev container." >&2
  exit 127
fi

mkdir -p fab/gerbers fab/drill fab/pdf fab/step

echo "Exporting schematic PDF..."
kicad-cli sch export pdf "${PROJECT_BASE}.kicad_sch" --output fab/pdf/mastertemp_esp32_schematic.pdf

echo "Exporting Gerbers..."
kicad-cli pcb export gerbers "${PROJECT_BASE}.kicad_pcb" --output fab/gerbers

echo "Exporting drill files..."
kicad-cli pcb export drill "${PROJECT_BASE}.kicad_pcb" --output fab/drill

echo "Exporting STEP model..."
kicad-cli pcb export step "${PROJECT_BASE}.kicad_pcb" --output fab/step/mastertemp_esp32.step

echo "Fabrication outputs written under fab/"
