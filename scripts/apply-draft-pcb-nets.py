#!/usr/bin/env python3
"""Apply first-pass PCB nets and critical draft routing.

This is a PCB-side draft to make the placed control-board circuitry traceable
while schematic symbols are still being captured. It deliberately routes only
the safety-critical heat-request chain and nearby relay drive nets.
"""

from __future__ import annotations

from pathlib import Path

import pcbnew


REPO_ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = REPO_ROOT / "pcb" / "mastertemp_esp32" / "mastertemp_esp32.kicad_pcb"


NETS_BY_PAD = {
    "J1": {
        "1": "VAC24_A",
        "2": "VAC24_B",
        "3": "CHASSIS_SHIELD",
    },
    "F1": {
        "1": "VAC24_A_FUSED",
        "2": "VAC24_A",
    },
    "MOV1": {
        "1": "VAC24_A_FUSED",
        "2": "VAC24_B",
    },
    "TVS1": {
        "1": "VAC24_A_FUSED",
        "2": "VAC24_B",
    },
    "D1": {
        "1": "VAC24_A_FUSED",
        "2": "VAC24_B",
        "3": "VRAW",
        "4": "PGND_RAW",
    },
    "C1": {
        "1": "VRAW",
        "2": "PGND_RAW",
    },
    "U1": {
        "1": "PGND_RAW",
        "2": "VRAW",
        "3": "VRAW",
        "4": "RON_5V_TBD",
        "5": "FB_5V_TBD",
        "6": "+5V_PGOOD",
        "7": "BST_5V",
        "8": "SW_5V",
        "9": "PGND_RAW",
    },
    "L1": {
        "1": "SW_5V",
        "2": "+5V",
    },
    "C4": {
        "1": "VRAW",
        "2": "PGND_RAW",
    },
    "C5": {
        "1": "BST_5V",
        "2": "SW_5V",
    },
    "R5": {
        "1": "+5V",
        "2": "FB_5V_TBD",
    },
    "R6": {
        "1": "FB_5V_TBD",
        "2": "PGND_RAW",
    },
    "R7": {
        "1": "RON_5V_TBD",
        "2": "PGND_RAW",
    },
    "J2": {
        "1": "VAL_SENSE_AC",
        "2": "TH_HEAT_REQUEST_OUT",
        "3": "IND_SENSE_AC",
        "4": "ICM_GND_REF",
        "5": "ICM_24VAC_SOURCE",
        "6": "FIREMAN_24VAC",
        "7": "FIREMAN_SWITCH_RETURN",
    },
    "J3": {
        "1": "PS_SWITCH",
        "2": "HLS_SWITCH",
        "3": "ES1_SWITCH",
        "4": "AFS_SWITCH_DYNAMIC",
        "5": "AGS_SWITCH",
        "6": "SFS_INPUT",
        "7": "GAS_MONITOR_ONLY",
    },
    "J4": {
        "1": "THERMISTOR_A",
        "2": "THERMISTOR_B",
    },
    "J5": {
        "1": "SPA_LINE",
        "2": "COMMON_LINE",
        "3": "POOL_LINE",
    },
    "R1": {
        "1": "ISO_REMOTE_5V",
        "2": "SPA_LED_A",
    },
    "R2": {
        "1": "ISO_REMOTE_5V",
        "2": "POOL_LED_A",
    },
    "R3": {
        "1": "+3V3",
        "2": "REMOTE_SPA_SENSE",
    },
    "R4": {
        "1": "+3V3",
        "2": "REMOTE_POOL_SENSE",
    },
    "R8": {
        "1": "VAL_SENSE_AC",
        "2": "VAL_OPTO_LIMIT_A",
    },
    "R9": {
        "1": "VAL_OPTO_LIMIT_A",
        "2": "VAL_OPTO_INPUT",
    },
    "R10": {
        "1": "RELAY_K1_GATE",
        "2": "GND",
    },
    "R11": {
        "1": "RELAY_K2_GATE",
        "2": "GND",
    },
    "R22": {
        "1": "RELAY_K1_GATE_DRIVE",
        "2": "RELAY_K1_GATE",
    },
    "R23": {
        "1": "RELAY_K2_GATE_DRIVE",
        "2": "RELAY_K2_GATE",
    },
    "R24": {
        "1": "+3V3_ADC",
        "2": "THERMISTOR_ADC",
    },
    "R25": {
        "1": "+3V3",
        "2": "I2C_SDA",
    },
    "R26": {
        "1": "+3V3",
        "2": "I2C_SCL",
    },
    "R27": {
        "1": "SFS_INPUT",
        "2": "SFS_FIELD_INPUT",
    },
    "R28": {
        "1": "VRAW",
        "2": "VRAW_MONITOR_ADC",
    },
    "R29": {
        "1": "VRAW_MONITOR_ADC",
        "2": "AGND",
    },
    "R30": {
        "1": "+3V3",
        "2": "THERMISTOR_RANGE_OK",
    },
    "R31": {
        "1": "+3V3",
        "2": "SFS_RANGE_OK",
    },
    "R32": {
        "1": "+3V3_ADC",
        "2": "THERM_LOW_REF_TBD",
    },
    "R33": {
        "1": "THERM_LOW_REF_TBD",
        "2": "AGND",
    },
    "R34": {
        "1": "+3V3_ADC",
        "2": "THERM_HIGH_REF_TBD",
    },
    "R35": {
        "1": "THERM_HIGH_REF_TBD",
        "2": "AGND",
    },
    "R36": {
        "1": "+3V3_ADC",
        "2": "SFS_LOW_REF_TBD",
    },
    "R37": {
        "1": "SFS_LOW_REF_TBD",
        "2": "AGND",
    },
    "R38": {
        "1": "+3V3_ADC",
        "2": "SFS_HIGH_REF_TBD",
    },
    "R39": {
        "1": "SFS_HIGH_REF_TBD",
        "2": "AGND",
    },
    "R12": {
        "1": "VAL_OPTO_GPIO",
        "2": "+3V3",
    },
    "R13": {
        "1": "TH_HEAT_REQUEST_OUT",
        "2": "TH_OPTO_LIMIT_A",
    },
    "R14": {
        "1": "TH_OPTO_LIMIT_A",
        "2": "TH_OPTO_INPUT",
    },
    "R15": {
        "1": "TH_OPTO_GPIO",
        "2": "+3V3",
    },
    "R16": {
        "1": "IND_SENSE_AC",
        "2": "IND_OPTO_LIMIT_A",
    },
    "R17": {
        "1": "IND_OPTO_LIMIT_A",
        "2": "IND_OPTO_INPUT",
    },
    "R18": {
        "1": "IND_OPTO_GPIO",
        "2": "+3V3",
    },
    "R19": {
        "1": "ICM_24VAC_SOURCE",
        "2": "VAC24_OPTO_LIMIT_A",
    },
    "R20": {
        "1": "VAC24_OPTO_LIMIT_A",
        "2": "VAC24_OPTO_INPUT",
    },
    "R21": {
        "1": "VAC24_OPTO_GPIO",
        "2": "+3V3",
    },
    "C2": {
        "1": "REMOTE_SPA_SENSE",
        "2": "GND",
    },
    "C3": {
        "1": "REMOTE_POOL_SENSE",
        "2": "GND",
    },
    "K1": {
        "1": "K1_COIL_LOW",
        "2": "ICM_24VAC_SOURCE",
        "3": "HEAT_CHAIN_K1_K2",
        "5": "+5V_RELAY",
    },
    "K2": {
        "1": "K2_COIL_LOW",
        "2": "HEAT_CHAIN_K1_K2",
        "3": "TH_HEAT_REQUEST_OUT",
        "5": "+5V_RELAY",
    },
    "D2": {
        "1": "+5V_RELAY",
        "2": "K1_COIL_LOW",
    },
    "D3": {
        "1": "+5V_RELAY",
        "2": "K2_COIL_LOW",
    },
    "Q1": {
        "1": "RELAY_K1_GATE",
        "2": "GND",
        "3": "K1_COIL_LOW",
    },
    "Q2": {
        "1": "RELAY_K2_GATE",
        "2": "GND",
        "3": "K2_COIL_LOW",
    },
    "TP1": {"1": "VRAW"},
    "TP2": {"1": "+5V"},
    "TP3": {"1": "+3V3"},
    "TP4": {"1": "WATCHDOG_OK"},
    "TP5": {"1": "SAFETY_STATIC_OK"},
    "TP6": {"1": "K1_COIL_LOW"},
    "TP7": {"1": "K2_COIL_LOW"},
    "TP8": {"1": "TH_FEEDBACK"},
    "TP9": {"1": "VAL_SENSE_AC"},
    "U2": {
        "1": "+3V3",
        "2": "+5V",
        "3": "+5V",
        "4": "SW_3V3",
        "5": "GND",
        "6": "BST_3V3",
    },
    "L2": {
        "1": "SW_3V3",
        "2": "+3V3",
    },
    "C6": {
        "1": "BST_3V3",
        "2": "SW_3V3",
    },
    "C7": {
        "1": "+5V",
        "2": "GND",
    },
    "C8": {
        "1": "+3V3",
        "2": "GND",
    },
    "C9": {
        "1": "THERMISTOR_ADC",
        "2": "AGND",
    },
    "C10": {
        "1": "SFS_ADC",
        "2": "AGND",
    },
    "C11": {
        "1": "VRAW_MONITOR_ADC",
        "2": "AGND",
    },
    "U3": {
        "1": "BROWNOUT_OK",
        "2": "GND",
        "3": "+3V3",
    },
    "U4": {
        "1": "WATCHDOG_OK",
        "2": "GND",
        "5": "+3V3",
    },
    "U5": {
        "1": "GND",
        "2": "+3V3",
        "3": "ESP32_EN",
    },
    "U6": {
        "9": "+3V3",
        "10": "GND",
        "12": "I2C_SCL",
        "13": "I2C_SDA",
        "15": "GND",
        "16": "GND",
        "17": "GND",
        "18": "+3V3",
        "21": "VAL_OPTO_GPIO",
        "22": "TH_OPTO_GPIO",
        "23": "IND_OPTO_GPIO",
        "24": "VAC24_OPTO_GPIO",
    },
    "U7": {
        "3": "I2C_SDA",
        "4": "I2C_SCL",
        "5": "GND",
        "6": "THERMISTOR_ADC",
        "7": "SFS_ADC",
        "8": "VRAW_MONITOR_ADC",
        "9": "VAL_SENSE_ADC",
        "10": "+3V3",
    },
    "U8": {
        "1": "GND",
        "3": "+5V",
        "7": "COMMON_LINE",
        "8": "ISO_REMOTE_5V",
    },
    "U11": {
        "1": "VAL_OPTO_INPUT",
        "2": "ICM_GND_REF",
        "4": "GND",
        "5": "VAL_OPTO_GPIO",
    },
    "U9": {
        "1": "TH_OPTO_INPUT",
        "2": "ICM_GND_REF",
        "4": "GND",
        "5": "TH_OPTO_GPIO",
    },
    "U10": {
        "1": "IND_OPTO_INPUT",
        "2": "ICM_GND_REF",
        "4": "GND",
        "5": "IND_OPTO_GPIO",
    },
    "U12": {
        "1": "VAC24_OPTO_INPUT",
        "2": "ICM_GND_REF",
        "4": "GND",
        "5": "VAC24_OPTO_GPIO",
    },
    "U14": {
        "1": "THERMISTOR_A",
        "2": "THERMISTOR_B",
        "3": "+3V3_ADC",
        "4": "AGND",
        "5": "THERMISTOR_ADC",
        "6": "THERM_WINDOW_SENSE",
    },
    "U16": {
        "1": "THERM_WINDOW_SENSE",
        "2": "THERM_LOW_REF_TBD",
        "3": "THERM_HIGH_REF_TBD",
        "4": "THERMISTOR_RANGE_OK",
        "5": "GND",
    },
    "U17": {
        "1": "SFS_WINDOW_SENSE",
        "2": "SFS_LOW_REF_TBD",
        "3": "SFS_HIGH_REF_TBD",
        "4": "SFS_RANGE_OK",
        "5": "GND",
    },
    "U18": {
        "1": "SFS_FIELD_INPUT",
        "2": "SFS_RETURN_OR_REF",
        "3": "+3V3_ADC",
        "4": "AGND",
        "5": "SFS_ADC",
    },
    "U19": {
        "1": "SPA_LED_A",
        "2": "SPA_LINE",
        "3": "GND",
        "4": "REMOTE_SPA_SENSE",
    },
    "U20": {
        "1": "POOL_LED_A",
        "2": "POOL_LINE",
        "3": "GND",
        "4": "REMOTE_POOL_SENSE",
    },
}

