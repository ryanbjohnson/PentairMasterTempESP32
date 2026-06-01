# Draft PCB Circuit Design Pass

Date: 2026-05-31

Status: PCB-side draft routing and net assignment. This records the control-board circuit intent now applied to the board file by `scripts/apply-draft-pcb-nets.py`. Full release still requires symbol-level schematic capture and schematic-to-PCB synchronization.

## Scope

This pass covers the control board only:

- 24 VAC operating-control interface.
- Dual normally-open heat-request relay contacts in series.
- Sense-only diagnostic nets for `VAL`, `IND`, `TH`, `24VAC`, and `GAS`.
- External Pool/Common/Spa dry-contact input naming.
- Thermistor and SFS signal naming.
- ESP32, supervisor, ADC, I/O expander, relay-driver, and test-point net naming.

The keypad, membrane pad electronics, display, buzzer, and status LED remain out of scope.

## Applied Critical Contact Chain

| Function | PCB net | Applied pads |
| --- | --- | --- |
| ICM 24 VAC source into first relay contact | `ICM_24VAC_SOURCE` | `J2.5`, `K1.2` |
| Relay-to-relay series link | `HEAT_CHAIN_K1_K2` | `K1.3`, `K2.2` |
| Heat request output back to TH | `TH_HEAT_REQUEST_OUT` | `K2.3`, `J2.2` |

The first-pass board route connects the relay contact chain with 0.60 mm copper. `ICM_24VAC_SOURCE` and `HEAT_CHAIN_K1_K2` are routed on `F.Cu`; `TH_HEAT_REQUEST_OUT` is routed on `B.Cu` to avoid a same-layer crossing.

## Applied Relay Driver Nets

| Function | PCB net | Applied pads |
| --- | --- | --- |
| K1 coil low-side node | `K1_COIL_LOW` | `K1.1`, `Q1.3`, `TP6.1` |
| K2 coil low-side node | `K2_COIL_LOW` | `K2.1`, `Q2.3`, `TP7.1` |
| Relay coil supply | `+5V_RELAY` | `K1.5`, `K2.5` |
| K1 gate command | `RELAY_K1_GATE` | `Q1.1` |
| K2 gate command | `RELAY_K2_GATE` | `Q2.1` |
| Driver source reference | `GND` | `Q1.2`, `Q2.2` |

These nets are named on pads but not fully routed until the ESP32/supervisor schematic is captured and relay-drive logic is reviewed.

## Applied Connector Nets

| Connector | Pad order |
| --- | --- |
| `J1` 24 VAC input | `24VAC_A`, `24VAC_B`, `EARTH_SHIELD_REF` |
| `J2` operating control | `VAL_SENSE_AC`, `TH_HEAT_REQUEST_OUT`, `IND_SENSE_AC`, `ICM_GND_REF`, `ICM_24VAC_SOURCE`, `FIREMAN_24VAC`, `FIREMAN_SWITCH_RETURN` |
| `J3` safety stack | `PS_SWITCH`, `HLS_SWITCH`, `ES1_SWITCH`, `AFS_SWITCH_DYNAMIC`, `AGS_SWITCH`, `SFS_INPUT`, `GAS_MONITOR_ONLY` |
| `J4` thermistor | `THERMISTOR_A`, `THERMISTOR_B` |
| `J5` external control | `SPA_LINE`, `COMMON_LINE`, `POOL_LINE` |

## Verification State

- ERC report: zero violations because the schematic sheets are still mostly notes and hierarchy.
- PCB DRC report: no shorts, clearance errors, courtyard errors, keepout errors, or drill errors after this pass.
- Remaining DRC findings are silkscreen warnings and expected unrouted items.
- Schematic parity is expected to fail until real KiCad symbols and generated netlist replace the PCB-side draft net assignment.

## Next Real Electrical Work

- Convert each text design block into symbols, hierarchical pins, labels, and footprints.
- Add missing passives: optocoupler input resistors, pullups, gate resistors, pulldowns, flyback diodes, buck feedback/compensation/filter parts, ADC protection, and thermistor/SFS dividers.
- Run KiCad update-PCB-from-schematic and replace this PCB-side draft net application with schematic-derived nets.
- Complete routing, zones, silkscreen cleanup, fabrication outputs, and qualified safety review.
