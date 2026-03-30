import streamlit as st
import math

# ---- Your Real Data ----
cutting_data = [
    {"min_d": 0.5, "max_d": 1, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
    {"min_d": 1, "max_d": 3, "rpm": 6500, "feed_min": 100, "max_depth": 5},
    {"min_d": 3, "max_d": 5, "vc": 50, "feed_min": 450, "max_depth": 20},
    {"min_d": 5, "max_d": 8, "vc": 80, "feed_min": 550, "max_depth": 30},
    {"min_d": 8, "max_d": 10, "vc": 100, "feed_min": 480, "max_depth": 40},
    {"min_d": 10, "max_d": 15, "vc": 120, "feed_min": 550, "max_depth": 50}
]

tap_data = [
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
def get_parameters(diameter):
    for row in cutting_data:
        if row["min_d"] <= diameter <= row["max_d"]:
            if "rpm" in row:
                rpm = row["rpm"]
            else:
                rpm = (1000 * row["vc"]) / (math.pi * diameter)
            return rpm, row["feed_min"], row["max_depth"]
    return None, None, None

def get_diameter(tap):
    return float(tap.replace("M", ""))

st.title("Smart Drilling/Tapping Calculator (Aluminum)")

operation = st.selectbox("Select Operation", ["Drilling", "Tapping"])

if operation == "Drilling":

    st.title("Drilling Calculator")

    diameter = st.number_input("Drill Diameter (mm)", value=5.0)
    depth = st.number_input("Depth (mm)", value=10.0)
    count = st.number_input("Number of Holes", value=1)

    rpm, feed_min, max_depth = get_parameters(diameter)

    if rpm is not None:
        st.write("Recommended RPM:", round(rpm, 2))
        st.write("Feed (mm/min):", feed_min)
        st.write("Max Allowed Depth:", max_depth)
    else:
        st.error("Diameter not in defined range")

    manual_mode = False

    if max_depth is not None and depth > max_depth:
        st.warning("Depth exceeds recommended limit. Enter manual values.")
        manual_mode = True

    if manual_mode:
        vc_manual = st.number_input("Enter Vc manually", value=50.0, key="vc_manual")
        feed_rev_manual = st.number_input("Enter Feed (mm/rev)", value=0.1, key="feed_manual")

        rpm = (1000 * vc_manual) / (math.pi * diameter)
        feed_min = feed_rev_manual * rpm

    if st.button("Calculate Drill Time"):
        if rpm is not None:
            time_per_hole = depth / feed_min
            total_time_sec = time_per_hole * count * 60
            st.write("Total Time (sec):", round(total_time_sec, 2))

elif operation == "Tapping":

    st.title("Tapping Calculator")

    # ---- Pitch selection ----
    pitch_list = sorted(list(set(row["pitch"] for row in tap_data)))
    selected_pitch = st.selectbox("Select Pitch", pitch_list)

    filtered = [row for row in tap_data if row["pitch"] == selected_pitch]
    tap_options = list(set(row["tap"] for row in filtered))

    selected_tap = st.selectbox("Select Tap Size", tap_options)

    selected_row = next(row for row in filtered if row["tap"] == selected_tap)

    diameter = get_diameter(selected_tap)
    pitch = selected_row["pitch"]
    vc = selected_row["vc"]
    max_depth = selected_row["max_depth"]

    # ---- Tap type ----
    tap_type = st.selectbox("Tap Type", ["Through", "Blind"])

    tap_depth = st.number_input("Tap Depth (mm)", value=8.0)

if tap_type == "Blind":
    drill_depth = st.number_input("Drill Depth (mm)", value=10.0)
else:
    drill_depth = None
    count = st.number_input("Number of Holes", value=1)

    st.write("Diameter:", diameter)
    st.write("Pitch:", pitch)
    st.write("Recommended Vc:", vc)
    st.write("Max Depth:", max_depth)

    # ---- Depth validation ----
    valid_tap = True

    if tap_type == "Blind":
        if drill_depth < (tap_depth + 3 * pitch):
            st.error("Thread milling recommended instead of tapping")
            valid_tap = False

    # ---- Max depth check ----
    manual_mode = False
    if tap_depth > max_depth:
        st.warning("Depth exceeds recommended limit. Enter Vc manually.")
        manual_mode = True

    if manual_mode:
        vc = st.number_input("Enter Vc manually", value=vc, key="tap_vc")

    # ---- Calculation ----
    if valid_tap:
        rpm = (1000 * vc) / (math.pi * diameter)
        feed_min = pitch * rpm

        cut_length = (tap_depth + (pitch * 3 * 2)) * 2 + 4

        st.write("RPM:", round(rpm, 2))
        st.write("Feed (mm/min):", round(feed_min, 2))
        st.write("Cut Length (mm):", round(cut_length, 2))

        if st.button("Calculate Tap Time"):
            time_per_hole = cut_length / feed_min
            total_time_sec = time_per_hole * count * 60

            st.write("Total Time (sec):", round(total_time_sec, 2))