CLEAR_NETS_BY_PAD = {
    "U16": {"6"},
    "U17": {"6"},
}


ROUTES_MM = [
    # net, layer, width_mm, point sequence. These are first-pass local routes
    # for traceability and DRC pressure; final power layout still needs review.
    ("ICM_24VAC_SOURCE", pcbnew.F_Cu, 0.60, ["J2:5", (64.32, 98.0), (53.16, 98.0), "K1:2"]),
    ("HEAT_CHAIN_K1_K2", pcbnew.B_Cu, 0.60, ["K1:3", (60.78, 84.0), (76.16, 84.0), "K2:2"]),
    ("TH_HEAT_REQUEST_OUT", pcbnew.B_Cu, 0.60, ["K2:3", (87.78, 99.0), (49.08, 99.0), "J2:2"]),
    ("K1_COIL_LOW", pcbnew.F_Cu, 0.35, ["K1:1", (34.94, 88.0), "Q1:3"]),
    ("K1_COIL_LOW", pcbnew.F_Cu, 0.25, [(34.94, 88.0), "TP6:1"]),
    ("K2_COIL_LOW", pcbnew.F_Cu, 0.35, ["K2:1", (66.0, 93.0), (78.94, 93.0), "Q2:3"]),
    ("K2_COIL_LOW", pcbnew.F_Cu, 0.25, [(78.94, 93.0), "TP7:1"]),
    ("RELAY_K1_GATE", pcbnew.F_Cu, 0.20, ["Q1:1", (29.5, 95.05), (29.5, 101.5), "R10:1"]),
    ("RELAY_K1_GATE", pcbnew.F_Cu, 0.20, ["R22:2", (26.9125, 95.05), (29.5, 95.05)]),
    ("RELAY_K2_GATE", pcbnew.F_Cu, 0.20, ["Q2:1", (69.5, 95.05), (69.5, 98.5), "R11:1"]),
    ("RELAY_K2_GATE", pcbnew.F_Cu, 0.20, ["R23:2", (69.5, 95.05)]),
    ("+5V_RELAY", pcbnew.F_Cu, 0.35, ["K1:5", "K2:5"]),
    ("+5V_RELAY", pcbnew.F_Cu, 0.35, ["K1:5", (38.0, 80.38), "D2:1"]),
    ("K1_COIL_LOW", pcbnew.F_Cu, 0.35, ["D2:2", (38.0, 88.0), "K1:1"]),
    ("+5V_RELAY", pcbnew.F_Cu, 0.35, ["K2:5", (66.0, 74.35), "D3:1"]),
    ("K2_COIL_LOW", pcbnew.F_Cu, 0.35, ["D3:2", (70.0, 88.0), "K2:1"]),
    ("VAC24_A", pcbnew.F_Cu, 0.50, ["J1:1", (34.00, 47.0), "F1:2"]),
    ("VAC24_A_FUSED", pcbnew.F_Cu, 0.50, ["F1:1", (24.00, 47.0), (24.00, 53.0), (37.00, 53.0), "MOV1:1"]),
    ("VAC24_A_FUSED", pcbnew.B_Cu, 0.50, ["MOV1:1", (37.00, 41.0), (51.03, 41.0)]),
    ("VAC24_A_FUSED", pcbnew.F_Cu, 0.50, ["D1:1", (51.03, 41.0), (60.85, 41.0), "TVS1:1"]),
    ("VAC24_B", pcbnew.F_Cu, 0.50, ["J1:2", (39.08, 31.0), (42.00, 31.0), (42.00, 48.9), "MOV1:2"]),
    ("VAC24_B", pcbnew.F_Cu, 0.50, ["MOV1:2", (56.98, 48.9), "D1:2"]),
    ("VAC24_B", pcbnew.F_Cu, 0.50, ["D1:2", (56.98, 51.0), (65.15, 51.0), "TVS1:2"]),
    ("VRAW", pcbnew.F_Cu, 0.40, ["D1:3", (56.48, 56.0), "C4:1"]),
    ("VRAW", pcbnew.F_Cu, 0.50, ["D1:3", (73.0, 52.0), "C1:1"]),
    ("VRAW", pcbnew.F_Cu, 0.25, ["C1:1", (73.0, 36.0), "TP1:1"]),
    ("VRAW", pcbnew.F_Cu, 0.25, ["U1:2", "U1:3"]),
    ("VRAW", pcbnew.F_Cu, 0.25, ["U1:2", (49.50, 65.36), (49.50, 62.0), (56.48, 62.0), "C4:1"]),
    ("VRAW", pcbnew.F_Cu, 0.20, ["TP1:1", (98.0, 40.0), "R28:1"]),
    ("PGND_RAW", pcbnew.F_Cu, 0.40, ["D1:4", (53.53, 52.0), "C4:2"]),
    ("PGND_RAW", pcbnew.F_Cu, 0.25, ["U1:1", "U1:9"]),
    ("PGND_RAW", pcbnew.F_Cu, 0.35, ["C4:2", (51.5, 60.0)]),
    ("PGND_RAW", pcbnew.B_Cu, 0.35, [(51.5, 60.0), (51.5, 64.1)]),
    ("PGND_RAW", pcbnew.F_Cu, 0.35, [(51.5, 64.1), "U1:1"]),
    ("PGND_RAW", pcbnew.B_Cu, 0.35, ["C1:2", (78.0, 60.0), (51.5, 60.0)]),
    ("PGND_RAW", pcbnew.F_Cu, 0.25, [(54.398, 65.225), (55.602, 65.225), (55.602, 66.775), (54.398, 66.775), (54.398, 65.225)]),
    ("PGND_RAW", pcbnew.F_Cu, 0.25, ["R6:2", (61.91, 75.0), (55.91, 75.0), "R7:2"]),
    ("PGND_RAW", pcbnew.F_Cu, 0.25, ["R7:2", (55.91, 68.2), (55.60, 66.78)]),
    ("SW_5V", pcbnew.F_Cu, 0.35, ["U1:8", (62.0, 64.1), (62.0, 66.0), "L1:1"]),
    ("+5V", pcbnew.F_Cu, 0.50, ["L1:2", (74.95, 70.0), "R5:1"]),
    ("+5V", pcbnew.F_Cu, 0.35, ["R5:1", (82.0, 70.0), "C7:1"]),
    ("+5V", pcbnew.F_Cu, 0.25, ["U2:2", "U2:3", (93.53, 66.95), "C7:1"]),
    ("+5V", pcbnew.F_Cu, 0.25, ["C7:1", (93.53, 68.5)]),
    ("+5V", pcbnew.F_Cu, 0.20, ["U8:3", (88.8, 84.46), (88.8, 70.0), "C7:1"]),
    ("+5V", pcbnew.B_Cu, 0.25, [(93.53, 68.5), (106.0, 38.5)]),
    ("+5V", pcbnew.F_Cu, 0.25, [(106.0, 38.5), "TP2:1"]),
    ("FB_5V_TBD", pcbnew.F_Cu, 0.20, ["U1:5", (60.09, 67.91), "R5:2", "R6:1"]),
    ("RON_5V_TBD", pcbnew.F_Cu, 0.20, ["U1:4", (54.09, 67.91), "R7:1"]),
    ("SW_5V", pcbnew.F_Cu, 0.20, ["C5:2", (62.0, 64.1)]),
    ("BST_5V", pcbnew.F_Cu, 0.20, ["U1:7", (59.2, 65.36)]),
    ("BST_5V", pcbnew.B_Cu, 0.20, [(59.2, 65.36), (59.4, 62.0)]),
    ("BST_5V", pcbnew.F_Cu, 0.20, [(59.4, 62.0), "C5:1"]),
    ("BST_3V3", pcbnew.F_Cu, 0.20, ["U2:6", (98.50, 65.05), "C6:1"]),
    ("SW_3V3", pcbnew.F_Cu, 0.25, ["U2:4", (98.50, 66.95), "C6:2"]),
    ("SW_3V3", pcbnew.F_Cu, 0.35, ["U2:4", (99.0, 66.95), (99.0, 66.0), "L2:1"]),
    ("+3V3", pcbnew.F_Cu, 0.25, ["U2:1", (93.86, 63.5), (104.48, 63.5), "L2:2"]),
    ("+3V3", pcbnew.F_Cu, 0.35, ["L2:2", (104.48, 70.0), "C8:1"]),
    ("+3V3", pcbnew.F_Cu, 0.30, ["C8:1", (106.05, 52.0), (111.14, 52.0), "U3:3"]),
    ("+3V3", pcbnew.F_Cu, 0.25, ["U3:3", (111.14, 45.0), (121.14, 45.0), "U4:5"]),
    ("+3V3", pcbnew.F_Cu, 0.25, ["TP3:1", (111.0, 36.0), (111.0, 45.0)]),
    ("+3V3", pcbnew.F_Cu, 0.20, ["U6:9", (106.6, 61.975), (106.6, 63.5), (104.48, 63.5)]),
    ("+3V3", pcbnew.F_Cu, 0.20, ["U6:18", (121.0, 63.275), (121.0, 52.0), (111.14, 52.0)]),
    ("+3V3", pcbnew.F_Cu, 0.25, ["C8:1", (106.05, 68.0), (118.0, 68.0), (118.0, 77.0), "U7:10"]),
    ("+3V3", pcbnew.F_Cu, 0.25, [(118.0, 68.0), (140.0, 68.0), (140.0, 51.01), "U5:2"]),
    ("+3V3", pcbnew.F_Cu, 0.25, [(140.0, 68.0), (143.0, 68.0), (143.0, 86.0), (126.09, 86.0), "R4:1"]),
    ("+3V3", pcbnew.F_Cu, 0.25, [(126.09, 86.0), (115.09, 86.0), "R3:1"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(127.0875, 74.0), (127.0875, 68.0)]),
    ("+3V3", pcbnew.F_Cu, 0.20, ["R31:1", (132.0, 86.0), (126.09, 86.0)]),
    ("GND", pcbnew.F_Cu, 0.35, ["C7:2", (96.48, 72.5), (107.95, 72.5), "C8:2"]),
    ("GND", pcbnew.F_Cu, 0.20, ["U8:1", (92.0, 81.92), (92.0, 72.5), (96.48, 72.5)]),
    ("GND", pcbnew.F_Cu, 0.20, ["U2:5", (97.6, 66.0)]),
    ("GND", pcbnew.B_Cu, 0.20, [(97.6, 66.0), (97.6, 70.0)]),
    ("GND", pcbnew.F_Cu, 0.20, [(97.6, 70.0), "C7:2"]),
    ("GND", pcbnew.F_Cu, 0.20, ["U6:10", (108.6, 62.625)]),
    ("GND", pcbnew.B_Cu, 0.20, [(108.6, 62.625), (117.5, 62.625)]),
    ("GND", pcbnew.F_Cu, 0.20, ["U6:17", "U6:16", "U6:15", (119.4, 66.0)]),
    ("GND", pcbnew.B_Cu, 0.20, [(119.4, 66.0), (117.5, 66.0)]),
    ("GND", pcbnew.B_Cu, 0.20, [(106.0, 72.5), (117.5, 72.5)]),
    ("GND", pcbnew.F_Cu, 0.25, ["U7:5", (111.8, 81.5)]),
    ("GND", pcbnew.F_Cu, 0.20, ["U16:5", (128.0, 75.0)]),
    ("GND", pcbnew.F_Cu, 0.20, ["U17:5", (128.0, 83.0)]),
    ("GND", pcbnew.In2_Cu, 0.20, [(128.0, 75.0), (132.0, 75.0), (132.0, 74.0), (111.8, 74.0), (111.8, 81.5)]),
    ("GND", pcbnew.In2_Cu, 0.20, [(128.0, 83.0), (132.0, 83.0), (132.0, 74.0)]),
    ("GND", pcbnew.F_Cu, 0.20, ["U3:2", (107.5, 48.95)]),
    ("GND", pcbnew.F_Cu, 0.20, ["U4:2", (117.5, 48.0)]),
    ("GND", pcbnew.B_Cu, 0.20, [(107.5, 48.95), (117.5, 48.0), (117.5, 81.5), (111.8, 81.5)]),
    ("GND", pcbnew.B_Cu, 0.20, [(111.8, 81.5), (117.5, 81.5)]),
    ("GND", pcbnew.F_Cu, 0.25, ["U5:1", (142.0, 49.74)]),
    ("GND", pcbnew.B_Cu, 0.25, [(142.0, 49.74), (117.5, 48.0)]),
    ("GND", pcbnew.F_Cu, 0.25, ["Q1:2", (33.06, 97.7)]),
    ("GND", pcbnew.F_Cu, 0.20, ["R10:2", (33.06, 101.5), (33.06, 97.7)]),
    ("GND", pcbnew.F_Cu, 0.25, ["Q2:2", (77.06, 97.7)]),
    ("GND", pcbnew.F_Cu, 0.20, ["R11:2", (77.06, 98.5), (77.06, 97.7)]),
    ("GND", pcbnew.B_Cu, 0.25, [(33.06, 97.7), (77.06, 97.7)]),
    ("GND", pcbnew.F_Cu, 0.25, [(77.06, 97.7), (111.8, 97.7)]),
    ("GND", pcbnew.B_Cu, 0.25, [(111.8, 97.7), (111.8, 87.0)]),
    ("WATCHDOG_OK", pcbnew.F_Cu, 0.20, ["U4:1", (117.8, 46.0)]),
    ("WATCHDOG_OK", pcbnew.B_Cu, 0.20, [(117.8, 46.0), (122.0, 38.0)]),
    ("WATCHDOG_OK", pcbnew.F_Cu, 0.20, [(122.0, 38.0), "TP4:1"]),
    ("I2C_SDA", pcbnew.F_Cu, 0.20, ["U6:13", (108.2, 64.575)]),
    ("I2C_SDA", pcbnew.In2_Cu, 0.20, [(108.2, 64.575), (101.0, 64.575), (101.0, 58.8), (102.0875, 58.8)]),
    ("I2C_SDA", pcbnew.F_Cu, 0.20, [(102.0875, 58.8), "R25:2"]),
    ("I2C_SDA", pcbnew.In1_Cu, 0.20, [(108.2, 64.575), (108.2, 77.0), (109.5, 77.0), (109.5, 77.4)]),
    ("I2C_SDA", pcbnew.F_Cu, 0.20, [(109.5, 77.4), (110.6, 77.4), (110.6, 78.0), "U7:3"]),
    ("I2C_SCL", pcbnew.F_Cu, 0.20, ["U6:12", (108.8, 63.925)]),
    ("I2C_SCL", pcbnew.B_Cu, 0.20, [(108.8, 63.925), (100.0, 63.925), (100.0, 56.0), (102.0875, 56.0)]),
    ("I2C_SCL", pcbnew.F_Cu, 0.20, [(102.0875, 56.0), "R26:2"]),
    ("I2C_SCL", pcbnew.In1_Cu, 0.20, [(108.8, 63.925), (108.8, 76.0), (111.3, 76.0), (111.3, 78.5), (109.5, 78.5)]),
    ("I2C_SCL", pcbnew.F_Cu, 0.20, [(109.5, 78.5), "U7:4"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(106.05, 52.0), (103.9125, 52.0), (103.9125, 56.0), "R26:1"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(103.9125, 56.0), (103.9125, 58.8), "R25:1"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(121.0, 52.0), (125.4125, 52.0), "R12:2"]),
    ("VAL_OPTO_GPIO", pcbnew.F_Cu, 0.20, ["U6:21", (119.0, 61.325)]),
    ("VAL_OPTO_GPIO", pcbnew.In1_Cu, 0.20, [(119.0, 61.325), (124.0, 44.0)]),
    ("VAL_OPTO_GPIO", pcbnew.F_Cu, 0.20, [(124.0, 44.0), "R12:1"]),
    ("VAL_OPTO_GPIO", pcbnew.In1_Cu, 0.20, [(119.0, 61.325), (119.0, 32.0), (52.0, 32.0), (52.0, 58.54), "U11:5"]),
    ("TH_OPTO_GPIO", pcbnew.F_Cu, 0.20, ["U6:22", (116.5, 60.675)]),
    ("TH_OPTO_GPIO", pcbnew.In2_Cu, 0.20, [(116.5, 60.675), (116.5, 37.0), (33.0, 37.0), (33.0, 58.54), "U9:5"]),
    ("TH_OPTO_GPIO", pcbnew.In2_Cu, 0.20, [(116.5, 60.675), (116.5, 54.0), (129.0, 54.0), (129.0, 50.0)]),
    ("TH_OPTO_GPIO", pcbnew.F_Cu, 0.20, [(129.0, 50.0), "R15:1"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(121.0, 52.0), (131.4125, 52.0), "R15:2"]),
    ("IND_OPTO_GPIO", pcbnew.F_Cu, 0.20, ["U6:23", (115.8, 60.025)]),
    ("IND_OPTO_GPIO", pcbnew.In2_Cu, 0.20, [(115.8, 60.025), (115.8, 40.0), (35.0, 40.0), (35.0, 56.0)]),
    ("IND_OPTO_GPIO", pcbnew.B_Cu, 0.20, [(35.0, 56.0), (35.0, 71.54), "U10:5"]),
    ("IND_OPTO_GPIO", pcbnew.In1_Cu, 0.20, [(115.8, 60.025), (115.8, 63.0), (135.0, 63.0), (135.0, 50.0)]),
    ("IND_OPTO_GPIO", pcbnew.F_Cu, 0.20, [(135.0, 50.0), "R18:1"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(131.4125, 52.0), (137.4125, 52.0), "R18:2"]),
    ("VAC24_OPTO_GPIO", pcbnew.F_Cu, 0.20, ["U6:24", (115.0, 59.375)]),
    ("VAC24_OPTO_GPIO", pcbnew.In1_Cu, 0.20, [(115.0, 59.375), (115.0, 34.0), (58.0, 34.0), (58.0, 62.0)]),
    ("VAC24_OPTO_GPIO", pcbnew.B_Cu, 0.20, [(58.0, 62.0), (58.0, 71.54), "U12:5"]),
    ("VAC24_OPTO_GPIO", pcbnew.In1_Cu, 0.20, [(115.0, 59.375), (115.0, 65.0), (133.0, 65.0)]),
    ("VAC24_OPTO_GPIO", pcbnew.F_Cu, 0.20, [(133.0, 65.0), (133.0, 54.0), "R21:1"]),
    ("+3V3", pcbnew.F_Cu, 0.20, [(137.4125, 52.0), (137.4125, 54.0), "R21:2"]),
    ("GND", pcbnew.In2_Cu, 0.20, ["U11:4", (55.0, 61.08), (55.0, 72.5), (106.0, 72.5)]),
    ("GND", pcbnew.In2_Cu, 0.20, ["U9:4", (38.62, 62.5), (48.62, 62.5), (48.62, 61.08)]),
    ("GND", pcbnew.In2_Cu, 0.20, ["U10:4", (38.62, 76.0), (55.0, 76.0), (55.0, 72.5)]),
    ("GND", pcbnew.In2_Cu, 0.20, ["U12:4", (48.62, 76.0), (55.0, 76.0)]),
    ("VAL_SENSE_AC", pcbnew.F_Cu, 0.20, [(22.0, 64.0), "R8:1"]),
    ("VAL_OPTO_LIMIT_A", pcbnew.F_Cu, 0.20, ["R8:2", "R9:1"]),
    ("VAL_OPTO_INPUT", pcbnew.F_Cu, 0.20, ["R9:2", (33.5, 64.0), (33.5, 54.5), (39.0, 54.5), "U11:1"]),
    ("ICM_GND_REF", pcbnew.In1_Cu, 0.20, ["J2:4", (59.24, 112.0), (57.0, 112.0), (57.0, 66.5), (44.0, 66.5), (44.0, 60.0), "U11:2"]),
    ("ICM_GND_REF", pcbnew.In1_Cu, 0.20, ["U9:2", (28.0, 58.54), (28.0, 66.5), (44.0, 66.5)]),
    ("ICM_GND_REF", pcbnew.In1_Cu, 0.20, ["U10:2", (28.0, 71.54), (28.0, 66.5)]),
    ("ICM_GND_REF", pcbnew.In1_Cu, 0.20, ["U12:2", (42.5, 71.54), (42.5, 66.5), (44.0, 66.5)]),
    ("TH_HEAT_REQUEST_OUT", pcbnew.F_Cu, 0.20, ["J2:2", (49.08, 108.0), (20.8, 108.0), (20.8, 56.0), "R13:1"]),
    ("TH_OPTO_LIMIT_A", pcbnew.F_Cu, 0.20, ["R13:2", "R14:1"]),
    ("TH_OPTO_INPUT", pcbnew.F_Cu, 0.20, ["R14:2", "U9:1"]),
    ("IND_SENSE_AC", pcbnew.In2_Cu, 0.20, ["J2:3", (54.16, 110.0), (23.0875, 110.0), (23.0875, 71.0)]),
    ("IND_SENSE_AC", pcbnew.F_Cu, 0.20, [(23.0875, 71.0), "R16:1"]),
    ("IND_OPTO_LIMIT_A", pcbnew.F_Cu, 0.20, ["R16:2", "R17:1"]),
    ("IND_OPTO_INPUT", pcbnew.F_Cu, 0.20, ["R17:2", "U10:1"]),
    ("ICM_24VAC_SOURCE", pcbnew.B_Cu, 0.20, ["K1:2", (53.16, 78.0), (34.0, 78.0)]),
    ("ICM_24VAC_SOURCE", pcbnew.F_Cu, 0.20, [(34.0, 78.0), "R19:1"]),
    ("VAC24_OPTO_LIMIT_A", pcbnew.F_Cu, 0.20, ["R19:2", "R20:1"]),
    ("VAC24_OPTO_INPUT", pcbnew.F_Cu, 0.20, ["R20:2", (27.0875, 75.5), (43.0, 75.5), (43.0, 69.0), "U12:1"]),
    ("VAL_SENSE_AC", pcbnew.B_Cu, 0.20, ["J2:1", (22.0, 104.0), (22.0, 25.0), (124.5, 25.0), (124.5, 43.0)]),
    ("VAL_SENSE_AC", pcbnew.F_Cu, 0.20, [(124.5, 43.0), "TP9:1"]),
    ("SPA_LINE", pcbnew.B_Cu, 0.25, ["U19:2", (116.0, 101.5), (160.0, 101.5), "J5:1"]),
    ("COMMON_LINE", pcbnew.F_Cu, 0.25, ["U8:7", (88.0, 89.54)]),
    ("COMMON_LINE", pcbnew.In2_Cu, 0.25, [(88.0, 89.54), (78.0, 89.54), (78.0, 116.0), (165.08, 116.0), "J5:2"]),
    ("POOL_LINE", pcbnew.B_Cu, 0.25, ["U20:2", (127.0, 99.5), (170.16, 99.5), "J5:3"]),
    ("ISO_REMOTE_5V", pcbnew.F_Cu, 0.25, ["U8:8", (101.5, 89.54)]),
    ("ISO_REMOTE_5V", pcbnew.B_Cu, 0.25, [(101.5, 89.54), (101.5, 100.0), (113.5, 100.0)]),
    ("ISO_REMOTE_5V", pcbnew.F_Cu, 0.25, [(113.5, 100.0), "R1:1"]),
    ("ISO_REMOTE_5V", pcbnew.F_Cu, 0.25, ["R1:1", (115.09, 102.0), (126.09, 102.0), "R2:1"]),
    ("SPA_LED_A", pcbnew.F_Cu, 0.20, ["R1:2", (119.2, 100.0), (119.2, 92.5), (116.0, 92.5), "U19:1"]),
    ("POOL_LED_A", pcbnew.F_Cu, 0.20, ["R2:2", (130.2, 100.0), (130.2, 92.5), (127.0, 92.5), "U20:1"]),
    ("REMOTE_SPA_SENSE", pcbnew.F_Cu, 0.20, ["R3:2", "C2:1"]),
    ("REMOTE_SPA_SENSE", pcbnew.F_Cu, 0.20, ["C2:1", (115.05, 89.5), (123.62, 89.5), "U19:4"]),
    ("REMOTE_POOL_SENSE", pcbnew.F_Cu, 0.20, ["R4:2", "C3:1"]),
    ("REMOTE_POOL_SENSE", pcbnew.F_Cu, 0.20, ["C3:1", (126.05, 89.5), (134.62, 89.5), "U20:4"]),
    ("GND", pcbnew.F_Cu, 0.20, ["U7:5", (111.8, 81.5)]),
    ("GND", pcbnew.B_Cu, 0.20, [(111.8, 81.5), (111.8, 87.0), (116.95, 91.8)]),
    ("GND", pcbnew.F_Cu, 0.20, ["C2:2", (116.95, 91.8)]),
    ("GND", pcbnew.B_Cu, 0.20, [(116.95, 91.8), (125.0, 91.8), (125.0, 96.54), "U19:3"]),
    ("GND", pcbnew.F_Cu, 0.20, ["C3:2", (127.95, 91.8)]),
    ("GND", pcbnew.B_Cu, 0.20, [(116.95, 91.8), (127.95, 91.8)]),
    ("GND", pcbnew.B_Cu, 0.20, [(127.95, 91.8), (136.0, 91.8), (136.0, 96.54), "U20:3"]),
    ("THERMISTOR_A", pcbnew.F_Cu, 0.20, ["U14:1", (144.5, 80.2)]),
    ("THERMISTOR_A", pcbnew.In1_Cu, 0.20, ["J4:1", (122.0, 104.0), (122.0, 80.2), (144.5, 80.2)]),
    ("THERMISTOR_B", pcbnew.F_Cu, 0.20, ["U14:2", (144.5, 82.8)]),
    ("THERMISTOR_B", pcbnew.In1_Cu, 0.20, ["J4:2", (142.0, 104.0), (142.0, 82.8), (144.5, 82.8)]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, ["U14:3", (144.5, 84.2)]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, [(144.5, 84.2), (152.0875, 86.0), "R24:1"]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, ["U18:3", (130.0, 79.5)]),
    ("+3V3_ADC", pcbnew.In2_Cu, 0.20, [(144.5, 84.2), (126.0, 84.2), (126.0, 79.5), (130.0, 79.5)]),
    ("AGND", pcbnew.F_Cu, 0.20, ["U14:4", (149.1375, 84.7), (157.5, 84.7), (157.5, 84.2)]),
    ("AGND", pcbnew.F_Cu, 0.20, [(157.5, 84.2), (159.4, 84.2), (159.4, 86.0), "C9:2"]),
    ("AGND", pcbnew.F_Cu, 0.20, ["U18:4", (140.0, 79.5)]),
    ("AGND", pcbnew.F_Cu, 0.20, [(140.0, 79.5), (142.0, 79.5), (142.0, 75.0), (138.9125, 75.0), "C10:2"]),
    ("AGND", pcbnew.In1_Cu, 0.20, [(157.5, 84.2), (157.5, 79.5), (140.0, 79.5)]),
    ("AGND", pcbnew.F_Cu, 0.20, ["R29:2", "C11:2"]),
    ("AGND", pcbnew.F_Cu, 0.20, ["C11:2", (138.95, 72.5), "C10:2"]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, ["R24:1", (152.0875, 88.0), (160.0, 88.0), (160.0, 82.0), "R32:1"]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, [(160.0, 88.0), "R34:1"]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, [(160.0, 88.0), (160.0, 90.0), "R36:1"]),
    ("+3V3_ADC", pcbnew.F_Cu, 0.20, [(160.0, 90.0), (160.0, 94.0), "R38:1"]),
    ("AGND", pcbnew.F_Cu, 0.20, ["C9:2", (158.7, 87.0)]),
    ("AGND", pcbnew.In2_Cu, 0.20, [(158.7, 87.0), (169.5, 87.0)]),
    ("AGND", pcbnew.F_Cu, 0.20, [(169.5, 87.0), (169.5, 88.0), "R35:2"]),
    ("AGND", pcbnew.F_Cu, 0.20, [(169.5, 88.0), (169.5, 82.0), "R33:2"]),
    ("AGND", pcbnew.F_Cu, 0.20, [(169.5, 88.0), (169.5, 90.0), "R37:2"]),
    ("AGND", pcbnew.F_Cu, 0.20, [(169.5, 90.0), (169.5, 94.0), "R39:2"]),
    ("THERM_LOW_REF_TBD", pcbnew.F_Cu, 0.20, ["R32:2", "R33:1"]),
    ("THERM_LOW_REF_TBD", pcbnew.F_Cu, 0.20, ["U16:2", (120.0, 75.0)]),
    ("THERM_LOW_REF_TBD", pcbnew.B_Cu, 0.20, [(120.0, 75.0), (120.0, 81.0), (164.0, 81.0), (164.0, 82.0)]),
    ("THERM_HIGH_REF_TBD", pcbnew.F_Cu, 0.20, ["R34:2", "R35:1"]),
    ("THERM_HIGH_REF_TBD", pcbnew.F_Cu, 0.20, ["U16:3", (122.0, 75.95)]),
    ("THERM_HIGH_REF_TBD", pcbnew.B_Cu, 0.20, [(122.0, 75.95), (122.0, 78.0), (166.0, 78.0), (166.0, 88.0), (164.0, 88.0)]),
    ("SFS_LOW_REF_TBD", pcbnew.F_Cu, 0.20, ["R36:2", "R37:1"]),
    ("SFS_LOW_REF_TBD", pcbnew.F_Cu, 0.20, ["U17:2", (121.0, 83.0)]),
    ("SFS_LOW_REF_TBD", pcbnew.B_Cu, 0.20, [(121.0, 83.0), (121.0, 90.0), (164.0, 90.0)]),
    ("SFS_HIGH_REF_TBD", pcbnew.F_Cu, 0.20, ["R38:2", "R39:1"]),
    ("SFS_HIGH_REF_TBD", pcbnew.F_Cu, 0.20, ["U17:3", (124.0, 83.95)]),
    ("SFS_HIGH_REF_TBD", pcbnew.B_Cu, 0.20, [(124.0, 83.95), (124.0, 82.0), (119.0, 82.0), (119.0, 91.0), (164.0, 91.0), (164.0, 94.0)]),
    ("THERMISTOR_ADC", pcbnew.F_Cu, 0.20, ["U14:5", (151.5, 82.0)]),
    ("THERMISTOR_ADC", pcbnew.In2_Cu, 0.20, [(151.5, 82.0), (153.4, 85.3)]),
    ("THERMISTOR_ADC", pcbnew.F_Cu, 0.20, [(153.4, 85.3), "R24:2"]),
    ("THERMISTOR_ADC", pcbnew.F_Cu, 0.20, [(153.9125, 86.0), (156.05, 86.0), "C9:1"]),
    ("THERMISTOR_ADC", pcbnew.F_Cu, 0.20, ["U7:6", (116.2, 82.0), (118.0, 82.0)]),
    ("THERMISTOR_ADC", pcbnew.In2_Cu, 0.20, [(151.5, 82.0), (151.5, 85.0), (116.0, 85.0), (116.0, 91.0), (118.0, 91.0), (118.0, 82.0)]),
    ("THERM_WINDOW_SENSE", pcbnew.F_Cu, 0.20, ["U14:6", (151.5, 80.2)]),
    ("THERM_WINDOW_SENSE", pcbnew.F_Cu, 0.20, ["U16:1", (120.0, 72.8)]),
    ("THERM_WINDOW_SENSE", pcbnew.In2_Cu, 0.20, [(151.5, 80.2), (151.5, 78.5), (136.0, 78.5), (136.0, 72.5), (120.0, 72.5), (120.0, 72.8)]),
    ("THERMISTOR_RANGE_OK", pcbnew.F_Cu, 0.20, ["U16:4", (128.9125, 75.95), "R30:2"]),
    ("SFS_INPUT", pcbnew.B_Cu, 0.20, ["J3:6", (109.4, 116.0), (172.0, 116.0), (172.0, 74.0), (129.0875, 74.0), (129.0875, 77.05)]),
    ("SFS_INPUT", pcbnew.F_Cu, 0.20, [(129.0875, 77.05), "R27:1"]),
    ("SFS_FIELD_INPUT", pcbnew.F_Cu, 0.20, ["R27:2", "U18:1"]),
    ("SFS_ADC", pcbnew.F_Cu, 0.20, ["U18:5", (140.0, 77.0)]),
    ("SFS_ADC", pcbnew.F_Cu, 0.20, ["U18:5", (137.0875, 75.0), "C10:1"]),
    ("SFS_ADC", pcbnew.F_Cu, 0.20, ["U7:7", (120.0, 78.5), (120.0, 83.5)]),
    ("SFS_ADC", pcbnew.In1_Cu, 0.20, [(140.0, 77.0), (170.0, 77.0), (170.0, 78.0), (120.0, 78.0), (120.0, 83.5)]),
    ("SFS_RANGE_OK", pcbnew.F_Cu, 0.20, ["U17:4", (132.0, 83.95), "R31:2"]),
    ("VRAW_MONITOR_ADC", pcbnew.F_Cu, 0.20, ["R28:2", (103.0, 40.0), (103.0, 42.0)]),
    ("VRAW_MONITOR_ADC", pcbnew.In2_Cu, 0.20, [(103.0, 42.0), (99.0, 42.0), (99.0, 69.5), (133.0875, 69.5)]),
    ("VRAW_MONITOR_ADC", pcbnew.F_Cu, 0.20, [(133.0875, 69.5), "R29:1"]),
    ("VRAW_MONITOR_ADC", pcbnew.F_Cu, 0.20, ["R29:1", "C11:1"]),
    ("VRAW_MONITOR_ADC", pcbnew.In1_Cu, 0.20, [(133.0875, 69.5), (119.2, 69.5), (119.2, 76.0)]),
    ("VRAW_MONITOR_ADC", pcbnew.F_Cu, 0.20, [(119.2, 76.0), (119.2, 78.0), "U7:8"]),
]

