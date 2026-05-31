# AI-Assisted KiCad Workflow

Use AI for small, reviewable PCB tasks:

1. Convert requirements into connector and sheet checklists.
2. Draft one schematic sheet at a time.
3. Generate symbol/footprint skeletons for project-local parts.
4. Review ERC/DRC JSON output and propose fixes.
5. Maintain BOM attributes and review substitutions.
6. Create fabrication and bench-test checklists.

Do not use AI output as final approval for:

- Gas-appliance safety behavior.
- Creepage/clearance around field wiring.
- Relay failure-mode assumptions.
- Certification or code compliance.
- Heater-specific harness mapping.

For this board, make the first implementation pass in this order:

1. `power_24vac`
2. `esp32_supervisor`
3. `icm_interface`
4. `safety_inputs`
5. `thermistor_sfs`
6. `ui_remote`
7. PCB outline, connector placement, and safety-zone layout
8. Routing and fabrication outputs
