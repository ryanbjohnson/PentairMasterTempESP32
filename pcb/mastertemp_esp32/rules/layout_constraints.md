# Layout Constraints

These are human-readable constraints for the first KiCad layout pass. Convert them into KiCad board setup rules/custom DRC once the exact KiCad version is selected.

## Zones

- Zone A: 24 VAC input, fuse, MOV/TVS, bridge, bulk capacitor.
- Zone B: VRAW buck converter and hot switching loop.
- Zone C: ESP32, watchdog, ADC, I2C, logic.
- Zone D: relay contacts and ICM connector.
- Zone E: remote/UI field wiring.

## First-pass floorplan

- Board outline target: keep the existing 160 mm x 100 mm scaffold until the real enclosure and heater mounting envelope are measured.
- Left edge: place all heater/field connectors so harnesses enter from one service side.
- Top-left: place `J1_POWER`, fuse/PTC, MOV, bridge, TVS, and VRAW bulk capacitor in Zone A.
- Center-left: place `U1` 24 VAC-derived 5 V buck and its inductor/diode/input capacitors in Zone B, with the switch loop compact and away from sensor traces.
- Right side: place ESP32 module in Zone C with antenna pointed toward the nearest board edge and a no-copper/no-component keepout under and in front of the antenna.
- Bottom-left: place `J2_ICM`, `K1`, and `K2` in Zone D with the relay-contact path short, wide, and visibly separated from logic copper.
- Bottom/right edge: place `J3_SAFETY_SENSORS`, `J4_REMOTE`, and `J5_UI` in Zone E, grouped by harness function rather than by schematic page.
- Center/right: place ADC, thermistor/SFS protection, comparators, watchdog, reset supervisor, and I/O expander close to the ESP32 but outside the antenna keepout.
- Keep optocouplers straddling the field/logic boundary, with field-side pins facing connectors and logic-side pins facing ESP32/MCP23017.
- Reserve room for isolation slots between relay contacts/AC sense field wiring and SELV logic where footprints permit.

## Required separations

- No line voltage on PCB.
- Keep field wiring and logic separated by practical clearance and silkscreen boundaries.
- Add isolation slots under/near optocouplers and relay contact regions where they improve tolerance to contamination or miswire.
- Keep ESP32 antenna clear of copper, connectors, relays, transformer wiring, and enclosure metal.
- Route thermistor and SFS traces away from relay coils, buck switch nodes, AC sense inputs, and connector ESD current paths.

## Required labels

- NO LINE VOLTAGE ON CONTROL TERMINALS
- 24 VAC CLASS II CONTROL POWER ONLY
- GAS VALVE MONITOR ONLY - DO NOT DRIVE
- INSTALL/SERVICE BY QUALIFIED TECHNICIAN
- VERIFY WIRING AGAINST HEATER MANUAL BEFORE POWER

## Open mechanical inputs

- Exact enclosure internal dimensions, lid clearance, standoff locations, and cable gland/harness-entry direction.
- Exact heater control compartment mounting method and whether this board is an interposer, replacement panel board, or bench-test module.
- Connector family, pitch, wire gauge, pluggable/keyed requirements, and service-loop clearance.
- Required conformal coating, drainage/orientation constraints, and minimum contamination class for creepage decisions.
