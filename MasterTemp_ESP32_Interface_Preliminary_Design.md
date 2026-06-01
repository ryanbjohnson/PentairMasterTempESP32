# Pentair MasterTemp 125 ESP32 Interface Board - Preliminary Design Package

Status: preliminary engineering design for review only. This is not a certified gas-appliance control, not a release-to-manufacturing package, and not an installation instruction. A licensed/qualified pool-heater service technician and a controls engineer familiar with ANSI Z21.56/CSA 4.7 gas-fired pool-heater requirements must review, test, and approve any hardware before it is connected to a live heater.

## 1. Safety Boundary

This design is an operating-control/interface board. It must preserve the factory ignition control module (ICM) and must not directly drive the gas valve. The board only requests heat by switching the existing 24 VAC call-for-heat signal to `TH` on the ICM through isolated, normally-open relay contacts.

Hard requirements:

- No line voltage is routed on this PCB.
- No output from the ESP32 is allowed to energize the gas valve.
- Loss of ESP32 power, watchdog heartbeat, 3.3 V rail, 5 V rail, 24 VAC input, or firmware control opens the heat request.
- Two normally-open relay contacts are placed in series in the `TH` call-for-heat path.
- Hardware interlocks disable heat independently of MQTT, Wi-Fi, web UI, Home Assistant, and OTA.
- Safety switches are never bypassed in firmware.
- Final installation must keep the OEM heater grounding/bonding and line-voltage compartment unchanged.

Manufacturer facts used for this design:

- The MasterTemp 125 is a 120/240 VAC gas-fired heater using a Class II 24 VAC transformer for the control system.
- The Pentair manual identifies `VAL`, `TH`, `IND`, `GND`, `24VAC`, `FS`, thermistor, safety-switch, membrane-pad, and external pool/spa/common interface points.
- Pentair documents that the Fireman's Switch completes the heater 24 V AC control-board circuit, is sized around 24 VAC at 0.5 A, and must not receive line voltage.
- Pentair troubleshooting checks for 24 VAC between `TH` and `GND` immediately after a call for heat, and for 24 VAC on `VAL`/gas-valve-related signals only during the ignition trial.
- Pentair's connected-heater parts matrix lists old control board `42002-0007S` as basic PCBA superseded by kit `461105`; the older ICM `42001-0052S` is superseded by `476223`.

Sources:

- Pentair MasterTemp 125 Installation and User's Guide, Rev. C: https://www.pentair.com/content/dam/extranet/aquatics/pool-pad-pro-assets/heaters-%26-heat-pumps/inground-heaters/mastertemp-125-heater/MasterTemp%20125%20Installation%20and%20Users%20Guide%20-%20English%20-%20Rev%20C.pdf
  - Local checked-in copy: `pcb/mastertemp_esp32/references/manuals/mastertemp_125_installation_users_guide_english_rev_c.pdf`
- Pentair MasterTemp/Max-E-Therm connected-heater parts matrix: https://www.pentair.com/content/dam/extranet/nam/pentair-pool/residential/parts-sheets/heaters/mastertemp-max-e-therm-parts-matrix-connected-heater-update-v1.pdf
- Pentair electrical-system replacement parts sheet showing 42002-0007S and factory sensors: https://www.pentair.com/content/dam/extranet/nam/pentair-pool/residential/parts-sheets/heaters/MaxETherm_Heater_Electrical_System.pdf

## 2. System Architecture

Functional blocks:

1. 24 VAC input protection and power conversion.
2. ESP32-WROOM controller with external watchdog/supervisor.
3. Isolated 24 VAC sense inputs for ICM and heater-status signals.
4. Protected dry-contact sensing for remote Pool/Common/Spa and local UI.
5. Safety-switch sensing and hardware heat-enable chain.
6. Thermistor and stack-flue-sensor analog measurement through protected ADC channels.
7. Dual series relay heat-request output to ICM `TH`.
8. Relay feedback sensing for welded-contact or unexpected `TH` voltage detection.
9. Local UI header, optional OLED/I2C display, LEDs, buzzer, UART/JTAG programming.

