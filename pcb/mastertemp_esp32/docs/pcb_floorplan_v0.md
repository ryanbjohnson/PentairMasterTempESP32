# PCB Floorplan v0

Date: 2026-05-31

This is the first physical design pass for the MasterTemp ESP32 interface board. It intentionally uses board-level placement envelopes and labels rather than unsynchronized footprints, because the schematic sheets are still TODO-only. Real footprints should be added after the matching schematic symbols and part selections exist.

An OEM Pentair control-board photo was reviewed on 2026-06-01 and summarized in `oem_board_photo_layout_notes.md`. The photo supports an edge-serviceable layout with field connectors around the perimeter, repeated sense/protection cells just inside the connector edge, central control logic, a compact switching-supply island, and service/debug headers along the lower edge.

## Placement Intent

- `J1 POWER` sits at the upper-left service edge for 24 VAC Class II input.
- `J2 OPERATING CONTROL` follows the Rev C manual operating-control terminal organization: `VAL`, `TH`, `IND`, `GND`, `24VAC`, `24VAC`, `FS`.
- `J3 SAFETY STACK`, `J4 THERMISTOR`, `J5 EXT CTRL`, and `J6 MEMBRANE REF` mirror the major operating-control connector groups shown in Rev C Figure 24.
- `J6` is a reference/compatibility envelope only; keypad, membrane-pad, display, buzzer, and status-LED electronics are not part of this design scope.
- `K1` and `K2` are placed in series between the ICM connector and the logic/control regions.
- AC optocoupler sensing straddles the left-side field/logic boundary.
- The 100 V buck area is kept center-left with room for a compact switch loop.
- The ESP32 module is on the right side with its antenna aimed toward the board edge.
- `J3`, `J4`, and `J5` occupy the bottom/right service edges for safety, remote, and UI wiring.
- ADC/comparator circuitry is grouped in the lower-right logic area and kept away from the buck and relay regions.
- A test-pad row is reserved for power rails, watchdog, safety chain, relay drive, TH feedback, and VAL sense.
- An OEM ignition-control module terminal-row envelope is included as a reference for `S1/240`, `S1/120`, `L1`, `L2`, `S2`, `TH`, `IND`, `VAL`, and `GND`.

## OEM Photo-Informed Refinements

- Keep the board easy to service from the edges: heater-facing connectors should remain on perimeter edges with readable labels and enough finger/tool clearance.
- Place `J2` and `J3` next to repeated optocoupler/protection/sense cells so operating-control and safety-stack channels are visually traceable.
- Group the safety sense channels as a readable bank near `J3`: `PS`, `HLS`, `ES1`, `AFS`, `AGS`, `SFS`, and `GAS`.
- Keep relay hardware in a corner/edge zone with the `TH` contact-chain path obvious and separated from MCU, crystal, ADC, and sensor front ends.
- Keep the buck converter as a compact island with regulator, diode, inductor, and bulk capacitors close together; route thermistor and SFS signals around it, not through it.
- Put ESP32 support, watchdog, and relay-gate logic near the center/right logic region, but keep the ESP32 antenna at a clear board edge.
- Preserve a lower-edge debug/service strip for programming, rail checks, watchdog, safety-chain state, relay drive, `TH` feedback, and `VAL` sense.
- Treat UI/keypad/membrane reference connectors as perimeter compatibility features, not as core logic placement drivers.

## Release Caveats

- This is not yet a routable or fabricable electrical layout.
- Connector footprints, relay footprints, mounting holes, and exact keepouts must be replaced with real footprints after schematic capture.
- Internal isolation slots are marked as future placement targets only.
- Schematic parity is intentionally preserved by avoiding board-only footprints at this stage.
- The installed heater harness must be checked before relying on the Rev C diagram for final pin order.
- The OEM-board photo is a layout reference only and does not verify connector pin order, ratings, component values, or safety compliance.
