# Roadmap

This roadmap is planning guidance, not a promise of dates.

## Phase 1: Public Project Hygiene

- Root README and contributor documentation.
- Issue and pull-request templates.
- Safety/security reporting process.
- License decision.

## Phase 2: Complete First-Pass Schematic

- Finish `thermistor_sfs` capture.
- Finish `ui_remote` capture.
- Replace review stubs with documented circuits where field assumptions are closed.
- Maintain zero ERC violations.

## Phase 3: PCB Synchronization And Layout

- Synchronize footprints and netlist to the captured schematic.
- Resolve schematic/PCB parity findings.
- Route safety-critical heat-request and power nets.
- Preserve ESP32 antenna keepout and analog quiet zones.
- Reduce DRC findings to zero unreviewed violations.

## Phase 4: Verification Package

- Complete field input verification.
- Generate schematic PDF, plots, Gerbers, drill files, BOM, and placement outputs.
- Write bench-test and safety-review records.
- Run FMEA for relay, watchdog, brownout, sensor, optocoupler, firmware, and miswire faults.

## Phase 5: Review Before Any Live-Heater Work

- Qualified technician review.
- Controls/electrical safety review.
- Applicable standards review.
- Explicit project-owner approval for any live-heater test.
