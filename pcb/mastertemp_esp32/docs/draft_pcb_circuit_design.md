# Draft PCB Circuit Design Pass

Date: 2026-06-02

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

The first-pass board route connects the relay contact chain with 0.60 mm copper. `ICM_24VAC_SOURCE` is routed on `F.Cu`; `HEAT_CHAIN_K1_K2` and `TH_HEAT_REQUEST_OUT` are routed on `B.Cu` to avoid same-layer crossings with the relay coil and flyback routing.

## Applied Relay Driver Nets

| Function | PCB net | Applied pads |
| --- | --- | --- |
| K1 coil low-side node | `K1_COIL_LOW` | `K1.1`, `Q1.3`, `TP6.1` |
| K2 coil low-side node | `K2_COIL_LOW` | `K2.1`, `Q2.3`, `TP7.1` |
| Relay coil supply | `+5V_RELAY` | `K1.5`, `K2.5` |
| K1 gate drive placeholder | `RELAY_K1_GATE_DRIVE` | `R22.1` |
| K2 gate drive placeholder | `RELAY_K2_GATE_DRIVE` | `R23.1` |
| K1 gate command | `RELAY_K1_GATE` | `R22.2`, `Q1.1`, `R10.1` |
| K2 gate command | `RELAY_K2_GATE` | `R23.2`, `Q2.1`, `R11.1` |
| K1 gate pulldown return | `GND` | `R10.2` |
| K2 gate pulldown return | `GND` | `R11.2` |
| Driver source reference | `GND` | `Q1.2`, `Q2.2` |

The relay coil low-side traces, local `+5V_RELAY` rail between relay coil pins, K1/K2 flyback diode connections, MOSFET source grounds, first-pass relay-gate pulldowns, and first-pass relay-gate series resistors are routed. R10/R11/R22/R23 values remain TBD pending the ESP32/supervisor relay-drive review.

## Applied Low-Voltage Routing

