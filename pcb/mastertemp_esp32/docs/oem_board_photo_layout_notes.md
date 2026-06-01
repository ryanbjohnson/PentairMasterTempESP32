# OEM Board Photo Layout Notes

Date: 2026-06-01

Source: user-provided front-side photo of the original Pentair control board. Intended repo location: `../references/images/original_pentair_control_board_front.jpg`.

Status: visual reference only. The photo is useful for layout strategy, connector/service orientation, and major functional zoning. It is not sufficient evidence for final pin order, ratings, creepage, component values, or replacement-circuit approval.

## Visible Board Organization

- The board is a wide horizontal rectangle with four corner mounting holes and field/service connectors concentrated on the left, top, right, and bottom edges.
- A large relay occupies the upper-left corner, physically separated from the MCU and low-voltage logic. Its contact/load side appears near field wiring, with coil/drive circuitry just inside the board.
- Two tall left-edge harness connectors are stacked vertically. Their adjacent silkscreen and small opto/transistor groups indicate safety and operating-control sense inputs are routed inward from the service edge.
- The top edge has two multi-pin white harness connectors near the center. Their placement keeps field harnesses serviceable while short traces feed the MCU and support logic.
- The right edge carries a membrane/keypad-style connector and nearby status LED/button parts. This strongly suggests user-interface wiring is kept at the board perimeter.
- The switching supply is clustered in the upper-right quadrant: electrolytic capacitors, regulator IC, diode, inductor, and local passives are packed tightly together.
- The main microcontroller sits near the board center, with crystal immediately below and dense fanout to surrounding connectors and drivers.
- Test/program headers and a low-voltage pin header are along the lower edge, separated from high-current relay and supply areas.
- LED indicators are distributed along the lower and right portions, close to the functions they report.

## Layout Ideas To Carry Forward

- Preserve edge-serviceability: place all heater-facing connectors on board edges, with silkscreen labels readable from the service side.
- Keep relay/contact circuitry in a corner or edge zone, away from MCU, crystal, ADC, and sensor front ends.
- Route field input sense channels as short, parallel channels from the connector edge into identical optocoupler or protection cells. The OEM board appears to use repeated cells, which is good for review and troubleshooting.
- Keep the buck converter compact and self-contained: short input loop, diode/inductor/regulator/bulk cap close together, and no sensor traces through the switching-current loop.
- Place MCU centrally only if it reduces harness fanout length. For this ESP32 design, central logic is useful, but the antenna edge keepout may justify moving the ESP32 module toward a clear board edge while keeping helper ICs central.
- Keep crystal/clock parts tight to the MCU and away from relay, switching regulator, and long field traces.
- Put programming/test headers on a service edge, not buried between tall connectors or relay hardware.
- Keep diagnostic LEDs near the related connector or function, but do not let LED routing cut through isolation or analog-sensitive areas.
- Use the bottom edge for test pads and programming access, mirroring the OEM service/debug style.
- Maintain a visual and physical field-to-logic progression: connector edge, protection/wetting/opto cells, logic/MCU, then relay drivers.

## Differences For This ESP32 Interface Board

- The OEM board appears to include original control-board logic. This project is an operating-control interface and must preserve the OEM ignition control module; it must not add direct gas-valve drive.
- The ESP32 antenna imposes a copper/component keepout that the OEM board did not have. Put the module at a clear board edge with the antenna facing outward.
- The dual series heat-request relays should remain visibly isolated and reviewable. Do not hide the contact-chain path under dense logic routing.
- Thermistor and SFS analog inputs need a quieter zone than the photo's general-purpose digital fanout suggests. Keep those traces away from the buck converter, relay coils, and AC sense inputs.
- The field verification record still governs final connector order and assumptions. The photo supports the manual-aligned connector grouping but does not close any release gate by itself.

## Actionable Floorplan Changes

- Shift from generic placement envelopes toward an OEM-inspired left-to-right service flow:
  field connectors -> protection/sense cells -> MCU/supervisor/gates -> relay drivers/relay contacts and edge test headers.
- Keep the 24 VAC supply cluster tight in one upper corner, with explicit keepout from thermistor/SFS analog routing.
- Group `PS`, `HLS`, `ES1`, `AFS`, `AGS`, `SFS`, and `GAS` sense cells as a repeated vertical bank next to `J3`, matching the photo's readable troubleshooting pattern.
- Reserve a lower-edge debug strip for `+5V`, `+3V3`, `GND`, watchdog, `SAFETY_STATIC_OK`, relay gates/coils, `TH`, and `VAL` sense.
- Add mounting-hole and connector-service keepouts early, because the OEM board uses nearly the full width while preserving access at every edge.
