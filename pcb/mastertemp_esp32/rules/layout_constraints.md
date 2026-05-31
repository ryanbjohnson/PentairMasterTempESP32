# Layout Constraints

These are human-readable constraints for the first KiCad layout pass. Convert them into KiCad board setup rules/custom DRC once the exact KiCad version is selected.

## Zones

- Zone A: 24 VAC input, fuse, MOV/TVS, bridge, bulk capacitor.
- Zone B: VRAW buck converter and hot switching loop.
- Zone C: ESP32, watchdog, ADC, I2C, logic.
- Zone D: relay contacts and ICM connector.
- Zone E: remote/UI field wiring.

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
