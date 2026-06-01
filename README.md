# Pentair MasterTemp ESP32 Interface

Open hardware and firmware-planning repository for a draft ESP32-based operating-control interface for the Pentair MasterTemp 125 heater family.

This project is early-stage engineering work. It is not a finished product, not certified, and not approved for connection to a live gas appliance.

## Safety First

- Read [DISCLAIMER.md](DISCLAIMER.md) before using any design file in this repository.
- Do not route or apply line voltage on this PCB.
- Do not add any ESP32-controlled gas-valve output.
- Preserve the OEM ignition control module and its sequencing.
- Keep the heat-request path fail-open with two normally-open relay contacts in series unless a qualified safety review approves a different architecture.
- Treat Wi-Fi, MQTT, Home Assistant, and firmware commands as advisory only. They must never override safety faults.
- A qualified technician and controls/electrical safety reviewer must approve any live-heater test.

## Current Status

The repository currently contains a KiCad scaffold and first-pass schematic capture for major control-board blocks:

- 24 VAC power entry and low-voltage rails.
- Operating-control/ICM interface and dual relay heat-request chain.
- ESP32 supervisor, watchdog, brownout, and relay-gate contract.
- Manual-aligned safety-stack input sheet and static safety gate.
- Field verification and OEM-board photo layout notes.

Remaining work includes final schematic capture, field verification, PCB/schematic parity cleanup, routing, FMEA, bench validation, and professional safety review.

## Repository Map

- `MasterTemp_ESP32_Interface_Preliminary_Design.md`: top-level design intent and safety boundary.
- `pcb/mastertemp_esp32/`: KiCad project.
- `pcb/mastertemp_esp32/docs/`: design notes, manual review, field verification, and layout notes.
- `pcb/mastertemp_esp32/references/`: project-local manuals and visual references used during review.
- `pcb/requirements/`: machine-readable requirements.
- `scripts/`: headless KiCad and test automation.
- `tests/`: scaffold and safety-boundary regression tests.

## Development Quick Start

Install KiCad 8 and Python 3, or use the included dev container.

Run checks:

```bash
./scripts/run-tests.sh
./scripts/kicad-check.sh
```

Open the KiCad project:

```bash
pcb/mastertemp_esp32/mastertemp_esp32.kicad_pro
```

Generated outputs go in ignored `reports/` and `fab/` directories.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening issues or pull requests. Contributions that weaken the safety boundary, directly drive the gas valve, add line-voltage routing, or bypass the OEM ignition control module will not be accepted.

Useful first contributions:

- Improve field-verification checklists and documentation.
- Capture missing schematic detail with clear review stubs where assumptions remain open.
- Reduce ERC/DRC/parity issues without masking safety problems.
- Improve tests that enforce the safety boundary.
- Review connector pinout assumptions against installed-heater evidence.

## Security And Safety Reports

Report safety or security issues using GitHub private vulnerability reporting when available, or follow [SECURITY.md](SECURITY.md). Do not publish exploit steps, unsafe bypass instructions, or live-appliance test procedures in public issues.

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).

Before first public hardware release, the project owner may choose to move hardware design files to a hardware-specific license such as CERN-OHL-S-2.0; see [docs/licensing.md](docs/licensing.md).

## Publishing Checklist

Before making the repository public or tagging a release, review [docs/open_source_release_checklist.md](docs/open_source_release_checklist.md).