Important sequencing note: `AFS` is a proving switch. It is expected to prove combustion-air flow after blower operation begins, so the firmware must check it for sane idle/run behavior instead of blindly requiring it closed before the call for heat. The hardware chain should include Fireman's Switch/remote enable, water pressure, high-limit, AGS, and analog overtemperature comparators as static pre-fire enables. `AFS` is monitored dynamically and can be included in a delayed run-enable circuit only after blower/IND activity is detected.

## 3. Schematic-Level Design

### Page 1 - 24 VAC Input and Power

Connector `J1 POWER`, 3.5 or 5.08 mm keyed pluggable terminal:

| Pin | Net | Description |
| --- | --- | --- |
| 1 | `VAC24_A` | Heater transformer secondary |
| 2 | `VAC24_B` | Heater transformer secondary |
| 3 | `CHASSIS_SHIELD` | Optional shield/bond reference, no DC tie by default |

Power path:

- `VAC24_A` -> `F1` 0.5 A fuse/PTC -> `MOV1` across `VAC24_A_FUSED`/`VAC24_B`.
- `D1` bridge rectifier converts `VAC24_A_FUSED`/`VAC24_B` to `VRAW`/`PGND_RAW`.
- `TVS1` bidirectional or post-bridge TVS clamps transients.
- `C1/C2` bulk capacitance on `VRAW`; use 63 V or 100 V ratings.
- `U1` high-voltage buck: `VRAW` to `+5V`.
- `U2` synchronous buck: `+5V` to `+3V3`.
- `U3` 3.3 V reset supervisor drives `ESP32_EN` and `HEAT_ENABLE_HW`.
- `U4` watchdog supervisor requires ESP32 heartbeat before relay drive is allowed.

Nominal voltage calculation:

- 24 VAC RMS nominal gives about 34 V peak before bridge drops.
- 24 VAC at +10 percent gives about 37 V peak.
- Unloaded Class II transformers can exceed nominal; all `VRAW` parts should be 63 V minimum, with the 5 V buck rated 80-100 V.

### Page 2 - MCU, Supervisors, and Digital I/O

Controller:

- `U5`: Espressif `ESP32-WROOM-32E-N16`.
- `U6`: Microchip `MCP23017-E/SS` I/O expander for LEDs, buttons, and non-time-critical opto inputs.
- `U7`: TI `ADS1115IDGSR` external ADC for thermistor, SFS, and rail monitoring.
- `U16/U17`: hardware window comparators for thermistor and SFS plausibility gates.

Supervisor logic:

- ESP32 outputs `WDI_HEARTBEAT` at 10-50 Hz only while the firmware is in a healthy non-OTA runtime loop.
- `U4 /WDO` must be inactive for heat enable.
- `U3 /RESET` must be inactive for heat enable.
- Relay drive is permitted only when:
  `HEAT_CMD_GPIO` AND `WATCHDOG_OK` AND `BROWNOUT_OK` AND `SAFETY_STATIC_OK` AND `NOT_OTA` AND `NOT_FAULT_LOCKOUT`.

Recommended hardware implementation:

- Use a small logic gate such as `SN74LVC1G08DBVR` for each relay-enable path.
- Use pull-downs on every relay-driver MOSFET gate.
- Make default gate state low during ESP32 reset/boot.

### Page 3 - Safety Inputs and Static Hardware Chain

Use two circuits for each safety contact where practical:

1. A low-current isolated sense input so firmware knows which safety opened.
2. A hardware safety-enable path so the relay coil cannot energize if a critical safety is open.

Critical static chain:

`FIREMAN_CLOSED` -> `PS_CLOSED` -> `HLS_CLOSED` -> `AGS_CLOSED` -> `ES1_CLOSED_OR_JUMPERED` -> `THERMISTOR_RANGE_OK` -> `SFS_RANGE_OK` -> `SAFETY_STATIC_OK`.

Notes:

- `PS` should close only with valid pump flow/pressure.
- `HLS` and `AGS` are closed in normal operation and open on overtemperature.
- `ES1` is spare; follow the exact heater wiring diagram for whether it is jumpered.
- `SFS` is not a simple low-resistance dry contact in all variants; treat it as an analog/high-impedance sensor and verify against the exact heater harness.
- `AFS` is dynamic. Firmware must confirm "open when idle" and "closed after blower/IND proves airflow." If `AFS` opens during firing, drop `TH` immediately.

