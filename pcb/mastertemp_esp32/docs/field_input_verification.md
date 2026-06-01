# Field Input Verification

Status: manual-assumed, field-open release gate. Values below are seeded from the included `../references/manuals/mastertemp_125_installation_users_guide_english_rev_c.pdf`, P/N 475000 Rev. C 3/2019. Do not mark the related README checklist items complete until the installed heater data below is measured, photographed where practical, and reviewed against the matching manual revision.

## Heater Identity

| Item | Recorded value | Evidence | Review status |
| --- | --- | --- | --- |
| MasterTemp 125 model number | MasterTemp 125, exact fuel/variant TBD | Manual applies to all MasterTemp 125 heater models; nameplate photo required | Manual assumed; field open |
| Serial number/date range | TBD | Nameplate photo required | Open |
| Connected or non-connected variant | TBD | Control-board/parts photo required | Open |
| Installed control board part number | `42002-0007S` appears in Rev. C replacement-parts table, exact installed part TBD | Board label/photo required | Manual reference only; field open |
| Installed ICM part number | `42001-0052S` appears in Rev. C replacement-parts table, exact installed part TBD | Module label/photo required | Manual reference only; field open |
| Manual revision matched to unit | Rev. C, 3/2019 assumed | Included PDF footer and cover show P/N 475000 Rev. C 3/2019; confirm against unit documents | Manual assumed; field open |

## Harness And Connector Verification

| Connector/group | Expected reference | Field verification required | Review status |
| --- | --- | --- | --- |
| Operating-control terminals | Rev. C Figure 24: `VAL`, `TH`, `IND`, `GND`, `24VAC`, `24VAC`, `FS` | Photograph terminal block and verify conductor order/colors | Manual assumed; field open |
| Safety stack | Rev. C Figure 24: `PS`, `HLS`, `ES1`, `AFS`, `AGS`, `SFS`, `GAS` | Photograph terminal block and verify conductor order/colors | Manual assumed; field open |
| Thermistor | Rev. C Figure 24 shows separate thermistor connector pair near operating control | Verify connector style, wire colors, and resistance at known water temperature | Manual assumed; field open |
| External control | Rev. C Figure 24: `Spa Line`, `Common Line`, `Pool Line` | Verify connector style and absence/presence of external controller wiring | Manual assumed; field open |
| Fireman's Switch | Rev. C text states the controller/timer/relay completes a 24 VAC control-board circuit and should be rated 24 VAC at 0.5 A | Verify wiring and confirm no line voltage is present | Manual assumed; field open |

## Electrical Measurements

Use an isolated meter and a qualified technician. Record meter model, measurement conditions, and whether the heater was idle, calling for heat, or firing.

| Measurement | Condition | Recorded value | Acceptance/review note | Review status |
| --- | --- | --- | --- | --- |
| 24 VAC transformer secondary | No-load | 24 VAC nominal Class II transformer assumed; no-load voltage TBD | Size `VRAW` and surge margin from measured high line/unloaded behavior | Manual assumed; field open |
| 24 VAC transformer secondary | Loaded/idle control powered | 24 VAC nominal assumed; loaded value TBD | Confirm supply design margin | Manual assumed; field open |
| 24 VAC transformer secondary | Heat call active | 24 VAC nominal assumed; active value TBD | Confirm relay/contact and sense design assumptions | Manual assumed; field open |
| `TH` to `GND` | Immediately after heat request | 24 VAC expected per troubleshooting flow; measured value TBD | Manual troubleshooting expects 24 VAC behavior | Manual assumed; field open |
| `VAL`/gas-valve monitor | Ignition trial only | 24 VAC expected during ignition try; measured value TBD | Sense-only validation; no drive allowed | Manual assumed; field open |
| Fireman's Switch current/voltage | Closed and open states | 24 VAC at up to 0.5 A control circuit assumed; measured value TBD | Confirm low-voltage control-only interface | Manual assumed; field open |

## Sensor Characterization

| Sensor | Field data required | Recorded value | Review status |
| --- | --- | --- | --- |
| Water thermistor | Resistance at known water temperature; open/short behavior if safely simulated | Manual shows thermistor sensor and diagnostic LED; curve TBD | Manual assumed; field open |
| Stack flue sensor | Electrical type, normal range, fault range, and harness behavior | Manual states SFS shuts down heater at 480 F / 249 C; electrical type/range TBD | Manual assumed; field open |
| AFS | Idle state and proven-airflow state timing relative to blower/`IND` | Manual states AFS closes after sufficient airflow; timing TBD | Manual assumed; field open |
| PS/HLS/AGS/ES1 | Normal closed/open behavior and installed jumper state where applicable | Manual states PS proves pump, HLS opens above 135 F / 57 C, AGS opens above 140 F / 60 C; ES1 jumper/use TBD | Manual assumed; field open |

## Mechanical Inputs

| Item | Recorded value | Review status |
| --- | --- | --- |
| Enclosure selection | TBD | Open |
| Mounting-hole pattern | TBD | Open |
| Standoff height | TBD | Open |
| Cable-entry direction | TBD | Open |
| Service clearance | TBD | Open |
| Environmental exposure assumptions | TBD | Open |

## Certification And Review Path

| Item | Recorded value | Review status |
| --- | --- | --- |
| Qualified technician reviewer | TBD | Open |
| Controls/electrical safety reviewer | TBD | Open |
| Applicable standards/review basis | TBD | Open |
| FMEA owner and review date | TBD | Open |
| Bench-test approval before live-heater connection | TBD | Open |
