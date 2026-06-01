## Summary

Describe the change and why it is needed.

## Safety Boundary

Confirm each item:

- [ ] No direct gas-valve drive was added.
- [ ] No line-voltage routing, connector, or net label was added.
- [ ] OEM ignition-control sequencing remains preserved.
- [ ] Heat-request output remains fail-open and safety-gated.
- [ ] Firmware, Wi-Fi, MQTT, Home Assistant, and OTA cannot override safety faults.
- [ ] Open assumptions are documented as review items.

## Verification

- [ ] `./scripts/run-tests.sh`
- [ ] `./scripts/kicad-check.sh`
- [ ] KiCad GUI review, if applicable
- [ ] Not run; reason:

## Evidence

List any manual sections, field measurements, photos, datasheets, or review records used.

## Release Impact

- [ ] Documentation only
- [ ] Schematic change
- [ ] PCB/layout change
- [ ] Requirements/test change
- [ ] Safety-critical behavior or assumption
