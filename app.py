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

# ==========================================
# 1. MATERIAL MASTER TABLE
# ==========================================
material_tables = {
    "Aluminium": {
        "drill": drill_data_aluminium, 
        "boring": boring_data_aluminium,     
        "tap": tap_data_aluminium,
        "threadmill": threadmill_data_aluminium, # ADD THIS LINE
        "face_mill": face_mill_data_aluminium    # ADD THIS TOO if you have it
    },
    "Steel_C22": {"drill": [], "boring": [], "tap": [], "threadmill": []},
    "Steel_C45": {"drill": [], "boring": [], "tap": [], "threadmill": []},
    "Steel_C60": {"drill": [], "boring": [], "tap": [], "threadmill": []},
    "Stainless_Steel": {"drill": [], "boring": [], "tap": [], "threadmill": []}
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
            return rpm, row["feed_min"], row["max_depth"]
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
# 3. GLOBAL SELECTIONS & APP UI
# ==========================================
st.title("Smart Machining Calculator")

# Main Operation Menu
operation = st.selectbox("Select Operation", ["Drilling", "Boring / Hole Milling", "Tapping", "Face Milling"])

# --- GLOBAL SELECTIONS ---
st.sidebar.header("Global Settings")

# 1. Material Selection
material = st.sidebar.selectbox("Select Material", list(kc_data.keys()), key="global_mat")
kc = kc_data[material]

# 2. Machine Selection (This must come FIRST)
machine = st.sidebar.selectbox("Select Machine", list(machine_data.keys()), key="global_mach")

# 3. Data Lookup (This uses the 'machine' variable from above)
m_power = machine_data[machine]["power"]
m_torque = machine_data[machine]["torque"]
m_taper = machine_data[machine].get("taper", "BT40") 

st.sidebar.markdown("---")
st.sidebar.header("Quality Requirements")
ra_input = st.sidebar.number_input("Surface Finish (Ra)", value=3.2, step=0.1)

# ONLY show Diameter Tolerance if it is NOT Face Milling
if operation != "Face Milling":
    tol_input = st.sidebar.number_input("Diameter Tolerance (±)", value=0.1, format="%.3f")
else:
    # We set a default value so the code doesn't crash, but the user doesn't see the box
    tol_input = 0.1

# ==========================================
# 4. OPERATION: DRILLING
# ==========================================
if operation == "Drilling":
    st.subheader("Drilling Calculator")
    dia = st.number_input("Drill Diameter (mm)", value=10.0)
    dep = st.number_input("Depth (mm)", value=20.0)
    cnt = st.number_input("Number of Holes", value=1)

    rpm, f_min, mx_dep = get_parameters(dia, material)
    
    if rpm:
        st.write(f"**RPM:** {int(rpm)} | **Feed:** {f_min} mm/min")
        f_rev = f_min / rpm
        # Drilling Power Formula
        p_req = (f_rev * (rpm * math.pi * dia / 1000) * dia * kc) / (240000 * 0.8)
        t_req = (p_req * 9550) / rpm
        
        st.write(f"**Power:** {round(p_req, 2)} kW | **Torque:** {round(t_req, 2)} Nm")
        
        if p_req <= m_power and t_req <= m_torque:
            st.success("✅ Machine Capacity OK")
        else:
            st.error("❌ Machine Capacity Exceeded")
            
        if st.button("Calculate Time"):
            st.info(f"Total Time: {round((dep/f_min)*cnt*60, 2)} seconds")
    else:
        st.error("Diameter not in database")

# ==========================================
# 5. OPERATION: BORING / HOLE MILLING
# ==========================================
elif operation == "Boring / Hole Milling":
    if material != "Aluminium":
        st.error(f"⚠️ Boring data for {material} is under preparation.")
        st.stop()

    st.subheader("Boring & Hole Mill Planner")
    col1, col2 = st.columns(2)
    with col1:
        f_dia = st.number_input("Finish Bore Diameter (mm)", value=33.0)
        b_dep = st.number_input("Bore Depth (mm)", value=50.0)
    
    e_mode = st.radio("Starting Condition", ["Solid", "Core Hole"], horizontal=True)
    s_dia = st.number_input("Core Dia", value=28.0) if e_mode == "Core Hole" else min(f_dia - 1.0, 30.0)
    
    # Process Logic
    needs_b = False
    limit = 0.2 if f_dia > 20 else 0.1
    if ra_input < 3.2 or tol_input < limit: needs_b = True

    if not needs_b:
        st.success("✅ Drilling is sufficient for this tolerance.")
    else:
        params = get_boring_params(f_dia, material)
        if params:
            max_stk = params["ap"] * 2
            tools_n = math.ceil((f_dia - s_dia) / max_stk)
            curr_d1 = s_dia
            total_t = 0
            
            for i in range(tools_n):
                step_d = s_dia + ((f_dia - s_dia) / tools_n) * (i + 1)
                p = get_boring_params(step_d, material)
                rpm_b, f_b = p["rpm"], p["feed_min"]
                
                if b_dep > (3 * step_d):
                    st.warning(f"Long Tool Safety: Enter Manual Vc/Feed for Ø{step_d}")
                    v_man = st.number_input(f"Vc Ø{step_d}", value=60, key=f"v{i}")
                    fr_man = st.number_input(f"f/rev Ø{step_d}", value=0.1, key=f"fr{i}")
                    rpm_b = (1000 * v_man) / (math.pi * step_d)
                    f_b = rpm_b * fr_man

                # Boring Power
                p_b = ((math.pi*step_d*rpm_b/1000)*(f_b/rpm_b)*((step_d-curr_d1)/2)*kc)/(48000)
                t_b = (p_b * 9550) / rpm_b if rpm_b > 0 else 0
                
                st.write(f"**Step {i+1}:** Ø{round(step_d,2)} | {int(rpm_b)} RPM | {f_b} mm/min | {round(p_b,2)} kW")
                total_t += (b_dep / f_b)
                curr_d1 = step_d
            
            st.metric("Total Boring Time", f"{round(total_t * 60, 2)} sec")

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

    # 1. System Detection Info
    st.info(f"Machine: {machine} | Spindle: {m_taper} | Material: {material}")

    # 2. Filtering Logic (Finds tools based on machine taper and finish requirements)
    suitable_tools = [
        tool for tool in face_mill_data_aluminium 
        if m_taper in tool["spindles"] and tool.get("ra", 3.2) <= ra_input
    ]

    if not suitable_tools:
        st.error(f"No suitable Face Mills found for {m_taper} with Ra {ra_input}.")
        st.stop()

    # 3. Shape & Selection Mode
    shape = st.selectbox("Component Shape", ["Rectangular", "Circular"], key="fm_shape_sel")
    tool_mode = st.selectbox("Tool Selection Mode", ["Auto", "Manual"], key="fm_mode_sel")

    # 4. Tool Selection Logic
    # We use a default width for the Auto-filter until the user enters their actual size
    temp_W = 100.0 

    selected_tool = None
    if tool_mode == "Auto":
        for t in sorted(suitable_tools, key=lambda x: x['dia']):
            if t['max_width'] >= temp_W:
                selected_tool = t
                break
        if not selected_tool:
            selected_tool = max(suitable_tools, key=lambda x: x['dia'])
    else:
        tool_names = [f"Dia {t['dia']}mm" for t in suitable_tools]
        selected_tool_name = st.selectbox("Select Tool", tool_names, key="fm_tool_manual")
        selected_tool = next(t for t in suitable_tools if f"Dia {t['dia']}mm" == selected_tool_name)

    # 5. Final Calculations (Runs once a tool is picked)
    if selected_tool:
        tool_dia = selected_tool["dia"]
        ae = selected_tool["max_width"] 
        rpm = selected_tool["rpm"]
        vf = selected_tool["feed"]      
        ap_limit = selected_tool["stock"]

        # --- COMPONENT INPUTS ---
        st.divider()
        if shape == "Rectangular":
            L = st.number_input("Length (mm)", value=100.0, key="fm_L")
            W = st.number_input("Width (mm)", value=100.0, key="fm_W")
            long_dim = max(L, W)
        else:
            # Setting default to 150 to match your test case
            comp_dia = st.number_input("Component Diameter (mm)", value=150.0, key="fm_circ_dia")
            W = comp_dia  
            long_dim = comp_dia

        # --- POWER VALIDATION ---
        efficiency = 0.8
        req_power = (ae * ap_limit * vf * kc) / (60e6 * efficiency)
        st.metric("Required Power", f"{req_power:.2f} kW", delta=f"Limit: {m_power} kW", delta_color="inverse")

        if req_power > m_power:
            st.error(f"⚠️ Machine Overload! Required {req_power:.2f}kW exceeds limit.")
        else:
            st.success(f"✅ Tool: Ø{tool_dia}mm | RPM: {rpm} | Feed: {vf} mm/min")

        # --- PROCESS PARAMETERS ---
        total_stock = st.number_input("Total Stock to Remove (mm)", value=2.0, key="fm_total_stock")
        finish_required = ra_input < 1.6 
        rough_stock = total_stock - 0.5 if finish_required else total_stock
        passes = math.ceil(rough_stock / ap_limit) if ap_limit > 0 else 1

        # --- CALCULATE CUT LENGTH (TRAVEL DISTANCE) ---
        if shape == "Rectangular":
            width_passes = math.ceil(W / ae)
            cut_length = (long_dim + tool_dia + 4) * width_passes
        else:
            # MACHINIST REALISTIC CIRCULAR LOGIC (BASED ON YOUR AUTOCAD)
            if comp_dia <= ae:
                # If tool covers the whole part in one move
                cut_length = comp_dia + tool_dia + 10
                st.info(f"Using Ø{tool_dia}mm Tool: Single traverse.")
            else:
                # 1. Start with the outer spindle center diameter
                overhang = tool_dia - ae
                first_path_dia = (comp_dia - tool_dia) + (2 * overhang)
                
                current_path_dia = max(first_path_dia, 0)
                total_circ_dist = 0
                pass_count = 0
                
                # 2. Gap-Aware Loop: Checks if the tool edge crosses the center
                while True:
                    total_circ_dist += math.pi * current_path_dia
                    pass_count += 1
                    
                    # Inner Edge = (Current Path Center) - (Tool Radius)
                    # If this is > 0, there is still a "hole" or "island" in the middle
                    inner_edge_pos = (current_path_dia / 2) - (tool_dia / 2)
                    
                    # Break only if the tool overlaps the center point by 2mm
                    if inner_edge_pos <= -2: 
                        break
                    
                    # Step inward by double the engagement width (ae * 2)
                    current_path_dia -= (ae * 2)
                    
                    # Clamp to 0 if the math tries to go negative
                    if current_path_dia < 0:
                        current_path_dia = 0
                    
                    # Safety break to prevent infinite loops
                    if pass_count > 15: break

                # 3. Add Entry/Exit travel (Lead)
                cut_length = total_circ_dist + tool_dia
                st.success(f"Using Ø{tool_dia}mm Tool: {pass_count} Interpolation Rings calculated.")

        # --- FINAL CALCULATION AND BUTTON ---
        if st.button("Calculate Milling Time", key="fm_calc_btn"):
            time_min = (cut_length * passes) / vf
            if finish_required:
                # Add extra finish pass at slower feed
                time_min += (cut_length / (vf * 0.8))
            
            st.subheader("Final Estimates")
            col_a, col_b = st.columns(2)
            col_a.metric("Depth Passes", f"{passes}")
            col_b.metric("Total Time", f"{time_min * 60:.1f} sec")