Per-contact sense circuit, dry contact:

- Isolated 5 V wetting source `+5V_ISO` from `U8` isolated DC/DC.
- Contact closure drives an optocoupler LED through 2.2 k to 4.7 k.
- Optocoupler transistor pulls an ESP32/MCP23017 input low.
- Add 100 nF debounce capacitor on the logic side, then debounce again in firmware.
- Add ESD/TVS at harness connector.

### Page 4 - Thermistor and Stack Flue Sensor

Thermistor input:

- `J3_THERM_A/B` two-pin protected input.
- 10.0 k, 0.1 percent pull-up to `+3V3_ADC`.
- 1 k series resistor into `ADS1115_AIN0`.
- 100 nF C0G/X7R to analog ground at ADC pin.
- Low-leakage ESD clamp to rails.
- Firmware rejects open, short, out-of-range, implausible rate-of-change, and ADC saturation.
- Independent window comparator output `THERMISTOR_RANGE_OK` must drop heat enable on open, short, or overtemperature threshold even if firmware is stuck.

SFS input:

- `J3_SFS_A/B` two-pin protected high-impedance input.
- Use a high-value divider/current source suitable for the installed SFS type.
- Buffer with low-bias op amp before ADC if the selected excitation impedance is above 1 Mohm.
- Add a hardware comparator window `SFS_RANGE_OK` so extreme SFS open/short/fault disables heat without firmware.
- Final resistor values must be validated with the exact Pentair SFS installed on the heater.

### Page 5 - 24 VAC Sense Inputs

Use AC-input optocouplers for:

- `ICM_TH_SENSE`
- `ICM_IND_SENSE`
- `ICM_VAL_SENSE`
- `ICM_24VAC_SENSE`
- Optional `TH_OUTPUT_FEEDBACK`

Typical circuit:

- Field signal pair -> two series input resistors -> `H11AA1M` input.
- Start value: 2 x 12.1 k, 0.25 W, 1 percent in series for a 24 VAC signal.
- Logic transistor side: 10 k pull-up to 3.3 V, Schmitt input or RC pulse stretcher.
- Firmware treats AC sense as a pulse train and declares signal present only after several valid half-cycles.

Do not use these sense circuits to source current into the ICM. They are monitor-only.

### Page 6 - Call-for-Heat Output

The heat-request output is a dry, isolated, dual-relay series path:

`ICM_24VAC_SOURCE` -> `K1_COM` -> `K1_NO` -> `K2_COM` -> `K2_NO` -> `ICM_TH`.

Relay gating:

- `K1` coil: controlled by firmware heat command plus watchdog/brownout gate.
- `K2` coil: controlled by static safety hardware chain plus firmware heat command gate.
- Both relays are normally open.
- Loss of board power opens both relays.
- A stuck relay is detected by `TH_OUTPUT_FEEDBACK` when firmware expects off.

Relay contact rating:

- Minimum 30 VAC / 1 A resistive.
- Use relays with substantially higher agency-rated contact capacity where possible.
- Contacts are switching only the heater's 24 VAC control circuit, never line voltage.

Gas valve:

- No board output is provided for direct gas-valve drive.
- `VAL` is monitor-only through an isolated AC sense input.

### Page 7 - External Controls and UI

Remote Pool/Common/Spa:

- `POOL_REMOTE`, `COMMON_REMOTE`, `SPA_REMOTE` are dry-contact sense inputs.
- The board supplies wetting current through isolated sensing only.
- Do not accept externally supplied voltage on these terminals.
- If Pool and Spa are both asserted, enter conflict fault and keep heat off.

Local controls:

- `BTN_POOL`
- `BTN_SPA`
- `BTN_OFF`
- `BTN_UP`
- `BTN_DOWN`
- `BTN_RESET_SERVICE`

Display:

- I2C OLED/LCD header on `DISPLAY_SDA`, `DISPLAY_SCL`, `+3V3`, `GND`.
- Optional buzzer and WS2812/status LED header, powered from `+5V` with level-shifted data if used.

## 4. Connector Pinout Table

### J1 - Power

