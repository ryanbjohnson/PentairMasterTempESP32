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
| U1 | TI `LM5164YDRCR` candidate | 100 V input 5 V buck | `Texas_S-PVSON-N10` |
| U2 | Diodes Inc. `AP63203WU-7` | 3.3 V buck | `TSOT-23-6` |
| U3 | TI `TPS3839G33DBZR` | 3.3 V reset/brownout supervisor | `SOT-23-3` |
| U4 | TI `TPS3823-33DBVR` | Watchdog supervisor | `SOT-23-5` |
| U5 | Espressif `ESP32-WROOM-32E-N16` | Controller module | `ESP32-WROOM-32E` |
| U6 | Microchip `MCP23017-E/SS` | I/O expander | `SSOP-28_5.3x10.2mm_P0.65mm` |
| U7 | TI `ADS1115IDGSR` | External ADC | `VSSOP-10_3x3mm_P0.5mm` |
| U8 | Murata `NXE1S0505MC-R7` | Isolated 5 V wetting supply | `Converter_DCDC_Murata_NXE1SxxxxMC_SMD` |
| U9-U12 | onsemi `H11AA1M` | AC optocoupler sense channels | `DIP-6_W7.62mm` |
| U16-U17 | TI `TLV6700DDCR` | Thermistor/SFS window comparators | `SOT-23-6` |
| U18 | TI `OPA333AIDBVR` | Optional SFS buffer | `SOT-23-5` |
| Q1-Q2 | `AO3400A` candidate | Relay low-side drivers | `SOT-23` |

## Source Checks

- Phoenix Contact lists `MSTBA 2,5/7-G-5,08` part `1757297` as a 7-position, 5.08 mm pitch COMBICON MSTB header rated 12 A and 320 V in the catalog context.
- Espressif's ESP32-WROOM-32E datasheet lists the `ESP32-WROOM-32E-N16` ordering code with 16 MB flash and -40 C to 85 C ambient rating.
- TI's LM5164 datasheet covers a 100 V input synchronous buck family and provides reference BOM/layout data; final values must be calculated for the selected 24 VAC transformer range.
- Diodes Inc.'s AP63203 datasheet lists `AP63203WU-7` as a fixed 3.3 V TSOT26 regulator variant.
- TI's TLV6700 datasheet lists `TLV6700DDCR` active in 6-pin SOT-23-THIN/DDC with -40 C to 125 C operation.
- DigiKey currently lists `H11AA1M` as an onsemi 6-DIP optoisolator with 4170 Vrms isolation and active stock.

## Checked Source Links

- Phoenix Contact `1757297`: https://www.phoenixcontact.com/en-nl/products/pcb-header-mstba-25-7-g-508-1757297
- Espressif ESP32-WROOM-32E datasheet: https://documentation.espressif.com/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.html
- TI LM5164 product page: https://www.ti.com/product/LM5164
- Omron G5Q relay family: https://components.omron.com/us-en/products/relays/G5Q
- TI ADS1115IDGSR: https://www.ti.com/product/ADS1115/part-details/ADS1115IDGSR
- Microchip MCP23017: https://www.microchip.com/en-us/product/mcp23017
- Diodes Inc. AP63203: https://www.diodes.com/part/view/AP63203/
- TI TLV6700DDCR: https://www.ti.com/product/TLV6700/part-details/TLV6700DDCR
- DigiKey/onsemi `H11AA1M`: https://www.digikey.com/en/products/detail/onsemi/H11AA1M/1053602

## Open Sourcing Items

- Confirm final relay choice with safety review. `G5Q-1A-DC5` is placed as a more robust NO relay candidate; contact-rating, coil power, agency rating, and failure-mode requirements still need approval.
- Confirm exact connector family against enclosure, wire gauge, harness strain relief, and service clearances.
- Confirm U1 package and buck compensation/reference component values against the exact TI design procedure.
- Confirm whether a certified 24 VAC to 5 V module is preferable to an onboard buck for EMC, thermal, and certification reasons.
