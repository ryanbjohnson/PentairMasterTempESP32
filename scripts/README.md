# KiCad Scripts

These scripts assume `kicad-cli` is available.

On Windows, install KiCad natively and add its `bin` directory to PATH, or use the VS Code dev container for headless checks.

Typical commands:

```powershell
.\scripts\kicad-check.ps1
.\scripts\kicad-export.ps1
.\scripts\open-kicad-project.ps1
```

Inside the dev container:

```bash
./scripts/kicad-check.sh
./scripts/kicad-export.sh
```

The dev container is useful for repeatable ERC/DRC/export automation. It is not the preferred way to run the KiCad GUI on Windows.