| Pin | Signal | Type |
| --- | --- | --- |
| 1 | `24VAC_IN_1` | 24 VAC transformer secondary |
| 2 | `24VAC_IN_2` | 24 VAC transformer secondary |
| 3 | `CHASSIS_SHIELD` | Shield/bond reference, normally isolated from logic |

### J2 - Ignition Control Module Interface

| Pin | Signal | Type |
| --- | --- | --- |
| 1 | `ICM_24VAC_SOURCE` | 24 VAC source for relay contact COM |
| 2 | `ICM_GND_REF` | 24 VAC reference for sense only |
| 3 | `ICM_TH_OUT` | Relay-switched 24 VAC call for heat to TH |
| 4 | `ICM_TH_SENSE_A` | Isolated AC sense |
| 5 | `ICM_IND_SENSE_A` | Isolated AC sense |
| 6 | `ICM_VAL_SENSE_A` | Isolated AC sense |
| 7 | `ICM_SENSE_REF` | Return/reference for AC sense inputs |

### J3 - Safety and Sensors

Use paired terminals where possible so the board can preserve the field wiring instead of relying on chassis/common returns.

| Pin | Signal | Type |
| --- | --- | --- |
| 1 | `PS_A` | Water pressure switch |
| 2 | `PS_B` | Water pressure switch |
| 3 | `HLS_A` | High-limit switch |
| 4 | `HLS_B` | High-limit switch |
| 5 | `ES1_A` | Extra switch/jumper |
| 6 | `ES1_B` | Extra switch/jumper |
| 7 | `AFS_A` | Air-flow proving switch |
| 8 | `AFS_B` | Air-flow proving switch |
| 9 | `AGS_A` | Automatic gas shutoff switch |
| 10 | `AGS_B` | Automatic gas shutoff switch |
| 11 | `SFS_A` | Stack flue sensor |
| 12 | `SFS_B` | Stack flue sensor |
| 13 | `THERM_A` | Water thermistor |
| 14 | `THERM_B` | Water thermistor |

### J4 - Remote Controls

| Pin | Signal | Type |
| --- | --- | --- |
| 1 | `POOL_REMOTE` | Dry-contact sense |
| 2 | `COMMON_REMOTE` | Dry-contact common |
| 3 | `SPA_REMOTE` | Dry-contact sense |
| 4 | `FIREMAN_A` | Fireman's Switch loop |
| 5 | `FIREMAN_B` | Fireman's Switch loop |

### J5 - Local UI

| Pin | Signal | Type |
| --- | --- | --- |
| 1 | `BTN_POOL` | Momentary input |
| 2 | `BTN_SPA` | Momentary input |
| 3 | `BTN_OFF` | Momentary input |
| 4 | `BTN_UP` | Momentary input |
| 5 | `BTN_DOWN` | Momentary input |
| 6 | `BTN_RESET` | Momentary input |
| 7 | `UI_GND` | Logic ground |
| 8 | `DISPLAY_SDA` | I2C |
| 9 | `DISPLAY_SCL` | I2C |
| 10 | `+3V3_UI` | Display/UI power |
| 11 | `BUZZER` | Output |
| 12 | `STATUS_LED_DATA` | Output |

### J6 - Programming/Service

| Pin | Signal |
| --- | --- |
| 1 | `+3V3` |
| 2 | `GND` |
| 3 | `ESP_TX0` |
| 4 | `ESP_RX0` |
| 5 | `EN` |
| 6 | `GPIO0_BOOT` |

## 5. Candidate BOM

This BOM is a starting point for schematic capture. It is not procurement-approved; verify package, availability, lifecycle, agency ratings, and derating before layout release.

