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

def drilling_time(depth, feed_min):
    return depth / feed_min

st.title("Smart Drilling Calculator (Aluminum)")

# ---- Inputs ----
diameter = st.number_input("Drill Diameter (mm)", value=5.0)
depth = st.number_input("Depth (mm)", value=10.0)
count = st.number_input("Number of Holes", value=1)

# ---- Get parameters ----
rpm, feed_rev, max_depth = get_parameters(diameter)

# ---- Auto calculation ----
feed_min = feed_rev * rpm

st.write("Recommended RPM:", round(rpm, 2))
st.write("Recommended Feed (mm/rev):", feed_rev)
st.write("Feed (mm/min):", round(feed_min, 2))
st.write("Max Allowed Depth:", max_depth)

if max_depth is not None and depth > max_depth:
    st.warning("Depth exceeds recommended limit. Please enter manual values.")

    vc_manual = st.number_input("Enter Vc manually", value=50.0)
    feed_rev_manual = st.number_input("Enter Feed (mm/rev) manually", value=0.1)

    # override values
    rpm = (1000 * vc_manual) / (math.pi * diameter)
    feed_min = feed_rev_manual * rpm

rpm, feed_min, max_depth = get_parameters(diameter)

st.write("Recommended RPM:", rpm)
st.write("Recommended Feed (mm/min):", feed_min)
st.write("Max Allowed Depth:", max_depth)

# ⚠️ Check depth condition
manual_mode = False

if depth > max_depth:
    st.warning("Depth exceeds recommended limit. Please enter manual values.")
    manual_mode = True

    vc_manual = st.number_input("Enter Vc manually")
    feed_manual = st.number_input("Enter Feed (mm/min) manually")

    rpm = (1000 * vc_manual) / (math.pi * diameter)
    feed_min = feed_manual

# ---- Get Parameters ----
rpm, feed_min, max_depth = get_parameters(diameter)

st.write("RPM:", rpm)
st.write("Feed (mm/min):", feed_min)

# ---- Calculation ----
if st.button("Calculate"):
    if rpm is None:
        st.write("No data available")
    else:
        time_per_hole = depth / feed_min
        total_time_sec = time_per_hole * count * 60

        st.write("Total Time (sec):", round(total_time_sec, 2))
        
