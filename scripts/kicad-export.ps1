param(
    [string]$ProjectBase = "pcb/mastertemp_esp32/mastertemp_esp32"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not (Get-Command kicad-cli -ErrorAction SilentlyContinue)) {
    throw "kicad-cli was not found on PATH. Install KiCad natively or open the VS Code dev container."
}

New-Item -ItemType Directory -Force -Path "fab/gerbers", "fab/drill", "fab/pdf", "fab/step" | Out-Null

$Schematic = "$ProjectBase.kicad_sch"
$Board = "$ProjectBase.kicad_pcb"

Write-Host "Exporting schematic PDF..."
kicad-cli sch export pdf $Schematic --output "fab/pdf/mastertemp_esp32_schematic.pdf"

Write-Host "Exporting Gerbers..."
kicad-cli pcb export gerbers $Board --output "fab/gerbers"

Write-Host "Exporting drill files..."
kicad-cli pcb export drill $Board --output "fab/drill"

Write-Host "Exporting STEP model..."
kicad-cli pcb export step $Board --output "fab/step/mastertemp_esp32.step"

Write-Host "Fabrication outputs written under fab/"