| Ref | Qty | Part number | Manufacturer | Function |
| --- | --- | --- | --- | --- |
| U5 | 1 | `ESP32-WROOM-32E-N16` | Espressif | Wi-Fi MCU module |
| U1 | 1 | `LM5164YDRCR` | Texas Instruments | 100 V input buck, 5 V rail |
| U2 | 1 | `AP63203WU-7` | Diodes Inc. | 5 V to 3.3 V buck |
| U3 | 1 | `TPS3839G33DBZR` | Texas Instruments | 3.3 V brownout supervisor |
| U4 | 1 | `TPS3823-33DBVR` | Texas Instruments | Watchdog/reset supervisor |
| U6 | 1 | `MCP23017-E/SS` | Microchip | I/O expander |
| U7 | 1 | `ADS1115IDGSR` | Texas Instruments | 16-bit I2C ADC |
| U8 | 1 | `NXE1S0505MC-R7` | Murata | Isolated 5 V for dry-contact wetting |
| U16-U17 | 2 | `TLV6700DDCR` | Texas Instruments | Window comparators for sensor validity gates |
| U18 | 1 | `OPA333AIDBVR` | Texas Instruments | Low-bias analog buffer for SFS if needed |
| U9-U12 | 4 | `H11AA1M` | onsemi | AC optocoupler sense |
| U13-U15 | 3 | `TLP293-4(GB,E)` | Toshiba | Quad optocouplers for dry contacts |
| K1-K2 | 2 | `G5V-1-DC5` | Omron | Series NO heat-request relays |
| Q1-Q2 | 2 | `AO3400A` | Alpha & Omega | Relay low-side drivers |
| D1 | 1 | `MB10S-13-F` | Diodes Inc. | Bridge rectifier |
| D2-D3 | 2 | `SS14` | Vishay/Diodes Inc. | Relay flyback diodes |
| F1 | 1 | `0451.500MRL` | Littelfuse | 0.5 A input fuse |
| MOV1 | 1 | `V47ZA1P` | Littelfuse | 24 VAC surge clamp |
| TVS1 | 1 | `SMBJ51CA` | Littelfuse | Post-bridge transient clamp |
| C1 | 1 | `EEU-FR1J471L` | Panasonic | 470 uF, 63 V bulk capacitor |
| C2-C3 | 2 | `CGA5L3X7R2A475K160AE` | TDK | 4.7 uF, 100 V input ceramic |
| L1 | 1 | `744773470` | Wurth Elektronik | 47 uH buck inductor, validate with U1 |
| L2 | 1 | `74438323022` | Wurth Elektronik | 2.2 uH buck inductor |
| R_AC | 8 | 12.1 k, 0.25 W, 1% | Yageo/Vishay | AC opto input resistors, two per sense |
| R_WET | as needed | 2.2 k to 4.7 k, 0.1 W | Yageo/Vishay | Dry-contact opto LED resistors |
| R_TH | 1 | 10.0 k, 0.1%, 25 ppm | Vishay | Thermistor pull-up |
| R_GATE | 2 | 100 ohm | Any | MOSFET gate resistors |
| R_PD | 2 | 100 k | Any | Relay gate pull-downs |
| J1-J6 | as needed | Phoenix Contact MSTB/MC keyed pluggable series | Phoenix Contact | Field connectors |
| ENC | 1 | `1554H2GYCL` or similar | Hammond | Polycarbonate enclosure, gasketed |

Possible alternates:

- Use an ESP32-S3-WROOM module if more RAM, USB, or safer ADC isolation strategy is needed.
- Use force-guided safety relays if a certification path requires positively guided contacts and contact monitoring.
- Use a certified external 24 VAC to 5 V DC module instead of the onboard buck if thermal/EMC qualification becomes the bigger risk.

## 6. Firmware Pin Map

ESP32 pins:

| Signal | GPIO | Notes |
| --- | --- | --- |
| `I2C_SDA` | GPIO21 | ADS1115, MCP23017, OLED |
| `I2C_SCL` | GPIO22 | I2C clock |
| `HEAT_K1_CMD` | GPIO25 | Relay K1 command, gated in hardware |
| `HEAT_K2_CMD` | GPIO26 | Relay K2 command, gated in hardware |
| `WDI_HEARTBEAT` | GPIO27 | External watchdog input |
| `ICM_TH_PRESENT` | GPIO34 | Input-only, opto pulse |
| `ICM_IND_PRESENT` | GPIO35 | Input-only, opto pulse |
| `ICM_VAL_PRESENT` | GPIO32 | Opto pulse |
| `ICM_24VAC_PRESENT` | GPIO33 | Opto pulse |
| `MCP23017_INT` | GPIO39 | Input-only interrupt |
| `ADS1115_ALERT` | GPIO36 | Input-only alert |
| `BUZZER_PWM` | GPIO14 | Optional |
| `WS2812_DATA` | GPIO13 | Optional level-shifted LED |
| `UART0_TX` | GPIO1 | Service programming |
| `UART0_RX` | GPIO3 | Service programming |
| `BOOT` | GPIO0 | Bootloader only, pulled up |
| `EN` | EN | Supervisor reset |

