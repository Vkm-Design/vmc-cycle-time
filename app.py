import streamlit as st
import math

# ---- Your Real Data ----
cutting_data = [
    {"min_d": 0.5, "max_d": 0.9, "rpm": 8500, "feed_min": 60},
    {"min_d": 1, "max_d": 3, "rpm": 6500, "feed_min": 100},
    {"min_d": 3.1, "max_d": 5, "vc": 50, "feed_min": 450},
    {"min_d": 5.1, "max_d": 8, "vc": 80, "feed_min": 550},
    {"min_d": 8.1, "max_d": 10, "vc": 100, "feed_min": 480},
    {"min_d": 10.1, "max_d": 15, "vc": 120, "feed_min": 550}
]

def get_parameters(diameter):
    for row in cutting_data:
        if row["min_d"] <= diameter <= row["max_d"]:
            if "rpm" in row:
                rpm = row["rpm"]
            else:
                rpm = (1000 * row["vc"]) / (math.pi * diameter)
            return rpm, row["feed_min"]
    return None, None

def drilling_time(depth, feed_min):
    return depth / feed_min

st.title("Smart Drilling Calculator (Aluminum)")

# ---- Inputs ----
diameter = st.number_input("Drill Diameter (mm)", value=5.0)
depth = st.number_input("Depth (mm)", value=10.0)
count = st.number_input("Number of Holes", value=1)

# ---- Get Parameters ----
rpm, feed_min = get_parameters(diameter)

st.write("RPM:", rpm)
st.write("Feed (mm/min):", feed_min)

# ---- Calculation ----
if st.button("Calculate"):
    if rpm is None:
        st.write("No data available for this diameter")
    else:
        time_per_hole = drilling_time(depth, feed_min)
        total_time_sec = time_per_hole * count * 60

        st.write("Total Time (sec):", round(total_time_sec, 2))
