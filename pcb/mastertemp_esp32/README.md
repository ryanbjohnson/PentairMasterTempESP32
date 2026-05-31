# MasterTemp ESP32 KiCad Scaffold

This folder is the KiCad project area for the MasterTemp 125 ESP32 interface board.

The current files are a scaffold, not a completed schematic or board layout. The design intent and safety constraints live in:

- `../../MasterTemp_ESP32_Interface_Preliminary_Design.md`
- `../requirements/mastertemp_esp32_requirements.yaml`

## Recommended workflow

1. Open `mastertemp_esp32.kicad_pro` in KiCad.
2. Immediately save the project from KiCad once, so your installed KiCad version normalizes the project metadata.
3. Work sheet by sheet, starting with `sheets/power_24vac.kicad_sch`.
4. After each sheet-level change, run ERC.
5. After placement/routing changes, run DRC.
6. Keep all project-local symbols in `libraries/symbols/mastertemp_esp32.kicad_sym`.
7. Keep all project-local footprints in `libraries/footprints/mastertemp_esp32.pretty`.

## Safety notes

- This project is an operating-control interface only.
- Do not add any ESP32-controlled gas-valve output.
- Do not route line voltage on this PCB.
- Preserve the OEM ignition control module and its sequencing.
- The heat-request output must remain dual normally-open relay contacts in series unless a qualified safety review approves another architecture.

## Folder map

- `sheets/`: hierarchical schematic sheets.
- `libraries/`: project-local symbols and footprints.
- `rules/`: layout constraints and DRC notes.
- `docs/`: design workflow notes, pin maps, and review records.