Avoid using ESP32 strapping pins for relay commands. Relay outputs must remain deasserted during bootloader, reset, crash, OTA, and brownout.

MCP23017 allocation:

- GPA0-GPA5: local buttons.
- GPA6-GPA7: remote Pool/Spa conflict inputs.
- GPB0-GPB5: safety contact sense status.
- GPB6-GPB7: service/heating/status LEDs.

ADS1115 allocation:

- AIN0: water thermistor divider.
- AIN1: SFS measurement.
- AIN2: 5 V rail monitor.
- AIN3: VRAW scaled monitor or spare.

## 7. Firmware State Machine

### Power-up self-test

- Keep K1 and K2 off.
- Hold `WDI_HEARTBEAT` inactive until initialization completes.
- Validate NVS settings CRC and temperature calibration bounds.
- Validate thermistor range and ADC sanity.
- Validate SFS range and comparator state.
- Confirm no relay feedback is present with relay commands off.
- Confirm no conflicting Pool/Spa commands.
- Confirm AFS is in its expected idle state; a stuck AFS enters service fault.

### Idle

- Display current water temperature and selected mode.
- Publish MQTT telemetry.
- Monitor all safeties continuously.
- Permit OTA only in Idle and only when no post-purge or anti-short-cycle timer is active.

### Heat demand pending

Conditions required:

- Pool or Spa mode selected, not Off.
- Setpoint above measured water temperature plus hysteresis.
- Setpoint no higher than 104 deg F / 40 deg C default maximum.
- Fireman's Switch closed.
- Water pressure switch closed.
- HLS and AGS closed.
- Thermistor and SFS valid.
- No active lockout.
- Pool and Spa inputs not both active.
- Watchdog, brownout, and relay-feedback tests pass.

### Ignition sequence monitor

- Energize K1/K2 only after all gates are true.
- Confirm `TH` feedback appears.
- Watch `IND`/blower-related sense if connected.
- Require AFS to prove within a configured timeout after blower/IND activity.
- Monitor `VAL` as sense-only; do not drive it.
- If `VAL` appears when no valid `TH` command exists, enter service lockout.
- If ignition sequence times out, drop `TH`, log fault, and lock out or retry according to configured policy.

### Heating

- Maintain heat request only while all permissives remain true.
- Drop K1/K2 immediately on safety fault, thermistor/SFS invalid reading, overtemperature, watchdog event, brownout, relay-feedback mismatch, remote conflict, or user Off.
- Log runtime and ignition count.
- Publish heating state and active fault state over MQTT.

### Post-purge / cooldown

- Keep K1/K2 off.
- Continue monitoring blower/IND/VAL feedback.
- Do not re-fire until the post-purge observation has completed and the anti-short-cycle timer has expired.
- Manual default: 45 s blower/post-purge observation and 5 min anti-short-cycle delay.

### Fault lockout

Manual reset required for:

- High-limit or AGS fault.
- SFS invalid or overtemperature.
- Thermistor open/short/out-of-range.
- Watchdog reset while heating.
- Brownout while heating.
- Relay feedback indicates welded/stuck contact.
- `VAL` present without commanded heat.
- AFS stuck closed at idle or failure to prove after blower start.

Timed retry may be allowed only for benign demand/timeouts after professional review. Do not auto-retry high-limit, gas-valve, relay-feedback, or sensor-validity faults.

## 8. MQTT and Home Assistant

Suggested MQTT topics:

- `pentair/mastertemp125/state`
- `pentair/mastertemp125/availability`
- `pentair/mastertemp125/water_temp_f`
- `pentair/mastertemp125/pool_setpoint_f`
- `pentair/mastertemp125/spa_setpoint_f`
- `pentair/mastertemp125/mode/set`
- `pentair/mastertemp125/fault`
- `pentair/mastertemp125/runtime_seconds`
- `pentair/mastertemp125/ignition_count`

Rules:

