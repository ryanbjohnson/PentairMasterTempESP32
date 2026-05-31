# Design Start Review

Date: 2026-05-31

## Current Project State

This repository is a KiCad scaffold for a Pentair MasterTemp 125 ESP32 operating-control interface board. The system-level design intent is already well defined in `MasterTemp_ESP32_Interface_Preliminary_Design.md` and mirrored in `pcb/requirements/mastertemp_esp32_requirements.yaml`.

The KiCad project is not yet electrically captured. The root schematic contains six hierarchical sheets, but each child sheet currently contains only TODO notes. The project-local symbol library and footprint library are empty. The PCB file contains a 160 mm x 100 mm outline, four copper layers, net classes, and silkscreen zone labels, but no footprints, nets, or routed copper.

## Baseline Findings

- Safety boundary is clear: no line voltage, no direct gas-valve drive, preserve the OEM ignition control module, and switch only the 24 VAC `TH` call-for-heat path through two normally-open relay contacts in series.
- Requirements and documentation agree on the main sheet structure: power, ESP32/supervisor, ICM interface, safety inputs, thermistor/SFS, and UI/remote.
- Net classes already exist in the KiCad project for default logic, 24 VAC control, relay-contact 24 VAC, rectified VRAW, and sensor ADC routing.
- The board stackup is intended to be four-layer: top signal, inner ground, inner power, bottom signal.
- The current scripts expect newer KiCad CLI functionality. The installed CLI in this environment is KiCad 7.0.11, whose `sch` command does not support `erc`, so the existing check script cannot run here as written.

## Design Assumptions For First Pass

- Treat the board as an interposer/interface until the exact heater revision and harness pinout are confirmed.
- Keep the first board outline at the scaffold size of 160 mm x 100 mm while schematic capture proceeds.
- Use keyed pluggable field connectors for all heater-facing wiring, with grouped harness entry along the left/bottom service edges.
- Use standard KiCad symbols and footprints wherever possible. Add project-local symbols only for heater-specific connectors, labels, review blocks, or parts missing from the installed libraries.
- Keep the 24 VAC-derived supply onboard for the first electrical pass, but preserve the option to replace it with a certified DC module if EMC, thermal, or certification risk becomes dominant.

## First Schematic Pass

Capture in this order:

1. `power_24vac`: `J1_POWER`, input fuse/PTC, MOV/TVS, bridge, VRAW bulk capacitance, 5 V regulator placeholder, 3.3 V regulator placeholder, power-good/brownout outputs.
2. `icm_interface`: `J2_ICM`, dual series relay contacts, relay coil drivers, flyback diodes, AC optocoupler sense channels, and TH output feedback.
3. `esp32_supervisor`: ESP32 module, programming header, watchdog, reset supervisor, I2C pullups, relay-enable gate inputs, and bootstrap-safe relay command pins.
4. `safety_inputs`: dry-contact optocoupler sense channels, Fireman's Switch, static safety chain output, and a clearly separate dynamic AFS monitor.
5. `thermistor_sfs`: thermistor divider, SFS measurement placeholder, ADS1115, filter/protection, and hardware range comparator outputs.
6. `ui_remote`: remote Pool/Common/Spa dry-contact sense, local buttons, display header, buzzer, and status LED output.

## First PCB Floorplan

- Zone A, top-left: 24 VAC input, protection, rectifier, and VRAW bulk capacitor.
- Zone B, center-left: high-voltage buck converter and its compact switching loop.
- Zone C, right side: ESP32, watchdog, reset supervisor, ADC, I/O expander, display/UI logic, and I2C.
- Zone D, bottom-left: ICM connector and the two series heat-request relay contacts.
- Zone E, bottom/right edge: safety, sensor, remote, and UI connectors.
- Optocouplers sit across the field/logic boundary, with field pins toward connectors and logic pins toward the ESP32/MCP23017.
- Thermistor/SFS analog routing stays away from relay coils, buck switch node, AC optocouplers, and ESD return paths.

## Required Inputs Before Release

- Exact MasterTemp 125 revision and photographed/verified harness pinout.
- No-load and loaded voltage measurements from the heater 24 VAC transformer.
- Confirmed water thermistor curve and stack-flue-sensor electrical type.
- Enclosure choice, mounting holes, cable entry direction, standoff heights, and service clearance.
- Professional safety review/FMEA before connecting to a live heater.
