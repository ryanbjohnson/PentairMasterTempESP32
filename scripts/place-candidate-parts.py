#!/usr/bin/env python3
"""Place first-pass candidate footprints on the MasterTemp control PCB.

This is intentionally placement-only: schematic symbols and final net
assignments still need to be captured before release routing.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pcbnew


REPO_ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = REPO_ROOT / "pcb" / "mastertemp_esp32" / "mastertemp_esp32.kicad_pcb"


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def load_fp(lib: str, name: str) -> pcbnew.FOOTPRINT:
    fp = pcbnew.FootprintLoad(str(Path("/usr/share/kicad/footprints") / f"{lib}.pretty"), name)
    if fp is None:
        raise RuntimeError(f"Could not load footprint {lib}:{name}")
    return fp


def load_part_footprint(ref: str, lib: str, name: str) -> pcbnew.FOOTPRINT:
    try:
        return load_fp(lib, name)
    except Exception as exc:
        raise RuntimeError(f"Could not load footprint for {ref}: {lib}:{name}") from exc

SYNC_FPID_REFS = {
    "J1", "F1", "MOV1", "TVS1", "D1", "C1", "U1", "L1", "U2", "L2", "U3",
    "C4", "C5", "C6", "C7", "C8", "R5", "R6", "R7",
    "D2", "D3",
    "J5", "J6", "U19", "U20", "R1", "R2", "R3", "R4", "C2", "C3",
}

FORCE_RELOAD_REFS = {"U5"}


PARTS = [
    # ref, value, library, footprint, x, y, rotation degrees
    ("J1", "24VAC_IN", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_3-G-5,08_1x03_P5.08mm_Horizontal", 34, 34, 0),
    ("J2", "OPERATING_CONTROL", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_7-G-5,08_1x07_P5.08mm_Horizontal", 44, 104, 0),
    ("J3", "SAFETY_STACK", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_7-G-5,08_1x07_P5.08mm_Horizontal", 84, 104, 0),
    ("J4", "THERMISTOR", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_2-G-5,08_1x02_P5.08mm_Horizontal", 132, 104, 0),
    ("J5", "EXT_CONTROL", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_3-G-5,08_1x03_P5.08mm_Horizontal", 160, 104, 0),
    ("J6", "MEMBRANE_REF", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBVA_2,5_9-G-5,08_1x09_P5.08mm_Vertical", 176, 96, 90),
    ("K1", "G5Q-1A-DC5", "Relay_THT", "Relay_SPST_Omron-G5Q-1A", 43, 88, 0),
    ("K2", "G5Q-1A-DC5", "Relay_THT", "Relay_SPST_Omron-G5Q-1A", 66, 88, 0),
    ("D2", "K1_FLYBACK_TBD", "Diode_SMD", "D_SOD-123", 38, 84, 270),
    ("D3", "K2_FLYBACK_TBD", "Diode_SMD", "D_SOD-123", 70, 76, 270),
    ("U1", "LM5164DDAR", "Package_SO", "TI_SO-PowerPAD-8", 55, 66, 0),
    ("L1", "68uH", "Inductor_SMD", "L_12x12mm_H8mm", 70, 66, 0),
    ("D1", "MB10S", "Diode_SMD", "Diode_Bridge_Vishay_MBLS", 54, 50, 0),
    ("TVS1", "SMBJ51CA", "Diode_SMD", "D_SMB", 63, 47, 0),
    ("C1", "470uF_63V", "Capacitor_THT", "CP_Radial_D10.0mm_P5.00mm", 73, 47, 0),
    ("F1", "0.5A_FUSE", "Fuse", "Fuse_1206_3216Metric", 29, 47, 0),
    ("MOV1", "V47ZA1P", "Varistor", "RV_Disc_D7mm_W3.9mm_P5mm", 37, 47, 0),
    ("U2", "AP63203WU-7", "Package_TO_SOT_SMD", "TSOT-23-6", 95, 66, 0),
    ("L2", "2.2uH", "Inductor_SMD", "L_Vishay_IFSC-1515AH_4x4x1.8mm", 103, 66, 0),
    ("U3", "TPS3839G33DBZR", "Package_TO_SOT_SMD", "SOT-23-3", 110, 48, 0),
    ("C4", "2.2uF_100V_VRAW_IN_TBD", "Capacitor_SMD", "C_1210_3225Metric", 55, 60, 180),
    ("C5", "2.2nF_50V_BST_5V", "Capacitor_SMD", "C_0603_1608Metric", 61, 62, 0),
    ("R5", "RFB5V_TOP_TBD", "Resistor_SMD", "R_0805_2012Metric", 61, 70, 180),
    ("R6", "RFB5V_BOT_TBD", "Resistor_SMD", "R_0805_2012Metric", 61, 73, 0),
    ("R7", "RON5V_TBD", "Resistor_SMD", "R_0805_2012Metric", 55, 72, 0),
    ("C6", "100nF_BST_3V3", "Capacitor_SMD", "C_0603_1608Metric", 98.5, 66, 270),
    ("C7", "10uF_50V_3V3_IN_TBD", "Capacitor_SMD", "C_1210_3225Metric", 95, 70, 0),
    ("C8", "22uF_10V_3V3_OUT_TBD", "Capacitor_SMD", "C_0805_2012Metric", 107, 70, 0),
    ("U4", "TPS3823-33DBVR", "Package_TO_SOT_SMD", "SOT-23-5", 120, 48, 0),
    ("U5", "ESP32-WROOM-32E-N16", "RF_Module", "ESP32-WROOM-32E", 153, 55, 0),
    ("U6", "MCP23017-E/SS", "Package_SO", "SSOP-28_5.3x10.2mm_P0.65mm", 114, 61, 0),
    ("U7", "ADS1115IDGSR", "Package_SO", "VSSOP-10_3x3mm_P0.5mm", 114, 78, 0),
    ("U14", "THERMISTOR_AFE_TBD", "Package_TO_SOT_SMD", "SOT-23-6", 148, 82, 0),
    ("U8", "NXE1S0505MC-R7", "Converter_DCDC", "Converter_DCDC_Murata_NXExSxxxxMC_SMD", 95, 87, 0),
    ("U9", "H11AA1M_TH", "Package_DIP", "DIP-6_W7.62mm", 31, 56, 0),
    ("U10", "H11AA1M_IND", "Package_DIP", "DIP-6_W7.62mm", 31, 69, 0),
    ("U11", "H11AA1M_VAL", "Package_DIP", "DIP-6_W7.62mm", 41, 56, 0),
    ("U12", "H11AA1M_24VAC", "Package_DIP", "DIP-6_W7.62mm", 41, 69, 0),
    ("U16", "TLV6700DDCR_THERM", "Package_TO_SOT_SMD", "SOT-23-6", 124, 75, 0),
    ("U17", "TLV6700DDCR_SFS", "Package_TO_SOT_SMD", "SOT-23-6", 124, 83, 0),
    ("U18", "OPA333AIDBVR", "Package_TO_SOT_SMD", "SOT-23-5", 134, 78, 0),
    ("U19", "LTV-817S_SPA_CANDIDATE", "Package_DIP", "DIP-4_W7.62mm", 116, 94, 0),
    ("U20", "LTV-817S_POOL_CANDIDATE", "Package_DIP", "DIP-4_W7.62mm", 127, 94, 0),
    ("R1", "2.2k_REMOTE_WET_TBD", "Resistor_SMD", "R_0805_2012Metric", 116, 100, 0),
    ("R2", "2.2k_REMOTE_WET_TBD", "Resistor_SMD", "R_0805_2012Metric", 127, 100, 0),
    ("R3", "10k_REMOTE_PULLUP", "Resistor_SMD", "R_0805_2012Metric", 116, 88, 0),
    ("R4", "10k_REMOTE_PULLUP", "Resistor_SMD", "R_0805_2012Metric", 127, 88, 0),
    ("R8", "VAL_OPTO_LIMIT_A_TBD", "Resistor_SMD", "R_0805_2012Metric", 24, 64, 0),
    ("R9", "VAL_OPTO_LIMIT_B_TBD", "Resistor_SMD", "R_0805_2012Metric", 29, 64, 0),
    ("R10", "K1_GATE_PULLDOWN_TBD", "Resistor_SMD", "R_0805_2012Metric", 30.5, 101.5, 0),
    ("R11", "K2_GATE_PULLDOWN_TBD", "Resistor_SMD", "R_0805_2012Metric", 70.5, 98.5, 0),
    ("R12", "VAL_OPTO_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 124.5, 50.0, 0),
    ("R13", "TH_OPTO_LIMIT_A_TBD", "Resistor_SMD", "R_0805_2012Metric", 22, 56, 0),
    ("R14", "TH_OPTO_LIMIT_B_TBD", "Resistor_SMD", "R_0805_2012Metric", 26, 56, 0),
    ("R15", "TH_OPTO_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 130.5, 50.0, 0),
    ("R16", "IND_OPTO_LIMIT_A_TBD", "Resistor_SMD", "R_0805_2012Metric", 24, 69, 0),
    ("R17", "IND_OPTO_LIMIT_B_TBD", "Resistor_SMD", "R_0805_2012Metric", 28, 69, 0),
    ("R18", "IND_OPTO_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 136.5, 50.0, 0),
    ("R19", "VAC24_OPTO_LIMIT_A_TBD", "Resistor_SMD", "R_0805_2012Metric", 32, 78, 180),
    ("R20", "VAC24_OPTO_LIMIT_B_TBD", "Resistor_SMD", "R_0805_2012Metric", 28, 78, 180),
    ("R21", "VAC24_OPTO_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 136.5, 54.0, 0),
    ("R22", "K1_GATE_SERIES_TBD", "Resistor_SMD", "R_0805_2012Metric", 26.0, 98.0, 0),
    ("R23", "K2_GATE_SERIES_TBD", "Resistor_SMD", "R_0805_2012Metric", 68.0, 95.0, 0),
    ("R24", "THERM_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 153.0, 86.0, 0),
    ("R25", "I2C_SDA_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 103.0, 58.8, 180),
    ("R26", "I2C_SCL_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 103.0, 56.0, 180),
    ("R27", "SFS_INPUT_SERIES_TBD", "Resistor_SMD", "R_0805_2012Metric", 130.0, 77.05, 0),
    ("R28", "VRAW_MON_TOP_TBD", "Resistor_SMD", "R_0805_2012Metric", 101.0, 40.0, 0),
    ("R29", "VRAW_MON_BOT_TBD", "Resistor_SMD", "R_0805_2012Metric", 134.0, 70.0, 0),
    ("R30", "THERM_RANGE_OK_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 128.0, 74.0, 0),
    ("R31", "SFS_RANGE_OK_PULLUP_TBD", "Resistor_SMD", "R_0805_2012Metric", 132.0, 84.0, 90),
    ("R32", "THERM_LOW_REF_TOP_TBD", "Resistor_SMD", "R_0805_2012Metric", 162.0, 82.0, 0),
    ("R33", "THERM_LOW_REF_BOT_TBD", "Resistor_SMD", "R_0805_2012Metric", 166.0, 82.0, 0),
    ("R34", "THERM_HIGH_REF_TOP_TBD", "Resistor_SMD", "R_0805_2012Metric", 162.0, 88.0, 0),
    ("R35", "THERM_HIGH_REF_BOT_TBD", "Resistor_SMD", "R_0805_2012Metric", 166.0, 88.0, 0),
    ("R36", "SFS_LOW_REF_TOP_TBD", "Resistor_SMD", "R_0805_2012Metric", 162.0, 90.0, 0),
    ("R37", "SFS_LOW_REF_BOT_TBD", "Resistor_SMD", "R_0805_2012Metric", 166.0, 90.0, 0),
    ("R38", "SFS_HIGH_REF_TOP_TBD", "Resistor_SMD", "R_0805_2012Metric", 162.0, 94.0, 0),
    ("R39", "SFS_HIGH_REF_BOT_TBD", "Resistor_SMD", "R_0805_2012Metric", 166.0, 94.0, 0),
    ("C2", "100nF_REMOTE_FILTER_TBD", "Capacitor_SMD", "C_0805_2012Metric", 116, 91, 0),
    ("C3", "100nF_REMOTE_FILTER_TBD", "Capacitor_SMD", "C_0805_2012Metric", 127, 91, 0),
    ("C9", "THERM_ADC_FILTER_TBD", "Capacitor_SMD", "C_0805_2012Metric", 157.0, 86.0, 0),
    ("C10", "SFS_ADC_FILTER_TBD", "Capacitor_SMD", "C_0805_2012Metric", 138.0, 75.0, 0),
    ("C11", "VRAW_MON_FILTER_TBD", "Capacitor_SMD", "C_0805_2012Metric", 134.0, 72.5, 0),
    ("Q1", "AO3400A", "Package_TO_SOT_SMD", "SOT-23", 34, 96, 0),
    ("Q2", "AO3400A", "Package_TO_SOT_SMD", "SOT-23", 78, 96, 0),
]

TEST_POINTS = [
    ("TP1", "VRAW", 98, 36),
    ("TP2", "+5V", 106, 36),
    ("TP3", "+3V3", 114, 36),
    ("TP4", "WATCHDOG_OK", 122, 36),
    ("TP5", "SAFETY_STATIC_OK", 126, 36),
    ("TP6", "K1_COIL", 31, 88),
    ("TP7", "K2_COIL", 82, 93),
    ("TP8", "TH_FEEDBACK", 114, 43),
    ("TP9", "VAL_SENSE", 122, 43),
]


INTERNAL_REFS_WITH_DENSE_SILK = {
    "C2", "C3", "C4", "C7",
    "R5", "R6", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", "R24", "R25", "R26", "R27", "R28", "R29", "R30", "R31", "R32", "R33", "R34", "R35", "R36", "R37", "R38", "R39", "C11",
    "U1", "U10", "U12", "U16", "U17", "U18",
    "U14",
    "Q1",
}


BOARD_NOTES_FOR_FAB_DRAWING = {
    "J1 POWER 3P\n24 VAC CLASS II ONLY",
    "J2 OPERATING CONTROL 7P\nVAL TH IND GND 24VAC 24VAC FS",
    "J3 SAFETY STACK 7P\nPS HLS ES1 AFS AGS SFS GAS",
    "J5 EXT CTRL 3P\nSPA COMMON POOL",
    "J6 MEMBRANE REF 9P\nKEYPAD OUT OF SCOPE",
    "J6 SERVICE UART",
    "U5 ESP32-WROOM\nANTENNA TOWARD EDGE",
    "ICM TH RELAY CONTACT ZONE",
    "NO LINE VOLTAGE ON CONTROL TERMINALS",
    "GAS MONITOR ONLY - NO DRIVE",
}


FAB_WARNING_TEXT = {
    "NO LINE VOLTAGE": (105.0, 23.5, 1.20, 0.18),
}


def ensure_text(board: pcbnew.BOARD, text: str, x: float, y: float, size: float, thickness: float) -> None:
    for drawing in board.GetDrawings():
        if isinstance(drawing, pcbnew.PCB_TEXT) and drawing.GetText() == text:
            drawing.SetLayer(pcbnew.F_SilkS)
            drawing.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
            drawing.SetTextHeight(mm(size))
            drawing.SetTextWidth(mm(size))
            drawing.SetTextThickness(mm(thickness))
            return

    drawing = pcbnew.PCB_TEXT(board)
    drawing.SetText(text)
    drawing.SetLayer(pcbnew.F_SilkS)
    drawing.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    drawing.SetTextHeight(mm(size))
    drawing.SetTextWidth(mm(size))
    drawing.SetTextThickness(mm(thickness))
    board.Add(drawing)


def apply_silkscreen_cleanup(board: pcbnew.BOARD, footprints: list[pcbnew.FOOTPRINT]) -> None:
    """Keep generated silkscreen DRC-clean while preserving placement notes."""
    for fp in footprints:
        if not hasattr(fp, "Value") or not hasattr(fp, "Reference"):
            continue
        ref = fp.GetReference()
        value_text = fp.Value()
        reference_text = fp.Reference()
        if not hasattr(value_text, "SetVisible") or not hasattr(reference_text, "SetVisible"):
            continue

        # Assembly values remain available in footprint properties; putting all
        # values on the board silkscreen makes the dense prototype unreadable.
        value_text.SetVisible(False)

        if ref in INTERNAL_REFS_WITH_DENSE_SILK:
            reference_text.SetVisible(False)

    for drawing in board.GetDrawings():
        if not isinstance(drawing, pcbnew.PCB_TEXT):
            continue
        if drawing.GetLayer() != pcbnew.F_SilkS:
            continue
        if drawing.GetText() in BOARD_NOTES_FOR_FAB_DRAWING or drawing.GetText().startswith("J4 THERM"):
            drawing.SetLayer(pcbnew.Cmts_User)

    for text, (x, y, size, thickness) in FAB_WARNING_TEXT.items():
        ensure_text(board, text, x, y, size, thickness)


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    existing = {fp.GetReference(): fp for fp in board.GetFootprints()}
    reloaded_footprint = False

    for ref, value, lib, name, x, y, rot in PARTS:
        fp = existing.get(ref)
        should_reload = (
            fp is not None
            and ref in SYNC_FPID_REFS
            and fp.GetFPIDAsString().split(":")[-1] != name
        )
        should_reload = should_reload or (
            fp is not None
            and ref in FORCE_RELOAD_REFS
            and not os.environ.get("PLACER_FORCE_RELOADED")
        )
        if should_reload:
            replacement = load_part_footprint(ref, lib, name)
            replacement.SetReference(ref)
            board.Remove(fp)
            board.Add(replacement)
            existing[ref] = replacement
            fp = replacement
            reloaded_footprint = True
            pcbnew.SaveBoard(str(BOARD_PATH), board)
            env = os.environ.copy()
            env["PLACER_FORCE_RELOADED"] = "1"
            os.execve(sys.executable, [sys.executable, __file__], env)
        if fp is None:
            fp = load_part_footprint(ref, lib, name)
            fp.SetReference(ref)
            board.Add(fp)
            existing[ref] = fp
        fp.SetValue(value)
        if ref == "U5":
            fp.SetFPID(pcbnew.LIB_ID("", name))
        else:
            fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetDNP(ref == "J6")
        fp.SetExcludedFromBOM(ref == "J6")
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(rot)

    if reloaded_footprint:
        pcbnew.SaveBoard(str(BOARD_PATH), board)
        env = os.environ.copy()
        env["PLACER_FORCE_RELOADED"] = "1"
        os.execve(sys.executable, [sys.executable, __file__], env)

    for ref, value, x, y in TEST_POINTS:
        fp = existing.get(ref)
        if fp is None:
            fp = load_fp("TestPoint", "TestPoint_Pad_D2.0mm")
            fp.SetReference(ref)
            board.Add(fp)
        fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))

    apply_silkscreen_cleanup(board, list(existing.values()))
    pcbnew.SaveBoard(str(BOARD_PATH), board)


if __name__ == "__main__":
    main()
