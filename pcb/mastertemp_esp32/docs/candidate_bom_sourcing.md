# Candidate BOM and Sourcing Notes

Date: 2026-05-31

Status: candidate engineering BOM only. These parts are placed on the draft PCB to drive mechanical and routing work. They are not procurement-approved, agency-approved, or release-approved for connection to a live heater.

## Candidate Parts

| Ref | Candidate part | Function | Footprint placed |
| --- | --- | --- | --- |
| J1 | Phoenix Contact MSTBA 2,5/3-G-5,08 family | 24 VAC input | `PhoenixContact_MSTBA_2,5_3-G-5,08_1x03_P5.08mm_Horizontal` |
| J2, J3 | Phoenix Contact MSTBA 2,5/7-G-5,08, `1757297` | Operating-control and safety-stack terminals | `PhoenixContact_MSTBA_2,5_7-G-5,08_1x07_P5.08mm_Horizontal` |
| J4 | Phoenix Contact MSTBA 2,5/2-G-5,08 family | Thermistor terminal | `PhoenixContact_MSTBA_2,5_2-G-5,08_1x02_P5.08mm_Horizontal` |
| J5 | Phoenix Contact MSTBA 2,5/3-G-5,08 family | External Pool/Common/Spa control | `PhoenixContact_MSTBA_2,5_3-G-5,08_1x03_P5.08mm_Horizontal` |
| J6 | Phoenix Contact MSTBA 2,5/9-G-5,08 family | OEM membrane connector reference only | `PhoenixContact_MSTBA_2,5_9-G-5,08_1x09_P5.08mm_Horizontal` |
| K1, K2 | Omron `G5Q-1A-DC5` candidate | Dual normally-open heat-request relays | `Relay_SPST_Omron-G5Q-1A` |
| U1 | TI `LM5164DDAR` candidate | 100 V input 5 V buck | `TI_SO-PowerPAD-8` |
| U2 | Diodes Inc. `AP63203WU-7` | 3.3 V buck | `TSOT-23-6` |
| U3 | TI `TPS3839G33DBZR` | 3.3 V reset/brownout supervisor | `SOT-23-3` |
| U4 | TI `TPS3823-33DBVR` | Watchdog supervisor | `SOT-23-5` |
| U5 | Espressif `ESP32-WROOM-32E-N16` | Controller module | `ESP32-WROOM-32E` |
| U6 | Microchip `MCP23017-E/SS` | I/O expander | `SSOP-28_5.3x10.2mm_P0.65mm` |
| U7 | TI `ADS1115IDGSR` | External ADC | `VSSOP-10_3x3mm_P0.5mm` |
| U8 | Murata `NXE1S0505MC-R7` | Isolated 5 V wetting supply | `Converter_DCDC_Murata_NXE1SxxxxMC_SMD` |
| U9-U12 | onsemi `H11AA1M` | AC optocoupler sense channels | `DIP-6_W7.62mm` |
| U14 | Thermistor AFE TBD | Thermistor divider/filter/protection placeholder | `SOT-23-6` |
| U16-U17 | TI `TLV6700DDCR` | Thermistor/SFS window comparators | `SOT-23-6` |
| U18 | TI `OPA333AIDBVR` | Optional SFS buffer | `SOT-23-5` |
| U19-U20 | LiteOn `LTV-817S` class candidate | External Pool/Spa dry-contact isolated sense | `DIP-4_W7.62mm` |
| R1-R2 | 2.2 k 0805 candidate | Remote dry-contact wetting-current limiters | `R_0805_2012Metric` |
| R3-R4 | 10 k 0805 candidate | Remote sense logic-side pullups | `R_0805_2012Metric` |
| R8-R9 | VAL optocoupler input limiters TBD | Two-part series current limiting for U11 H11AA1M AC input | `R_0805_2012Metric` |
| R13-R14 | TH optocoupler input limiters TBD | Two-part series current limiting for U9 H11AA1M AC input | `R_0805_2012Metric` |
| R16-R17 | IND optocoupler input limiters TBD | Two-part series current limiting for U10 H11AA1M AC input | `R_0805_2012Metric` |
| R19-R20 | 24 VAC optocoupler input limiters TBD | Two-part series current limiting for U12 H11AA1M AC input | `R_0805_2012Metric` |
| C2-C3 | 100 nF 0805 candidate | Remote sense debounce/filter capacitors | `C_0805_2012Metric` |
| C4 | 2.2 uF 100 V TBD | LM5164 local VRAW input bypass | `C_1210_3225Metric` |
| C5 | 2.2 nF 50 V TBD | LM5164 bootstrap capacitor | `C_0603_1608Metric` |
| R5-R6 | LM5164 feedback divider TBD | 5 V setpoint divider | `R_0805_2012Metric` |
| R7 | LM5164 RON TBD | On-time/frequency programming resistor | `R_0805_2012Metric` |
| R10-R11 | Relay MOSFET gate pulldowns TBD | Local off-state bias for K1/K2 low-side drivers | `R_0805_2012Metric` |
| R22-R23 | Relay MOSFET series-gate resistors TBD | Local drive damping/current limiting between relay-gate logic and Q1/Q2 gate nodes | `R_0805_2012Metric` |
| R24 | Thermistor pullup TBD | Water thermistor divider pullup placeholder from `+3V3_ADC` to `THERMISTOR_ADC` | `R_0805_2012Metric` |
| R25-R26 | I2C pullups TBD | SDA/SCL pullup placeholders from `+3V3` to the U6/U7 I2C bus | `R_0805_2012Metric` |
| R27 | SFS input series/protection TBD | Stack flue sensor input placeholder from `SFS_INPUT` to `SFS_FIELD_INPUT` | `R_0805_2012Metric` |
| R28-R29 | VRAW monitor divider TBD | Raw 24 VAC-derived rail monitor divider from `VRAW` to `VRAW_MONITOR_ADC` and `AGND` | `R_0805_2012Metric` |
| R30-R31 | Comparator output pullups TBD | Thermistor/SFS range comparator output pullup placeholders to `+3V3` | `R_0805_2012Metric` |
| R32-R39 | Comparator threshold dividers TBD | Thermistor/SFS low/high reference ladder placeholders from `+3V3_ADC` to `AGND` | `R_0805_2012Metric` |
| R12 | VAL optocoupler pullup TBD | Logic-side pullup for U11 collector / MCP23017 GPA0 | `R_0805_2012Metric` |
| R15 | TH optocoupler pullup TBD | Logic-side pullup for U9 collector / MCP23017 GPA1 | `R_0805_2012Metric` |
| R18 | IND optocoupler pullup TBD | Logic-side pullup for U10 collector / MCP23017 GPA2 | `R_0805_2012Metric` |
| R21 | 24 VAC optocoupler pullup TBD | Logic-side pullup for U12 collector / MCP23017 GPA3 | `R_0805_2012Metric` |
| C6 | 100 nF TBD | AP63203 bootstrap capacitor | `C_0603_1608Metric` |
| C7 | 10 uF 50 V TBD | AP63203 local +5 V input bypass | `C_1210_3225Metric` |
| C8 | 22 uF 10 V TBD | AP63203 +3V3 output capacitor | `C_0805_2012Metric` |
| C9 | Thermistor ADC filter TBD | Water thermistor ADC low-pass filter placeholder from `THERMISTOR_ADC` to `AGND` | `C_0805_2012Metric` |
| C10 | SFS ADC filter TBD | Stack flue sensor ADC low-pass filter placeholder from `SFS_ADC` to `AGND` | `C_0805_2012Metric` |
| C11 | VRAW monitor ADC filter TBD | Raw-rail monitor ADC low-pass filter placeholder from `VRAW_MONITOR_ADC` to `AGND` | `C_0805_2012Metric` |
| Q1-Q2 | `AO3400A` candidate | Relay low-side drivers | `SOT-23` |

