# Governance

This project is currently maintainer-led.

## Maintainer Responsibilities

Maintainers are responsible for:

- Preserving the documented safety boundary.
- Reviewing pull requests for technical quality and risk.
- Keeping release gates honest.
- Deciding when assumptions are sufficiently verified.
- Blocking changes that encourage unsafe installation, testing, or operation.

## Decision Making

Routine documentation, tests, and scaffold improvements can be merged after normal review.

Changes that affect heat-request behavior, relay topology, safety inputs, power isolation, field wiring, thermistor/SFS validity, watchdog/brownout behavior, or live-test procedure require explicit safety review before merge.

## Releases

No release should be described as installable, certified, production-ready, or safe for live-heater use until the checklist in `pcb/mastertemp_esp32/README.md` is complete and reviewed.

## Ownership

If additional maintainers are added, they should understand KiCad, embedded controls, and the project's gas-appliance safety boundary.