VIAS_MM = [
    # net, x_mm, y_mm, width_mm, drill_mm
    ("GND", 111.8, 81.5, 0.60, 0.30),
    ("GND", 107.5, 48.95, 0.60, 0.30),
    ("GND", 117.5, 48.0, 0.60, 0.30),
    ("GND", 116.95, 91.8, 0.60, 0.30),
    ("GND", 127.95, 91.8, 0.60, 0.30),
    ("GND", 108.6, 62.625, 0.50, 0.25),
    ("GND", 119.4, 66.0, 0.50, 0.25),
    ("GND", 106.0, 72.5, 0.50, 0.25),
    ("COMMON_LINE", 88.0, 89.54, 0.60, 0.30),
    ("ISO_REMOTE_5V", 101.5, 89.54, 0.60, 0.30),
    ("ISO_REMOTE_5V", 113.5, 100.0, 0.60, 0.30),
    ("I2C_SDA", 108.2, 64.575, 0.50, 0.25),
    ("I2C_SDA", 102.0875, 58.8, 0.50, 0.25),
    ("I2C_SDA", 109.5, 77.4, 0.50, 0.25),
    ("I2C_SCL", 108.8, 63.925, 0.50, 0.25),
    ("I2C_SCL", 102.0875, 56.0, 0.50, 0.25),
    ("I2C_SCL", 109.5, 78.5, 0.50, 0.25),
    ("VAL_OPTO_GPIO", 119.0, 61.325, 0.50, 0.25),
    ("VAL_OPTO_GPIO", 124.0, 44.0, 0.50, 0.25),
    ("TH_OPTO_GPIO", 116.5, 60.675, 0.50, 0.25),
    ("TH_OPTO_GPIO", 129.0, 50.0, 0.50, 0.25),
    ("IND_OPTO_GPIO", 115.8, 60.025, 0.50, 0.25),
    ("IND_OPTO_GPIO", 35.0, 56.0, 0.50, 0.25),
    ("IND_OPTO_GPIO", 135.0, 50.0, 0.50, 0.25),
    ("VAC24_OPTO_GPIO", 115.0, 59.375, 0.50, 0.25),
    ("VAC24_OPTO_GPIO", 58.0, 62.0, 0.50, 0.25),
    ("VAC24_OPTO_GPIO", 133.0, 65.0, 0.50, 0.25),
    ("ICM_24VAC_SOURCE", 34.0, 78.0, 0.50, 0.25),
    ("IND_SENSE_AC", 23.0875, 71.0, 0.50, 0.25),
    ("+5V", 93.53, 68.5, 0.60, 0.30),
    ("+5V", 106.0, 38.5, 0.60, 0.30),
    ("PGND_RAW", 51.5, 60.0, 0.60, 0.30),
    ("PGND_RAW", 51.5, 64.1, 0.60, 0.30),
    ("WATCHDOG_OK", 117.8, 46.0, 0.60, 0.30),
    ("WATCHDOG_OK", 122.0, 38.0, 0.60, 0.30),
    ("VAC24_A_FUSED", 51.03, 41.0, 0.60, 0.30),
    ("BST_5V", 59.2, 65.36, 0.60, 0.30),
    ("BST_5V", 59.4, 62.0, 0.60, 0.30),
    ("GND", 97.6, 66.0, 0.60, 0.30),
    ("GND", 97.6, 70.0, 0.60, 0.30),
    ("GND", 33.06, 97.7, 0.60, 0.30),
    ("GND", 77.06, 97.7, 0.60, 0.30),
    ("GND", 111.8, 97.7, 0.60, 0.30),
    ("GND", 142.0, 49.74, 0.60, 0.30),
    ("VAL_SENSE_AC", 124.5, 43.0, 0.60, 0.30),
    ("VAL_SENSE_AC", 22.0, 64.0, 0.50, 0.25),
    ("GND", 128.0, 75.0, 0.60, 0.30),
    ("GND", 128.0, 83.0, 0.60, 0.30),
    ("THERMISTOR_A", 144.5, 80.2, 0.60, 0.30),
    ("THERMISTOR_B", 144.5, 82.8, 0.60, 0.30),
    ("+3V3_ADC", 144.5, 84.2, 0.60, 0.30),
    ("+3V3_ADC", 130.0, 79.5, 0.60, 0.30),
    ("AGND", 157.5, 84.2, 0.60, 0.30),
    ("AGND", 140.0, 79.5, 0.60, 0.30),
    ("THERMISTOR_ADC", 151.5, 82.0, 0.60, 0.30),
    ("THERMISTOR_ADC", 153.4, 85.3, 0.60, 0.30),
    ("THERMISTOR_ADC", 118.0, 82.0, 0.60, 0.30),
    ("THERM_WINDOW_SENSE", 151.5, 80.2, 0.60, 0.30),
    ("THERM_WINDOW_SENSE", 120.0, 72.8, 0.60, 0.30),
    ("SFS_ADC", 140.0, 77.0, 0.60, 0.30),
    ("SFS_ADC", 120.0, 83.5, 0.60, 0.30),
    ("SFS_INPUT", 129.0875, 77.05, 0.50, 0.25),
    ("AGND", 158.7, 87.0, 0.50, 0.25),
    ("AGND", 169.5, 87.0, 0.50, 0.25),
    ("THERM_LOW_REF_TBD", 120.0, 75.0, 0.50, 0.25),
    ("THERM_LOW_REF_TBD", 164.0, 82.0, 0.50, 0.25),
    ("THERM_HIGH_REF_TBD", 122.0, 75.95, 0.50, 0.25),
    ("THERM_HIGH_REF_TBD", 164.0, 88.0, 0.50, 0.25),
    ("SFS_LOW_REF_TBD", 121.0, 83.0, 0.50, 0.25),
    ("SFS_LOW_REF_TBD", 164.0, 90.0, 0.50, 0.25),
    ("SFS_HIGH_REF_TBD", 124.0, 83.95, 0.50, 0.25),
    ("SFS_HIGH_REF_TBD", 164.0, 94.0, 0.50, 0.25),
    ("VRAW_MONITOR_ADC", 103.0, 42.0, 0.50, 0.25),
    ("VRAW_MONITOR_ADC", 133.0875, 69.5, 0.50, 0.25),
    ("VRAW_MONITOR_ADC", 119.2, 76.0, 0.50, 0.25),
]


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def as_point(point: tuple[float, float]) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(point[0]), mm(point[1]))