- `VRAW` is first-pass routed from the bridge rectifier output to the local buck input capacitor, bulk reservoir capacitor, VRAW test point, U1 VIN pads, and the R28 raw-rail monitor top resistor.
- `PGND_RAW` is first-pass routed from the bridge rectifier return to the local buck input capacitor, bulk reservoir capacitor, and U1 PGND area with via-assisted local return stitching. The final high-current return shape still needs placement/layout review.
- `SW_5V` and `BST_5V` are first-pass routed through the 5 V buck switch/bootstrap loop, with the bootstrap net using a via-assisted back-layer hop to avoid the switch node.
- `+5V` is first-pass routed from the 5 V buck output/feed divider area to the 3.3 V regulator input decoupling node and TP2.
- `+3V3` is first-pass routed from the 3.3 V regulator output to its output capacitor, ADC supply, supervisor supply, ESP32 supply pad, 3.3 V test point, and the external-control Spa/Pool pullup resistor supply pads.
- `GND` now includes first-pass via-assisted routing from the ADC/local logic ground spine to the supervisor ground pins, ESP32 ground pad, relay-driver MOSFET sources, and the remote optocoupler/RC-filter ground cluster.
- `WATCHDOG_OK` is routed from the supervisor output to TP4 with a via-assisted back-layer hop around the local `+3V3` supervisor rail.
- `U6` is now schematic-owned as a local `MCP23017_SS` symbol. Its `VDD`, `VSS`, `SDA`, `SCL`, address pins, and reset pin are captured and first-pass routed; `A0`/`A1`/`A2` are tied low and `~RESET` is tied high. GPA0 is assigned to `VAL_OPTO_GPIO`, GPA1 is assigned to `TH_OPTO_GPIO`, GPA2 is assigned to `IND_OPTO_GPIO`, and GPA3 is assigned to `VAC24_OPTO_GPIO`; the remaining GPIO and interrupt pins remain explicitly no-connected until the expansion topology is assigned. R25/R26 add schematic-owned 0805 I2C pullup placeholders from `+3V3` to `I2C_SDA`/`I2C_SCL`, placed near U6 with short routed stubs to the shared U6/U7 bus.
- `VAC24_A_FUSED` now ties the fuse/MOV island to the bridge/TVS protection island using a back-layer bridge and front-layer via handoff.
- `VAL_SENSE_AC` is routed from J2 to TP9 as a perimeter diagnostic trace. It remains monitor-only and does not drive the gas valve.
- `REMOTE_SPA_SENSE` and `REMOTE_POOL_SENSE` are locally routed from their pullup resistors through the RC filter capacitors to the optocoupler output pins.
- `U8` is now schematic-owned as the Murata `NXE1S0505MC-R7` isolated 5 V converter. Per the NXE1 pin table, pad 1 is `GND`/`-Vin`, pad 3 is `+5V`/`+Vin`, pad 7 is `COMMON_LINE`/`-Vout`, pad 8 is `ISO_REMOTE_5V`/`+Vout`, and pad 14 remains no-connect. The isolated output is first-pass routed to the external-control wetting supply and common return.
- `U9`-`U12` now use a real project-local `H11AA1M` AC-input phototransistor optocoupler symbol instead of a generic DIP placeholder. The onsemi/Fairchild pinout is captured as pins 1-2 AC input, pin 3 NC, pin 4 emitter, pin 5 collector, and pin 6 base. `U11` has its VAL monitor transistor output side captured: emitter to `GND`, collector to `VAL_OPTO_GPIO` on MCP23017 GPA0, with R12 as a schematic-owned 0805 pullup placeholder to `+3V3`. Its AC input side is captured through two 0805 current-limit placeholders: `VAL_SENSE_AC` -> `R8` -> `VAL_OPTO_LIMIT_A` -> `R9` -> `VAL_OPTO_INPUT` -> `U11.1`, with `U11.2` returned to `ICM_GND_REF`. `U9` repeats that monitor pattern for TH: `TH_HEAT_REQUEST_OUT` -> `R13` -> `TH_OPTO_LIMIT_A` -> `R14` -> `TH_OPTO_INPUT` -> `U9.1`, with `U9.2` returned to `ICM_GND_REF`; U9 emitter returns to `GND`, collector connects to `TH_OPTO_GPIO` on MCP23017 GPA1, and R15 pulls the collector to `+3V3`. `U10` repeats the same pattern for IND: `IND_SENSE_AC` -> `R16` -> `IND_OPTO_LIMIT_A` -> `R17` -> `IND_OPTO_INPUT` -> `U10.1`, with `U10.2` returned to `ICM_GND_REF`; U10 emitter returns to `GND`, collector connects to `IND_OPTO_GPIO` on MCP23017 GPA2, and R18 pulls the collector to `+3V3`. `U12` now repeats the same sense-only pattern for the 24 VAC source: `ICM_24VAC_SOURCE` -> `R19` -> `VAC24_OPTO_LIMIT_A` -> `R20` -> `VAC24_OPTO_INPUT` -> `U12.1`, with `U12.2` returned to `ICM_GND_REF`; U12 emitter returns to `GND`, collector connects to `VAC24_OPTO_GPIO` on MCP23017 GPA3, and R21 pulls the collector to `+3V3`. R8/R9/R12/R13/R14/R15/R16/R17/R18/R19/R20/R21 final resistance, power/leakage, filtering, surge, and sensing margin remain review items.
- `R10` and `R11` are now schematic-owned 0805 relay-gate pulldown placeholders. They tie `RELAY_K1_GATE` and `RELAY_K2_GATE` to `GND` locally at Q1/Q2 so the MOSFET gates have a defined off-state once final drive values are selected. `R22` and `R23` are schematic-owned 0805 series-gate placeholders that split the schematic-only relay-gate logic outputs into `RELAY_K1_GATE_DRIVE`/`RELAY_K2_GATE_DRIVE` and the local MOSFET gate nodes.
- `SPA_LINE` and `POOL_LINE` are first-pass routed from the remote optocoupler input side to the external-control connector, `ISO_REMOTE_5V` is sourced from U8 and locally routed between the Spa/Pool remote wetting resistors, `COMMON_LINE` is sourced from U8 isolated return to J5.2, and the optocoupler LED anode nets are locally routed from the wetting resistors to the optocouplers.
- `U14` is now a schematic-owned thermistor AFE placeholder with a matching `SOT-23-6` PCB footprint. Its thermistor input, ADC output, window-sense, analog rail, and analog return nets are first-pass routed on the inner layers with short local pad escapes. R24 adds a schematic-owned 0805 thermistor pullup placeholder from `+3V3_ADC` to `THERMISTOR_ADC`, and C9 adds a schematic-owned 0805 ADC filter placeholder from `THERMISTOR_ADC` to `AGND`; both are locally routed near the U14/U7 analog cluster. Threshold/reference component values and the final thermistor/SFS analog topology remain review items.
- `U18` is the schematic-owned SFS buffer/excitation placeholder. R27 now reserves a routed 0805 series/protection element from the J3 `SFS_INPUT` field terminal to `SFS_FIELD_INPUT`, and C10 reserves a routed 0805 ADC-side filter from `SFS_ADC` to `AGND`. This keeps the SFS input path physically present while leaving the unknown `SFS_RETURN_OR_REF`, excitation, clamp strategy, and final value choices open until the installed SFS is characterized.
- ADS1115 AIN2 is now named and routed as `VRAW_MONITOR_ADC` instead of the stale `TH_FEEDBACK_ADC` label. R28 reserves the top divider resistor from `VRAW` near TP1, while R29 and C11 reserve the bottom divider/filter elements from `VRAW_MONITOR_ADC` to `AGND` in the analog cluster. The monitor node reaches U7 AIN2 with via-assisted inner-layer routing; final divider ratio, voltage/power ratings, leakage, filtering, and firmware scaling remain review items.
- R30/R31 add routed 0805 pullup placeholders from `+3V3` to `THERMISTOR_RANGE_OK` and `SFS_RANGE_OK` at U16/U17. These preserve physical pullup locations for the comparator outputs while leaving final values, population policy, output polarity, and static-safety logic review open.
- R32-R39 add routed 0805 threshold-divider placeholders from `+3V3_ADC` to `AGND` for the U16/U17 low/high comparator references. R32/R33 create `THERM_LOW_REF_TBD`, R34/R35 create `THERM_HIGH_REF_TBD`, R36/R37 create `SFS_LOW_REF_TBD`, and R38/R39 create `SFS_HIGH_REF_TBD`. These nets are routed into the comparator inputs with via-assisted local escapes; final resistor values, tolerances, hysteresis policy, and fault thresholds remain tied to measured thermistor/SFS curves and TLV6700 behavior.

