import streamlit as st
import math

def rpm(vc, d):
    return (1000 * vc) / (math.pi * d)

def drilling_time(depth, feed, rpm):
    return depth / (feed * rpm)  # time in minutes

st.title("Drilling Cycle Time Calculator")

vc = st.number_input("Cutting Speed (Vc)", value=200.0)
diameter = st.number_input("Drill Diameter (mm)", value=10.0)
feed = st.number_input("Feed (mm/rev)", value=0.2)
depth = st.number_input("Depth (mm)", value=20.0)
count = st.number_input("Number of Holes", value=1)

if st.button("Calculate"):
    r = rpm(vc, diameter)
    time_per_hole_min = drilling_time(depth, feed, r)
    total_time_min = time_per_hole_min * count

    # convert to seconds
    time_per_hole_sec = time_per_hole_min * 60
    total_time_sec = total_time_min * 60

    st.write("RPM:", round(r, 2))
    st.write("Time per hole (sec):", round(time_per_hole_sec, 2))
    st.write("Total time (sec):", round(total_time_sec, 2))