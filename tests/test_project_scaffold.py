import json
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
            "J6 MEMBRANE REF 9P",
            "KEYPAD OUT OF SCOPE",
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
        self.assertIn('(layer "Edge.Cuts")', board)
        self.assertRegex(board, r"\(start\s+20\s+20\)")
        self.assertRegex(board, r"\(end\s+180\s+120\)")

    def test_completion_checklist_exists_in_project_readme(self):
        readme = PROJECT_README.read_text(encoding="utf-8")

        self.assertIn("## Completion checklist", readme)
        self.assertIn("### Schematic capture", readme)
        self.assertIn("### Safety review", readme)
        self.assertIn("### PCB layout", readme)

    def test_control_board_scope_excludes_keypad_design(self):
        requirements = REQUIREMENTS.read_text(encoding="utf-8")
        ui_sheet = (PROJECT_DIR / "sheets" / "ui_remote.kicad_sch").read_text(encoding="utf-8")
        readme = PROJECT_README.read_text(encoding="utf-8")

        combined = "\n".join([requirements, ui_sheet, readme]).lower()
        self.assertIn("keypad", combined)
        self.assertIn("out of scope", combined)
        self.assertIn("external-control dry contacts only", combined)
        self.assertNotIn("status led design is in scope", combined)

    def test_control_board_schematic_pass_notes_exist(self):
        icm_sheet = (PROJECT_DIR / "sheets" / "icm_interface.kicad_sch").read_text(encoding="utf-8")
        safety_sheet = (PROJECT_DIR / "sheets" / "safety_inputs.kicad_sch").read_text(encoding="utf-8")

        self.assertIn("J2 OPERATING CONTROL TERMINALS", icm_sheet)
        self.assertIn("ICM_24VAC_SOURCE -> K1_COM -> K1_NO -> K2_COM -> K2_NO -> TH_HEAT_REQUEST_OUT", icm_sheet)
        self.assertIn("VAL and GAS are diagnostic monitor inputs only", icm_sheet)
        self.assertIn("J3 SAFETY STACK TERMINALS", safety_sheet)
        self.assertIn("STATIC HEAT ENABLE CHAIN", safety_sheet)
        self.assertIn("AFS DYNAMIC POLICY", safety_sheet)

    def test_candidate_parts_are_placed_on_pcb(self):
        board = BOARD.read_text(encoding="utf-8")
        required_refs = [
            "J1", "J2", "J3", "J4", "J5", "J6",
            "K1", "K2",
            "U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8",
            "U9", "U10", "U11", "U12", "U16", "U17", "U18",
            "Q1", "Q2",
            "TP1", "TP9",
        ]

        for ref in required_refs:
            self.assertIn(f'"{ref}"', board)

        bom = PROJECT_DIR / "docs" / "candidate_bom_sourcing.md"
        self.assertTrue(bom.exists())
        bom_text = bom.read_text(encoding="utf-8")
        self.assertIn("candidate engineering BOM only", bom_text)
        self.assertIn("G5Q-1A-DC5", bom_text)

    def test_draft_pcb_net_application_is_documented(self):
        script = REPO_ROOT / "scripts" / "apply-draft-pcb-nets.py"
        doc = PROJECT_DIR / "docs" / "draft_pcb_circuit_design.md"
        self.assertTrue(script.exists())
        self.assertTrue(doc.exists())

        doc_text = doc.read_text(encoding="utf-8")
        for net in ["ICM_24VAC_SOURCE", "HEAT_CHAIN_K1_K2", "TH_HEAT_REQUEST_OUT"]:
            self.assertIn(net, doc_text)


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

        drc = json.loads((REPO_ROOT / "reports" / "drc.json").read_text(encoding="utf-8"))
        blocker_types = {
            "clearance",
            "courtyards_overlap",
            "drill_out_of_range",
            "hole_near_hole",
            "items_not_allowed",
            "pth_inside_courtyard",
            "shorting_items",
            "tracks_crossing",
        }
        blockers = [violation for violation in drc["violations"] if violation["type"] in blocker_types]
        self.assertEqual(blockers, [], "Draft PCB should have no electrical/mechanical blocker DRC items")

    def test_critical_heat_request_nets_are_applied_to_pcb(self):
        try:
            import pcbnew
        except ImportError as exc:
            self.skipTest(f"pcbnew Python module is not available: {exc}")

        board = pcbnew.LoadBoard(str(BOARD))
        refs = {fp.GetReference(): fp for fp in board.GetFootprints()}

        expected_pad_nets = {
            ("J2", "5"): "ICM_24VAC_SOURCE",
            ("K1", "2"): "ICM_24VAC_SOURCE",
            ("K1", "3"): "HEAT_CHAIN_K1_K2",
            ("K2", "2"): "HEAT_CHAIN_K1_K2",
            ("K2", "3"): "TH_HEAT_REQUEST_OUT",
            ("J2", "2"): "TH_HEAT_REQUEST_OUT",
        }

        for (ref, pad_no), net in expected_pad_nets.items():
            pads = {pad.GetNumber(): pad for pad in refs[ref].Pads()}
            self.assertEqual(pads[pad_no].GetNetname(), net)

        routed_nets = {track.GetNetname() for track in board.GetTracks()}
        for net in ["ICM_24VAC_SOURCE", "HEAT_CHAIN_K1_K2", "TH_HEAT_REQUEST_OUT"]:
            self.assertIn(net, routed_nets)


if __name__ == "__main__":
    unittest.main()
