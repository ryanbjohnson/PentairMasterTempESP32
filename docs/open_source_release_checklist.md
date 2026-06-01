# Open Source Release Checklist

Use this before making the GitHub repository public.

## Repository Metadata

- [ ] Repository description clearly says this is an experimental KiCad/open hardware project.
- [ ] Repository topics include `kicad`, `esp32`, `open-hardware`, and `pool-heater` only if the owner is comfortable with discovery.
- [ ] GitHub private vulnerability reporting is enabled.
- [ ] Branch protection is enabled for `main`.
- [ ] Pull requests are required before merge.
- [ ] GitHub Actions checks are enabled.

## Documentation

- [ ] Root `README.md` is accurate.
- [ ] `CONTRIBUTING.md` reflects the desired contribution workflow.
- [ ] `SECURITY.md` has a real private reporting path.
- [ ] `LICENSE` matches the owner's intended license.
- [ ] `docs/licensing.md` decision is resolved if a hardware-specific license is preferred.
- [ ] `DISCLAIMER.md` is linked from project descriptions or release notes.
- [ ] Project-specific checklist in `pcb/mastertemp_esp32/README.md` is current.

## Safety And Privacy

- [ ] No private serial numbers, addresses, or identifying field photos are committed.
- [ ] No public docs instruct unqualified live-heater testing.
- [ ] No docs describe bypassing heater safety systems.
- [ ] The README clearly states the design is not certified or installable.
- [ ] Field input assumptions remain marked as open until verified.

## Generated Files

- [ ] `reports/` is not committed.
- [ ] `fab/` is not committed unless publishing a reviewed release package.
- [ ] KiCad backups, lock files, and local history are not committed.

## First Public Release

- [ ] Do not tag a hardware release until ERC, DRC, parity, field verification, FMEA, and safety review gates are complete.
- [ ] Use pre-release labels for any design snapshot before certified/reviewed hardware.
- [ ] Release notes repeat that the design is not approved for live-heater installation.
