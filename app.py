import streamlit as st
import math

# ================= MATERIAL TABLE =================
kc_data = {
    "Aluminium": 700,
    "Steel_Hardness_upto_30_HRC": 1950,
    "Steel_Hardness_30_to_40_HRC": 2250,
    "Stainless_Steel": 2400
}

# ================= MACHINE TABLE (WITH TAPER TAGS) =================
machine_data = {
    "Ace BT40": {"power": 5.5, "torque": 35, "taper": "BT40"},
    "Ace HSK63": {"power": 5.5, "torque": 35, "taper": "HSK A63"},

    "Brother Std BT30": {"power": 7, "torque": 26.8, "taper": "BT30"},
    "Brother High Torque BT30": {"power": 9.2, "torque": 61.1, "taper": "BT30"},

    "Fanuc Std BT30": {"power": 3.7, "torque": 11.8, "taper": "BT30"},
    "Fanuc High Torque BT30": {"power": 3.7, "torque": 27.6, "taper": "BT30"},

    "Makino Slim HSK50": {"power": 11, "torque": 33, "taper": "HSK A50"},
    "Makino PS65 BT40": {"power": 18.5, "torque": 95, "taper": "BT40"},
    "Makino PS65 HSK63": {"power": 18.5, "torque": 95, "taper": "HSK A63"}
}


