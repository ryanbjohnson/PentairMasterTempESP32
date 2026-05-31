param(
    [string]$ProjectBase = "pcb/mastertemp_esp32/mastertemp_esp32"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

if (-not (Get-Command kicad-cli -ErrorAction SilentlyContinue)) {
    throw "kicad-cli was not found on PATH. Install KiCad natively or open the VS Code dev container."
}

$Reports = Join-Path $RepoRoot "reports"
New-Item -ItemType Directory -Force -Path $Reports | Out-Null

$Schematic = "$ProjectBase.kicad_sch"
$Board = "$ProjectBase.kicad_pcb"

Write-Host "KiCad CLI:"
kicad-cli version

Write-Host "Running schematic ERC..."
kicad-cli sch erc $Schematic --format json --output "reports/erc.json" --exit-code-violations

Write-Host "Running PCB DRC..."
kicad-cli pcb drc $Board --format json --schematic-parity --output "reports/drc.json" --exit-code-violations

Write-Host "Reports written to reports/erc.json and reports/drc.json"
