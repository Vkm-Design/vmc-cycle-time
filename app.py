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
            {"min_d": 0.5, "max_d": 0.99, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
            {"min_d": 1, "max_d": 2.99, "rpm": 6500, "feed_min": 100, "max_depth": 5},

            {"min_d": 3, "max_d": 4.99, "vc": 50, "feed_min": 450, "max_depth": 20},
            {"min_d": 5, "max_d": 7.99, "vc": 80, "feed_min": 550, "max_depth": 30},
            {"min_d": 8, "max_d": 9.99, "vc": 100, "feed_min": 480, "max_depth": 40},
            {"min_d": 10, "max_d": 14.99, "vc": 120, "feed_min": 550, "max_depth": 50},

            {"min_d": 15, "max_d": 15.99, "rpm": 2464, "feed_min": 444, "max_depth": 48},
            {"min_d": 16, "max_d": 16.99, "rpm": 2508, "feed_min": 451, "max_depth": 51},
            {"min_d": 17, "max_d": 17.99, "rpm": 2364, "feed_min": 426, "max_depth": 54},
            {"min_d": 18, "max_d": 18.99, "rpm": 2409, "feed_min": 482, "max_depth": 57},
            {"min_d": 19, "max_d": 19.99, "rpm": 2448, "feed_min": 490, "max_depth": 60},

            {"min_d": 20, "max_d": 20.99, "rpm": 2484, "feed_min": 248, "max_depth": 63},
            {"min_d": 21, "max_d": 21.99, "rpm": 2369, "feed_min": 237, "max_depth": 66},
            {"min_d": 22, "max_d": 22.99, "rpm": 2263, "feed_min": 226, "max_depth": 69},
            {"min_d": 23, "max_d": 23.99, "rpm": 2167, "feed_min": 238, "max_depth": 72},

            {"min_d": 24, "max_d": 24.99, "rpm": 2338, "feed_min": 234, "max_depth": 75},
            {"min_d": 25, "max_d": 25.99, "rpm": 2371, "feed_min": 249, "max_depth": 78},
            {"min_d": 26, "max_d": 26.99, "rpm": 2402, "feed_min": 240, "max_depth": 81},
            {"min_d": 27, "max_d": 27.99, "rpm": 2315, "feed_min": 232, "max_depth": 84},
            {"min_d": 28, "max_d": 28.99, "rpm": 2233, "feed_min": 223, "max_depth": 87},
            {"min_d": 29, "max_d": 29.99, "rpm": 2158, "feed_min": 216, "max_depth": 90},
            {"min_d": 30, "max_d": 34.99, "vc": 150, "feed_min": 159, "max_depth": 105},
            {"min_d": 35, "max_d": 44.99, "vc": 170, "feed_min": 155, "max_depth": 125},
            {"min_d": 45, "max_d": 54.99, "vc": 180, "feed_min": 127, "max_depth": 125},
            {"min_d": 55, "max_d": 65, "vc": 180, "feed_min": 115, "max_depth": 150},
]