drill_data_aluminium = [
            {"min_d": 0.5, "max_d": 1, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
            {"min_d": 1, "max_d": 3, "rpm": 6500, "feed_min": 100, "max_depth": 5},

            {"min_d": 3, "max_d": 5, "vc": 50, "feed_min": 450, "max_depth": 20},
            {"min_d": 5, "max_d": 8, "vc": 80, "feed_min": 550, "max_depth": 30},
            {"min_d": 8, "max_d": 10, "vc": 100, "feed_min": 480, "max_depth": 40},
            {"min_d": 10, "max_d": 15, "vc": 120, "feed_min": 550, "max_depth": 50},

            {"min_d": 15, "max_d": 16, "rpm": 2464, "feed_min": 444, "max_depth": 48},
            {"min_d": 16, "max_d": 17, "rpm": 2508, "feed_min": 451, "max_depth": 51},
            {"min_d": 17, "max_d": 18, "rpm": 2364, "feed_min": 426, "max_depth": 54},
            {"min_d": 18, "max_d": 19, "rpm": 2409, "feed_min": 482, "max_depth": 57},
            {"min_d": 19, "max_d": 20, "rpm": 2448, "feed_min": 490, "max_depth": 60},

            {"min_d": 20, "max_d": 21, "rpm": 2484, "feed_min": 248, "max_depth": 63},
            {"min_d": 21, "max_d": 22, "rpm": 2369, "feed_min": 237, "max_depth": 66},
            {"min_d": 22, "max_d": 23, "rpm": 2263, "feed_min": 226, "max_depth": 69},
            {"min_d": 23, "max_d": 24, "rpm": 2167, "feed_min": 238, "max_depth": 72},

            {"min_d": 24, "max_d": 25, "rpm": 2338, "feed_min": 234, "max_depth": 75},
            {"min_d": 25, "max_d": 26, "rpm": 2371, "feed_min": 249, "max_depth": 78},
            {"min_d": 26, "max_d": 27, "rpm": 2402, "feed_min": 240, "max_depth": 81},
            {"min_d": 27, "max_d": 28, "rpm": 2315, "feed_min": 232, "max_depth": 84},
            {"min_d": 28, "max_d": 29, "rpm": 2233, "feed_min": 223, "max_depth": 87},
            {"min_d": 29, "max_d": 30, "rpm": 2158, "feed_min": 216, "max_depth": 90},
            {"min_d": 30, "max_d": 35, "vc": 150, "feed_min": 159, "max_depth": 105},
            {"min_d": 35, "max_d": 45, "vc": 170, "feed_min": 155, "max_depth": 125},
            {"min_d": 45, "max_d": 55, "vc": 180, "feed_min": 127, "max_depth": 125},
            {"min_d": 55, "max_d": 65, "vc": 180, "feed_min": 115, "max_depth": 150},
]

drill_data_Steel_Hardness_upto_30_HRC = [
            {"min_d": 0.5, "max_d": 1, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
            {"min_d": 1, "max_d": 2, "rpm": 6365, "feed_min": 95, "max_depth": 5},
            {"min_d": 2, "max_d": 3, "rpm": 5570, "feed_min": 167, "max_depth": 10},

            {"min_d": 3, "max_d": 4, "vc": 40, "feed_min": 297, "max_depth": 15},
            {"min_d": 4, "max_d": 6, "vc": 45, "feed_min": 301, "max_depth": 20},
            {"min_d": 6, "max_d": 8, "vc": 50, "feed_min": 301, "max_depth": 30},
            {"min_d": 8, "max_d": 10, "vc": 60, "feed_min": 334, "max_depth": 50},
            {"min_d": 10, "max_d": 12, "vc": 60, "feed_min": 306, "max_depth": 50},
            {"min_d": 12, "max_d": 14, "vc": 60, "feed_min": 255, "max_depth": 60},

            {"min_d": 14, "max_d": 16, "rpm": 1478, "feed_min": 259, "max_depth": 70},
            {"min_d": 16, "max_d": 18, "rpm": 1293, "feed_min": 233, "max_depth": 80},
            {"min_d": 18, "max_d": 21, "rpm": 1238, "feed_min": 248, "max_depth": 90},
            {"min_d": 21, "max_d": 27, "rpm": 1364, "feed_min": 205, "max_depth": 105},
            {"min_d": 27, "max_d": 32, "rpm": 1061, "feed_min": 127, "max_depth": 135},

            {"min_d": 32, "max_d": 45, "vc": 90, "feed_min": 107, "max_depth": 105},
            {"min_d": 45, "max_d": 51, "vc": 100, "feed_min": 106, "max_depth": 125},
            {"min_d": 51, "max_d": 65, "vc": 100, "feed_min": 94, "max_depth": 150},
           
]

tap_data_aluminium  = [
    {"tap": "M3", "pitch": 0.5, "vc": 5, "max_depth": 9},
    {"tap": "M3.5", "pitch": 0.6, "vc": 5, "max_depth": 10.5},
    {"tap": "M4", "pitch": 0.7, "vc": 6, "max_depth": 12},
    {"tap": "M5", "pitch": 0.8, "vc": 8, "max_depth": 15},
    {"tap": "M6", "pitch": 1, "vc": 10, "max_depth": 18},
    {"tap": "M7", "pitch": 1, "vc": 10, "max_depth": 21},
    {"tap": "M8", "pitch": 1.25, "vc": 12, "max_depth": 24},
    {"tap": "M10", "pitch": 1.5, "vc": 15, "max_depth": 30},
    {"tap": "M12", "pitch": 1.75, "vc": 15, "max_depth": 36},
    {"tap": "M14", "pitch": 2, "vc": 16, "max_depth": 42},
    {"tap": "M16", "pitch": 2, "vc": 20, "max_depth": 48},
    {"tap": "M16", "pitch": 1, "vc": 20, "max_depth": 48},
    {"tap": "M16", "pitch": 1.5, "vc": 20, "max_depth": 48},
    {"tap": "M6", "pitch": 0.5, "vc": 10, "max_depth": 18},
    {"tap": "M6", "pitch": 0.75, "vc": 10, "max_depth": 18},
    {"tap": "M8", "pitch": 0.5, "vc": 12, "max_depth": 24},
    {"tap": "M8", "pitch": 0.75, "vc": 12, "max_depth": 24},
    {"tap": "M8", "pitch": 1, "vc": 12, "max_depth": 24},
    {"tap": "M9", "pitch": 1, "vc": 12, "max_depth": 27},
    {"tap": "M10", "pitch": 0.75, "vc": 15, "max_depth": 30},
    {"tap": "M10", "pitch": 1.25, "vc": 15, "max_depth": 30},
    {"tap": "M10", "pitch": 1, "vc": 15, "max_depth": 30},
    {"tap": "M12", "pitch": 1, "vc": 15, "max_depth": 36},
    {"tap": "M12", "pitch": 1.25, "vc": 15, "max_depth": 36},
    {"tap": "M12", "pitch": 1.5, "vc": 15, "max_depth": 36},
    {"tap": "M14", "pitch": 1, "vc": 16, "max_depth": 42},
    {"tap": "M14", "pitch": 1.25, "vc": 16, "max_depth": 42},
    {"tap": "M14", "pitch": 1.5, "vc": 16, "max_depth": 42},
    {"tap": "M18", "pitch": 2.5, "vc": 20, "max_depth": 54},
    {"tap": "M20", "pitch": 2.5, "vc": 20, "max_depth": 60},
]

tap_data_Steel_Hardness_upto_30_HRC = [
    {"tap": "M3", "pitch": 0.5, "vc": 5, "max_depth": 9},
    {"tap": "M3.5", "pitch": 0.6, "vc": 5, "max_depth": 10.5},
    {"tap": "M4", "pitch": 0.7, "vc": 5, "max_depth": 12},
    {"tap": "M5", "pitch": 0.8, "vc": 6, "max_depth": 15},
    {"tap": "M6", "pitch": 1, "vc": 8, "max_depth": 18},
    {"tap": "M7", "pitch": 1, "vc": 8, "max_depth": 21},
    {"tap": "M8", "pitch": 1.25, "vc": 8, "max_depth": 24},
    {"tap": "M10", "pitch": 1.5, "vc": 10, "max_depth": 30},
    {"tap": "M12", "pitch": 1.75, "vc": 12, "max_depth": 36},
    {"tap": "M14", "pitch": 2, "vc": 15, "max_depth": 42},
    {"tap": "M16", "pitch": 2, "vc": 15, "max_depth": 48},
    {"tap": "M16", "pitch": 1, "vc": 15, "max_depth": 48},
    {"tap": "M16", "pitch": 1.5, "vc": 15, "max_depth": 48},
    {"tap": "M6", "pitch": 0.5, "vc": 8, "max_depth": 18},
    {"tap": "M6", "pitch": 0.75, "vc": 8, "max_depth": 18},
    {"tap": "M8", "pitch": 0.5, "vc": 8, "max_depth": 24},
    {"tap": "M8", "pitch": 0.75, "vc": 8, "max_depth": 24},
    {"tap": "M8", "pitch": 1, "vc": 8, "max_depth": 24},
    {"tap": "M9", "pitch": 1, "vc": 8, "max_depth": 27},
    {"tap": "M10", "pitch": 0.75, "vc": 10, "max_depth": 30},
    {"tap": "M10", "pitch": 1.25, "vc": 10, "max_depth": 30},
    {"tap": "M10", "pitch": 1, "vc": 10, "max_depth": 30},
    {"tap": "M12", "pitch": 1, "vc": 12, "max_depth": 36},
    {"tap": "M12", "pitch": 1.25, "vc": 12, "max_depth": 36},
    {"tap": "M12", "pitch": 1.5, "vc": 12, "max_depth": 36},
    {"tap": "M14", "pitch": 1, "vc": 15, "max_depth": 42},
    {"tap": "M14", "pitch": 1.25, "vc": 15, "max_depth": 42},
    {"tap": "M14", "pitch": 1.5, "vc": 15, "max_depth": 42},
    {"tap": "M18", "pitch": 2.5, "vc": 20, "max_depth": 54},
    {"tap": "M20", "pitch": 2.5, "vc": 20, "max_depth": 60},
]
threadmill_data_aluminium = [
    {"tap": "M3", "tool_dia": 2.3, "pitch": 0.5, "vc": 30, "feed_rev": 0.06, "max_depth": 7.5},
    {"tap": "M4", "tool_dia": 3, "pitch": 0.7, "vc": 30, "feed_rev": 0.09, "max_depth": 10},
    {"tap": "M5", "tool_dia": 4, "pitch": 0.8, "vc": 50, "feed_rev": 0.12, "max_depth": 12.5},
    {"tap": "M6", "tool_dia": 4.8, "pitch": 1, "vc": 50, "feed_rev": 0.14, "max_depth": 15},
    {"tap": "M8", "tool_dia": 6.4, "pitch": 1.25, "vc": 60, "feed_rev": 0.15, "max_depth": 20},
    {"tap": "M8", "tool_dia": 6.4, "pitch": 1, "vc": 60, "feed_rev": 0.14, "max_depth": 20},
    {"tap": "M10", "tool_dia": 7.95, "pitch": 1.5, "vc": 70, "feed_rev": 0.14, "max_depth": 25},
    {"tap": "M10", "tool_dia": 7.95, "pitch": 1, "vc": 70, "feed_rev": 0.14, "max_depth": 25},
    {"tap": "M10", "tool_dia": 7.95, "pitch": 1.25, "vc": 80, "feed_rev": 0.14, "max_depth": 25},
    {"tap": "M12", "tool_dia": 9.95, "pitch": 1.75, "vc": 80, "feed_rev": 0.20, "max_depth": 30},
    {"tap": "M12", "tool_dia": 9.95, "pitch": 1.5, "vc": 80, "feed_rev": 0.20, "max_depth": 30},
    {"tap": "M14", "tool_dia": 11.2, "pitch": 2, "vc": 90, "feed_rev": 0.20, "max_depth": 35},
    {"tap": "M14", "tool_dia": 11.2, "pitch": 1.5, "vc": 90, "feed_rev": 0.20, "max_depth": 35},
    {"tap": "M16", "tool_dia": 12.8, "pitch": 2, "vc": 120, "feed_rev": 0.20, "max_depth": 40},
    {"tap": "M16", "tool_dia": 12.8, "pitch": 1.5, "vc": 120, "feed_rev": 0.20, "max_depth": 40},
    {"tap": "M20", "tool_dia": 14.95, "pitch": 2.5, "vc": 120, "feed_rev": 0.20, "max_depth": 50},
    {"tap": "M20", "tool_dia": 14.95, "pitch": 1.5, "vc": 120, "feed_rev": 0.20, "max_depth": 50},
]
threadmill_data_Steel_Hardness_upto_30_HRC = [
    {"tap": "M3", "tool_dia": 2.3, "pitch": 0.5, "vc": 15, "feed_rev": 0.06, "max_depth": 7.5},
    {"tap": "M4", "tool_dia": 3, "pitch": 0.7, "vc": 15, "feed_rev": 0.09, "max_depth": 10},
    {"tap": "M5", "tool_dia": 4, "pitch": 0.8, "vc": 20, "feed_rev": 0.12, "max_depth": 12.5},
    {"tap": "M6", "tool_dia": 4.8, "pitch": 1, "vc": 25, "feed_rev": 0.14, "max_depth": 15},
    {"tap": "M8", "tool_dia": 6.4, "pitch": 1.25, "vc": 30, "feed_rev": 0.15, "max_depth": 20},
    {"tap": "M8", "tool_dia": 6.4, "pitch": 1, "vc": 30, "feed_rev": 0.15, "max_depth": 20},
    {"tap": "M10", "tool_dia": 7.95, "pitch": 1.5, "vc": 30, "feed_rev": 0.15, "max_depth": 25},
    {"tap": "M10", "tool_dia": 7.95, "pitch": 1, "vc": 30, "feed_rev": 0.15, "max_depth": 25},
    {"tap": "M10", "tool_dia": 7.95, "pitch": 1.25, "vc": 30, "feed_rev": 0.15, "max_depth": 25},
    {"tap": "M12", "tool_dia": 9.95, "pitch": 1.75, "vc": 45, "feed_rev": 0.15, "max_depth": 30},
    {"tap": "M12", "tool_dia": 9.95, "pitch": 1.5, "vc": 45, "feed_rev": 0.15, "max_depth": 30},
    {"tap": "M14", "tool_dia": 11.2, "pitch": 2, "vc": 45, "feed_rev": 0.20, "max_depth": 35},
    {"tap": "M14", "tool_dia": 11.2, "pitch": 1.5, "vc": 45, "feed_rev": 0.20, "max_depth": 35},
    {"tap": "M16", "tool_dia": 12.8, "pitch": 2, "vc": 60, "feed_rev": 0.20, "max_depth": 40},
    {"tap": "M16", "tool_dia": 12.8, "pitch": 1.5, "vc": 60, "feed_rev": 0.20, "max_depth": 40},
    {"tap": "M20", "tool_dia": 14.95, "pitch": 2.5, "vc": 70, "feed_rev": 0.21, "max_depth": 50},
    {"tap": "M20", "tool_dia": 14.95, "pitch": 1.5, "vc": 70, "feed_rev": 0.21, "max_depth": 50},
]
face_mill_data_aluminium = [
    {"dia": 3, "stock": 1, "vc": 50, "rpm": 5304, "feed": 477.4, "max_width": 2.4, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 6, "stock": 1.5, "vc": 70, "rpm": 3713, "feed": 445.6, "max_width": 4.8, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 8, "stock": 1.5, "vc": 100, "rpm": 3978, "feed": 477.4, "max_width": 6.4, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 10, "stock": 2, "vc": 120, "rpm": 3819, "feed": 572.9, "max_width": 8, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 12, "stock": 2, "vc": 140, "rpm": 3713, "feed": 557.0, "max_width": 9.6, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 14, "stock": 2, "vc": 160, "rpm": 3637, "feed": 654.7, "max_width": 11.2, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 16, "stock": 2, "vc": 180, "rpm": 3581, "feed": 644.5, "max_width": 12.8, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 20, "stock": 2, "vc": 200, "rpm": 3183, "feed": 668.4, "max_width": 16, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 25, "stock": 2, "vc": 300, "rpm": 3819, "feed": 802.0, "max_width": 17.5, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 32, "stock": 2, "vc": 350, "rpm": 3481, "feed": 1044.3, "max_width": 22.4, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 40, "stock": 2, "vc": 350, "rpm": 2785, "feed": 1113.9, "max_width": 28, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 50, "stock": 2, "vc": 400, "rpm": 2546, "feed": 1273.1, "max_width": 35, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 63, "stock": 2, "vc": 450, "rpm": 2273, "feed": 1227.6, "max_width": 44.1, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 80, "stock": 2, "vc": 450, "rpm": 1790, "feed": 1289.0, "max_width": 56, "spindles": ["HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 100, "stock": 2, "vc": 500, "rpm": 1591, "feed": 1273.1, "max_width": 70, "spindles": ["HSK A100","BT50"]},
]

face_mill_data_Steel_Hardness_upto_30_HRC = [
    {"dia": 3, "stock": 0.7, "vc": 40, "rpm": 4244, "feed": 213.9, "max_width": 2.4, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 6, "stock": 1.4, "vc": 60, "rpm": 3183, "feed": 244.4, "max_width": 4.8, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 8, "stock": 1.8, "vc": 80, "rpm": 3183, "feed": 320.8, "max_width": 6.4, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 10, "stock": 2.1, "vc": 80, "rpm": 2546, "feed": 336.9, "max_width": 8, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 12, "stock": 2.2, "vc": 100, "rpm": 2652, "feed": 417.7, "max_width": 9.6, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 14, "stock": 2.5, "vc": 120, "rpm": 2728, "feed": 491, "max_width": 11.2, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 16, "stock": 2.9, "vc": 120, "rpm": 2387, "feed": 458.3, "max_width": 12.8, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 20, "stock": 3.2, "vc": 140, "rpm": 2228, "feed": 467.9, "max_width": 16, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 25, "stock": 2, "vc": 100, "rpm": 1273, "feed": 305.5, "max_width": 17.5, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 32, "stock": 2, "vc": 100, "rpm": 995, "feed": 305.5, "max_width": 22.4, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 40, "stock": 2, "vc": 120, "rpm": 995, "feed": 381.9, "max_width": 28, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 50, "stock": 2, "vc": 140, "rpm": 891, "feed": 445.6, "max_width": 35, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 63, "stock": 2, "vc": 140, "rpm": 707, "feed": 381.9, "max_width": 44.1, "spindles": ["BT30","BBT30","HSK A50","HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 80, "stock": 2, "vc": 140, "rpm": 557, "feed": 356.5, "max_width": 56, "spindles": ["HSK A63","HSK A100","BT40","BT50"]},
    {"dia": 100, "stock": 2, "vc": 140, "rpm": 446, "feed": 356.5, "max_width": 70, "spindles": ["HSK A100","BT50"]},
]
boring_data_aluminium = [
    {"min": 0, "max": 1, "rpm": 7957, "feed_min": 159.1, "ap": 0.1},
    {"min": 1, "max": 2, "rpm": 7161, "feed_min": 143.2, "ap": 0.2},
    {"min": 2, "max": 3, "rpm": 5304, "feed_min": 265.2, "ap": 0.3},
    {"min": 3, "max": 4, "rpm": 4774, "feed_min": 477.4, "ap": 0.5},
    {"min": 4, "max": 5, "rpm": 4456, "feed_min": 445.6, "ap": 1.0},
    {"min": 5, "max": 6, "rpm": 4244, "feed_min": 424.4, "ap": 1.5},
    {"min": 6, "max": 7, "rpm": 3637, "feed_min": 363.7, "ap": 1.8},
    {"min": 7, "max": 8, "rpm": 3581, "feed_min": 429.7, "ap": 2.1},
    {"min": 8, "max": 9, "rpm": 3929, "feed_min": 471.5, "ap": 2.4},
    {"min": 9, "max": 10, "rpm": 3183, "feed_min": 381.9, "ap": 2.7},
    {"min": 10, "max": 11, "rpm": 3472, "feed_min": 486.1, "ap": 3.0},
    {"min": 11, "max": 12, "rpm": 3183, "feed_min": 477.4, "ap": 3.3},
    {"min": 12, "max": 13, "rpm": 3183, "feed_min": 477.4, "ap": 3.6},
    {"min": 13, "max": 14, "rpm": 3183, "feed_min": 477.4, "ap": 3.9},
    {"min": 14, "max": 15, "rpm": 3183, "feed_min": 477.4, "ap": 4.2},
    {"min": 15, "max": 16, "rpm": 2984, "feed_min": 447.6, "ap": 4.5},
    {"min": 16, "max": 17, "rpm": 2808, "feed_min": 421.2, "ap": 4.8},
    {"min": 17, "max": 18, "rpm": 2829, "feed_min": 424.4, "ap": 5.1},
    {"min": 18, "max": 19, "rpm": 3015, "feed_min": 452.3, "ap": 5.4},
    {"min": 19, "max": 20, "rpm": 2864, "feed_min": 429.7, "ap": 5.7},
    {"min": 20, "max": 25, "rpm": 2864, "feed_min": 515.6, "ap": 5.0},
    {"min": 25, "max": 30, "rpm": 2801, "feed_min": 560.1, "ap": 6.0},
    {"min": 30, "max": 35, "rpm": 2546, "feed_min": 509.2, "ap": 6.0},
    {"min": 35, "max": 40, "rpm": 2273, "feed_min": 454.7, "ap": 8.0},
    {"min": 40, "max": 45, "rpm": 1989, "feed_min": 477.4, "ap": 10.0},
    {"min": 45, "max": 50, "rpm": 1980, "feed_min": 435.7, "ap": 10.0},
    {"min": 50, "max": 55, "rpm": 1910, "feed_min": 420.1, "ap": 10.0},
    {"min": 55, "max": 60, "rpm": 1736, "feed_min": 381.9, "ap": 10.0},
    {"min": 60, "max": 65, "rpm": 1591, "feed_min": 350.1, "ap": 10.0},
    {"min": 65, "max": 70, "rpm": 1714, "feed_min": 377.0, "ap": 10.0},
]

boring_data_Steel_Hardness_upto_30_HRC = [
    {"min": 2, "max": 3, "rpm": 4244, "feed_min": 127.3, "ap": 0.2},
    {"min": 3, "max": 4, "rpm": 3183, "feed_min": 191, "ap": 0.3},
    {"min": 4, "max": 5, "rpm": 2864, "feed_min": 171.9, "ap": 0.5},
    {"min": 5, "max": 6, "rpm": 2652, "feed_min": 185.7, "ap": 1},
    {"min": 6, "max": 7, "rpm": 2273, "feed_min": 204.6, "ap": 1.5},
    {"min": 7, "max": 8, "rpm": 2387, "feed_min": 214.8, "ap": 1.5},
    {"min": 8, "max": 9, "rpm": 2358, "feed_min": 235.8, "ap": 2},
    {"min": 9, "max": 10, "rpm": 1910, "feed_min": 191, "ap": 2},
    {"min": 10, "max": 11, "rpm": 1736, "feed_min": 208.3, "ap": 2},
    {"min": 11, "max": 12, "rpm": 1591, "feed_min": 191, "ap": 2.5},
    {"min": 12, "max": 13, "rpm": 1469, "feed_min": 176.3, "ap": 2.5},
    {"min": 13, "max": 14, "rpm": 1364, "feed_min": 204.6, "ap": 2.5},
    {"min": 14, "max": 15, "rpm": 1379, "feed_min": 206.9, "ap": 2.5},
    {"min": 15, "max": 16, "rpm": 1293, "feed_min": 193.9, "ap": 2.5},
    {"min": 16, "max": 17, "rpm": 1217, "feed_min": 182.5, "ap": 3},
    {"min": 17, "max": 18, "rpm": 1238, "feed_min": 185.7, "ap": 3},
    {"min": 18, "max": 19, "rpm": 1173, "feed_min": 175.9, "ap": 3},
    {"min": 19, "max": 20, "rpm": 1432, "feed_min": 214.8, "ap": 3},
    {"min": 20, "max": 25, "rpm": 1910, "feed_min": 306, "ap": 3.0},
    {"min": 25, "max": 30, "rpm": 1528, "feed_min": 244, "ap": 3.0},
    {"min": 30, "max": 35, "rpm": 1485, "feed_min": 297, "ap": 3.0},
    {"min": 35, "max": 40, "rpm": 1455, "feed_min": 291, "ap": 4.0},
    {"min": 40, "max": 45, "rpm": 1432, "feed_min": 286, "ap": 4.0},
    {"min": 45, "max": 50, "rpm": 1132, "feed_min": 249, "ap": 4.0},
    {"min": 50, "max": 55, "rpm": 1018, "feed_min": 224, "ap": 5.0},
    {"min": 55, "max": 60, "rpm": 810, "feed_min": 178, "ap": 5.0},
    {"min": 60, "max": 65, "rpm": 743, "feed_min": 163, "ap": 6.0},
    {"min": 65, "max": 70, "rpm": 545, "feed_min": 129.0, "ap": 6.0},
    {"min": 70, "max": 85, "rpm": 500, "feed_min": 100.0, "ap": 6.0},
]

# ================= FINE BORING DATA =================

fine_boring_data_aluminium = [
    {"min": 3, "max": 5, "rpm": 6365, "feed_rev": 0.08, "ap": 0.5},
    {"min": 5, "max": 8, "rpm": 5729, "feed_rev": 0.08, "ap": 0.5},
    {"min": 8, "max": 12, "rpm": 5570, "feed_rev": 0.08, "ap": 0.5},
    {"min": 12, "max": 16, "rpm": 4244, "feed_rev": 0.08, "ap": 0.5},
    {"min": 16, "max": 20, "rpm": 3581, "feed_rev": 0.08, "ap": 0.5},
    {"min": 20, "max": 25, "vc": 175, "feed_rev": 0.08, "ap": 0.5},
    {"min": 25, "max": 30, "vc": 175, "feed_rev": 0.08, "ap": 0.5},
    {"min": 30, "max": 35, "vc": 175, "feed_rev": 0.08, "ap": 0.5},
    {"min": 35, "max": 40, "vc": 175, "feed_rev": 0.10, "ap": 0.5},
    {"min": 40, "max": 45, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 45, "max": 50, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 50, "max": 55, "vc": 200, "feed_rev": 0.10, "ap": 0.5},
    {"min": 55, "max": 60, "vc": 200, "feed_rev": 0.10, "ap": 0.5},
    {"min": 60, "max": 65, "vc": 200, "feed_rev": 0.10, "ap": 0.5},
    {"min": 65, "max": 70, "vc": 200, "feed_rev": 0.12, "ap": 0.5},
]

fine_boring__data_Steel_Hardness_upto_30_HRC = [

    {"min": 3, "max": 5, "rpm": 4244, "feed_rev": 0.06, "ap": 0.5},
    {"min": 5, "max": 8, "rpm": 3183, "feed_rev": 0.12, "ap": 0.5},
    {"min": 8, "max": 12, "rpm": 2785, "feed_rev": 0.06, "ap": 0.5},
    {"min": 12, "max": 16, "rpm": 2652, "feed_rev": 0.07, "ap": 0.5},
    {"min": 16, "max": 20, "rpm": 2387, "feed_rev": 0.08, "ap": 0.5},
    {"min": 20, "max": 25, "vc": 140, "feed_rev": 0.08, "ap": 0.3},
    {"min": 25, "max": 30, "vc": 140, "feed_rev": 0.08, "ap": 0.3},
    {"min": 30, "max": 35, "vc": 155, "feed_rev": 0.08, "ap": 0.4},
    {"min": 35, "max": 40, "vc": 160, "feed_rev": 0.08, "ap": 0.4},
    {"min": 40, "max": 45, "vc": 170, "feed_rev": 0.08, "ap": 0.4},
    {"min": 45, "max": 50, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 50, "max": 55, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 55, "max": 60, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 60, "max": 65, "vc": 160, "feed_rev": 0.10, "ap": 0.5},
    {"min": 65, "max": 70, "vc": 140, "feed_rev": 0.1, "ap": 0.5},
    {"min": 70, "max": 80, "vc": 140, "feed_rev": 0.1, "ap": 0.5},
]

# ==========================================
# 1. MATERIAL MASTER TABLE
# ==========================================
material_tables = {
    "Aluminium": {
        "drill": drill_data_aluminium,
        "boring": boring_data_aluminium,
        "fine_boring": fine_boring_data_aluminium,
        "tap": tap_data_aluminium,
        "threadmill": threadmill_data_aluminium,
        "face_mill": face_mill_data_aluminium
    },

    "Steel_Hardness_upto_30_HRC": {
        "drill": drill_data_Steel_Hardness_upto_30_HRC,
        "boring": boring_data_Steel_Hardness_upto_30_HRC,
        "fine_boring": fine_boring__data_Steel_Hardness_upto_30_HRC,
        "tap": tap_data_Steel_Hardness_upto_30_HRC,
        "threadmill": threadmill_data_Steel_Hardness_upto_30_HRC,
        "face_mill": face_mill_data_Steel_Hardness_upto_30_HRC
    },

    "Steel_Hardness_30_to_40_HRC": {
        "drill": drill_data_Steel_Hardness_upto_30_HRC,
        "boring": boring_data_Steel_Hardness_upto_30_HRC,
        "fine_boring": fine_boring__data_Steel_Hardness_upto_30_HRC,
        "tap": tap_data_Steel_Hardness_upto_30_HRC,
        "threadmill": threadmill_data_Steel_Hardness_upto_30_HRC,
        "face_mill": face_mill_data_Steel_Hardness_upto_30_HRC
    },

    "Stainless_Steel": {
        "drill": drill_data_Steel_Hardness_upto_30_HRC,
        "boring": boring_data_Steel_Hardness_upto_30_HRC,
        "fine_boring": fine_boring__data_Steel_Hardness_upto_30_HRC,
        "tap": tap_data_Steel_Hardness_upto_30_HRC,
        "threadmill": threadmill_data_Steel_Hardness_upto_30_HRC,
        "face_mill": face_mill_data_Steel_Hardness_upto_30_HRC
    }
}

# ==========================================
# 2. LOOKUP FUNCTIONS
# ==========================================
def get_parameters(diameter, material):
    table = material_tables[material]["drill"]

    for row in table:
        if row["min_d"] <= diameter < row["max_d"]:  # changed <= to < for max_d

            if "rpm" in row:
                rpm = row["rpm"]
            else:
                rpm = (1000 * row["vc"]) / (math.pi * diameter)

            feed = row["feed_min"]
            max_depth = row["max_depth"]

            # Harder steel correction
            if material == "Steel_Hardness_30_to_40_HRC":
                rpm *= 0.90      # 10% lower speed
                feed *= 0.95     # 5% lower feed

            elif material == "Stainless_Steel":
                rpm *= 0.75
                feed *= 0.80

            return rpm, feed, max_depth

    return None, None, None

def get_boring_params(dia, material):

    if "boring" in material_tables[material] and len(material_tables[material]["boring"]) > 0:
        table = material_tables[material]["boring"]
    else:
        table = material_tables["Aluminium"]["boring"]

    for row in table:
        if row["min"] <= dia < row["max"]:

            result = row.copy()

            if material == "Steel_Hardness_30_to_40_HRC":
                result["rpm"] *= 0.90
                result["feed_min"] *= 0.95

            elif material == "Stainless_Steel":
                result["rpm"] *= 0.80
                result["feed_min"] *= 0.90

            return result

    return None

def get_fine_boring_params(dia, material):

    if (
        "fine_boring" in material_tables[material]
        and len(material_tables[material]["fine_boring"]) > 0
    ):
        table = material_tables[material]["fine_boring"]
    else:
        return None

    for row in table:
        if row["min"] <= dia < row["max"]:

            result = row.copy()

            # Handle both rpm-direct and vc-based rows
            if "rpm" not in result:
                result["rpm"] = (1000 * result["vc"]) / (math.pi * dia)

            if material == "Steel_Hardness_30_to_40_HRC":
                result["vc"] *= 0.90
                result["feed_rev"] *= 0.95

            elif material == "Stainless_Steel":
                result["vc"] *= 0.80
                result["feed_rev"] *= 0.90

            return result

    return None

def get_diameter(tap):
    return float(tap.replace("M", ""))

def filter_tools_by_spindle(spindle, material):
    # Ensure face_mill exists in your table for this material
    if "face_mill" in material_tables[material]:
        table = material_tables[material]["face_mill"]
        return [t for t in table if spindle in t["spindles"]]
    return []

def select_tool_rect(min_dim, tools):
    tools_sorted = sorted(tools, key=lambda x: x["max_width"], reverse=True)
    return tools_sorted[0] if tools_sorted else None

def select_tool_circular(dia, tools):
    for t in tools:
        if t["max_width"] >= dia:
            return t
    return None

st.title("Smart Machining Calculator")
st.divider()
# ==========================================
# SIDEBAR - GLOBAL SETTINGS
# ==========================================
st.sidebar.header("Global Settings")
material = st.sidebar.selectbox("Select Material", list(kc_data.keys()), key="global_mat")
kc = kc_data[material]
machine = st.sidebar.selectbox("Select Machine", list(machine_data.keys()), key="global_mach")

if "last_machine" not in st.session_state:
    st.session_state.last_machine = machine
if st.session_state.last_machine != machine:
    st.session_state.global_power = machine_data[machine]["power"]
    st.session_state.global_torque = machine_data[machine]["torque"]
    st.session_state.last_machine = machine

default_power = machine_data[machine]["power"]
default_torque = machine_data[machine]["torque"]
m_taper = machine_data[machine].get("taper", "BT40")

m_power = st.sidebar.number_input("Available Spindle Power (kW)", min_value=0.1, value=float(default_power), step=0.5, key="global_power")
m_torque = st.sidebar.number_input("Available Spindle Torque (Nm)", min_value=0.1, value=float(default_torque), step=1.0, key="global_torque")
st.sidebar.info(f"Using: {m_power:.1f}kW | {m_torque:.1f}Nm | {m_taper}")
st.sidebar.markdown("---")

st.sidebar.header("Cycle Time Settings")
tool_change_time = st.sidebar.number_input("Tool Change Time (sec)", min_value=0.0, value=8.0, step=0.5, key="tool_change_time")
position_time = st.sidebar.number_input("Position / Index Time (sec)", min_value=0.0, value=3.0, step=0.5, key="position_time")

usable_power = m_power * 0.85
usable_torque = m_torque * 0.85
st.sidebar.caption(f"Calculation uses 85% capacity: {usable_power:.2f} kW | {usable_torque:.1f} Nm")

# ==========================================
# INDIVIDUAL MODE (4 spaces indentation)
# ==========================================
operation = None

if operation != "Tapping":
    st.sidebar.header("Quality Requirements")
    ra_input = st.sidebar.number_input("Surface Finish (Ra)", value=3.2, step=0.1, key="sidebar_ra")
    if operation in ["Drilling", "Boring / Hole Milling"]:
        tol_input = st.sidebar.number_input("Diameter Tolerance (±)", value=0.100, format="%.3f", key="sidebar_tol")
    else:
        tol_input = 0.1
else:
    ra_input, tol_input = 3.2, 0.1

def calculate_boring_operation(
    f_dia,
    b_dep,
    bor_ht,
    e_mode,
    bor_cnt,
    tol_input,
    ra_input,
    material,
    core_dia=0.0
):

    tool_count_bor = 0
    total_time_sec = 0.0
    step_details = []

    tol_band = tol_input * 2

    fine_boring_required = (
        tol_band < 0.2 or
        ra_input <= 1.6
    )

    step_details.append(
        f"Fine Boring Required = {fine_boring_required}"
    )
    if fine_boring_required:
        f_tool_check = get_fine_boring_params(f_dia, material)
        finish_stock = f_tool_check["ap"] if f_tool_check else 0.5
        rough_target_dia = f_dia - finish_stock
    else:
        finish_stock = 0.0
        rough_target_dia = f_dia
    
    step_details.append(
        f"Rough Target Dia = {rough_target_dia}"
    )
    
    # ==========================================
    # 4. OPERATION: DRILLING
    # ==========================================
    if operation == "Drilling":
        st.subheader(f"Drilling Calculator ({machine})")
            
        col1, col2 = st.columns(2)
        with col1:
             dia = st.number_input("Drill Diameter (mm)", value=25.0, step=0.1, key="dr_dia_in")
             dep = st.number_input("Drawing Depth (mm)", value=50.0, step=1.0, key="dr_dep_in")
        with col2:
            hole_type = st.radio("Hole Type", ["Blind Hole", "Through Hole"], horizontal=True, key="dr_ht")
            cnt = st.number_input("Number of Holes", value=1, step=1, key="dr_cnt_in")
        
        # --- QUALITY & TOLERANCE CHECKS ---
        if dia <= 16 and tol_input < 0.1:
            st.warning(f"⚠️ Tolerance ±{tol_input} is too tight for Ø{dia} drilling. Use Finish Boring Bar.")
        elif dia > 16 and tol_input < 0.2:
            st.warning(f"⚠️ Tolerance ±{tol_input} is tight for Ø{dia} drilling. Consider Finish Boring.")
            
        if ra_input < 3.2:
            st.info("💡 Ra < 3.2 requested: Drilling is a roughing operation. Finish Boring pass required.")
        
        # --- L/D & PARAMETER LOOKUP ---
        rpm_val, f_min_val, max_d_val = get_parameters(dia, material)
            
        if max_d_val and dep > max_d_val:
            st.error(f"❗ Depth {dep}mm exceeds Max Table Depth ({max_d_val}mm) for Ø{dia}.")
            u_vc = st.number_input("Enter Manual Vc (m/min)", value=80.0)
            u_fr = st.number_input("Enter Manual Feed/Rev (mm/rev)", value=0.1)
            rpm = (u_vc * 1000) / (math.pi * dia)
            f_min = rpm * u_fr
        else:
            rpm, f_min = rpm_val, f_min_val
        
        if rpm:
            point_len = (0.18 * dia) if dia <= 20 else 0
            actual_travel = (dep + 3 + point_len) if hole_type == "Blind Hole" else (dep + 6 + point_len)
                
            v_c = (math.pi * dia * rpm) / 1000
            p_req = ((f_min / rpm) * v_c * dia * kc) / (240000 * 0.8)
            torque_req = (p_req * 9550) / rpm
                
        
            power_load = (p_req / usable_power) * 100
            torque_load = (torque_req / usable_torque) * 100
                
            st.write(f"**Travel:** {round(actual_travel, 2)} mm | **RPM:** {int(rpm)} | **Feed:** {f_min} mm/min")
            st.write(f"**Power Required:** {round(p_req, 2)} kW")
            st.write(f"**Torque Required:** {round(torque_req, 2)} Nm")
            st.write(
                f"**Machine Load:** Power {power_load:.0f}% | Torque {torque_load:.0f}%"
            )
                
            if p_req > usable_power or torque_req > usable_torque:
                if p_req > usable_power:
                    st.error(
                        f"🚨 Power Alert: {p_req:.2f} kW exceeds usable machine limit ({usable_power:.2f} kW)"
                    )
        
                if torque_req > usable_torque:
                    st.error(
                        f"🚨 Torque Alert: {torque_req:.1f} Nm exceeds usable machine limit ({usable_torque:.1f} Nm)"
                    )
                
            if st.button("Calculate Drilling Total"):
                cut_time = (actual_travel / f_min) * 60 * cnt
                total_op_time = tool_change_time + cut_time + (cnt - 1) * position_time
        
                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("Cut Time", f"{round(cut_time, 2)} sec")
                col2.metric("Tool Change", f"{round(tool_change_time, 2)} sec")
                col3.metric("Total Cycle Time", f"{round(total_op_time, 2)} sec")
        
    elif operation == "Boring / Hole Milling":
        
        st.subheader(f"Boring Planner ({machine})")
        
        # ==========================================
        # FINE BORING MATERIAL VALIDATION
        # ==========================================
        
        if (
            "fine_boring" not in material_tables[material]
            or len(material_tables[material]["fine_boring"]) == 0
            ):
            st.warning(
                f"Fine boring parameters currently not defined for {material}."
             )
        
        col1, col2 = st.columns(2)
    
        with col1:
    
            f_dia = float(
                 st.number_input(
                    "Finish Bore Diameter (mm)",
                     value=48.0,
                    step=0.1,
                     key="bor_f_dia"
                )
            )
    
            b_dep = float(
                st.number_input(
                    "Drawing Depth (mm)",
                    value=50.0,
                    step=1.0,
                    key="bor_depth"
                )
            )
    
        with col2:
    
            bor_ht = st.radio(
                "Hole Type",
                ["Blind Hole", "Through Hole"],
                horizontal=True,
                key="bor_ht"
             )
    
            e_mode = st.radio(
                "Starting Condition",
                ["Solid", "Core Hole"],
                horizontal=True,
                key="bor_mode"
            )
    
            bor_cnt = st.number_input(
                "Number of Positions",
                value=1,
                step=1,
                key="bor_cnt"
            )
        
        # ==========================================
        # DEPTH VALIDATION
        # ==========================================
        
        if b_dep > 150:
        
            st.error(
                f"Depth {b_dep}mm exceeds validated boring limit of 150mm."
            )
        
            st.warning(
                "Check tool weight, machine spindle capability, "
                "fixture rigidity and process feasibility manually."
            )
        
            st.stop()
        
        # ==========================================
        # L/D VALIDATION
        # ==========================================
        
        ld_ratio = b_dep / f_dia
        
        if ld_ratio > 3:
        
            st.error(
                f"L/D Ratio = {round(ld_ratio,1)} exceeds recommended limit of 3."
            )
        
            st.warning(
                "Check boring bar rigidity, machine capability "
                 "and fixture stability."
             )
        
            st.stop()
        # ==========================================
        # FINAL PASS STRATEGY
        # ==========================================
        
        # Convert ± tolerance into total tolerance band
        tol_band = tol_input * 2
        
        # ==========================================
        # FINE BORING TRIGGER
        # ==========================================
        
        # Fine boring required for:
        # 1. Tolerance tighter than ±0.1
        # 2. Surface finish Ra 1.6 or better
        
        fine_boring_required = (
            tol_band < 0.2 or
               ra_input <= 1.6
        )
    
        tool_count_bor = 0
        # ==========================================
        # STOCK STRATEGY
        # ==========================================
        
        if fine_boring_required:
            f_tool_check = get_fine_boring_params(f_dia, material)
            finish_stock = f_tool_check["ap"] if f_tool_check else 0.5  # fallback 0.5
            rough_target_dia = f_dia - finish_stock
        else:
            finish_stock = 0.0
            rough_target_dia = f_dia
    
        step_details.append(
            f"Fine Boring Required = {fine_boring_required}"
        )
        step_details.append(
            f"Rough Target Dia = {rough_target_dia}"
        )
        
        if f_dia <= 5:
            drill_stock = 0.5
        elif f_dia <= 10:
            drill_stock = 0.7
        else:
            drill_stock = 1.0
        
        # ==========================================
        # SPECIAL PROCESS VALIDATION
        # ==========================================
        
        if ra_input < 0.8:
    
            st.warning(
                "Required surface finish is beyond standard fine boring capability. "
                "Consider burnishing, honing or special finishing process."
            )
    
        if tol_band < 0.015:
    
            st.warning(
                "Required tolerance is beyond standard fine boring capability. "
                "Consider honing, reaming or special precision process."
            )
    
        # ==========================================
        # STRATEGY DISPLAY
        # ==========================================
    
        if fine_boring_required:
     
            st.warning(
                "Fine boring activated due to tolerance/surface finish requirement."
            )
    
        else:
    
            st.info(
                "Standard rough boring will finish directly to final size."
            )
        # ==========================================
        # INITIALIZE VARIABLES
        # ==========================================
        current_dia = 0.0
        
        
        # --- 3. STEP 1: DRILLING (Only if Solid) ---
    
        if e_mode == "Solid":
    
            drill_data = material_tables[material]["drill"]
    
            sorted_drills = sorted(
                drill_data,
                key=lambda x: x['max_d'],
                reverse=True
            )
    
            safe_drill_dia = 0.0
    
            for drill in sorted_drills:
                    actual_dia = min(drill['max_d'] - 0.01, rough_target_dia - drill_stock)
                    actual_dia = round(actual_dia, 2)
    
                    # actual_dia must fall within this row's own range
                    if actual_dia < drill['min_d'] or actual_dia >= drill['max_d']:
                        continue
    
                    # Safety check — drill must always be smaller than bore target
                    if actual_dia >= rough_target_dia:
                        continue
                    d_params = get_parameters(actual_dia, material)
                    if d_params[0] is not None and d_params[1] is not None:
                        d_rpm, d_fmin = d_params[0], d_params[1]
                        p_check = (
                            (
                                (d_fmin / d_rpm)
                                * (math.pi * actual_dia  * d_rpm / 1000)
                                * actual_dia
                                * kc
                            ) / 192000
                        )
        
                        torque_req = (p_check * 9550) / d_rpm
                        
                        if (
                            p_check <= usable_power
                            and torque_req <= usable_torque
                        ):
    
                            safe_drill_dia = actual_dia
                            tool_count_bor += 1
                            break
    
            if safe_drill_dia > 0:
    
                d_travel = (
                    b_dep
                    + (6 if bor_ht == "Through Hole" else 3)
                    + ((0.18 * safe_drill_dia) if safe_drill_dia <= 20 else 0)
                )
    
                d_time = (d_travel / d_fmin) * 60
    
                total_time_sec += d_time
                step_details.append(
                    f"Drill Ø{safe_drill_dia}"
                )
                st.success(
                    f"Step 1: Drilling Ø{safe_drill_dia} | "
                    f"Power: {round(p_check,2)}kW | "
                    f"Time: {round(d_time, 2)}s"
                )
        
                current_dia = safe_drill_dia
    
            else:
    
                st.error(   
                    f"❌ No suitable drill found for Ø{rough_target_dia:.1f} based on available machine capacity."
                )
                st.stop()
    
        else:
    
            current_dia = float(
                st.number_input(
                    "Core Dia",
                    value=30.0,
                    key="bor_core_in"
                )
            )
        
        # --- 4. STEP 2: ROUGH BORING (Stock-Aware Multi-Pass) ---
    
        st.info(f"Step 2: Boring Sequence to Ø{rough_target_dia}")
    
        bor_travel = b_dep + (3 if bor_ht == "Blind Hole" else 6)
    
        while current_dia < rough_target_dia:
    
            tool = get_boring_params(current_dia, material)
            tool_count_bor += 1
    
            if not tool:
    
                st.warning(f"No boring data found for Ø{current_dia}.")
                break
    
            # Max stock increment from table
            max_dia_increment = tool['ap']
    
            d2 = round(min(
                rough_target_dia,
                current_dia + max_dia_increment
            ),3)
    
            # Feed per revolution
            f_rev_b = tool['feed_min'] / tool['rpm']
            # Boring Power Formula
            # --- MATERIAL REMOVAL RATE (cm3/min) ---
            mrr_bor = (
                ((math.pi * ((d2**2) - (current_dia**2))) / 4)
                * (tool['feed_min'] / 1000)
            )
    
            # --- POWER CALCULATION (kW) ---
            efficiency = 0.85
        
            p_bor = ((mrr_bor * kc) / (60000)) / efficiency
    
            # --- TORQUE (Nm) ---
            torque_bor = (p_bor * 9550) / tool['rpm']
    
            # --- MACHINE LOAD (%) ---
            machine_load = (p_bor / m_power) * 100
    
            # --- TIME ---
            p_time = (bor_travel / tool['feed_min']) * 60
    
            total_time_sec += p_time
            step_details.append(
                f"Bore Ø{current_dia} ➔ Ø{d2}"
            )
    
            st.write(
                f"🔹 Boring Ø{current_dia} ➔ Ø{d2} | "
                f"Stock: {round(d2-current_dia, 2)}mm | "
                f"Power: {round(p_bor, 2)}kW | "
                f"Time: {round(p_time, 1)}s"
            )
    
            current_dia = round(d2, 3)
    
        # ==========================================
        # STEP 3 : FINAL BORING PASS
        # ==========================================
    
        if fine_boring_required:
    
            f_tool = get_fine_boring_params(f_dia, material)
    
            if f_tool:
                tool_count_bor += 1
                finish_feed_rev = f_tool["feed_rev"]
        
                finish_rpm = f_tool["rpm"]
                    
                finish_feed = (
                    finish_feed_rev
                    * finish_rpm
                )
    
                finish_time = (
                    (bor_travel / finish_feed)
                    * 60
                )
    
                total_time_sec += finish_time
                step_details.append(
                    f"Fine Bore Ø{current_dia} ➔ Ø{f_dia}"
                )
                st.success(
                    f"Step 3: Fine Boring Ø{current_dia} ➔ Ø{f_dia} | "
                    f"RPM: {round(finish_rpm)} | "
                    f"Feed: {round(finish_feed,1)} mm/min | "
                    f"Time: {round(finish_time,1)}s"
                )
    
            else:
        
                st.error(
                    "Fine boring data not available for this diameter/material."
                )
    return {
        "time": total_time_sec,
        "tools": tool_count_bor,
        "steps": step_details
    }
# ==========================================
# STEP 4 : Tapping operation
# ==========================================    
elif operation == "Tapping":
    st.title("Tapping Calculator")

    # 1. Material Guardrail

    if (
        "tap" not in material_tables[material]
        or len(material_tables[material]["tap"]) == 0
    ):
        st.error(
            f"⚠️ Tap data not available for {material}."
        )
        st.stop()

    # 2. Tap Data Selection
    if material in material_tables:
        tap_table = material_tables[material]["tap"]
    else:
        st.error(f"Cutting parameters for {material} are not yet defined.")
        st.stop() 

    pitch_list = sorted(list(set(row["pitch"] for row in tap_table)))
    selected_pitch = st.selectbox("Select Pitch", pitch_list, key="tap_pitch_sel")

    filtered = [row for row in tap_table if row["pitch"] == selected_pitch]
    tap_options = list(set(row["tap"] for row in filtered))

    selected_tap = st.selectbox("Select Tap Size", tap_options, key="tap_size_sel")
    selected_row = next(row for row in filtered if row["tap"] == selected_tap)

    # Tool Parameters
    diameter = get_diameter(selected_tap)
    pitch = selected_row["pitch"]
    vc = selected_row["vc"]
    
    if material == "Steel_Hardness_30_to_40_HRC":
        vc *= 0.90

    elif material == "Stainless_Steel":
        vc *= 0.80

    max_depth = selected_row["max_depth"]

    # 3. Input Parameters
    tap_type = st.selectbox("Tap Type", ["Through", "Blind"], key="tap_type_sel")
    tap_depth = st.number_input("Tap Depth (mm)", value=8.0, key="tap_depth_input")
    count = st.number_input("Number of Holes", value=1, key="tap_count_input")

    if tap_type == "Blind":
        drill_depth = st.number_input("Drill Depth (mm)", value=10.0, key="drill_depth_input")
    else:
        drill_depth = None
    
    # Display Tool Data
    st.write(f"**Tap Diameter:** {diameter} mm | **Pitch:** {pitch} mm")
    st.write(f"**Recommended Vc:** {vc} m/min | **Max Tool Depth:** {max_depth} mm")

    # 4. Mechanical Validation & Clearance
    valid_tap = True
    use_threadmill = False
    manual_mode = False
    stop_all = False

    if tap_type == "Blind":
        clearance = drill_depth - tap_depth
        st.write(f"**Clearance:** {round(clearance, 2)} mm")
    
        if drill_depth <= tap_depth:
            st.error("Error: Drill depth must be greater than tap depth.")
            valid_tap = False
            stop_all = True
        elif clearance < (1 * pitch):
            st.error("Insufficient clearance. Not safe for tapping.")
            valid_tap = False
            use_threadmill = True
        elif clearance <= (2 * pitch):
            st.warning("Low clearance. Thread milling recommended.")
            valid_tap = False
            use_threadmill = True
        else:
            st.success("Clearance is safe for tapping.")

    # 5. Depth Check
    if valid_tap and not stop_all:
        if tap_depth > max_depth:
            st.warning("Depth exceeds tool limit. Adjust Vc manually.")
            manual_mode = True

    if manual_mode and valid_tap:
        vc = st.number_input("Enter Vc manually", value=vc, key="tap_vc_manual")

    # 6. Tapping Calculation
    if valid_tap:
        rpm = (1000 * vc) / (math.pi * diameter)
        feed_min = pitch * rpm
        # Cut length calculation: (Depth + 3 pitches for entry/exit) * 2 for in/out + safety
        cut_length = (tap_depth + (pitch * 3)) * 2 + 4
    
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("RPM", f"{round(rpm, 0)}")
        col2.metric("Feed", f"{round(feed_min, 0)} mm/min")
        col3.metric("Travel", f"{round(cut_length, 1)} mm")

        if st.button("Calculate Tapping Time", key="tap_calc_btn"):
            time_per_hole = cut_length / feed_min
            cut_time = time_per_hole * count * 60

            total_op_time = tool_change_time + cut_time + (count - 1) * position_time

            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Cut Time", f"{round(cut_time, 2)} sec")
            col2.metric("Tool Change", f"{round(tool_change_time, 2)} sec")
            col3.metric("Total Cycle Time", f"{round(total_op_time, 2)} sec")
                
    
    # 7. Thread Milling Logic
    if use_threadmill and not stop_all:
        st.divider()
        st.subheader("Thread Milling Calculation")
        
        threadmill_table = material_tables[material]["threadmill"]
        # Requested thread size
        requested_dia = get_diameter(selected_tap)

        # Approximate thread minor diameter
        minor_dia = requested_dia - (1.0825 * pitch)
        
        # Step 1: Pitch match
        pitch_matches = [
            row for row in threadmill_table
            if row["pitch"] == pitch
        ]
            
        # Step 2: Depth capable
        depth_matches = [
            row for row in pitch_matches
            if row["max_depth"] >= tap_depth
        ]
        
        # Step 3: Tool must fit inside thread minor diameter
        size_matches = [
            row for row in depth_matches
            if row["tool_dia"] < minor_dia
        ]
        
        # Step 4: Select largest available tool diameter
        if size_matches:
            tm_row = max(size_matches, key=lambda x: x["tool_dia"])
        else:
            tm_row = None
    
        if tm_row is None:
            st.error("No thread mill data available for this specific size.")
        else:
            vc_tm = tm_row["vc"]
            feed_rev = tm_row["feed_rev"]

            if material == "Steel_Hardness_30_to_40_HRC":
                vc_tm *= 0.90
                feed_rev *= 0.95

            elif material == "Stainless_Steel":
                 vc_tm *= 0.80
                 feed_rev *= 0.90
            tool_dia = tm_row["tool_dia"]
            max_depth_tm = tm_row["max_depth"]

            if tap_depth > max_depth_tm:
                st.warning("Special long-series thread mill may be required.")

            rpm_tm = (1000 * vc_tm) / (math.pi * tool_dia)
            feed_tm = feed_rev * rpm_tm
            # Helix path travel distance
            tm_cut_length = ((diameter - tool_dia) * math.pi * 3) + tap_depth + 4

            st.write(f"**TM RPM:** {round(rpm_tm, 0)} | **TM Feed:** {round(feed_tm, 0)} mm/min")

            if st.button("Calculate Thread Mill Time", key="tm_calc_btn"):
                cut_time = (tm_cut_length / feed_tm) * count * 60

                total_op_time = tool_change_time + cut_time + (count - 1) * position_time
            
                st.divider()
                col1, col2, col3 = st.columns(3)
                col1.metric("Cut Time", f"{round(cut_time, 2)} sec")
                col2.metric("Tool Change", f"{round(tool_change_time, 2)} sec")
                col3.metric("Total Cycle Time", f"{round(total_op_time, 2)} sec")
    
elif operation == "Face Milling":
    st.title("Face Milling Calculator")

    st.info(
     f"Machine: {machine} | Spindle: {m_taper} | Material: {material}"
     )

    # 2. Surface Finish & PCD Warning
    if material == "Aluminium":
        if ra_input < 0.8:
            is_pcd_required = False
            st.warning(
                "⚠️ Ra < 0.8 is beyond standard milling capability for Aluminium. "
                "Special process required — calculate separately."
            )
        elif ra_input < 2.0:
            is_pcd_required = True
            st.warning(
                "⚠️ PCD Tooling Required: 0.5mm stock left for PCD finish pass. "
                "Finish pass: RPM +10%, Feed -10%."
            )
        else:
            is_pcd_required = False
    else:
        is_pcd_required = False
        if ra_input < 0.8:
            st.warning(
                "⚠️ Ra < 0.8 requires Grinding or special process for Steel. "
                "Calculate separately."
            )
        elif ra_input < 2.0:
            st.info(
                "💡 Wiper geometry insert recommended for Steel finish pass. "
                "Feed will be reduced by 20%."
            )
       
    # 3. Filtering Logic
    face_table = material_tables[material]["face_mill"]

    suitable_tools = [
        tool for tool in face_table
        if m_taper in tool["spindles"]
    ]

    if not suitable_tools:
        st.error(f"No suitable Face Mills found for {m_taper} spindle.")
        st.stop()

    # 4. Shape & Selection Mode
    shape = st.selectbox("Component Shape", ["Rectangular", "Circular"], key="fm_shape_sel")

    tool_mode = st.selectbox("Tool Selection Mode", ["Auto", "Manual"], key="fm_mode_sel")

    # COMPONENT INPUTS
    if shape == "Rectangular":
        raw_L = st.number_input("Length (mm)", value=100.0, key="fm_L")
        raw_W = st.number_input("Width (mm)", value=40.0, key="fm_W")
        L = max(raw_L, raw_W)
        W = min(raw_L, raw_W)
    else:
        comp_dia = st.number_input("Component Diameter (mm)", value=100.0, key="fm_circ_dia")
        L = comp_dia
        W = comp_dia

    # TARGET DIA
    if shape == "Rectangular":
        target_dia = W / 0.7
    else:
        target_dia = (comp_dia / 2) / 0.7

    # TOOL SELECTION
    selected_tool = None

    if tool_mode == "Auto":

        possible_tools = sorted(suitable_tools, key=lambda x: x['dia'])

        for t in possible_tools:

            if t['dia'] >= target_dia:

                ae_check = t['max_width']
                ap_check = t['stock']
                vf_check = t['feed']

                efficiency = 0.8

                req_power = (ae_check * ap_check * vf_check * kc) / (60e6 * efficiency)

                if req_power <= m_power:
                    selected_tool = t
                    break

        if not selected_tool:
            selected_tool = max(possible_tools, key=lambda x: x['dia'])

        st.success(f"Auto Selected Cutter Ø{selected_tool['dia']} mm")

    else:
    
        tool_names = [f"Dia {t['dia']}mm" for t in suitable_tools]

        selected_tool_name = st.selectbox("Select Tool", tool_names, key="fm_tool_manual")

        selected_tool = next(
            t for t in suitable_tools
            if f"Dia {t['dia']}mm" == selected_tool_name
        )

    # TOOL PARAMETERS
    tool_dia = selected_tool["dia"]
    ae = selected_tool["max_width"]

    rpm = selected_tool["rpm"]
    vf = selected_tool["feed"]

    if material == "Steel_Hardness_30_to_40_HRC":
        rpm *= 0.90
        vf *= 0.95

    elif material == "Stainless_Steel":
        rpm *= 0.80
        vf *= 0.90
    
    ap_limit = selected_tool["stock"]

    # FINISH PASS PARAMETERS
    if is_pcd_required:
        finish_rpm = rpm * 1.10
        finish_vf = vf * 0.90
    elif material != "Aluminium" and ra_input < 2.0 and ra_input >= 0.8:
        finish_rpm = rpm
        finish_vf = vf * 0.80
    else:
        finish_rpm = rpm
        finish_vf = vf

    # --- POWER VALIDATION ---
    efficiency = 0.8
    req_power = (ae * ap_limit * vf * kc) / (60e6 * efficiency)

    st.metric(
        "Required Power",
        f"{req_power:.2f} kW",
        delta=f"Usable Limit: {usable_power:.2f} kW",
        delta_color="inverse"
    )
    # --- TORQUE CALCULATION ---
    torque_req = (req_power * 9550) / rpm

    power_load = (req_power / usable_power) * 100
    torque_load = (torque_req / usable_torque) * 100

    st.write(
        f"**Torque Required:** {torque_req:.1f} Nm"
    )

    st.write(
        f"**Machine Load:** Power {power_load:.0f}% | "
        f"Torque {torque_load:.0f}%"
    )

    if req_power > usable_power:
        st.error(
            f"🚨 Power Alert: {req_power:.2f} kW exceeds "
            f"usable limit ({usable_power:.2f} kW)"
        )

    if torque_req > usable_torque:
        st.error(
            f"🚨 Torque Alert: {torque_req:.1f} Nm exceeds "
            f"usable limit ({usable_torque:.1f} Nm)"
        )

    if (
        req_power <= usable_power
        and torque_req <= usable_torque
    ):
        st.success(
            f"✅ Tool: Ø{tool_dia}mm | RPM: {rpm:.0f} | Feed: {vf:.0f} mm/min"
        )
    
    # PROCESS PARAMETERS
    total_stock = st.number_input(
        "Total Stock to Remove (mm)", 
        value=5.5, 
        key="fm_total_stock"
    )

    fm_cnt = st.number_input(    # ← ADD THIS
        "Number of Positions",
        value=1,
        step=1,
        key="fm_cnt"
    )

    if ra_input < 0.8:
        rough_stock = max(0.0, total_stock - 0.5)
        rough_passes = math.ceil(rough_stock / ap_limit) if rough_stock > 0 else 0
        st.info(f"SPECIAL PROCESS STRATEGY: {rough_passes} Roughing passes. 0.5mm left for special finishing.")

    elif is_pcd_required:
        rough_stock = max(0.0, total_stock - 0.5)
        rough_passes = math.ceil(rough_stock / ap_limit) if rough_stock > 0 else 0
        st.info(f"PCD STRATEGY: {rough_passes} Roughing passes. 0.5mm left for PCD.")

    else:
        finish_required = ra_input < 2.0
        if finish_required and total_stock > 0.5:
            rough_stock = total_stock - 0.5
            rough_passes = math.ceil(rough_stock / ap_limit)
        else:
            rough_stock = total_stock
            rough_passes = math.ceil(rough_stock / ap_limit) if ap_limit > 0 else 1
    
    # CUT LENGTH
    if shape == "Rectangular":
        width_passes = math.ceil(W / ae)
        cut_length = (L + tool_dia + 4) * width_passes

    else:
        if comp_dia <= ae:
            cut_length = comp_dia + tool_dia + 10
        else:
            overhang = tool_dia - ae
            first_path_dia = (comp_dia - tool_dia) + (2 * overhang)

            current_path_dia = max(first_path_dia, 0)
            total_circ_dist = 0
            pass_count = 0

            while True:
                total_circ_dist += math.pi * current_path_dia
                pass_count += 1

                inner_edge_pos = (current_path_dia / 2) - (tool_dia / 2)

                if inner_edge_pos <= -2:
                    break

                current_path_dia -= (ae * 2)

                if current_path_dia < 0:
                    current_path_dia = 0
    
                if pass_count > 15:
                    break

            cut_length = total_circ_dist + tool_dia

    # FINAL CALCULATION
    if st.button("Calculate Milling Time", key="fm_calc_btn"):

        time_rough = (cut_length * rough_passes) / vf

        time_finish = 0
        if total_stock > 0.5:
            if ra_input < 0.8:
                # Special process — calculate finish pass at reduced feed
                time_finish = cut_length / finish_vf
            elif ra_input < 2.0:
                # PCD (aluminium) or Wiper (steel)
                time_finish = cut_length / finish_vf

        total_time_min = time_rough + time_finish
        cut_time = total_time_min * 60 * fm_cnt

        total_op_time = tool_change_time + cut_time + (fm_cnt - 1) * position_time

        st.subheader("Milling Estimates")
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Roughing Passes", f"{rough_passes}")
        col_b.metric("Rough Time", f"{time_rough * 60:.1f} sec")
        col_c.metric("Cut Time", f"{round(cut_time, 2)} sec")
        col_d.metric("Total Cycle Time", f"{round(total_op_time, 2)} sec")

        if ra_input < 0.8:
            if material == "Aluminium":
                st.warning(
                    "☝️ Roughing and finish milling time included. "
                    "Additional special finishing process required to achieve final Ra."
                )
            else:
                st.warning(
                    "☝️ Roughing and finish milling time included. "
                    "Grinding or special finishing process required to achieve final Ra."
                )
        elif ra_input < 2.0:
            if material == "Aluminium":
                st.info("☝️ PCD finish pass time included in total.")
            else:
                st.info("☝️ Wiper geometry finish pass time included in total.")


st.info("Combined Operations Planner")
    
# ==========================================
# INITIALIZE SESSION STATE
# ==========================================
if "operations" not in st.session_state:
    st.session_state.operations = []

if "combined_results" not in st.session_state:
    st.session_state.combined_results = []
    
# ==========================================
# ADD / CLEAR OPERATIONS BUTTONS
# ==========================================
st.subheader("Combined Operations Planner")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("➕ Add Operation", key="add_op"):
        st.session_state.operations.append({
            "type": "Hole",
            "id": len(st.session_state.operations) + 1
        })
with col2:
    if st.button("🗑️ Clear All", key="clear_ops"):
        st.session_state.operations = []
        st.session_state.combined_results = []
    
st.divider()
# ==========================================
# OPERATION INPUT ROWS
# ==========================================
for i, op in enumerate(st.session_state.operations):

    st.markdown(f"### Operation {i + 1}")

    op_type = st.selectbox(
        "Operation Type",
        ["Face Mill", "Hole", "Tap"],
        key=f"op_type_{i}"
    )
    current_type = st.session_state.operations[i].get("type")

    if current_type != op_type:
        st.session_state.operations[i] = {
            "id": st.session_state.operations[i]["id"],
            "type": op_type
        }
    st.session_state.operations[i]["type"] = op_type

    # ---- FACE MILL INPUTS ----
    if op_type == "Face Mill":
        col1, col2 = st.columns(2)
        with col1:
            shape = st.selectbox("Component Shape", ["Rectangular", "Circular"], key=f"fm_shape_{i}")
            if shape == "Rectangular":
                fm_L = st.number_input("Length (mm)", value=100.0, key=f"fm_L_{i}")
                fm_W = st.number_input("Width (mm)", value=40.0, key=f"fm_W_{i}")
            else:
                fm_dia = st.number_input("Component Diameter (mm)", value=100.0, key=f"fm_dia_{i}")
        with col2:
            fm_ra = st.number_input("Surface Finish Ra (μm)", value=3.2, step=0.1, key=f"fm_ra_{i}")
            fm_stock = st.number_input("Stock to Remove (mm)", value=1.0, step=0.1, key=f"fm_stock_{i}")
            fm_pos = st.number_input("Number of Positions", value=1, step=1, key=f"fm_pos_{i}")

        # 👇 ADD THIS BLOCK TO SAVE EVERYTHING TO YOUR DYNAMIC LIST
        face_mill_data = {
            "type": "Face Mill",
            "shape": shape,
            "ra": fm_ra,
            "stock": fm_stock,
            "fm_pos": fm_pos
        }
        
        # Save dimensions conditionally so you don't save empty/wrong variables
        if shape == "Rectangular":
            face_mill_data["length"] = fm_L
            face_mill_data["width"] = fm_W
        else:
            face_mill_data["dia"] = fm_dia

        # Push everything into the session state list slot
        st.session_state.operations[i].update(face_mill_data)
        st.session_state.operations[i]["tool_count"] = 1

    # ---- HOLE INPUTS ----
    elif op_type == "Hole":
        col1, col2 = st.columns(2)
        with col1:
            h_dia = st.number_input("Finish Diameter (mm)", value=25.0, step=0.1, key=f"h_dia_{i}")
            h_dep = st.number_input("Depth (mm)", value=30.0, step=1.0, key=f"h_dep_{i}")
            h_cnt = st.number_input("Number of Positions", value=1, step=1, key=f"h_cnt_{i}")
        with col2:
            h_tol = st.number_input("Tolerance (±)", value=0.1, format="%.3f", key=f"h_tol_{i}")
            h_ra = st.number_input("Surface Finish Ra (μm)", value=3.2, step=0.1, key=f"h_ra_{i}")
            h_ht = st.radio("Hole Type", ["Blind Hole", "Through Hole"], horizontal=True, key=f"h_ht_{i}")
            h_mode = st.radio(
                "Starting Condition",
                ["Solid", "Core Hole"],
                horizontal=True,
                key=f"h_mode_{i}"
            )
        if h_mode == "Core Hole":

            core_dia = st.number_input(
                "Core Hole Diameter (mm)",
                value=max(5.0, h_dia - 3),
                step=0.1,
                key=f"core_dia_{i}"
            )

            st.session_state.operations[i]["core_dia"] = core_dia

        st.session_state.operations[i].update({
            "type": "Hole",
            "dia": h_dia,
            "depth": h_dep,
            "tol": h_tol,
            "ra": h_ra,
            "hole_type": h_ht,
            "start_mode": h_mode,
            "count": h_cnt
        })
        st.session_state.operations[i]["tool_count"] = 0

    # ---- TAP INPUTS ----
    elif op_type == "Tap":
        col1, col2 = st.columns(2)
        with col1:
            t_size = st.text_input("Tap Size (e.g. M10)", value="M10", key=f"t_size_{i}")
            t_pitch = st.number_input("Pitch (mm)", value=1.5, step=0.25, key=f"t_pitch_{i}")
            t_cnt = st.number_input("Number of Positions", value=1, step=1, key=f"t_cnt_{i}")
        with col2:
            t_ddep = st.number_input("Drill Depth (mm)", value=30.0, step=1.0, key=f"t_ddep_{i}")
            t_tdep = st.number_input("Tap Depth (mm)", value=25.0, step=1.0, key=f"t_tdep_{i}")
            t_ht = st.radio("Hole Type", ["Blind Hole", "Through Hole"], horizontal=True, key=f"t_ht_{i}")

        # 👇 ADD THIS CRITICAL LINE TO SAVE THE DATA
        st.session_state.operations[i].update({
            "type": "Tap",
            "t_size": t_size,
            "t_pitch": t_pitch,
            "t_cnt": t_cnt,
            "t_ddep": t_ddep,
            "t_tdep": t_tdep,
            "t_ht": t_ht
        })
        st.session_state.operations[i]["tool_count"] = 1

    
st.divider()
st.write(st.session_state.operations)
if st.button("🚀 Calculate Combined Cycle Time"):   
    # 1. Clear previous results to prevent stacking duplicates
    st.session_state.combined_results = []
    
    # Check if there are actually operations added
    if not st.session_state.operations:
        st.warning("⚠️ Please add at least one operation first.")
    else:
        # 2. Loop through every stored operation and pass data to your functions
        for i, op in enumerate(st.session_state.operations):
           
            op_time = 0.0
            op_positions = 0.0
            op_tools = 0
            details = ""

            # ---- HOLE LOGIC PROCESSING ----
            if op["type"] == "Hole":
                # Extract variables stored in your dictionary
                d = op["dia"]
                depth = op["depth"]
                ra = op["ra"]
                count = op["count"]
                mode = op["start_mode"]
                st.write("DEBUG HOLE OP:", op)

                result = calculate_boring_operation(
                    f_dia=d,
                    b_dep=depth,
                    bor_ht=op["hole_type"],
                    e_mode=mode,
                    bor_cnt=count,
                    tol_input=op["tol"],
                    ra_input=ra,
                    material=material,
                    core_dia=op.get("core_dia", 0.0)
                )
                st.write("DEBUG RESULT:", result)
                op_time = result["time"] * count
                tool_count_bor = result["tools"]
                
                details = " | ".join(result["steps"])
                
                op["tool_count"] = tool_count_bor
                
                   
                    
            # ---- FACE MILL LOGIC PROCESSING ----
            elif op["type"] == "Face Mill":
                # Call your existing face mill calculations
                # op_time = calculate_facemill_time(op) * op["fm_pos"]
                details = f"Face Milling Ra {op['ra']}μm"

            # ---- TAP LOGIC PROCESSING ----
            elif op["type"] == "Tap":
                # Call your existing tapping calculations
                # op_time = calculate_tapping_time(op) * op["t_cnt"]
                details = f"Tapping {op['t_size']}"

            # 3. Append calculated data to your combined results list
            
            st.session_state.combined_results.append({
                "op_num": i + 1,
                "type": op["type"],
                "details": details,
                "cycle_time": op_time
            })

        # ==========================================
        # DISPLAY RESULTS TABLE AND TOTAL TIME
        # ==========================================
        st.subheader("📊 Combined Cycle Time Report")
        
        # Calculate grand total
        total_cut_time = sum(item["cycle_time"] for item in st.session_state.combined_results)
        
        # Display as a neat summary table
        import pandas as pd
        report_df = pd.DataFrame(st.session_state.combined_results)
        report_df.columns = ["Op #", "Operation Type", "Details", "Cycle Time (sec)"]
        st.table(report_df)
        
        # Grand Total Message
        st.success(f"🏅 Total Combined Cycle Time = {total_cut_time:.2f} sec")
