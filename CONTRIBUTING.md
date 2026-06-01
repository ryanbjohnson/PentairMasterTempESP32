# Contributing

Thank you for helping. This project touches gas-appliance control wiring, so contribution quality is not just about style or passing tests. Changes must preserve the safety boundary and make assumptions visible.

## Non-Negotiable Safety Boundary

Do not submit changes that:

- Add direct ESP32, Wi-Fi, MQTT, Home Assistant, or firmware control of the gas valve.
- Add line-voltage routing, line-voltage connectors, or line-voltage net labels to this PCB.
- Bypass or replace the OEM ignition control module sequencing.
- Allow firmware to override an open safety input, invalid thermistor/SFS reading, watchdog timeout, brownout, relay fault, or OTA/fault lockout.
- Collapse the two normally-open series relay contacts into a single software-controlled heat-request output without a qualified safety review.
- Treat AFS as a static pre-fire interlock without preserving its dynamic airflow-proving behavior.
- Mark field assumptions as complete without measurement/photo evidence and review notes.

If a proposed improvement conflicts with these rules, open a discussion first and label it as a safety review item.

## Ways To Help

- Improve documentation, checklists, and manual-to-schematic traceability.
- Add focused schematic capture for one sheet at a time.
- Add tests that enforce safety requirements and repo structure.
- Reduce KiCad ERC, DRC, or schematic/PCB parity findings.
- Review field-verification assumptions against installed-heater evidence.
- Improve layout notes for serviceability, isolation, EMC, and analog signal integrity.

## Development Setup

Recommended tools:

- KiCad 8.x.
- Python 3.
- Bash or PowerShell.
- VS Code dev container if you want the checked environment.

Run before opening a pull request:

```bash
./scripts/run-tests.sh
./scripts/kicad-check.sh
```

The current draft PCB may intentionally have silkscreen warnings, unconnected items, and schematic/PCB parity warnings while schematic capture is incomplete. Do not hide real DRC/ERC problems by weakening checks without explaining why.

## Branch And Commit Guidance

- Use a short branch name such as `docs-field-verification`, `schematic-thermistor-sfs`, or `layout-relay-zone`.
- Keep pull requests focused on one topic.
- Explain assumptions and cite the project doc, manual section, field photo, or measurement that supports the change.
- Avoid unrelated formatting churn in KiCad files.
- Do not commit generated `reports/`, `fab/`, caches, local backups, or private field photos unless the project owner explicitly approves.

## KiCad Contribution Rules

- Keep project-local symbols in `pcb/mastertemp_esp32/libraries/symbols/mastertemp_esp32.kicad_sym`.
- Keep project-local footprints in `pcb/mastertemp_esp32/libraries/footprints/mastertemp_esp32.pretty`.
- Add review stubs for unresolved nets instead of silently leaving ambiguous labels.
- Preserve sheet-level notes when a value, topology, or field input remains unverified.
- Run ERC after schematic changes and DRC after placement/routing changes.
- Keep connector pin order tied to the manual review and field verification record.

## Documentation Rules

- Update `pcb/mastertemp_esp32/docs/field_input_verification.md` when a design decision depends on installed-heater evidence.
- Update the README checklist when a phase truly becomes complete.
- Use dates and source names for manual/photo/measurement references.
- Keep safety warnings concise and direct.

## Pull Request Checklist

Before requesting review, confirm:

- The safety boundary above is preserved.
- Tests/checks were run, or the reason they were not run is stated.
- New assumptions are documented as open review items.
- Generated files and local backups are not included.
- Schematic, PCB, docs, and requirements remain consistent.

## Live Heater Testing

Do not ask contributors to perform live gas-appliance testing from a GitHub issue or pull request. Live testing requires a qualified technician, appropriate instruments, local-code compliance, and project-owner approval.
