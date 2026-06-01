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
        "1": "24VAC_A",
        "2": "24VAC_B",
        "3": "EARTH_SHIELD_REF",
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
        "2": "GND",
        "5": "+5V",
        "6": "SW_3V3",
    },
    "L2": {
        "1": "SW_3V3",
        "2": "+3V3",
    },
    "U3": {
        "1": "ESP32_EN",
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
    "U7": {
        "3": "I2C_SDA",
        "4": "I2C_SCL",
        "5": "GND",
        "6": "THERMISTOR_ADC",
        "7": "SFS_ADC",
        "8": "TH_FEEDBACK_ADC",
        "9": "VAL_SENSE_ADC",
        "10": "+3V3",
    },
}


ROUTES_MM = [
    # net, layer, width_mm, point sequence. Route only the relay contact chain
    # here; the remaining nets stay as named/unrouted until schematic capture.
    ("ICM_24VAC_SOURCE", pcbnew.F_Cu, 0.60, ["J2:5", (64.32, 98.0), (53.16, 98.0), "K1:2"]),
    ("HEAT_CHAIN_K1_K2", pcbnew.F_Cu, 0.60, ["K1:3", (60.78, 84.0), (76.16, 84.0), "K2:2"]),
    ("TH_HEAT_REQUEST_OUT", pcbnew.B_Cu, 0.60, ["K2:3", (87.78, 99.0), (49.08, 99.0), "J2:2"]),
]


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def as_point(point: tuple[float, float]) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(point[0]), mm(point[1]))


def pad_lookup(board: pcbnew.BOARD) -> dict[str, dict[str, pcbnew.PAD]]:
    refs: dict[str, dict[str, pcbnew.PAD]] = {}
    for fp in board.GetFootprints():
        refs[fp.GetReference()] = {pad.GetNumber(): pad for pad in fp.Pads()}
    return refs


def resolve_point(refs: dict[str, dict[str, pcbnew.PAD]], item: str | tuple[float, float]) -> pcbnew.VECTOR2I:
    if isinstance(item, tuple):
        return as_point(item)
    ref, pad = item.split(":", 1)
    return refs[ref][pad].GetPosition()


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


def main() -> None:
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    board.GetDesignSettings().m_MinThroughDrill = mm(0.2)
    refs = pad_lookup(board)

    nets = {name for pads in NETS_BY_PAD.values() for name in pads.values()}
    nets.update(route[0] for route in ROUTES_MM)
    net_items = {name: ensure_net(board, name) for name in sorted(nets)}

    for ref, pads in NETS_BY_PAD.items():
        for pad_no, net_name in pads.items():
            refs[ref][pad_no].SetNet(net_items[net_name])

    clear_draft_tracks(board)
    for net_name, layer, width_mm, path in ROUTES_MM:
        points = [resolve_point(refs, item) for item in path]
        for start, end in zip(points, points[1:]):
            add_track(board, net_items[net_name], layer, start, end, width_mm)

    board.BuildListOfNets()
    board.SanitizeNetcodes()
    pcbnew.SaveBoard(str(BOARD_PATH), board)


if __name__ == "__main__":
    main()