drill_data_Steel_Hardness_upto_30_HRC = [
            {"min_d": 0.5, "max_d": 0.99, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
            {"min_d": 1, "max_d": 1.99, "rpm": 6365, "feed_min": 95, "max_depth": 5},
            {"min_d": 2, "max_d": 2.99, "rpm": 5570, "feed_min": 167, "max_depth": 10},

            {"min_d": 3, "max_d": 3.99, "vc": 40, "feed_min": 297, "max_depth": 15},
            {"min_d": 4, "max_d": 5.99, "vc": 45, "feed_min": 301, "max_depth": 20},
            {"min_d": 6, "max_d": 7.99, "vc": 50, "feed_min": 301, "max_depth": 30},
            {"min_d": 8, "max_d": 9.99, "vc": 60, "feed_min": 334, "max_depth": 50},
            {"min_d": 10, "max_d": 11.99, "vc": 60, "feed_min": 306, "max_depth": 50},
            {"min_d": 12, "max_d": 13.99, "vc": 60, "feed_min": 255, "max_depth": 60},

            {"min_d": 14, "max_d": 15.99, "rpm": 1478, "feed_min": 259, "max_depth": 70},
            {"min_d": 16, "max_d": 17.99, "rpm": 1293, "feed_min": 233, "max_depth": 80},
            {"min_d": 18, "max_d": 20.99, "rpm": 1238, "feed_min": 248, "max_depth": 90},
            {"min_d": 21, "max_d": 26.99, "rpm": 1364, "feed_min": 205, "max_depth": 105},
            {"min_d": 27, "max_d": 31.99, "rpm": 1061, "feed_min": 127, "max_depth": 135},

            {"min_d": 32, "max_d": 44.99, "vc": 90, "feed_min": 107, "max_depth": 105},
            {"min_d": 45, "max_d": 50.99, "vc": 100, "feed_min": 106, "max_depth": 125},
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
    {"min": 2, "max": 2.99, "rpm": 4244, "feed_min": 127.3, "ap": 0.2},
    {"min": 3, "max": 3.99, "rpm": 3183, "feed_min": 191, "ap": 0.3},
    {"min": 4, "max": 4.99, "rpm": 2864, "feed_min": 171.9, "ap": 0.5},
    {"min": 5, "max": 5.99, "rpm": 2652, "feed_min": 185.7, "ap": 1},
    {"min": 6, "max": 6.99, "rpm": 2273, "feed_min": 204.6, "ap": 1.5},
    {"min": 7, "max": 7.99, "rpm": 2387, "feed_min": 214.8, "ap": 1.5},
    {"min": 8, "max": 8.99, "rpm": 2358, "feed_min": 235.8, "ap": 2},
    {"min": 9, "max": 9.99, "rpm": 1910, "feed_min": 191, "ap": 2},
    {"min": 10, "max": 10.99, "rpm": 1736, "feed_min": 208.3, "ap": 2},
    {"min": 11, "max": 11.99, "rpm": 1591, "feed_min": 191, "ap": 2.5},
    {"min": 12, "max": 12.99, "rpm": 1469, "feed_min": 176.3, "ap": 2.5},
    {"min": 13, "max": 13.99, "rpm": 1364, "feed_min": 204.6, "ap": 2.5},
    {"min": 14, "max": 14.99, "rpm": 1379, "feed_min": 206.9, "ap": 2.5},
    {"min": 15, "max": 15.99, "rpm": 1293, "feed_min": 193.9, "ap": 2.5},
    {"min": 16, "max": 16.99, "rpm": 1217, "feed_min": 182.5, "ap": 3},
    {"min": 17, "max": 17.99, "rpm": 1238, "feed_min": 185.7, "ap": 3},
    {"min": 18, "max": 18.99, "rpm": 1173, "feed_min": 175.9, "ap": 3},
    {"min": 19, "max": 19.99, "rpm": 1432, "feed_min": 214.8, "ap": 3},
    {"min": 20, "max": 24.99, "rpm": 1910, "feed_min": 306, "ap": 3.0},
    {"min": 25, "max": 29.99, "rpm": 1528, "feed_min": 244, "ap": 3.0},
    {"min": 30, "max": 34.99, "rpm": 1485, "feed_min": 297, "ap": 3.0},
    {"min": 35, "max": 39.99, "rpm": 1455, "feed_min": 291, "ap": 4.0},
    {"min": 40, "max": 44.99, "rpm": 1432, "feed_min": 286, "ap": 4.0},
    {"min": 45, "max": 49.99, "rpm": 1132, "feed_min": 249, "ap": 4.0},
    {"min": 50, "max": 54.99, "rpm": 1018, "feed_min": 224, "ap": 5.0},
    {"min": 55, "max": 59.99, "rpm": 810, "feed_min": 178, "ap": 5.0},
    {"min": 60, "max": 64.99, "rpm": 743, "feed_min": 163, "ap": 6.0},
    {"min": 65, "max": 69.99, "rpm": 545, "feed_min": 129.0, "ap": 6.0},
    {"min": 70, "max": 85, "rpm": 500, "feed_min": 100.0, "ap": 6.0},
]

# ================= FINE BORING DATA =================

fine_boring_data_aluminium = [
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
    {"min": 20, "max": 24.99, "vc": 140, "feed_rev": 0.08, "ap": 0.3},
    {"min": 25, "max": 29.99, "vc": 140, "feed_rev": 0.08, "ap": 0.3},
    {"min": 30, "max": 34.99, "vc": 155, "feed_rev": 0.08, "ap": 0.4},
    {"min": 35, "max": 39.99, "vc": 160, "feed_rev": 0.08, "ap": 0.4},
    {"min": 40, "max": 44.99, "vc": 170, "feed_rev": 0.08, "ap": 0.4},
    {"min": 45, "max": 49.99, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 50, "max": 54.99, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 55, "max": 59.99, "vc": 180, "feed_rev": 0.10, "ap": 0.5},
    {"min": 60, "max": 64.99, "vc": 160, "feed_rev": 0.10, "ap": 0.5},
    {"min": 65, "max": 69.99, "vc": 140, "feed_rev": 0.1, "ap": 0.5},
    {"min": 70, "max": 80, "vc": 140, "feed_rev": 0.1, "ap": 0.5},
]

# ==========================================
# 1. MATERIAL MASTER TABLE
# ==========================================
material_tables = {
    "Aluminium": {
        "drill": drill_data_aluminium,
        "boring": boring_data_aluminium,
        "tap": tap_data_aluminium,
        "threadmill": threadmill_data_aluminium,
        "face_mill": face_mill_data_aluminium
    },

    "Steel_Hardness_upto_30_HRC": {
        "drill": drill_data_Steel_Hardness_upto_30_HRC,
        "boring": boring_data_Steel_Hardness_upto_30_HRC,
        "tap": tap_data_Steel_Hardness_upto_30_HRC,
        "threadmill": threadmill_data_Steel_Hardness_upto_30_HRC,
        "face_mill": face_mill_data_Steel_Hardness_upto_30_HRC
    },

    "Steel_Hardness_30_to_40_HRC": {
        "drill": drill_data_Steel_Hardness_upto_30_HRC,
        "boring": boring_data_Steel_Hardness_upto_30_HRC,
        "tap": tap_data_Steel_Hardness_upto_30_HRC,
        "threadmill": threadmill_data_Steel_Hardness_upto_30_HRC,
        "face_mill": face_mill_data_Steel_Hardness_upto_30_HRC
    },

    "Stainless_Steel": {
        "drill": drill_data_Steel_Hardness_upto_30_HRC,
        "boring": boring_data_Steel_Hardness_upto_30_HRC,
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
        if row["min_d"] <= diameter < row["max_d"]:

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
            return row
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
            return row

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

# ==========================================
# ==========================================
# 3. GLOBAL SELECTIONS & APP UI
# ==========================================
st.title("Smart Machining Calculator")

# Define operation first so sidebar can use it for visibility logic
operation = st.selectbox("Select Operation", ["Drilling", "Boring / Hole Milling", "Tapping", "Face Milling"])

st.sidebar.header("Global Settings")

# 1. Material Selection
material = st.sidebar.selectbox("Select Material", list(kc_data.keys()), key="global_mat")
kc = kc_data[material]

# 2. THE ONLY MACHINE PICKER (Syncs with all logic)
machine = st.sidebar.selectbox("Select Machine", list(machine_data.keys()), key="global_mach")

# 3. Assign Machine Specs
m_power = machine_data[machine]["power"]
m_torque = machine_data[machine]["torque"]
m_taper = machine_data[machine].get("taper", "BT40") 

st.sidebar.info(f"Machine Cap: {m_power}kW | {m_torque}Nm | {m_taper}")
st.sidebar.markdown("---")

# 4. QUALITY REQUIREMENTS (For L/D, Ra, and Tolerance logic)
if operation != "Tapping":
    st.sidebar.header("Quality Requirements")
    ra_input = st.sidebar.number_input("Surface Finish (Ra)", value=3.2, step=0.1, key="sidebar_ra")
    
    if operation in ["Drilling", "Boring / Hole Milling"]:
        tol_input = st.sidebar.number_input("Diameter Tolerance (±)", value=0.100, format="%.3f", key="sidebar_tol")
    else:
        tol_input = 0.1
else:
    ra_input, tol_input = 3.2, 0.1
    
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
        
        st.write(f"**Travel:** {round(actual_travel, 2)} mm | **RPM:** {int(rpm)} | **Feed:** {f_min} mm/min")
        st.write(f"**Power Required:** {round(p_req, 2)} kW")

        if p_req > m_power:
            st.error(f"🚨 Power Alert: {round(p_req,2)}kW exceeds {machine} limit.")
        
        if st.button("Calculate Drilling Total"):
            st.success(f"Total Time: {round((actual_travel/f_min)*60*cnt, 2)} seconds")

elif operation == "Boring / Hole Milling":

    st.subheader(f"Boring Planner ({machine})")

    # ==========================================
    # FINE BORING MATERIAL VALIDATION
    # ==========================================

    if material != "Aluminium":

        st.warning(
            "Fine boring parameters currently defined only for Aluminium."
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

    # ==========================================
    # STOCK STRATEGY
    # ==========================================

    if fine_boring_required:

        # Leave stock for final fine boring
        finish_stock = 0.5
        rough_target_dia = f_dia - finish_stock

    else:

        # Rough boring finishes directly to size
        finish_stock = 0.0
        rough_target_dia = f_dia

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

    total_time_sec = 0.0
    current_dia = 0.0

    # --- 3. STEP 1: DRILLING (Only if Solid) ---

    if e_mode == "Solid":

        drill_data = material_tables[material]["drill"]

        # Sort to find the largest drill that is still <= 30mm
        sorted_drills = sorted(
            [d for d in drill_data if d['max_d'] <= 30],
            key=lambda x: x['max_d'],
            reverse=True
        )

        safe_drill_dia = 0.0

        for drill in sorted_drills:

            if drill['max_d'] < rough_target_dia:

                d_params = get_parameters(drill['max_d'], material)

                if d_params[0] is not None and d_params[1] is not None:

                    d_rpm, d_fmin = d_params[0], d_params[1]

                    p_check = (
                        (
                            (d_fmin / d_rpm)
                            * (math.pi * drill['max_d'] * d_rpm / 1000)
                            * drill['max_d']
                            * kc
                        ) / 192000
                    )

                    if p_check <= m_power:

                        safe_drill_dia = drill['max_d']
                        break

        if safe_drill_dia > 0:

            d_travel = (
                b_dep
                + (6 if bor_ht == "Through Hole" else 3)
                + ((0.18 * safe_drill_dia) if safe_drill_dia <= 20 else 0)
            )

            d_time = (d_travel / d_fmin) * 60

            total_time_sec += d_time

            st.success(
                f"Step 1: Drilling Ø{safe_drill_dia} | "
                f"Power: {round(p_check,2)}kW | "
                f"Time: {round(d_time, 2)}s"
            )

            current_dia = safe_drill_dia

        else:

            st.error("❌ No safe drill found (Max Ø30 limit).")
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

        if not tool:

            st.warning(f"No boring data found for Ø{current_dia}.")
            break

        # Max stock increment from table
        max_dia_increment = tool['ap']

        d2 = min(
            rough_target_dia,
            current_dia + max_dia_increment
        )

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

        st.write(
            f"🔹 Boring Ø{current_dia} ➔ Ø{d2} | "
            f"Stock: {round(d2-current_dia, 2)}mm | "
            f"Power: {round(p_bor, 2)}kW | "
            f"Time: {round(p_time, 1)}s"
        )

        current_dia = d2

    # ==========================================
    # STEP 3 : FINAL BORING PASS
    # ==========================================

    if fine_boring_required:

        f_tool = get_fine_boring_params(f_dia, material)

        if f_tool:

            finish_vc = f_tool["vc"]
            finish_feed_rev = f_tool["feed_rev"]

            finish_rpm = (
                (1000 * finish_vc)
                / (math.pi * f_dia)
            )

            finish_feed = (
                finish_feed_rev
                * finish_rpm
            )

            finish_time = (
                (bor_travel / finish_feed)
                * 60
            )

            total_time_sec += finish_time

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


    # ==========================================
    # FINAL CONSOLIDATED CALCULATION
    # ==========================================

    if st.button(
        "Calculate Total Boring Cycle Time",
        key="bor_calc_final"
    ):

        st.divider()

        st.metric(
            "Total Combined Cycle Time",
            f"{round(total_time_sec, 2)} sec"
        )

        st.write(
            f"**Total Time in Minutes:** "
            f"{round(total_time_sec/60, 2)} min"
        )
    
elif operation == "Tapping":
    st.title("Tapping Calculator")

    # 1. Material Guardrail
    if material != "Aluminium":
        st.error(f"⚠️ Data bank missing for {material}. Currently, this calculator only supports Aluminium.")
        st.stop()

    st.info(f"Machine: {machine} | Spindle: {m_taper} | Material: {material}")

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
            total_time_sec = time_per_hole * count * 60
            st.subheader(f"Total Time: {round(total_time_sec, 1)} seconds")

    # 7. Thread Milling Logic
    if use_threadmill and not stop_all:
        st.divider()
        st.subheader("Thread Milling Calculation")
        
        threadmill_table = material_tables[material]["threadmill"]
        tm_row = next((row for row in threadmill_table if row["tap"] == selected_tap and row["pitch"] == pitch), None)

        if tm_row is None:
            st.error("No thread mill data available for this specific size.")
        else:
            vc_tm = tm_row["vc"]
            feed_rev = tm_row["feed_rev"]
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
                tm_time_sec = (tm_cut_length / feed_tm) * count * 60
                st.subheader(f"Total TM Time: {round(tm_time_sec, 1)} seconds")

elif operation == "Face Milling":
    st.title("Face Milling Calculator")

    # 1. Material Guardrail
    if material != "Aluminium":
        st.error(f"⚠️ Data bank missing for {material}. Currently, this calculator only supports Aluminium.")
        st.stop()

    st.info(f"Machine: {machine} | Spindle: {m_taper} | Material: {material}")

    # 2. Surface Finish & PCD Warning
    is_pcd_required = ra_input < 1.2

    if is_pcd_required:
        st.warning(
            "⚠️ **PCD Tooling Required:** Ra < 1.2 cannot be achieved with standard carbide. "
            "This calculator will now leave 0.5mm stock for a separate PCD finish pass. "
            "**Note:** You must add the PCD cycle time manually to your total estimate."
        )

    # 3. Filtering Logic
    suitable_tools = [
        tool for tool in face_mill_data_aluminium
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
    ap_limit = selected_tool["stock"]

    # --- POWER VALIDATION ---
    efficiency = 0.8
    req_power = (ae * ap_limit * vf * kc) / (60e6 * efficiency)

    st.metric(
        "Required Power",
        f"{req_power:.2f} kW",
        delta=f"Limit: {m_power} kW",
        delta_color="inverse"
    )

    if req_power > m_power:
        st.error("⚠️ Machine Overload!")
    else:
        st.success(f"✅ Tool: Ø{tool_dia}mm | RPM: {rpm} | Feed: {vf} mm/min")

    # PROCESS PARAMETERS
    total_stock = st.number_input("Total Stock to Remove (mm)", value=5.5, key="fm_total_stock")

    if is_pcd_required:
        rough_stock = max(0.0, total_stock - 0.5)
        rough_passes = math.ceil(rough_stock / ap_limit) if rough_stock > 0 else 0
        st.info(f"PCD STRATEGY: {rough_passes} Roughing passes. 0.5mm left for PCD.")
    else:
        finish_required = ra_input < 3.2

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
        if not is_pcd_required and ra_input < 3.2 and total_stock > 0.5:
            time_finish = cut_length / (vf * 0.8)

        total_time_min = time_rough + time_finish

        st.subheader("Roughing Estimates")

        col_a, col_b = st.columns(2)
        col_a.metric("Roughing Passes", f"{rough_passes}")
        col_b.metric("Roughing Time", f"{total_time_min * 60:.1f} sec")

        if is_pcd_required:
            st.warning("☝️ Add PCD finishing time separately")
