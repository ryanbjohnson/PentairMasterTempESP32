# MasterTemp 125 Rev C Manual Review

Source file: `../../../MasterTemp 125 Installation and Users Guide - English - Rev C.pdf`

PDF metadata:

- Title: `MasterTemp 125 Heater Manual (English)`
- Revision shown in footer: Rev. C, 3/2019
- Pages: 56
- PDF modified date: 2021-05-11

## Electrical Pages Reviewed

- Page 28: electrical connections and line-voltage warnings.
- Page 29: Fireman's Switch and remote control connection instructions.
- Page 30, Figure 24: heater wiring diagram, 3-wire system.
- Page 31, Figure 25: heater electrical schematic ladder diagram.

## Manual-Derived Design Facts

- The heater has line-voltage `120/240 VAC` wiring in the junction box, but this project PCB must not carry line voltage.
- The manual warns that touching any `24 VAC` control wire, including the Fireman's Switch jumper, to a `120/240 V` terminal can destroy the control board.
- The Fireman's Switch/timer connection is a `24 VAC` control-board circuit and the external contact should be rated for `24 VAC at 0.5 A`.
- The manual calls for `18 AWG` wire with insulation rated for at least `105 C` temperature rise for the Fireman's Switch wiring.
- The operating-control top terminal order shown in Figure 24 is `VAL`, `TH`, `IND`, `GND`, `24VAC`, plus a separate `24VAC` / `FS` Fireman's Switch block.
- The operating-control left safety stack shown in Figure 24 is `PS`, `HLS`, `ES1`, `AFS`, `AGS`, `SFS`, `GAS`.
- The operating-control has a separate thermistor connector pair near the top-right of the board.
- The operating-control has a right-side `J6` membrane-pad connector.
- The three-wire external-control interface shown in Figure 24 is `Spa Line`, `Common Line`, `Pool Line`.
- The ignition-control module terminal row shown in Figure 24/Figure 25 includes `S1/240`, `S1/120`, `L1`, `L2`, `S2`, `TH`, `IND`, `VAL`, and `GND`.
- The ladder diagram shows the OEM ignition-control module owns ignition, blower, gas-valve, `TH`, `IND`, `VAL`, and `GND` sequencing.

## Project Updates From This Review

- Renamed the generic draft `J2 ICM` interface to a manual-aligned `J2 OPERATING CONTROL 7P` envelope.
- Split the previous combined safety/sensor connector concept into manual-aligned envelopes:
  - `J3 SAFETY STACK 7P`
  - `J4 THERMISTOR 2P`
  - `J5 EXT CTRL 3P`
  - `J6 MEMBRANE / UI`
- Added a PCB reference envelope for the OEM ignition-control module terminal row.
- Kept `VAL` and `GAS` marked monitor-only; no board output should drive the gas valve.

## Open Verification Items

- The PDF diagrams are authoritative for the Rev C manual, but the installed heater revision and harness must still be inspected before schematic release.
- Wire colors from the PDF should be treated as service hints, not a substitute for continuity verification on the installed unit.
- The exact J6 membrane-pad pin mapping still needs harness-level verification.
