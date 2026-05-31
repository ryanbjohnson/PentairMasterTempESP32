$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Project = Resolve-Path (Join-Path $RepoRoot "pcb/mastertemp_esp32/mastertemp_esp32.kicad_pro")

$Command = Get-Command kicad -ErrorAction SilentlyContinue
if ($Command) {
    & $Command.Source $Project
    exit $LASTEXITCODE
}

$Candidates = @(
    "C:\Program Files\KiCad\10.0\bin\kicad.exe",
    "C:\Program Files\KiCad\9.0\bin\kicad.exe",
    "C:\Program Files\KiCad\8.0\bin\kicad.exe",
    "C:\Program Files\KiCad\7.0\bin\kicad.exe"
)

foreach ($Candidate in $Candidates) {
    if (Test-Path -LiteralPath $Candidate) {
        & $Candidate $Project
        exit $LASTEXITCODE
    }
}

throw "KiCad was not found. Install KiCad natively, then open $Project."