- Wi-Fi failure must never block local safety operation.
- MQTT commands are advisory UI commands only; they cannot override a safety fault.
- OTA is refused unless state is Idle, heat relays are off, `VAL` is not present, and post-purge/anti-short-cycle timers are clear.
- Home Assistant discovery should expose climate control, binary sensors for safeties, and diagnostic sensors, but no entity should bypass local lockouts.

## 9. Power Budget

Estimated worst-case board load:

| Load | Voltage | Current | Power |
| --- | --- | --- | --- |
| ESP32 Wi-Fi burst | 3.3 V | 500 mA peak | 1.65 W peak |
| ESP32 average | 3.3 V | 120-180 mA | 0.4-0.6 W |
| Relays K1/K2 | 5 V | 60 mA total typical | 0.3 W |
| Optos/isolated wetting | 5 V | 50-100 mA | 0.25-0.5 W |
| OLED/status LEDs | 3.3/5 V | 50-150 mA | 0.2-0.6 W |
| Margin | - | - | 1 W |

Recommended supply ratings:

- 5 V rail: at least 1.2 A continuous.
- 3.3 V rail: at least 700 mA peak, 400 mA continuous.
- Thermal design: verify at 50 deg C ambient inside the heater control compartment.
- Brownout threshold: disable relays before ESP32 operation becomes undefined.

## 10. PCB Layout Requirements

Board stack:

- Prefer 4-layer PCB: signal/top, solid ground, power, signal/bottom.
- 2-layer acceptable only after EMC/noise testing, with short high-current loops and careful grounding.

Zones:

- Zone A: 24 VAC field wiring, fusing, bridge, surge protection.
- Zone B: `VRAW` buck converter and bulk capacitor.
- Zone C: logic/ESP32/ADC/I2C.
- Zone D: relay contacts and ICM connector.
- Zone E: external remote/UI field connector.

Clearance:

- No line voltage on PCB.
- Maintain at least 6.4 mm clearance between any connector area that could be miswired to field wiring and SELV logic where practical.
- Add isolation slots under/around optocouplers and relay contact areas.
- Maintain clear silkscreen boundary: "24 VAC CONTROL ONLY - NO LINE VOLTAGE".
- Keep ESP32 antenna beyond copper pour and away from relay/transformer wiring.

Routing:

- Route `VRAW` buck input loop compactly.
- Keep thermistor/SFS traces away from relay coils, buck switch node, and AC sense inputs.
- Use star/quiet analog ground into ADC reference region.
- Place TVS parts at connector entry.
- Put relay contacts in series with wide, separated traces; label COM/NO clearly.
- Provide test pads for `+5V`, `+3V3`, `VRAW`, `WATCHDOG_OK`, `SAFETY_STATIC_OK`, `K1_COIL`, `K2_COIL`, `TH_FEEDBACK`, `VAL_SENSE`.

Silkscreen warnings:

- "NO LINE VOLTAGE ON CONTROL TERMINALS"
- "GAS VALVE MONITOR ONLY - DO NOT DRIVE"
- "24 VAC CLASS II CONTROL POWER ONLY"
- "INSTALL/SERVICE BY QUALIFIED TECHNICIAN"
- "VERIFY WIRING AGAINST HEATER MANUAL BEFORE POWER"

## 11. Enclosure and Mounting

Recommended:

- Mount inside the existing low-voltage/control-board compartment only if line-voltage separation and temperature limits are preserved.
- Use a gasketed polycarbonate enclosure if mounted separately: Hammond `1554H2GYCL` or equivalent.
- Use nylon or metal standoffs with bonded ground only where required by heater enclosure practice.
- Do not tie ESP32 digital ground to chassis/bonding conductor unless an EMI/safety review intentionally adds a defined network, such as Y-cap/RC/TVS strategy allowed by applicable standards.
- All external wires should use 105 deg C rated insulation where they share routing with heater wiring, matching the manual's service guidance.

## 12. Bench Test Procedure

Before heater connection:

