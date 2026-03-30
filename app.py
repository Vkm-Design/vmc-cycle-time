import streamlit as st
import math

# ---- Your Real Data ----
cutting_data = [
    {"min_d": 0.5, "max_d": 0.9, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
    {"min_d": 1, "max_d": 3, "rpm": 6500, "feed_min": 100, "max_depth": 5},
    {"min_d": 3.1, "max_d": 5, "vc": 50, "feed_min": 450, "max_depth": 20},
    {"min_d": 5.1, "max_d": 8, "vc": 80, "feed_min": 550, "max_depth": 30},
    {"min_d": 8.1, "max_d": 10, "vc": 100, "feed_min": 480, "max_depth": 40},
    {"min_d": 10.1, "max_d": 15, "vc": 120, "feed_min": 550, "max_depth": 50}
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

st.title("Smart Drilling Calculator (Aluminum)")

# ---- Inputs ----
diameter = st.number_input("Drill Diameter (mm)", value=5.0)
depth = st.number_input("Depth (mm)", value=10.0)
count = st.number_input("Number of Holes", value=1)

# ---- Get Parameters ----
rpm, feed_min, max_depth = get_parameters(diameter)

# ---- Show recommended ----
st.write("Recommended RPM:", round(rpm, 2))
st.write("Recommended Feed (mm/min):", feed_min)
st.write("Max Allowed Depth:", max_depth)

# ---- Depth check ----
manual_mode = False

if max_depth is not None and depth > max_depth:
    st.warning("Depth exceeds recommended limit. Enter manual values below.")
    manual_mode = True

# ---- Manual override ----
if manual_mode:
    vc_manual = st.number_input("Enter Vc manually", value=50.0, key="vc_manual_new")
    feed_manual = st.number_input("Enter Feed (mm/min) manually", value=300.0, key="feed_manual_new")

    rpm = (1000 * vc_manual) / (math.pi * diameter)
    feed_min = feed_manual

# ---- Calculation ----
if st.button("Calculate"):
    if rpm is None:
        st.write("No data available")
    else:
        time_per_hole = depth / feed_min
        total_time_sec = time_per_hole * count * 60

        st.write("Total Time (sec):", round(total_time_sec, 2))
