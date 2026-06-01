#!/usr/bin/env python3
"""Place first-pass candidate footprints on the MasterTemp control PCB.

This is intentionally placement-only: schematic symbols and final net
assignments still need to be captured before release routing.
"""

from __future__ import annotations

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


PARTS = [
    # ref, value, library, footprint, x, y, rotation degrees
    ("J1", "24VAC_IN", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_3-G-5,08_1x03_P5.08mm_Horizontal", 34, 34, 0),
    ("J2", "OPERATING_CONTROL", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_7-G-5,08_1x07_P5.08mm_Horizontal", 44, 104, 0),
    ("J3", "SAFETY_STACK", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_7-G-5,08_1x07_P5.08mm_Horizontal", 84, 104, 0),
    ("J4", "THERMISTOR", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_2-G-5,08_1x02_P5.08mm_Horizontal", 132, 104, 0),
    ("J5", "EXT_CONTROL", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_3-G-5,08_1x03_P5.08mm_Horizontal", 160, 104, 0),
    ("J6", "MEMBRANE_REF", "Connector_Phoenix_MSTB", "PhoenixContact_MSTBA_2,5_9-G-5,08_1x09_P5.08mm_Horizontal", 135, 84, 0),
    ("K1", "G5Q-1A-DC5", "Relay_THT", "Relay_SPST_Omron-G5Q-1A", 43, 88, 0),
    ("K2", "G5Q-1A-DC5", "Relay_THT", "Relay_SPST_Omron-G5Q-1A", 66, 88, 0),
    ("U1", "LM5164YDRCR", "Package_SON", "Texas_S-PVSON-N10", 55, 66, 0),
    ("L1", "68uH", "Inductor_SMD", "L_12x12mm_H8mm", 70, 66, 0),
    ("D1", "MB10S", "Package_SO", "SOIC-4_4.55x3.7mm_P2.54mm", 48, 47, 0),
    ("TVS1", "SMBJ51CA", "Diode_SMD", "D_SMB", 63, 47, 0),
    ("C1", "470uF_63V", "Capacitor_THT", "CP_Radial_D10.0mm_P5.00mm", 73, 47, 0),
    ("F1", "0.5A_FUSE", "Fuse", "Fuse_1206_3216Metric", 29, 47, 0),
    ("MOV1", "V47ZA1P", "Varistor", "RV_Disc_D7mm_W3.9mm_P5mm", 37, 47, 0),
    ("U2", "AP63203WU-7", "Package_TO_SOT_SMD", "TSOT-23-6", 95, 66, 0),
    ("L2", "2.2uH", "Inductor_SMD", "L_Vishay_IFSC-1515AH_4x4x1.8mm", 103, 66, 0),
    ("U3", "TPS3839G33DBZR", "Package_TO_SOT_SMD", "SOT-23-3", 110, 48, 0),
    ("U4", "TPS3823-33DBVR", "Package_TO_SOT_SMD", "SOT-23-5", 120, 48, 0),
    ("U5", "ESP32-WROOM-32E-N16", "RF_Module", "ESP32-WROOM-32E", 153, 55, 0),
    ("U6", "MCP23017-E/SS", "Package_SO", "SSOP-28_5.3x10.2mm_P0.65mm", 114, 61, 0),
    ("U7", "ADS1115IDGSR", "Package_SO", "VSSOP-10_3x3mm_P0.5mm", 114, 78, 0),
    ("U8", "NXE1S0505MC-R7", "Converter_DCDC", "Converter_DCDC_Murata_NXExSxxxxMC_SMD", 95, 87, 0),
    ("U9", "H11AA1M_TH", "Package_DIP", "DIP-6_W7.62mm", 31, 56, 0),
    ("U10", "H11AA1M_IND", "Package_DIP", "DIP-6_W7.62mm", 31, 69, 0),
    ("U11", "H11AA1M_VAL", "Package_DIP", "DIP-6_W7.62mm", 41, 56, 0),
    ("U12", "H11AA1M_24VAC", "Package_DIP", "DIP-6_W7.62mm", 41, 69, 0),
    ("U16", "TLV6700DDCR_THERM", "Package_TO_SOT_SMD", "SOT-23-6", 124, 75, 0),
    ("U17", "TLV6700DDCR_SFS", "Package_TO_SOT_SMD", "SOT-23-6", 124, 83, 0),
    ("U18", "OPA333AIDBVR", "Package_TO_SOT_SMD", "SOT-23-5", 134, 78, 0),
    ("Q1", "AO3400A", "Package_TO_SOT_SMD", "SOT-23", 34, 96, 0),
    ("Q2", "AO3400A", "Package_TO_SOT_SMD", "SOT-23", 78, 96, 0),
]

TEST_POINTS = [
    ("TP1", "VRAW", 98, 36),
    ("TP2", "+5V", 106, 36),
    ("TP3", "+3V3", 114, 36),
    ("TP4", "WATCHDOG_OK", 122, 36),
    ("TP5", "SAFETY_STATIC_OK", 126, 36),
    ("TP6", "K1_COIL", 98, 43),
    ("TP7", "K2_COIL", 106, 43),
    ("TP8", "TH_FEEDBACK", 114, 43),
    ("TP9", "VAL_SENSE", 122, 43),
]


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    existing = {fp.GetReference(): fp for fp in board.GetFootprints()}

    for ref, value, lib, name, x, y, rot in PARTS:
        fp = existing.get(ref)
        if fp is None:
            fp = load_fp(lib, name)
            fp.SetReference(ref)
            board.Add(fp)
        fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(rot)

    for ref, value, x, y in TEST_POINTS:
        fp = existing.get(ref)
        if fp is None:
            fp = load_fp("TestPoint", "TestPoint_Pad_D2.0mm")
            fp.SetReference(ref)
            board.Add(fp)
        fp.SetValue(value)
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))

    pcbnew.SaveBoard(str(BOARD_PATH), board)


if __name__ == "__main__":
    main()