1. Visual inspect PCB for solder bridges, wrong polarity capacitors, and relay contact clearance.
2. Confirm no continuity between relay contact field nets and ESP32 logic ground.
3. Power from an isolated bench 24 VAC transformer only.
4. Verify `VRAW`, `+5V`, and `+3V3` at low, nominal, and high simulated transformer input.
5. Hold ESP32 in reset; confirm K1/K2 contacts remain open.
6. Load blank firmware or stop heartbeat; confirm watchdog disables relay drive.
7. Force brownout; confirm relay coils drop out before ESP32 resets unpredictably.
8. Command heat with safety chain open; confirm K1/K2 do not both close.
9. Simulate each safety input open/closed and verify correct diagnostic state.
10. Simulate AFS stuck closed at idle; confirm lockout.
11. Simulate blower/IND then AFS closure; confirm allowed sequence.
12. Simulate thermistor normal, open, short, high temperature, and implausible jumps.
13. Simulate SFS normal, open, short, and overtemperature/fault values.
14. Apply Pool and Spa remote contacts independently; confirm dry-contact behavior.
15. Assert Pool and Spa simultaneously; confirm conflict fault and no heat request.
16. Confirm relay output switches only isolated 24 VAC to `TH`, never line voltage.
17. With relays off, inject unexpected `TH` feedback; confirm welded-contact/external-voltage fault.
18. With `VAL` sense active and no heat command, confirm service lockout.
19. Confirm OTA is rejected during any non-idle state.
20. Run 24-hour soak test with cycling relays and synthetic sensors.

On-heater test, qualified technician only:

1. Compare every harness wire against the exact MasterTemp 125 wiring diagram revision for the installed heater.
2. Confirm line power is off and locked out before wiring.
3. Confirm no line-voltage conductor is present on any board terminal.
4. First power the board from heater 24 VAC with heat output disconnected.
5. Verify sensor readings and safety states match actual heater conditions.
6. Connect `TH` output with gas shut off/manual valve off for initial sequence testing.
7. Verify `TH` appears only during valid call for heat and drops immediately on each simulated safety opening.
8. Verify blower/IND and AFS sequence.
9. Verify `VAL` is monitored only and never driven by this board.
10. Restore gas only after wiring, safeties, post-purge, and shutdown behavior are verified.
11. Perform combustion, gas-pressure, leak, venting, and CO tests according to the heater manual and local code.

## 13. Safety Validation Checklist

- [ ] The OEM ICM remains installed and handles ignition, flame proving, and gas-valve sequencing.
- [ ] ESP32 cannot directly energize gas valve.
- [ ] K1 and K2 are normally open and series-connected in the `TH` request path.
- [ ] Relay contacts open with no board power.
- [ ] Relay contacts open with ESP32 reset.
- [ ] Relay contacts open with watchdog timeout.
- [ ] Relay contacts open with 3.3 V brownout.
- [ ] Relay contacts open with Fireman's Switch open.
- [ ] Relay contacts open with PS open.
- [ ] Relay contacts open with HLS or AGS open.
- [ ] Relay contacts open on invalid thermistor.
- [ ] Relay contacts open on invalid SFS.
- [ ] AFS stuck-closed-at-idle fault is detected.
- [ ] AFS failure-to-prove fault is detected.
- [ ] Pool/Spa simultaneous command fault is detected.
- [ ] Unexpected `TH` voltage with relays off is detected.
- [ ] Unexpected `VAL` voltage without heat request is detected.
- [ ] Wi-Fi/MQTT/Home Assistant cannot override safety lockout.
- [ ] OTA cannot run while heating, post-purge, or anti-short-cycle timer is active.
- [ ] Silkscreen and connector labels explicitly warn against line voltage.
- [ ] Final design has professional review and heater-specific wiring verification.

## 14. Open Items Before CAD Release

1. Confirm exact MasterTemp 125 revision, serial date, connected/non-connected version, and harness connector pinout.
2. Measure actual transformer no-load and loaded voltage in the installed heater.
3. Confirm thermistor resistance curve and SFS electrical characteristics for the installed sensor revision.
4. Decide whether this is a true replacement PCBA or an interposer that keeps parts of the OEM operating control.
5. Choose certification target and required standards before final relay/watchdog/safety-chain design.
6. Validate relay contact rating, creepage, and failure-mode requirements with the certification path.
7. Perform FMEA for relay welded contact, optocoupler failure, ADC stuck reading, brownout oscillation, and firmware deadlock.
8. Create actual KiCad/Altium schematic, PCB, ERC/DRC, fabrication drawings, test fixture, and firmware after the above are closed.
