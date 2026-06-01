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

## Completion checklist

Use this as the live gate list for moving from scaffold to a reviewable PCB package. Keep each checkbox honest: complete means captured, checked, and reviewed, not merely started.

### Project setup

- [x] KiCad project scaffold exists with root schematic, child sheets, PCB file, local library tables, and scripts.
- [x] Four-layer board scaffold exists with preliminary 160 mm x 100 mm outline and functional placement zones.
- [x] PCB floorplan v0 exists with connector, relay, power, ESP32, analog, and test-pad placement envelopes.
- [x] Local MasterTemp 125 Rev C PDF electrical pages were reviewed and summarized in `docs/mastertemp125_rev_c_manual_review.md`.
- [x] Candidate sourced BOM and first-pass footprint placement exist for control-board circuitry.
- [x] PCB-side draft nets and first-pass relay contact-chain routing are applied and documented.
- [x] Headless KiCad `ERC` and `DRC` automation runs in the dev container.
- [x] Repository-level scaffold tests exist under `tests/`.
- [ ] KiCad project metadata has been opened and normalized once in the target GUI KiCad version.
- [ ] Generated `reports/` and `fab/` outputs are regenerated from the final release candidate.

### Inputs to close before electrical release

- [ ] Exact MasterTemp 125 model revision, serial/date range, and connected/non-connected variant are recorded.
- [x] Rev C manual connector groups are reflected in draft requirements and floorplan.
- [ ] Heater harness pinout is verified from the installed unit and matching manual revision.
- [ ] 24 VAC transformer no-load and loaded voltages are measured.
- [ ] Water thermistor resistance curve is confirmed.
- [ ] Stack flue sensor electrical type and valid/fault ranges are confirmed.
- [ ] Enclosure, mounting holes, standoff height, cable-entry direction, and service clearances are selected.
- [ ] Certification/review path is chosen, including current applicable pool-heater and automatic-control standards.

### Schematic capture

- [ ] `power_24vac`: connector, fuse/PTC, MOV/TVS, bridge, VRAW bulk, 5 V supply, 3.3 V supply, power-good/brownout.
- [ ] `icm_interface`: manual-aligned operating-control connector, dual series normally-open relay contacts, coil drivers, flyback, AC opto sense, TH feedback, ICM terminal reference.
- [ ] `esp32_supervisor`: ESP32 module, programming header, watchdog, reset supervisor, I2C, relay-enable logic.
- [ ] `safety_inputs`: Fireman's Switch, PS, HLS, ES1, AGS static chain, AFS dynamic monitor, dry-contact isolated sense.
- [ ] `thermistor_sfs`: thermistor divider, SFS measurement path, ADC, protection, hardware window comparators.
- [ ] `ui_remote`: Pool/Common/Spa external-control dry-contact sense only; keypad/display/buzzer/status LED design remains out of scope.
- [ ] ERC has zero unreviewed violations after each sheet is captured.
- [ ] All symbols have footprints assigned or documented as no-fit/test-only.

### Safety review

- [ ] OEM ignition control module remains responsible for ignition, flame proving, and gas-valve sequencing.
- [ ] No ESP32 or board output can directly energize the gas valve.
- [ ] No line-voltage nets, connectors, labels, or routing exist on this PCB.
- [ ] Two normally-open relay contacts are in series in the `TH` heat-request path.
- [ ] Relay drive drops out on ESP32 reset, watchdog timeout, brownout, firmware fault, OTA, static safety open, invalid sensor, and relay feedback fault.
- [ ] AFS is treated as a dynamic airflow-proving input, not as a static pre-fire interlock.
- [ ] Preliminary FMEA covers welded relay, optocoupler failure, stuck ADC, brownout oscillation, firmware deadlock, and miswire cases.

### PCB layout

- [x] First-pass placement envelopes follow the zone plan in `rules/layout_constraints.md`.
- [x] Draft connector envelopes follow Rev C Figure 24 operating-control groups.
- [x] Candidate footprints are placed according to first-pass sourced part numbers.
- [x] Critical relay contact-chain PCB nets are named and first-pass routed.
- [ ] Footprints are synchronized to final schematic symbols and netlist.
- [ ] ESP32 antenna keepout has no copper, components, or nearby metal-obstructing placement.
- [ ] Relay contact and 24 VAC control paths use assigned net classes and visible separation from logic.
- [ ] Field-side optocoupler pins face connectors and logic-side pins face MCU/expander circuitry.
- [ ] Thermistor/SFS analog traces avoid relay coils, AC sense, ESD discharge paths, and buck switch nodes.
- [ ] Test pads exist for `VRAW`, `+5V`, `+3V3`, watchdog, safety chain, relay coils, TH feedback, and VAL sense.
- [ ] Silkscreen warnings are present and readable.
- [ ] DRC has zero unreviewed violations and schematic parity passes. Current draft has only silkscreen DRC warnings plus expected unrouted/parity items from incomplete schematic capture.

### Fabrication and validation

- [ ] Schematic PDF, PCB plots, Gerbers, drill files, BOM, and placement outputs are generated.
- [ ] Bench test procedure is executed with an isolated 24 VAC transformer.
- [ ] Every required heat-request drop-out case is tested and recorded.
- [ ] Relay feedback/welded-contact detection is tested.
- [ ] `VAL` sense-only behavior is tested.
- [ ] 24-hour relay/sensor soak test is completed.
- [ ] Qualified technician review is complete before any live-heater connection.
