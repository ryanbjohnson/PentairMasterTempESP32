# Security And Safety Reporting

This project has both software-security and physical-safety concerns. Treat unsafe control behavior, safety bypasses, or misleading validation procedures as reportable issues.

## Please Report Privately

Use GitHub private vulnerability reporting if it is enabled for the repository. If it is not enabled yet, contact the project owner privately before posting details publicly.

Report privately if you find:

- A path for firmware, Wi-Fi, MQTT, Home Assistant, or remote commands to override a safety fault.
- Any design path that can energize the gas valve directly.
- A relay, watchdog, brownout, OTA, reset, or fault-lockout failure that can leave heat request asserted.
- Documentation that could lead a non-qualified person to perform unsafe live-heater testing.
- A supply, isolation, creepage, connector, or miswire issue that creates shock, fire, or gas-appliance risk.
- A software dependency or automation issue that compromises generated outputs.

## Public Issues Are Fine For

- Documentation typos.
- Non-sensitive KiCad ERC/DRC findings.
- Test failures that do not disclose an unsafe bypass path.
- Questions about setup or contribution workflow.

## Response Expectations

This is a volunteer/open hardware project. Maintainers will try to acknowledge private safety/security reports promptly, reproduce the issue, decide whether public disclosure is appropriate, and document the fix once it is safe to do so.

Do not connect this design to a live heater to prove a vulnerability unless you are qualified, authorized, and following applicable safety procedures.
