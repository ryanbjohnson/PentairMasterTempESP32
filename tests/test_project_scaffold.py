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

    def test_ui_remote_sheet_captures_external_control_connector(self):
        ui_sheet = (PROJECT_DIR / "sheets" / "ui_remote.kicad_sch").read_text(encoding="utf-8")

        required_phrases = [
            'lib_id "mastertemp_esp32:ExternalControl_3P"',
            'Reference" "J5"',
            'Value" "EXT_CONTROL"',
            "SPA_LINE",
            "COMMON_LINE",
            "POOL_LINE",
            'Reference" "U19"',
            'Reference" "U20"',
            "REMOTE_SPA_SENSE",
            "REMOTE_POOL_SENSE",
            "ISO_REMOTE_5V",
            'lib_id "mastertemp_esp32:MembraneReference_9P"',
            'Reference" "J6"',
            'Value" "MEMBRANE_REF"',
            "no keypad/display electronics designed",
        ]

        for phrase in required_phrases:
            self.assertIn(phrase, ui_sheet)

    def test_control_board_schematic_pass_notes_exist(self):
        icm_sheet = (PROJECT_DIR / "sheets" / "icm_interface.kicad_sch").read_text(encoding="utf-8")
        safety_sheet = (PROJECT_DIR / "sheets" / "safety_inputs.kicad_sch").read_text(encoding="utf-8")

        self.assertIn("J2 OPERATING CONTROL TERMINALS", icm_sheet)
        self.assertIn("ICM_24VAC_SOURCE -> K1_COM -> K1_NO -> K2_COM -> K2_NO -> TH_HEAT_REQUEST_OUT", icm_sheet)
        self.assertIn("VAL and GAS are diagnostic monitor inputs only", icm_sheet)
        self.assertIn('lib_id "mastertemp_esp32:H11AA1M"', icm_sheet)
        self.assertIn("AC_IN_1", icm_sheet)
        self.assertIn("COLLECTOR", icm_sheet)
        self.assertIn("J3 SAFETY STACK TERMINALS", safety_sheet)
        self.assertIn("STATIC HEAT ENABLE CHAIN", safety_sheet)
        self.assertIn("AFS DYNAMIC POLICY", safety_sheet)

    def test_candidate_parts_are_placed_on_pcb(self):
        board = BOARD.read_text(encoding="utf-8")
        required_refs = [
            "J1", "J2", "J3", "J4", "J5", "J6",
            "K1", "K2", "D2", "D3",
            "U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8",
            "U9", "U10", "U11", "U12", "U14", "U16", "U17", "U18",
            "U19", "U20",
            "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12",
            "R13", "R14", "R15", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", "R24", "R25", "R26", "R27", "R28", "R29", "R30", "R31",
            "R32", "R33", "R34", "R35", "R36", "R37", "R38", "R39",
            "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11",
            "Q1", "Q2",
            "TP1", "TP2", "TP3", "TP4", "TP5", "TP6", "TP7", "TP8", "TP9",
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
        self.assertEqual(drc["violations"], [], "Draft PCB should have no regular PCB DRC items")
        self.assertEqual(drc["unconnected_items"], [], "Draft PCB should have no unrouted PCB items")

        parity = json.loads((REPO_ROOT / "reports" / "drc-parity.json").read_text(encoding="utf-8"))
        self.assertEqual(parity["schematic_parity"], [], "Draft PCB should have no schematic parity items")

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

        route_layers = {
            (track.GetNetname(), board.GetLayerName(track.GetLayer()))
            for track in board.GetTracks()
        }
        self.assertIn(("ICM_24VAC_SOURCE", "F.Cu"), route_layers)
        self.assertIn(("HEAT_CHAIN_K1_K2", "B.Cu"), route_layers)
        self.assertIn(("TH_HEAT_REQUEST_OUT", "B.Cu"), route_layers)

    def test_power_tree_nets_are_applied_to_pcb(self):
        try:
            import pcbnew
        except ImportError as exc:
            self.skipTest(f"pcbnew Python module is not available: {exc}")

        board = pcbnew.LoadBoard(str(BOARD))
        refs = {fp.GetReference(): fp for fp in board.GetFootprints()}

        expected_pad_nets = {
            ("J1", "1"): "VAC24_A",
            ("J1", "2"): "VAC24_B",
            ("J1", "3"): "CHASSIS_SHIELD",
            ("F1", "1"): "VAC24_A_FUSED",
            ("F1", "2"): "VAC24_A",
            ("MOV1", "1"): "VAC24_A_FUSED",
            ("MOV1", "2"): "VAC24_B",
            ("TVS1", "1"): "VAC24_A_FUSED",
            ("TVS1", "2"): "VAC24_B",
            ("D1", "1"): "VAC24_A_FUSED",
            ("D1", "2"): "VAC24_B",
            ("D1", "3"): "VRAW",
            ("D1", "4"): "PGND_RAW",
            ("C1", "1"): "VRAW",
            ("C1", "2"): "PGND_RAW",
            ("U1", "1"): "PGND_RAW",
            ("U1", "2"): "VRAW",
            ("U1", "3"): "VRAW",
            ("U1", "4"): "RON_5V_TBD",
            ("U1", "5"): "FB_5V_TBD",
            ("U1", "6"): "+5V_PGOOD",
            ("U1", "7"): "BST_5V",
            ("U1", "8"): "SW_5V",
            ("U1", "9"): "PGND_RAW",
            ("L1", "1"): "SW_5V",
            ("L1", "2"): "+5V",
            ("C4", "1"): "VRAW",
            ("C4", "2"): "PGND_RAW",
            ("C5", "1"): "BST_5V",
            ("C5", "2"): "SW_5V",
            ("R5", "1"): "+5V",
            ("R5", "2"): "FB_5V_TBD",
            ("R6", "1"): "FB_5V_TBD",
            ("R6", "2"): "PGND_RAW",
            ("R7", "1"): "RON_5V_TBD",
            ("R7", "2"): "PGND_RAW",
            ("D2", "1"): "+5V_RELAY",
            ("D2", "2"): "K1_COIL_LOW",
            ("D3", "1"): "+5V_RELAY",
            ("D3", "2"): "K2_COIL_LOW",
            ("U2", "1"): "+3V3",
            ("U2", "2"): "+5V",
            ("U2", "3"): "+5V",
            ("U2", "4"): "SW_3V3",
            ("U2", "5"): "GND",
            ("U2", "6"): "BST_3V3",
            ("L2", "1"): "SW_3V3",
            ("L2", "2"): "+3V3",
            ("C6", "1"): "BST_3V3",
            ("C6", "2"): "SW_3V3",
            ("C7", "1"): "+5V",
            ("C7", "2"): "GND",
            ("C8", "1"): "+3V3",
            ("C8", "2"): "GND",
            ("U3", "1"): "BROWNOUT_OK",
            ("U3", "2"): "GND",
            ("U3", "3"): "+3V3",
            ("U5", "1"): "GND",
            ("U5", "2"): "+3V3",
            ("U6", "21"): "VAL_OPTO_GPIO",
            ("U6", "22"): "TH_OPTO_GPIO",
            ("U6", "23"): "IND_OPTO_GPIO",
            ("U6", "24"): "VAC24_OPTO_GPIO",
            ("R8", "1"): "VAL_SENSE_AC",
            ("R8", "2"): "VAL_OPTO_LIMIT_A",
            ("R9", "1"): "VAL_OPTO_LIMIT_A",
            ("R9", "2"): "VAL_OPTO_INPUT",
            ("R13", "1"): "TH_HEAT_REQUEST_OUT",
            ("R13", "2"): "TH_OPTO_LIMIT_A",
            ("R14", "1"): "TH_OPTO_LIMIT_A",
            ("R14", "2"): "TH_OPTO_INPUT",
            ("R15", "1"): "TH_OPTO_GPIO",
            ("R15", "2"): "+3V3",
            ("U9", "1"): "TH_OPTO_INPUT",
            ("U9", "2"): "ICM_GND_REF",
            ("U9", "4"): "GND",
            ("U9", "5"): "TH_OPTO_GPIO",
            ("R16", "1"): "IND_SENSE_AC",
            ("R16", "2"): "IND_OPTO_LIMIT_A",
            ("R17", "1"): "IND_OPTO_LIMIT_A",
            ("R17", "2"): "IND_OPTO_INPUT",
            ("R18", "1"): "IND_OPTO_GPIO",
            ("R18", "2"): "+3V3",
            ("U10", "1"): "IND_OPTO_INPUT",
            ("U10", "2"): "ICM_GND_REF",
            ("U10", "4"): "GND",
            ("U10", "5"): "IND_OPTO_GPIO",
            ("R19", "1"): "ICM_24VAC_SOURCE",
            ("R19", "2"): "VAC24_OPTO_LIMIT_A",
            ("R20", "1"): "VAC24_OPTO_LIMIT_A",
            ("R20", "2"): "VAC24_OPTO_INPUT",
            ("R21", "1"): "VAC24_OPTO_GPIO",
            ("R21", "2"): "+3V3",
            ("U12", "1"): "VAC24_OPTO_INPUT",
            ("U12", "2"): "ICM_GND_REF",
            ("U12", "4"): "GND",
            ("U12", "5"): "VAC24_OPTO_GPIO",
            ("U11", "1"): "VAL_OPTO_INPUT",
            ("U11", "2"): "ICM_GND_REF",
            ("U11", "4"): "GND",
            ("U11", "5"): "VAL_OPTO_GPIO",
            ("R10", "1"): "RELAY_K1_GATE",
            ("R10", "2"): "GND",
            ("R11", "1"): "RELAY_K2_GATE",
            ("R11", "2"): "GND",
            ("R22", "1"): "RELAY_K1_GATE_DRIVE",
            ("R22", "2"): "RELAY_K1_GATE",
            ("R23", "1"): "RELAY_K2_GATE_DRIVE",
            ("R23", "2"): "RELAY_K2_GATE",
            ("R24", "1"): "+3V3_ADC",
            ("R24", "2"): "THERMISTOR_ADC",
            ("R25", "1"): "+3V3",
            ("R25", "2"): "I2C_SDA",
            ("R26", "1"): "+3V3",
            ("R26", "2"): "I2C_SCL",
            ("R27", "1"): "SFS_INPUT",
            ("R27", "2"): "SFS_FIELD_INPUT",
            ("R28", "1"): "VRAW",
            ("R28", "2"): "VRAW_MONITOR_ADC",
            ("R29", "1"): "VRAW_MONITOR_ADC",
            ("R29", "2"): "AGND",
            ("R30", "1"): "+3V3",
            ("R30", "2"): "THERMISTOR_RANGE_OK",
            ("R31", "1"): "+3V3",
            ("R31", "2"): "SFS_RANGE_OK",
            ("R32", "1"): "+3V3_ADC",
            ("R32", "2"): "THERM_LOW_REF_TBD",
            ("R33", "1"): "THERM_LOW_REF_TBD",
            ("R33", "2"): "AGND",
            ("R34", "1"): "+3V3_ADC",
            ("R34", "2"): "THERM_HIGH_REF_TBD",
            ("R35", "1"): "THERM_HIGH_REF_TBD",
            ("R35", "2"): "AGND",
            ("R36", "1"): "+3V3_ADC",
            ("R36", "2"): "SFS_LOW_REF_TBD",
            ("R37", "1"): "SFS_LOW_REF_TBD",
            ("R37", "2"): "AGND",
            ("R38", "1"): "+3V3_ADC",
            ("R38", "2"): "SFS_HIGH_REF_TBD",
            ("R39", "1"): "SFS_HIGH_REF_TBD",
            ("R39", "2"): "AGND",
            ("C9", "1"): "THERMISTOR_ADC",
            ("C9", "2"): "AGND",
            ("C10", "1"): "SFS_ADC",
            ("C10", "2"): "AGND",
            ("C11", "1"): "VRAW_MONITOR_ADC",
            ("C11", "2"): "AGND",
            ("U7", "8"): "VRAW_MONITOR_ADC",
            ("R12", "1"): "VAL_OPTO_GPIO",
            ("R12", "2"): "+3V3",
            ("Q1", "2"): "GND",
            ("Q2", "2"): "GND",
            ("TP1", "1"): "VRAW",
            ("TP2", "1"): "+5V",
            ("TP3", "1"): "+3V3",
            ("TP4", "1"): "WATCHDOG_OK",
            ("TP5", "1"): "SAFETY_STATIC_OK",
            ("TP6", "1"): "K1_COIL_LOW",
            ("TP7", "1"): "K2_COIL_LOW",
            ("TP8", "1"): "TH_FEEDBACK",
            ("TP9", "1"): "VAL_SENSE_AC",
        }

        for (ref, pad_no), net in expected_pad_nets.items():
            pads = [pad for pad in refs[ref].Pads() if pad.GetNumber() == pad_no]
            self.assertTrue(pads, f"{ref} pad {pad_no} should exist")
            for pad in pads:
                self.assertEqual(pad.GetNetname(), net)

        self.assertEqual(refs["D1"].GetFPIDAsString(), "Diode_SMD:Diode_Bridge_Vishay_MBLS")
        self.assertEqual(refs["U1"].GetFPIDAsString(), "Package_SO:TI_SO-PowerPAD-8")

        routed_nets = {track.GetNetname() for track in board.GetTracks()}
        for net in [
            "VAC24_A_FUSED", "VAC24_B", "VRAW", "PGND_RAW", "SW_5V", "BST_5V", "+5V", "+3V3", "+5V_RELAY",
            "K1_COIL_LOW", "K2_COIL_LOW", "REMOTE_SPA_SENSE", "REMOTE_POOL_SENSE",
            "SPA_LINE", "POOL_LINE", "ISO_REMOTE_5V",
            "SPA_LED_A", "POOL_LED_A", "WATCHDOG_OK", "VAL_SENSE_AC",
            "VAL_OPTO_LIMIT_A", "VAL_OPTO_INPUT", "ICM_GND_REF", "VAL_OPTO_GPIO",
            "TH_OPTO_LIMIT_A", "TH_OPTO_INPUT", "TH_OPTO_GPIO",
            "IND_SENSE_AC", "IND_OPTO_LIMIT_A", "IND_OPTO_INPUT", "IND_OPTO_GPIO",
            "VAC24_OPTO_LIMIT_A", "VAC24_OPTO_INPUT", "VAC24_OPTO_GPIO",
            "RELAY_K1_GATE", "RELAY_K2_GATE",
            "+3V3_ADC", "AGND", "THERMISTOR_ADC",
            "I2C_SDA", "I2C_SCL",
            "SFS_INPUT", "SFS_FIELD_INPUT", "SFS_ADC", "VRAW_MONITOR_ADC",
            "THERMISTOR_RANGE_OK", "SFS_RANGE_OK",
            "THERM_LOW_REF_TBD", "THERM_HIGH_REF_TBD", "SFS_LOW_REF_TBD", "SFS_HIGH_REF_TBD",
        ]:
            self.assertIn(net, routed_nets)

        via_nets = {
            track.GetNetname()
            for track in board.GetTracks()
            if isinstance(track, pcbnew.PCB_VIA)
        }
        for net in ["GND", "+5V", "PGND_RAW", "WATCHDOG_OK", "VAC24_A_FUSED", "BST_5V", "VAL_SENSE_AC", "TH_OPTO_GPIO", "IND_OPTO_GPIO", "IND_SENSE_AC", "VAC24_OPTO_GPIO", "ICM_24VAC_SOURCE", "THERMISTOR_ADC", "I2C_SDA", "I2C_SCL", "SFS_INPUT", "SFS_ADC", "VRAW_MONITOR_ADC", "THERM_LOW_REF_TBD", "THERM_HIGH_REF_TBD", "SFS_LOW_REF_TBD", "SFS_HIGH_REF_TBD"]:
            self.assertIn(net, via_nets)

    def test_manufacturing_silkscreen_warnings_are_readable(self):
        try:
            import pcbnew
        except ImportError as exc:
            self.skipTest(f"pcbnew Python module is not available: {exc}")

        board = pcbnew.LoadBoard(str(BOARD))
        silk_texts = {}
        for drawing in board.GetDrawings():
            if not isinstance(drawing, pcbnew.PCB_TEXT):
                continue
            if board.GetLayerName(drawing.GetLayer()) != "F.Silkscreen":
                continue
            silk_texts[drawing.GetText()] = drawing

        expected_warnings = {
            "NO LINE VOLTAGE": (1.20, 0.18),
            "VAL / GAS MONITOR ONLY - NO DRIVE": (0.90, 0.14),
            "24 VAC FIELD / POWER ZONE": (1.50, 0.20),
            "ESP32 / LOGIC ZONE": (1.50, 0.20),
        }
        for text, (min_height, min_thickness) in expected_warnings.items():
            self.assertIn(text, silk_texts)
            self.assertGreaterEqual(pcbnew.ToMM(silk_texts[text].GetTextHeight()), min_height)
            self.assertGreaterEqual(pcbnew.ToMM(silk_texts[text].GetTextThickness()), min_thickness)


if __name__ == "__main__":
    unittest.main()
