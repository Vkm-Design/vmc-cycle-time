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

threadmill_data = [
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

face_mill_data = [
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

def filter_tools_by_spindle(spindle):
    return [t for t in face_mill_data if spindle in t["spindles"]]

def select_tool_rect(min_dim, tools):
    # Select biggest allowed tool for selected spindle
    tools_sorted = sorted(tools, key=lambda x: x["max_width"], reverse=True)
    return tools_sorted[0] if tools_sorted else None

def select_tool_circular(dia, tools):
    for t in tools:
        if t["max_width"] >= dia:
            return t
    return None

st.title("Smart Machining Calculator (Aluminum)")

operation = st.selectbox("Select Operation", ["Drilling", "Tapping", "Face Milling"])

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
    count = st.number_input("Number of Holes", value=1)

    if tap_type == "Blind":
        drill_depth = st.number_input("Drill Depth (mm)", value=10.0)
    else:
        drill_depth = None
        

    # ---- Show data ----
    st.write("Diameter:", diameter)
    st.write("Pitch:", pitch)
    st.write("Recommended Vc:", vc)
    st.write("Max Depth:", max_depth)

       # ---- Validation ----
    valid_tap = True
    use_threadmill = False
    manual_mode = False
    stop_all = False

    # ---- Clearance Logic ----
    if tap_type == "Blind":

        clearance = drill_depth - tap_depth

        st.write("Clearance:", round(clearance, 2))

        # ❌ Impossible case
        if drill_depth <= tap_depth:
            st.error("Drill depth is less than tap depth. Not possible to machine thread")
            valid_tap = False
            use_threadmill = False
            stop_all = True

        # ❌ Unsafe
        elif clearance < (1 * pitch):
            st.error("Insufficient clearance. Not safe for tapping")
            valid_tap = False
            use_threadmill = True

        # ⚠️ Thread mill zone
        elif clearance <= (2 * pitch):
            st.warning("Clearance not sufficient. Thread milling recommended")
            valid_tap = False
            use_threadmill = True

        # ✅ Safe for tapping
        else:
            st.success("Suitable for tapping")

    # ---- Tap depth check (ONLY if tapping allowed) ----
    if valid_tap and not stop_all:
        if tap_depth > max_depth:
            st.warning("Depth exceeds recommended limit. Enter Vc manually.")
            manual_mode = True

    # ---- Manual input ----
    if manual_mode and valid_tap:
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

    # ---- THREAD MILL LOGIC ----
    if use_threadmill and not stop_all:

        st.subheader("Thread Milling Calculation")

        tm_row = next(
            (row for row in threadmill_data
             if row["tap"] == selected_tap and row["pitch"] == pitch),
            None
        )

        if tm_row is None:
            st.error("No thread mill data available")

        else:
            vc_tm = tm_row["vc"]
            feed_rev = tm_row["feed_rev"]
            tool_dia = tm_row["tool_dia"]
            max_depth_tm = tm_row["max_depth"]

            D2 = diameter   # thread size
            D1 = tool_dia   # tool diameter

            # ---- Depth check ----
            if tap_depth > max_depth_tm:
                st.warning("Special thread mill recommended")

            else:
                rpm = (1000 * vc_tm) / (math.pi * tool_dia)
                feed_min = feed_rev * rpm

                cut_length = ((D2 - D1) * 3.14 * 3) + tap_depth + 4

                st.write("RPM:", round(rpm, 2))
                st.write("Feed (mm/min):", round(feed_min, 2))
                st.write("Cut Length (mm):", round(cut_length, 2))

                if st.button("Calculate Thread Mill Time"):
                    time_per_hole = cut_length / feed_min
                    total_time_sec = time_per_hole * count * 60

                    st.write("Total Time (sec):", round(total_time_sec, 2))

elif operation == "Face Milling":

    st.title("Face Milling Calculator")

    spindle = st.selectbox("Select Spindle", ["BT30","BBT30","BT40","BT50","HSK A50","HSK A63","HSK A100"])

    shape = st.selectbox("Component Shape", ["Rectangular", "Circular"])

    stock = st.number_input("Total Stock (mm)", value=3.0)

    tools = filter_tools_by_spindle(spindle)

    tool_mode = st.selectbox("Tool Selection Mode", ["Auto", "Manual"])

    selected_tool = None

    if shape == "Rectangular":
        L = st.number_input("Length (mm)", value=60.0)
        W = st.number_input("Width (mm)", value=10.0)

        min_dim = min(L, W)
        long_dim = max(L, W)
# Auto tool selection for circular
    if tool_mode == "Auto":
        tools_sorted = sorted(tools, key=lambda x: x["max_width"], reverse=True)
        selected_tool = tools_sorted[0] if tools_sorted else None
    else:
        dia_list = [t["dia"] for t in tools]
        dia = st.selectbox("Select Tool Diameter", dia_list)
        selected_tool = next(t for t in tools if t["dia"] == dia)
    if tool_mode == "Auto":
        selected_tool = select_tool_rect(min_dim, tools)
    else:
        dia_list = [t["dia"] for t in tools]
        dia = st.selectbox("Select Tool Diameter", dia_list)
        selected_tool = next(t for t in tools if t["dia"] == dia)

    if selected_tool:
        tool_dia = selected_tool["dia"]
        max_width = selected_tool["max_width"]

        # ---- Width Pass Calculation ----
        if W <= max_width:
            width_passes = 1
        else:
            width_passes = math.ceil(W / max_width)

        # ---- Single Pass Length ----
        single_pass_length = long_dim + tool_dia + 4

        # ---- Total Cut Length ----
        cut_length = single_pass_length * width_passes

        # ---- Display ----
        st.write("Width Passes:", width_passes)
        st.write("Single Pass Length:", round(single_pass_length, 2))
        st.write("Total Cut Length:", round(cut_length, 2))

        if width_passes > 1:
            st.warning("Multiple width passes required ⚠️")

    else:
        comp_dia = st.number_input("Component Diameter (mm)", value=50.0)

        if tool_mode == "Auto":
            selected_tool = select_tool_circular(comp_dia, tools)

        else:
            dia_list = [t["dia"] for t in tools]
            dia = st.selectbox("Select Tool Diameter", dia_list)
            selected_tool = next(t for t in tools if t["dia"] == dia)

        if selected_tool:
            tool_dia = selected_tool["dia"]

            if selected_tool["max_width"] >= comp_dia:
                cut_length = comp_dia + tool_dia
            else:
                eff_dia = comp_dia + 5
                cut_length = math.pi * (eff_dia - tool_dia) + comp_dia + tool_dia

    # ---- Surface Finish ----
    ra = st.number_input("Surface Finish Ra", value=3.2)

    if selected_tool:

        feed = selected_tool["feed"]
        rpm = selected_tool["rpm"]
        stock_limit = selected_tool["stock"]

        finish_required = ra < 1.6

        if finish_required:
            rough_stock = stock - 0.5
        else:
            rough_stock = stock

        passes = math.ceil(rough_stock / stock_limit)

        rough_depth = rough_stock / passes

        st.write("Selected Tool Dia:", selected_tool["dia"])
        st.write("RPM:", rpm)
        st.write("Feed:", feed)
        st.write("No. of Rough Passes:", passes)
        st.write("Depth per Pass:", round(rough_depth, 2))
        st.write("Cut Length:", round(cut_length, 2))

        if finish_required:
            finish_feed = feed * 0.8
            st.write("Finish Pass: 0.5 mm")
            st.write("Finish Feed:", round(finish_feed, 2))

        if st.button("Calculate Milling Time"):

            total_time = 0

            for i in range(passes):
                total_time += (cut_length / feed)

            if finish_required:
                total_time += (cut_length / finish_feed)

            total_time_sec = total_time * 60

            st.write("Total Time (sec):", round(total_time_sec, 2))