## Source Checks

- Phoenix Contact lists `MSTBA 2,5/7-G-5,08` part `1757297` as a 7-position, 5.08 mm pitch COMBICON MSTB header rated 12 A and 320 V in the catalog context.
- Espressif's ESP32-WROOM-32E datasheet lists the `ESP32-WROOM-32E-N16` ordering code with 16 MB flash and -40 C to 85 C ambient rating.
- TI's LM5164 datasheet covers a 100 V input synchronous buck family and provides reference BOM/layout data; final values must be calculated for the selected 24 VAC transformer range.
- Diodes Inc.'s AP63203 datasheet lists `AP63203WU-7` as a fixed 3.3 V TSOT26 regulator variant.
- TI's TLV6700 datasheet lists `TLV6700DDCR` active in 6-pin SOT-23-THIN/DDC with -40 C to 125 C operation.
- DigiKey currently lists `H11AA1M` as an onsemi 6-DIP optoisolator with 4170 Vrms isolation and active stock.
- The H11AA1M schematic symbol now follows the onsemi/Fairchild pinout: pins 1-2 AC input, pin 3 NC, pin 4 emitter, pin 5 collector, pin 6 base. U11 VAL input is captured through R8/R9 placeholder series limiters to `ICM_GND_REF`; its output collector has R12 as a logic-side pullup placeholder to `+3V3`. U9 TH input is captured through R13/R14 from `TH_HEAT_REQUEST_OUT` to `ICM_GND_REF`; its output collector has R15 as a logic-side pullup placeholder to `+3V3` and connects to MCP23017 GPA1. U10 IND input is captured through R16/R17 from `IND_SENSE_AC` to `ICM_GND_REF`; its output collector has R18 as a logic-side pullup placeholder to `+3V3` and connects to MCP23017 GPA2. U12 24 VAC input is captured through R19/R20 from `ICM_24VAC_SOURCE` to `ICM_GND_REF`; its output collector has R21 as a logic-side pullup placeholder to `+3V3` and connects to MCP23017 GPA3. Final resistor values, surge/power ratings, output filtering, and sensing margin remain design items.
- R10/R11 are first-pass 0805 gate pulldown placeholders for Q1/Q2. R22/R23 are first-pass 0805 series-gate placeholders between the schematic-only relay-gate logic drive nets and the local MOSFET gate nodes. Final resistance, tolerance, leakage margin, damping, and reset behavior need relay-drive review before release.
- R24 and C9 are first-pass 0805 thermistor divider/filter placeholders. R24 ties `+3V3_ADC` to `THERMISTOR_ADC`, and C9 filters `THERMISTOR_ADC` to `AGND`; final pullup value, rail choice, filter capacitance, leakage, ADC source impedance, and fault thresholds need field curve verification before release.
- R27 and C10 are first-pass 0805 SFS conditioning placeholders. R27 reserves a series/protection element from `SFS_INPUT` to `SFS_FIELD_INPUT`, and C10 reserves an ADC-side filter from `SFS_ADC` to `AGND`. Final topology, value, leakage, clamp strategy, and whether/how `SFS_RETURN_OR_REF` is referenced remain dependent on installed SFS characterization.
- R25/R26 are first-pass 0805 I2C pullup placeholders. They tie `I2C_SDA` and `I2C_SCL` to `+3V3` near U6; final values depend on bus capacitance, selected I2C speed, device leakage, and whether any module-level pullups remain installed.
- R28/R29 and C11 are first-pass 0805 raw-rail monitor placeholders. R28 samples `VRAW` near TP1, while R29 and C11 terminate/filter `VRAW_MONITOR_ADC` in the analog cluster at `AGND`; final divider ratio, resistor voltage/power rating, leakage, filter capacitance, ADC source impedance, and firmware scaling remain design items.
- R30/R31 are first-pass 0805 pullup placeholders for `THERMISTOR_RANGE_OK` and `SFS_RANGE_OK`. Final values and whether the pullups are populated depend on the selected comparator output topology, leakage, startup behavior, and static-safety logic review.
- R32-R39 are first-pass 0805 threshold-divider placeholders for the TLV6700 thermistor and SFS window references. Final values depend on the verified water thermistor curve, installed SFS electrical behavior, TLV6700 input/common-mode limits, hysteresis strategy, tolerance stackup, leakage, ADC rail accuracy, and fault thresholds.
- The `LTV-817S` class remote-input optocoupler and R/C values are first-pass placeholders for isolated dry-contact sensing. Final CTR, wetting current, leakage, debounce, and EMC values need review.