def pad_lookup(board: pcbnew.BOARD) -> dict[str, dict[str, list[pcbnew.PAD]]]:
    refs: dict[str, dict[str, list[pcbnew.PAD]]] = {}
    for fp in board.GetFootprints():
        pads: dict[str, list[pcbnew.PAD]] = {}
        for pad in fp.Pads():
            pads.setdefault(pad.GetNumber(), []).append(pad)
        refs[fp.GetReference()] = pads
    return refs


def resolve_point(refs: dict[str, dict[str, list[pcbnew.PAD]]], item: str | tuple[float, float]) -> pcbnew.VECTOR2I:
    if isinstance(item, tuple):
        return as_point(item)
    ref, pad = item.split(":", 1)
    return refs[ref][pad][0].GetPosition()


def ensure_net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    existing = board.FindNet(name)
    if existing:
        return existing
    net = pcbnew.NETINFO_ITEM(board, name)
    board.Add(net)
    return net


def clear_draft_tracks(board: pcbnew.BOARD) -> None:
    for track in list(board.GetTracks()):
        board.Remove(track)


def add_track(
    board: pcbnew.BOARD,
    net: pcbnew.NETINFO_ITEM,
    layer: int,
    start: pcbnew.VECTOR2I,
    end: pcbnew.VECTOR2I,
    width_mm: float,
) -> None:
    track = pcbnew.PCB_TRACK(board)
    track.SetLayer(layer)
    track.SetNet(net)
    track.SetStart(start)
    track.SetEnd(end)
    track.SetWidth(mm(width_mm))
    board.Add(track)


