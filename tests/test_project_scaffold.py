import re
import shutil
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = REPO_ROOT / "pcb" / "mastertemp_esp32"
ROOT_SCH = PROJECT_DIR / "mastertemp_esp32.kicad_sch"
BOARD = PROJECT_DIR / "mastertemp_esp32.kicad_pcb"
REQUIREMENTS = REPO_ROOT / "pcb" / "requirements" / "mastertemp_esp32_requirements.yaml"
DESIGN_DOC = REPO_ROOT / "MasterTemp_ESP32_Interface_Preliminary_Design.md"
PROJECT_README = PROJECT_DIR / "README.md"


class ProjectScaffoldTests(unittest.TestCase):
    def test_root_schematic_references_expected_child_sheets(self):
        text = ROOT_SCH.read_text(encoding="utf-8")
        expected_sheets = {
            "sheets/power_24vac.kicad_sch",
            "sheets/esp32_supervisor.kicad_sch",
            "sheets/icm_interface.kicad_sch",
            "sheets/safety_inputs.kicad_sch",
            "sheets/thermistor_sfs.kicad_sch",
            "sheets/ui_remote.kicad_sch",
        }

        for sheet in expected_sheets:
            self.assertIn(sheet, text)
            self.assertTrue((PROJECT_DIR / sheet).exists(), f"Missing child sheet: {sheet}")

    def test_safety_boundary_is_documented_consistently(self):
        design_doc = DESIGN_DOC.read_text(encoding="utf-8")
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        readme = PROJECT_README.read_text(encoding="utf-8")
        combined = "\n".join([design_doc, requirements, readme]).lower()

        required_phrases = [
            "no line voltage",
            "preserve the oem ignition control module",
            "two normally-open relay contacts",
            "fireman's switch",
            "watchdog",
            "brownout",
        ]

        for phrase in required_phrases:
            self.assertIn(phrase, combined)

        self.assertIn("gas valve", combined)
        self.assertIn("directly drive", combined)

    def test_requirements_keep_gas_valve_drive_disallowed(self):
        requirements = REQUIREMENTS.read_text(encoding="utf-8")

        self.assertRegex(requirements, r"direct_gas_valve_drive_allowed:\s*false")
        self.assertRegex(requirements, r"line_voltage_on_pcb_allowed:\s*false")
        self.assertRegex(requirements, r"relay_count:\s*2")
        self.assertRegex(requirements, r"fail_safe_state:\s*open")

    def test_board_has_expected_stackup_and_warning_labels(self):
        board = BOARD.read_text(encoding="utf-8")

        for layer in ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]:
            self.assertIn(layer, board)

        required_labels = [
            "NO LINE VOLTAGE ON CONTROL TERMINALS",
            "24 VAC FIELD / POWER ZONE",
            "ESP32 / LOGIC ZONE",
            "ICM TH RELAY CONTACT ZONE",
            "ESP32 ANTENNA KEEPOUT",
        ]

        for label in required_labels:
            self.assertIn(label, board)

    def test_board_floorplan_v0_has_major_placement_envelopes(self):
        board = BOARD.read_text(encoding="utf-8")

        required_labels = [
            "J1 POWER 3P",
            "J2 OPERATING CONTROL 7P",
            "VAL TH IND GND 24VAC 24VAC FS",
            "J3 SAFETY STACK 7P",
            "PS HLS ES1 AFS AGS SFS GAS",
            "J4 THERM",
            "J5 EXT CTRL 3P",
            "SPA COMMON POOL",
            "J6 MEMBRANE / UI 12P",
            "J6 SERVICE UART",
            "K1\\nNO RELAY",
            "K2\\nNO RELAY",
            "ICM REF\\nS1/240 S1/120 L1 L2 S2 TH IND VAL GND",
            "VAL / GAS MONITOR ONLY - NO DRIVE",
            "U1/L1 100 V BUCK",
            "U5 ESP32-WROOM",
            "TP ROW: VRAW +5V +3V3 WDG SAFETY K1 K2 TH VAL",
            "FUTURE ISOLATION SLOT",
        ]

        for label in required_labels:
            self.assertIn(label, board)

        floorplan_doc = PROJECT_DIR / "docs" / "pcb_floorplan_v0.md"
        self.assertTrue(floorplan_doc.exists())

    def test_manual_review_notes_exist(self):
        manual_review = PROJECT_DIR / "docs" / "mastertemp125_rev_c_manual_review.md"
        text = manual_review.read_text(encoding="utf-8")

        required_phrases = [
            "Rev. C, 3/2019",
            "Figure 24",
            "VAL`, `TH`, `IND`, `GND`, `24VAC`",
            "`PS`, `HLS`, `ES1`, `AFS`, `AGS`, `SFS`, `GAS`",
            "`Spa Line`, `Common Line`, `Pool Line`",
            "`24 VAC at 0.5 A`",
        ]

        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_board_outline_is_160_by_100_mm_scaffold(self):
        board = BOARD.read_text(encoding="utf-8")
        edge_rects = re.findall(
            r'\(gr_rect\s+\(start\s+([-0-9.]+)\s+([-0-9.]+)\)\s+\(end\s+([-0-9.]+)\s+([-0-9.]+)\).*?\(layer\s+"Edge.Cuts"\)',
            board,
            flags=re.S,
        )

        self.assertTrue(edge_rects, "Expected an Edge.Cuts rectangle for the scaffold outline")
        widths = {round(abs(float(x2) - float(x1)), 3) for x1, _, x2, _ in edge_rects}
        heights = {round(abs(float(y2) - float(y1)), 3) for _, y1, _, y2 in edge_rects}
        self.assertIn(160.0, widths)
        self.assertIn(100.0, heights)

    def test_completion_checklist_exists_in_project_readme(self):
        readme = PROJECT_README.read_text(encoding="utf-8")

        self.assertIn("## Completion checklist", readme)
        self.assertIn("### Schematic capture", readme)
        self.assertIn("### Safety review", readme)
        self.assertIn("### PCB layout", readme)


@unittest.skipUnless(shutil.which("kicad-cli"), "kicad-cli is not installed")
class KiCadCliTests(unittest.TestCase):
    def test_kicad_cli_checks_pass(self):
        result = subprocess.run(
            ["bash", "./scripts/kicad-check.sh"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=120,
        )

        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