## Checked Source Links

- Phoenix Contact `1757297`: https://www.phoenixcontact.com/en-nl/products/pcb-header-mstba-25-7-g-508-1757297
- Espressif ESP32-WROOM-32E datasheet: https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html
- TI LM5164 product page: https://www.ti.com/product/LM5164
- Omron G5Q relay family: https://components.omron.com/us-en/products/relays/G5Q
- TI ADS1115IDGSR: https://www.ti.com/product/ADS1115/part-details/ADS1115IDGSR
- Microchip MCP23017: https://www.microchip.com/en-us/product/mcp23017
- Murata NXE1S0505MC-R7 datasheet: https://www.murata.com/products/productdata/8807031865374/kdc-nxe1.pdf
- Diodes Inc. AP63203: https://www.diodes.com/part/view/AP63203/
- TI TLV6700DDCR: https://www.ti.com/product/TLV6700/part-details/TLV6700DDCR
- DigiKey/onsemi `H11AA1M`: https://www.digikey.com/en/products/detail/onsemi/H11AA1M/1053602
- LiteOn `LTV-817S` family: https://optoelectronics.liteon.com/en-global/Home/ProductDetail?partNo=LTV-817S

## Open Sourcing Items

- Confirm final relay choice with safety review. `G5Q-1A-DC5` is placed as a more robust NO relay candidate; contact-rating, coil power, agency rating, and failure-mode requirements still need approval.
- Confirm exact connector family against enclosure, wire gauge, harness strain relief, and service clearances.
- Confirm U1 package and buck compensation/reference component values against the exact TI design procedure.
- Confirm U6 MCP23017 GPIO allocation, interrupt use, I2C pullup strategy, address policy, and reset behavior before relying on the expander for any control or diagnostic functions.
- Confirm U8 isolated-supply creepage/clearance, load range, EMC filtering, and whether the isolated return should remain only `COMMON_LINE` for the external dry-contact interface.
- Confirm U9-U12 H11AA1M input current limiting, surge tolerance, CTR margin, output pullup/filtering, and whether the base pins should be tied or left open before connecting these monitors. U11 VAL, U9 TH, U10 IND, and U12 24 VAC now have first-pass resistor-chain and pullup placeholders.
- Confirm Q1/Q2 relay-drive gate network values, including R10/R11 pulldowns and R22/R23 series gate resistors, against ESP32 boot/reset states and supervisor behavior.
- Confirm the installed water thermistor curve and temperature range, then value R24/C9 and the comparator thresholds around the verified ADC source impedance and failure modes.
- Characterize the installed SFS electrical type/range before finalizing R27/C10, U18 usage, SFS return/reference handling, and U17 threshold components.
- Confirm I2C bus capacitance, firmware bus speed, and external/module pullup policy before assigning final R25/R26 values.
- Confirm the VRAW monitor divider/filter values and ratings for the expected 24 VAC transformer tolerance, rectified rail range, ADC input limits, startup behavior, leakage, and fault cases.
- Confirm U16/U17 output stage behavior and range-ok pullup values before relying on the static safety chain.
- Confirm U16/U17 low/high threshold divider values and hysteresis policy from measured thermistor/SFS curves before populating R32-R39.
- Confirm whether a certified 24 VAC to 5 V module is preferable to an onboard buck for EMC, thermal, and certification reasons.
- Confirm external-control wetting-current source, optocoupler CTR margin, leakage behavior, and both-contacts-closed fault handling before relying on the remote input circuit.