## Applied Connector Nets

| Connector | Pad order |
| --- | --- |
| `J1` 24 VAC input | `24VAC_A`, `24VAC_B`, `EARTH_SHIELD_REF` |
| `J2` operating control | `VAL_SENSE_AC`, `TH_HEAT_REQUEST_OUT`, `IND_SENSE_AC`, `ICM_GND_REF`, `ICM_24VAC_SOURCE`, `FIREMAN_24VAC`, `FIREMAN_SWITCH_RETURN` |
| `J3` safety stack | `PS_SWITCH`, `HLS_SWITCH`, `ES1_SWITCH`, `AFS_SWITCH_DYNAMIC`, `AGS_SWITCH`, `SFS_INPUT`, `GAS_MONITOR_ONLY` |
| `J4` thermistor | `THERMISTOR_A`, `THERMISTOR_B` |
| `J5` external control | `SPA_LINE`, `COMMON_LINE`, `POOL_LINE` |

## Verification State

- ERC report: zero violations after the MCP23017 core-pin capture and placeholder ownership cleanup.
- PCB DRC report: zero violations and zero unconnected items after this pass.
- Silkscreen cleanup moved dense/internal references and long floorplan notes off the manufacturing silkscreen while preserving the notes in the board file.
- Schematic parity report: zero issues after bringing all currently placed footprints under schematic ownership. U6 now has its MCP23017 supply/I2C/address/reset core captured, U8 now has its isolated-supply input/output pins captured, U11 now has a routed VAL optocoupler input resistor chain, output to MCP23017 GPA0, and R12 logic-side pullup placeholder, U9 now has a routed TH optocoupler input resistor chain, output to MCP23017 GPA1, and R15 logic-side pullup placeholder, U10 now has a routed IND optocoupler input resistor chain, output to MCP23017 GPA2, and R18 logic-side pullup placeholder, U12 now has a routed 24 VAC optocoupler input resistor chain, output to MCP23017 GPA3, and R21 logic-side pullup placeholder, R10/R11 now have routed relay-gate pulldown placeholders, R22/R23 now have relay-gate series placeholders, R24/C9 now have routed thermistor divider/filter placeholders, R25/R26 now have routed I2C pullup placeholders, R27/C10 now have routed SFS input/filter placeholders, R28/R29/C11 now have routed VRAW monitor divider/filter placeholders, R30/R31 now have routed comparator-output pullup placeholders, R32-R39 now have routed comparator threshold-divider placeholders, and U9-U12 now have real H11AA1M pin identities. Conceptual relay-gate and static-safety review blocks are schematic-only so they no longer collide with physical optocoupler references.

## Next Real Electrical Work

- Continue replacing uncommitted placeholder blocks with real symbols, hierarchical pins, labels, footprints, and values.
- Assign remaining U6 MCP23017 GPIO/interrupt usage and review firmware-safe reset behavior; R25/R26 now reserve I2C pullup positions, but final values still depend on bus capacitance, speed, leakage, and any external pullups.
- Review and value the U11 VAL, U9 TH, U10 IND, and U12 24 VAC monitor input resistors, pullups, filtering, surge tolerance, CTR margin, and base-pin handling.
- Add/value remaining passives: buck feedback/compensation/filter parts, ADC protection, SFS return/excitation/buffer parts, comparator threshold/hysteresis values for R32-R39, and final values/ratings for the existing optocoupler, relay-gate, thermistor, I2C, SFS, and VRAW monitor placeholders.
- Run KiCad update-PCB-from-schematic and replace this PCB-side draft net application with schematic-derived nets.
- Complete schematic synchronization, copper zones, fabrication outputs, and qualified safety review.