def add_via(
    board: pcbnew.BOARD,
    net: pcbnew.NETINFO_ITEM,
    point: pcbnew.VECTOR2I,
    width_mm: float,
    drill_mm: float,
) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetNet(net)
    via.SetPosition(point)
    via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    via.SetWidth(mm(width_mm))
    via.SetDrill(mm(drill_mm))
    board.Add(via)


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    board.GetDesignSettings().m_MinThroughDrill = mm(0.2)
    refs = pad_lookup(board)

    nets = {name for pads in NETS_BY_PAD.values() for name in pads.values()}
    nets.update(route[0] for route in ROUTES_MM)
    net_items = {name: ensure_net(board, name) for name in sorted(nets)}

    for ref, pads in CLEAR_NETS_BY_PAD.items():
        for pad_no in pads:
            for pad in refs[ref][pad_no]:
                pad.SetNetCode(0)

    for ref, pads in NETS_BY_PAD.items():
        for pad_no, net_name in pads.items():
            for pad in refs[ref][pad_no]:
                pad.SetNet(net_items[net_name])

    clear_draft_tracks(board)
    for net_name, layer, width_mm, path in ROUTES_MM:
        points = [resolve_point(refs, item) for item in path]
        for start, end in zip(points, points[1:]):
            add_track(board, net_items[net_name], layer, start, end, width_mm)

    for net_name, x, y, width_mm, drill_mm in VIAS_MM:
        add_via(board, net_items[net_name], as_point((x, y)), width_mm, drill_mm)

    board.BuildListOfNets()
    board.SanitizeNetcodes()
    pcbnew.SaveBoard(str(BOARD_PATH), board)


if __name__ == "__main__":
    main()
