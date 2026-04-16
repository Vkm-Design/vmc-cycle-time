import streamlit as st
import math

# ================= MATERIAL TABLE =================
kc_data = {
    "Aluminium": 800,
    "Steel_C22": 1700,
    "Steel_C45": 1950,
    "Steel_C60": 2250,
    "Stainless_Steel": 2400
}

# ================= MACHINE TABLE (CONTINUOUS VALUES ONLY) =================
machine_data = {
    "Ace BT40": {"power": 5.5, "torque": 35},
    "Ace HSK63": {"power": 5.5, "torque": 35},

    "Brother Std BT30": {"power": 7, "torque": 26.8},
    "Brother High Torque BT30": {"power": 9.2, "torque": 61.1},

    "Fanuc Std BT30": {"power": 3.7, "torque": 11.8},
    "Fanuc High Torque BT30": {"power": 3.7, "torque": 27.6},

    "Makino Slim HSK50": {"power": 11, "torque": 33},
    "Makino PS65 BT40": {"power": 18.5, "torque": 95},
    "Makino PS65 HSK63": {"power": 18.5, "torque": 95}
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

material_tables = {
    "Aluminium": {
        "drill": drill_data_aluminium, 
        "boring": boring_data_aluminium,     
        "tap": tap_data_aluminium      
    },
    "Steel_C22": {"drill": [], "boring": [], "tap": []},
    "Steel_C45": {"drill": [], "boring": [], "tap": []},
    "Steel_C60": {"drill": [], "boring": [], "tap": []},
    "Stainless_Steel": {"drill": [], "boring": [], "tap": []}
}

def get_parameters(diameter, material):

    table = material_tables[material]["drill"]

    for row in table:
        if row["min_d"] <= diameter < row["max_d"]:

            if "rpm" in row:
                rpm = row["rpm"]
            else:
                rpm = (1000 * row["vc"]) / (math.pi * diameter)

            return rpm, row["feed_min"], row["max_depth"]

    return None, None, None

def get_boring_params(dia, material):
    # Check if boring data exists for this material
    if "boring" in material_tables[material] and len(material_tables[material]["boring"]) > 0:
        table = material_tables[material]["boring"]
    else:
        # Fallback to Aluminium if table is empty (your safety rule)
        table = material_tables["Aluminium"]["boring"]
        
    for row in table:
        if row["min"] <= dia < row["max"]:
            return row
    return None

def get_diameter(tap):
    return float(tap.replace("M", ""))

def filter_tools_by_spindle(spindle, material):
    table = material_tables[material]["face_mill"]
    return [t for t in table if spindle in t["spindles"]]

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

operation = st.selectbox("Select Operation", ["Drilling", "Boring / Hole Milling", "Tapping", "Face Milling"])

if operation == "Drilling":

    st.title("Drilling Calculator")

    # 1. ---- Material Selection (Always from kc_data keys) ----
    material = st.selectbox("Select Material", list(kc_data.keys()), key="drill_mat")
    kc = kc_data[material]

    # 2. ---- Machine Selection ----
    machine = st.selectbox("Select Machine", list(machine_data.keys()))
    machine_power = machine_data[machine]["power"]
    machine_torque = machine_data[machine]["torque"]

    diameter = st.number_input("Drill Diameter (mm)", value=5.0)
    depth = st.number_input("Depth (mm)", value=10.0)
    count = st.number_input("Number of Holes", value=1)

    # 3. ---- Safety Check for Parameters Table ----
    if material in material_tables:
        rpm, feed_min, max_depth = get_parameters(diameter, material)
    else:
        st.error(f"Cutting parameters for {material} are not yet defined in 'material_tables'.")
        st.stop() # Prevents the program from crashing at get_parameters

    # 4. ---- Display Parameters ----
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

    # ================= POWER & TORQUE CALCULATION =================

    # Convert feed (mm/min) → feed per rev (mm/rev)
    if rpm > 0:
        frev = feed_min / rpm
    else:
        frev = 0

    # ---- Power Calculation (Drilling) ----
    power = (frev * (rpm * math.pi * diameter / 1000) * diameter * kc) / (240000 * 0.8)

    # ---- Torque Calculation ----
    if rpm > 0:
        torque = (power * 9550) / rpm
    else:
        torque = 0

    # ---- Display ----
    st.write("Required Power (kW):", round(power, 2))
    st.write("Required Torque (Nm):", round(torque, 2))

    if st.button("Calculate Drill Time"):
        if rpm is not None:
            time_per_hole = depth / feed_min
            total_time_sec = time_per_hole * count * 60
            st.write("Total Time (sec):", round(total_time_sec, 2))

    # ================= MACHINE VALIDATION =================

    st.write("Machine Power (kW):", machine_power)
    st.write("Machine Torque (Nm):", machine_torque)

    power_ok = power <= machine_power
    torque_ok = torque <= machine_torque

    if power_ok and torque_ok:
        st.success("✅ Machine is suitable for this operation")

    else:
        if not power_ok:
            st.error("❌ Power requirement exceeds machine capacity")

        if not torque_ok:
            st.error("❌ Torque requirement exceeds machine capacity")

        st.warning("⚠️ Suggestion: Select a higher capacity machine")

elif operation == "Boring / Hole Milling":
    # --- MATERIAL DATA CHECK ---
    if material != "Aluminium":
        st.error(f"⚠️ Boring data for {material} is currently under preparation.")
        st.info("Please select 'Aluminium' to test the logic, or contact the admin to upload Steel data tables.")
        st.stop() # This stops the rest of the boring code from running
    
    st.header("Boring & Hole Mill Planner")
    
    col1, col2 = st.columns(2)
    with col1:
        finish_dia = st.number_input("Finish Bore Diameter (mm)", value=33.0)
        bore_depth = st.number_input("Bore Depth (mm)", value=50.0)
    
    # --- Step 1: Solid vs Core Logic ---
    if finish_dia <= 3.0:
        st.info("Diameter ≤ 3mm. Solid drilling only (Boring/Core not possible).")
        entry_mode = "Solid"
    else:
        entry_mode = st.radio("Starting Condition", ["Solid", "Core Hole"], horizontal=True)

    if entry_mode == "Core Hole":
        start_dia = st.number_input("Existing Core Diameter (mm)", value=28.0)
    else:
        # If solid, drill first. Max drill Ø30 per your rule.
        start_dia = min(finish_dia - 1.0, 30.0)
        st.info(f"Process: Will start with a Ø{start_dia} Drill.")

    # --- Step 2: Process Analysis (Tolerance & Ra Gates) ---
    needs_boring = False
    if finish_dia > 20:
        term = "Boring Bar"
        # Rule: Tol >= 0.2 and Ra >= 3.2 is just a drill
        if ra_input < 3.2 or tol_input < 0.2: 
            needs_boring = True
    else:
        term = "Hole Mill"
        # Rule: Tol >= 0.1 and Ra >= 3.2 is just a drill
        if ra_input < 3.2 or tol_input < 0.1: 
            needs_boring = True

    if not needs_boring:
        st.success(f"✅ Analysis: Drilling is sufficient for Ø{finish_dia} with current Tolerance/Ra.")
    else:
        # --- Step 3: Boring Chain Calculation ---
        total_stock_dia = finish_dia - start_dia
        params = get_boring_params(finish_dia, material)
        
        if params:
            # ap is radial, so max diametrical stock is 2 * ap
            max_dia_stock = params["ap"] * 2
            num_tools = math.ceil(total_stock_dia / max_dia_stock)
            
            tool_steps = []
            for i in range(1, num_tools + 1):
                # Distribute stock equally across tools
                step_dia = start_dia + (total_stock_dia / num_tools) * i
                tool_steps.append(round(step_dia, 2))
            
            st.subheader(f"Calculated {term} Sequence")
            total_boring_time = 0
            current_d1 = start_dia
            
            for i, step_dia in enumerate(tool_steps):
                p = get_boring_params(step_dia, material)
                rpm = p["rpm"]
                feed_min = p["feed_min"]
                
                # Check 3xD Rule for Manual Overrides
                if bore_depth > (3 * step_dia):
                    st.warning(f"⚠️ Depth > 3xD for tool Ø{step_dia}. Adjusting parameters.")
                    vc_man = st.number_input(f"Manual Vc (m/min) for Ø{step_dia}", value=50.0, key=f"vc_{i}")
                    f_rev_man = st.number_input(f"Manual Feed (mm/rev) for Ø{step_dia}", value=0.1, key=f"f_{i}")
                    rpm = (1000 * vc_man) / (math.pi * step_dia)
                    feed_min = rpm * f_rev_man

                # Power Calculation (Based on your formula image)
                # Power = (Vc * Frev * (D2-D1)/2 * Kc) / (60 * 1000 * 0.8)
                vc_calc = (math.pi * step_dia * rpm) / 1000
                f_rev_calc = feed_min / rpm
                p_req = (vc_calc * f_rev_calc * ((step_dia - current_d1)/2) * kc) / (60 * 1000 * 0.8)
                
                st.write(f"**Tool {i+1}:** {term} Ø{step_dia} | RPM: {int(rpm)} | Feed: {feed_min} mm/min | Power: {round(p_req, 2)} kW")
                
                total_boring_time += (bore_depth / feed_min)
                current_d1 = step_dia
            
            st.divider()
            st.metric("Total Boring Cycle Time", f"{round(total_boring_time * 60, 2)} Seconds")
            
            if ra_input < 1.6:
                st.error("💡 High Surface Finish Requirement: A Finish Reamer is suggested after this cycle.")


elif operation == "Tapping":
    st.title("Tapping Calculator")

    # Change list(material_tables.keys()) to list(kc_data.keys())
    tap_material = st.selectbox(
        "Select Material",
        list(kc_data.keys()), 
        key="tap_material"
    )

    # This logic allows you to select "Steel" even before the table is ready
    if tap_material in material_tables:
        tap_table = material_tables[tap_material]["tap"]
    else:
        st.error(f"Cutting parameters for {tap_material} are not yet defined.")
        st.stop() # Prevents the code from crashing further down

    pitch_list = sorted(list(set(row["pitch"] for row in tap_table)))
    selected_pitch = st.selectbox("Select Pitch", pitch_list)

    filtered = [row for row in tap_table if row["pitch"] == selected_pitch]
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

    thread_material = st.selectbox(
        "Select Material",
        list(material_tables.keys()),
        key="thread_material"
    )

    threadmill_table = material_tables[thread_material]["threadmill"]
    if use_threadmill and not stop_all:

        st.subheader("Thread Milling Calculation")

        tm_row = next(
            (row for row in threadmill_table
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
    
    # 1. Select Material from the full kc_data list
    face_material = st.selectbox(
        "Select Material",
        list(kc_data.keys()), 
        key="face_material"
    )

    # 2. Select Spindle (Must be defined BEFORE filtering tools)
    spindle = st.selectbox(
        "Select Spindle", 
        ["BT30","BBT30","BT40","BT50","HSK A50","HSK A63","HSK A100"]
    )

    # 3. Check if material exists in your tool tables and filter
    if face_material in material_tables:
        tools = filter_tools_by_spindle(spindle, face_material)
    else:
        st.error(f"Face Mill parameters for {face_material} are not yet defined in 'material_tables'.")
        st.stop() # Stops the code here so it doesn't crash below

    # 4. Continue with Shape and Mode
    shape = st.selectbox("Component Shape", ["Rectangular", "Circular"])
    tool_mode = st.selectbox("Tool Selection Mode", ["Auto", "Manual"])

    # ... rest of your Face Milling logic follows ...

    # ================= RECTANGULAR =================
    if shape == "Rectangular":

        L = st.number_input("Length (mm)", value=60.0)
        W = st.number_input("Width (mm)", value=10.0)

        min_dim = min(L, W)
        long_dim = max(L, W)

        # Tool selection
        if tool_mode == "Auto":
            selected_tool = select_tool_rect(min_dim, tools)
        else:
            dia_list = [t["dia"] for t in tools]
            dia = st.selectbox("Select Tool Diameter", dia_list)
            selected_tool = next(t for t in tools if t["dia"] == dia)

        if selected_tool:
            tool_dia = selected_tool["dia"]
            max_width = selected_tool["max_width"]

            if W <= max_width:
                width_passes = 1
            else:
                width_passes = math.ceil(W / max_width)

            single_pass_length = long_dim + tool_dia + 4
            cut_length = single_pass_length * width_passes

    # ================= CIRCULAR =================
    elif shape == "Circular":

        comp_dia = st.number_input("Component Diameter (mm)", value=50.0)

        if tool_mode == "Auto":
            tools_sorted = sorted(tools, key=lambda x: x["max_width"], reverse=True)
            selected_tool = tools_sorted[0] if tools_sorted else None
        else:
            dia_list = [t["dia"] for t in tools]
            dia = st.selectbox("Select Tool Diameter", dia_list)
            selected_tool = next(t for t in tools if t["dia"] == dia)

        if selected_tool:
            tool_dia = selected_tool["dia"]
            max_width = selected_tool["max_width"]

            if comp_dia <= max_width:
                radial_passes = 1
            else:
                radial_passes = math.ceil(comp_dia / max_width)

            if comp_dia <= max_width:
                single_pass_length = comp_dia + tool_dia
            else:
                eff_dia = comp_dia + 5
                single_pass_length = math.pi * (eff_dia - tool_dia) + comp_dia + tool_dia

            cut_length = single_pass_length * radial_passes

            st.write("Radial Passes:", radial_passes)

            if radial_passes > 1:
                st.warning("Multiple radial passes required ⚠️")

    # ================= COMMON =================
    if selected_tool:

        ra = st.number_input("Surface Finish Ra", value=3.2)

        feed = selected_tool["feed"]
        rpm = selected_tool["rpm"]
        stock_limit = selected_tool["stock"]

        stock = st.number_input("Stock to Remove (mm)", value=2.0)

        finish_required = ra < 1.6

        if finish_required:
            rough_stock = stock - 0.5
        else:
            rough_stock = stock

        passes = math.ceil(rough_stock / stock_limit)
        if passes < 1:
            passes = 1

        rough_passes = []
        remaining = rough_stock

        for i in range(passes):
            if remaining >= stock_limit:
                depth = stock_limit
            else:
                depth = remaining

            rough_passes.append(round(depth, 2))
            remaining -= depth

        st.write("Rough Passes:", ", ".join(map(str, rough_passes)))

        if finish_required:
            st.write("Finish Pass: 0.5 mm")

        st.write("Selected Tool Dia:", selected_tool["dia"])
        st.write("RPM:", rpm)
        st.write("Feed:", feed)
        st.write("No. of Rough Passes:", len(rough_passes))
        st.write("Cut Length:", round(cut_length, 2))

        if finish_required:
            finish_feed = feed * 0.8
            st.write("Finish Feed:", round(finish_feed, 2))

        if st.button("Calculate Milling Time"):

            total_time = 0

            for depth in rough_passes:
                total_time += (cut_length / feed)

            if finish_required:
                total_time += (cut_length / finish_feed)

            total_time_sec = total_time * 60

            st.write("Total Time (sec):", round(total_time_sec, 2))
