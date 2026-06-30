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

    "Ace MCV 400/450 HSK A63": {
        "make": "Ace MCV",
        "model": "400/450",
        "power": 5.5,
        "peak_power": 7.5,
        "torque": 26,
        "peak_torque": 35,
        "taper": "HSK A63",
        "rpm": 10000,
        "tool_change_time": 5,
        "position_time": 2,
        "max_tool_diameter": 75,
        "max_tool_weight": 8,
        "no_of_tools": 24
    },


    "Ace MCV High Torque 400/450 HSK A63": {
        "make": "Ace MCV High Torque",
        "model": "400/450",
        "power": 7.5,
        "peak_power": 9,
        "torque": 35,
        "peak_torque": 43,
        "taper": "HSK A63",
        "rpm": 10000,
        "tool_change_time": 5,
        "position_time": 2,
        "max_tool_diameter": 75,
        "max_tool_weight": 8,
        "no_of_tools": 24
    },


    "Brother Std S500/700 BT30": {
        "make": "Brother Std",
        "model": "S500/700",
        "power": 7,
        "peak_power": 10.1,
        "torque": 26.8,
        "peak_torque": 40,
        "taper": "BT30",
        "rpm": 10000,
        "tool_change_time": 1.8,
        "position_time": 1,
        "max_tool_diameter": 100,
        "max_tool_weight": 3,
        "no_of_tools": 21
    },


    "Brother High Torque S500/700 BT30": {
        "make": "Brother High Torque",
        "model": "S500/700",
        "power": 9.2,
        "peak_power": 12.8,
        "torque": 61.1,
        "peak_torque": 92,
        "taper": "BT30",
        "rpm": 10000,
        "tool_change_time": 1.8,
        "position_time": 1,
        "max_tool_diameter": 100,
        "max_tool_weight": 3,
        "no_of_tools": 21
    },


    "Fanuc Std DiB5 BT30": {
        "make": "Fanuc Std",
        "model": "DiB5 S/M/L",
        "power": 3.7,
        "peak_power": 11,
        "torque": 11.8,
        "peak_torque": 35,
        "taper": "BT30",
        "rpm": 10000,
        "tool_change_time": 1.8,
        "position_time": 1,
        "max_tool_diameter": 80,
        "max_tool_weight": 3,
        "no_of_tools": 21
    },


    "Fanuc High Torque DiB5 BT30": {
        "make": "Fanuc High Torque",
        "model": "DiB5 S/M/L",
        "power": 3.7,
        "peak_power": 11,
        "torque": 27.6,
        "peak_torque": 80,
        "taper": "BT30",
        "rpm": 10000,
        "tool_change_time": 1.8,
        "position_time": 1,
        "max_tool_diameter": 80,
        "max_tool_weight": 3,
        "no_of_tools": 21
    },


    "Makino Slim 3n/5n HSK A50": {
        "make": "Makino Slim",
        "model": "3n/5n",
        "power": 11,
        "peak_power": 18,
        "torque": 33,
        "peak_torque": 80,
        "taper": "HSK A50",
        "rpm": 10000,
        "tool_change_time": 3.3,
        "position_time": 1.2,
        "max_tool_diameter": 80,
        "max_tool_weight": 2.4,
        "no_of_tools": 26
    },


    "Makino PS65/105 HSK A63": {
        "make": "Makino PS",
        "model": "PS65/105",
        "power": 18.5,
        "peak_power": 30,
        "torque": 95,
        "peak_torque": 175,
        "taper": "HSK A63",
        "rpm": 10000,
        "tool_change_time": 3.6,
        "position_time": 1.2,
        "max_tool_diameter": 75,
        "max_tool_weight": 8,
        "no_of_tools": 30
    },


    "BFW Dhruva 4070 HSK A63": {
        "make": "BFW Dhruva",
        "model": "4070",
        "power": 7.5,
        "peak_power": 9,
        "torque": 47.5,
        "peak_torque": 95,
        "taper": "HSK A63",
        "rpm": 10000,
        "tool_change_time": 5,
        "position_time": 2,
        "max_tool_diameter": 90,
        "max_tool_weight": 4,
        "no_of_tools": 14
    }

}
def calculate_facemill_time(op):
    # Retrieve global parameters
    global tool_change_time, position_time, m_taper, m_power, kc, material
    # Ensure material is taken from operation if provided
    op_material = op.get("material", material)
    kc_val = kc_data.get(op_material, kc)
    fm_pos = op.get("fm_pos", 1)
    cut_length = 0.0
    rough_passes = 0
    time_rough = 0.0
    time_finish = 0.0
    total_time_min = 0.0
    
    # Fallback if material tables missing or no face_mill entry
    if op_material not in material_tables or "face_mill" not in material_tables[op_material]:
        travel_time_per_pos = 5.0
        total_time = tool_change_time + (travel_time_per_pos * fm_pos) + max(fm_pos - 1, 0) * position_time
        return total_time

    face_table = material_tables[op_material]["face_mill"]
    # Filter tools that fit the spindle taper
    suitable_tools = [tool for tool in face_table if m_taper in tool["spindles"]]
    if not suitable_tools:
        st.error(f"No suitable Face Mills found for {m_taper} spindle.")
        st.stop()

    shape = op.get("shape", "Rectangular")
    ra_input = op.get("ra", 3.2)
    total_stock = op.get("stock", 1.0)

    # Determine target diameter
    if shape == "Rectangular":
        L = op.get("length", 100.0)
        W = op.get("width", 40.0)
        L_val = max(L, W)
        W_val = min(L, W)
        target_dia = W_val / 0.7
    else:
        comp_dia = op.get("dia", 100.0)
        target_dia = (comp_dia / 2) / 0.7

    # Select the tool using Auto mode logic
    selected_tool = None
    possible_tools = sorted(suitable_tools, key=lambda x: x['dia'])
    for t in possible_tools:
        if t['dia'] >= target_dia:
            ae_check = t['max_width']
            ap_check = t['stock']
            vf_check = t['feed']
            efficiency = 0.8
            req_power = (ae_check * ap_check * vf_check * kc_val) / (60e6 * efficiency)
            if req_power <= m_power:
                selected_tool = t
                break
    if not selected_tool:
        selected_tool = max(possible_tools, key=lambda x: x['dia']) if possible_tools else None

    if not selected_tool:
        st.error("No suitable Face Mill selected.")
        st.stop()

    tool_dia = selected_tool["dia"]
    ae = selected_tool["max_width"]
    rpm = selected_tool["rpm"]
    vf = selected_tool["feed"]

    # Material-specific speed/feed corrections
    if op_material == "Steel_Hardness_30_to_40_HRC":
        rpm *= 0.90
        vf *= 0.95
    elif op_material == "Stainless_Steel":
        rpm *= 0.80
        vf *= 0.90
    
    ap_limit = selected_tool["stock"]

    # Finish pass parameters
    if op_material == "Aluminium":
        is_pcd_required = 0.8 <= ra_input < 2.0
    else:
        is_pcd_required = False

    if is_pcd_required:
        finish_rpm = rpm * 1.10
        finish_vf = vf * 0.90
    elif op_material != "Aluminium" and 0.8 <= ra_input < 2.0:
        finish_rpm = rpm
        finish_vf = vf * 0.80
    else:
        finish_rpm = rpm
        finish_vf = vf

    # Rough/finish pass strategy
    if ra_input < 0.8:
        rough_stock = max(0.0, total_stock - 0.5)
        rough_passes = math.ceil(rough_stock / ap_limit) if rough_stock > 0 else 0
    elif is_pcd_required:
        rough_stock = max(0.0, total_stock - 0.5)
        rough_passes = math.ceil(rough_stock / ap_limit) if rough_stock > 0 else 0
    else:
        finish_required = ra_input < 2.0
        if finish_required and total_stock > 0.5:
            rough_stock = total_stock - 0.5
            rough_passes = math.ceil(rough_stock / ap_limit)
        else:
            rough_stock = total_stock
            rough_passes = math.ceil(rough_stock / ap_limit) if ap_limit > 0 else 1

    # Cut length calculation
    if shape == "Rectangular":
        width_passes = math.ceil(W_val / ae)
        cut_length = (L_val + tool_dia + 4) * width_passes
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

    # Time calculations (in minutes first, then converted to seconds)
    time_rough = (cut_length * rough_passes) / vf  
    time_finish = 0.0
    if total_stock > 0.5:
        if ra_input < 0.8 or ra_input < 2.0:
            time_finish = cut_length / finish_vf
    total_time_min = time_rough + time_finish        
    cut_time = total_time_min * 60 * fm_pos
    total_time = tool_change_time + cut_time + max(fm_pos - 1, 0) * position_time
    finish_passes = 1 if (total_stock > 0.5 and (ra_input < 0.8 or ra_input < 2.0)) else 0
    if ra_input < 0.8:
        finish_type = "Special Process"
    elif is_pcd_required:
        finish_type = "PCD Finish"
    elif op_material != "Aluminium" and 0.8 <= ra_input < 2.0:
        finish_type = "Wiper Finish"
    else:
        finish_type = "None"
        finish_passes = 0
    
    return {
        "time": total_time,
        "tool_dia": tool_dia,
        "rpm": round(rpm),
        "feed": round(vf),
        "rough_passes": rough_passes,
        "finish_passes": finish_passes,
        "time_rough_sec": round(time_rough * 60, 1),
        "time_finish_sec": round(time_finish * 60, 1),
        "finish_type": finish_type,
        "cut_length": round(cut_length, 1)
    }

def calculate_tapping_time(op):
    """Calculate tapping cycle time (Tap or Threadmill) based on selected parameters."""
    global tool_change_time, position_time, material
    op_material = op.get("material", material)
    
    # 1. Base tap parameters
    tap_table = material_tables[op_material]["tap"]
    filtered = [row for row in tap_table if row["pitch"] == op["t_pitch"]]
    selected_row = next(row for row in filtered if row["tap"] == op["t_size"])
    diameter = get_diameter(op["t_size"])
    pitch = op["t_pitch"]
    # DRILL TIME CALCULATION
    drill_dia = diameter - pitch  # tap dia minus pitch = drill dia
    d_rpm, d_fmin, d_max_depth = get_parameters(drill_dia, op_material)
    # Check drill depth against table
    if d_max_depth and op["t_ddep"] > d_max_depth:
        st.warning(
            f"⚠️ Drill depth {op['t_ddep']}mm exceeds table recommendation "
            f"of {d_max_depth}mm for Ø{round(drill_dia,2)}mm drill. "
            f"Use extended drill or check feasibility."
        )
        return {
            "time": 0.0,
            "process": "Error — Drill Depth Exceeded",
            "tool_dia": 0,
            "rpm": 0,
            "feed": 0,
            "cut_time": 0,
            "drill_dia": 0,
            "drill_rpm": 0,
            "drill_feed": 0,
            "drill_cut_time": 0
        }
    
    if d_rpm and d_fmin:
        drill_travel = op["t_ddep"] + 3 + ((0.18 * drill_dia) if drill_dia <= 20 else 0)
        drill_cut_time = (drill_travel / d_fmin) * 60  # per position only
        drill_total_time = drill_cut_time * op["t_cnt"]
    else:
        drill_cut_time = 0.0
        drill_total_time = 0.0
        drill_dia = 0.0
        d_rpm = 0
        d_fmin = 0
    
    # 2. Check for Threadmilling recommendation (Blind hole & Clearance <= 2 * pitch)
    use_threadmill = False
    if op.get("t_ht", "Blind Hole") == "Blind Hole":
        
        t_ddep = op.get("t_ddep", 30.0)
        t_tdep = op.get("t_tdep", 25.0)
        
        clearance = t_ddep - t_tdep
        if clearance < (1 * pitch):
            st.warning(
                f"⚠️ Drill depth ({t_ddep}mm) must be at least tap depth + 1 pitch ({t_tdep + pitch}mm). "
                f"Please check drill depth."
            )
            return {
                "time": 0.0,
                "process": "Error — Check Drill Depth",
                "tool_dia": 0,
                "rpm": 0,
                "feed": 0,
                "cut_time": 0,
                "drill_dia": 0,
                "drill_rpm": 0,
                "drill_feed": 0,
                "drill_cut_time": 0
            }
        elif clearance <= (2 * pitch):
            use_threadmill = True

    # 3. Calculate time based on strategy
    if use_threadmill:
        threadmill_table = material_tables[op_material]["threadmill"]
        minor_dia = diameter - (1.0825 * pitch)
        
        pitch_matches = [row for row in threadmill_table if row["pitch"] == pitch]
        depth_matches = [row for row in pitch_matches if row["max_depth"] >= op["t_tdep"]]
        size_matches = [row for row in depth_matches if row["tool_dia"] < minor_dia]
        
        tm_row = None
        if size_matches:
            tm_row = max(size_matches, key=lambda x: x["tool_dia"])
        if not tm_row:
            st.warning(
                f"⚠️ No standard threadmill available for {op['t_size']} "
                f"pitch {op['t_pitch']} at depth {op['t_tdep']}mm. "
                f"Special threadmill required — calculate separately."
            )
            return {
                "time": 0.0,
                "process": "Special Threadmill Required",
                "tool_dia": 0,
                "rpm": 0,
                "feed": 0,
                "cut_time": 0,
                "drill_dia": round(drill_dia, 2),      # ← ADD
                "drill_rpm": round(d_rpm) if d_rpm else 0,   # ← ADD
                "drill_feed": round(d_fmin) if d_fmin else 0,  # ← ADD
                "drill_cut_time": round(drill_cut_time, 2)    # ← ADD
            }
            
        if tm_row:
            vc_tm = tm_row["vc"]
            feed_rev = tm_row["feed_rev"]
            if op_material == "Steel_Hardness_30_to_40_HRC":
                vc_tm *= 0.90
                feed_rev *= 0.95
            elif op_material == "Stainless_Steel":
                vc_tm *= 0.80
                feed_rev *= 0.90
            tool_dia = tm_row["tool_dia"]
            
            rpm_tm = (1000 * vc_tm) / (math.pi * tool_dia)
            feed_tm = feed_rev * rpm_tm
            tm_cut_length = ((diameter - tool_dia) * math.pi * 3) + op["t_tdep"] + 4
            cut_time = (tm_cut_length / feed_tm) * 60  # per position only
            total_time = cut_time * op["t_cnt"]
            return {
                "time": total_time + drill_total_time,
                "process": "Threadmill",
                "tool_dia": tool_dia,
                "rpm": round(rpm_tm),
                "feed": round(feed_tm, 1),
                "cut_time": round(cut_time, 2),
                "drill_dia": round(drill_dia, 2),
                "drill_rpm": round(d_rpm) if d_rpm else 0,
                "drill_feed": round(d_fmin) if d_fmin else 0,
                "drill_cut_time": round(drill_cut_time, 2)
            }

    # Standard Tapping
    vc = selected_row["vc"]
    if op_material == "Steel_Hardness_30_to_40_HRC":
        vc *= 0.90
    elif op_material == "Stainless_Steel":
        vc *= 0.80
    rpm = (1000 * vc) / (math.pi * diameter)
    feed_min = pitch * rpm
    cut_length = (op["t_tdep"] + (pitch * 3)) * 2 + 4
    # Check tap depth against table
    if op["t_tdep"] > selected_row.get("max_depth", 999):
        st.warning(
            f"⚠️ Tap depth {op['t_tdep']}mm exceeds table recommendation "
            f"of {selected_row.get('max_depth')}mm for {op['t_size']}. "
            f"Use extended tap or check feasibility."
        )
        return {
            "time": 0.0,
            "process": "Error — Tap Depth Exceeded",
            "tool_dia": diameter,
            "rpm": 0,
            "feed": 0,
            "cut_time": 0,
            "drill_dia": round(drill_dia, 2),
            "drill_rpm": round(d_rpm) if d_rpm else 0,
            "drill_feed": round(d_fmin) if d_fmin else 0,
            "drill_cut_time": round(drill_cut_time, 2)
        }

    cut_time = (cut_length / feed_min) * 60  # per position only
    total_time = cut_time * op["t_cnt"]
    return {
        "time": total_time + drill_total_time,
        "process": "Tapping",
        "tool_dia": diameter,
        "rpm": round(rpm),
        "feed": round(feed_min, 1),
        "cut_time": round(cut_time, 2),
        "drill_dia": round(drill_dia, 2),
        "drill_rpm": round(d_rpm) if d_rpm else 0,
        "drill_feed": round(d_fmin) if d_fmin else 0,
        "drill_cut_time": round(drill_cut_time, 2)
    }

drill_data_aluminium = [
            {"min_d": 0.5, "max_d": 1, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
            {"min_d": 1, "max_d": 3, "rpm": 6500, "feed_min": 100, "max_depth": 5},

            {"min_d": 3, "max_d": 5, "vc": 50, "feed_min": 450, "max_depth": 20},
            {"min_d": 5, "max_d": 8, "vc": 80, "feed_min": 550, "max_depth": 30},
            {"min_d": 8, "max_d": 10, "vc": 100, "feed_min": 480, "max_depth": 40},
            {"min_d": 10, "max_d": 12, "vc": 120, "feed_min": 550, "max_depth": 60},
            {"min_d": 12, "max_d": 15, "vc": 120, "feed_min": 550, "max_depth": 75},
            {"min_d": 15, "max_d": 16, "rpm": 2464, "feed_min": 444, "max_depth": 80},
            {"min_d": 16, "max_d": 17, "rpm": 2508, "feed_min": 451, "max_depth": 85},
            {"min_d": 17, "max_d": 18, "rpm": 2364, "feed_min": 426, "max_depth": 90},
            {"min_d": 18, "max_d": 19, "rpm": 2409, "feed_min": 482, "max_depth": 95},
            {"min_d": 19, "max_d": 20, "rpm": 2448, "feed_min": 490, "max_depth": 100},

            {"min_d": 20, "max_d": 21, "rpm": 2484, "feed_min": 248, "max_depth": 80},
            {"min_d": 21, "max_d": 22, "rpm": 2369, "feed_min": 237, "max_depth": 80},
            {"min_d": 22, "max_d": 23, "rpm": 2263, "feed_min": 226, "max_depth": 80},
            {"min_d": 23, "max_d": 24, "rpm": 2167, "feed_min": 238, "max_depth": 100},

            {"min_d": 24, "max_d": 25, "rpm": 2338, "feed_min": 234, "max_depth": 100},
            {"min_d": 25, "max_d": 26, "rpm": 2371, "feed_min": 249, "max_depth": 100},
            {"min_d": 26, "max_d": 27, "rpm": 2402, "feed_min": 240, "max_depth": 100},
            {"min_d": 27, "max_d": 28, "rpm": 2315, "feed_min": 232, "max_depth": 100},
            {"min_d": 28, "max_d": 29, "rpm": 2233, "feed_min": 223, "max_depth": 100},
            {"min_d": 29, "max_d": 30, "rpm": 2158, "feed_min": 216, "max_depth": 100},
            {"min_d": 30, "max_d": 35, "vc": 150, "feed_min": 159, "max_depth": 100},
            {"min_d": 35, "max_d": 45, "vc": 170, "feed_min": 155, "max_depth": 100},
            {"min_d": 45, "max_d": 55, "vc": 180, "feed_min": 127, "max_depth": 100},
            {"min_d": 55, "max_d": 65, "vc": 180, "feed_min": 115, "max_depth": 100},
]

drill_data_Steel_Hardness_upto_30_HRC = [
            {"min_d": 0.5, "max_d": 1, "rpm": 8500, "feed_min": 60, "max_depth": 2.5},
            {"min_d": 1, "max_d": 2, "rpm": 6365, "feed_min": 95, "max_depth": 5},
            {"min_d": 2, "max_d": 3, "rpm": 5570, "feed_min": 167, "max_depth": 10},

            {"min_d": 3, "max_d": 4, "vc": 40, "feed_min": 297, "max_depth": 15},
            {"min_d": 4, "max_d": 5, "vc": 45, "feed_min": 301, "max_depth": 24},
            {"min_d": 5, "max_d": 6, "vc": 45, "feed_min": 301, "max_depth": 30},  
            {"min_d": 6, "max_d": 8, "vc": 50, "feed_min": 301, "max_depth": 36},
            {"min_d": 8, "max_d": 10, "vc": 60, "feed_min": 334, "max_depth": 50},
            {"min_d": 10, "max_d": 12, "vc": 60, "feed_min": 306, "max_depth": 55},
            {"min_d": 12, "max_d": 14, "vc": 60, "feed_min": 255, "max_depth": 60},

            {"min_d": 14, "max_d": 16, "rpm": 1478, "feed_min": 259, "max_depth": 72},
            {"min_d": 16, "max_d": 18, "rpm": 1293, "feed_min": 233, "max_depth": 80},
            {"min_d": 18, "max_d": 21, "rpm": 1238, "feed_min": 248, "max_depth": 90},
            {"min_d": 21, "max_d": 27, "rpm": 1364, "feed_min": 205, "max_depth": 100},
            {"min_d": 27, "max_d": 32, "rpm": 1061, "feed_min": 127, "max_depth": 100},

            {"min_d": 32, "max_d": 45, "vc": 90, "feed_min": 107, "max_depth": 105},
            {"min_d": 45, "max_d": 51, "vc": 100, "feed_min": 106, "max_depth": 100},
            {"min_d": 51, "max_d": 65, "vc": 100, "feed_min": 94, "max_depth": 100},
           
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
tool_change_time = machine_data[machine]["tool_change_time"]

position_time = machine_data[machine]["position_time"]

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

def calculate_hole_feature(op, material):

    dia = op["dia"]
    depth = op["depth"]
    tol = op["tol"]
    ra = op["ra"]
    mode = op["start_mode"]
    count = op["count"]
    tool_times = []
    
    # --------------------------------
    # CASE 1 : SOLID + LOOSE TOL + ROUGH FINISH
    # DRILL ONLY
    # --------------------------------
       
    if (
        mode == "Solid"
        and (
            (dia <= 15 and tol >= 0.1 and ra >= 2.4) or
            (dia > 15 and tol >= 0.2 and ra > 3.2)
        )
    ):
    
        drill_result = calculate_drilling_feature(
            dia,
            depth,
            count,
            material,
            op["hole_type"]
        )
        tool_times.append(drill_result["time"])
    
    
        drilled_dia = drill_result.get(
            "drill_dia",
            0
        )
    
      
        if drilled_dia >= dia:
      
            return {
                "time": drill_result["time"],
                "tools": drill_result["tools"],
                "steps": drill_result["steps"],
                "tool_rows": drill_result.get("tool_rows", [])
            }
        
        
        elif drilled_dia > 0:
        
            bore_result = calculate_boring_operation(
                f_dia=dia,
                b_dep=depth,
                bor_ht=op["hole_type"],
                e_mode="Core Hole",
                bor_cnt=count,
                tol_input=tol,
                ra_input=ra,
                material=material,
                core_dia=drilled_dia
            )   
            tool_times.append(bore_result["time"])
            
            return {
                "time": drill_result["time"] + bore_result["time"],
                "tools": drill_result["tools"] + bore_result["tools"],
                "steps": drill_result["steps"] + bore_result["steps"],
                "tool_rows": drill_result.get("tool_rows", []) + bore_result.get("tool_rows", [])    # ← combine both tool_rows
            }  
            
    
    # --------------------------------
    # CASE 2 : ALL OTHER HOLES
    # USE BORING LOGIC
    # --------------------------------
    
    else:
    
        return calculate_boring_operation(
            f_dia=dia,
            b_dep=depth,
            bor_ht=op["hole_type"],
            e_mode=mode,
            bor_cnt=count,
            tol_input=tol,
            ra_input=ra,
            material=material,
            core_dia=op.get("core_dia",0)
        )
    

def calculate_drilling_feature(
    dia,
    depth,
    count,
    material,
    hole_type
):

    drill_data = material_tables[material]["drill"]

    sorted_drills = sorted(
        drill_data,
        key=lambda x: x["max_d"],
        reverse=True
    )


    safe_drill_dia = 0


    for drill in sorted_drills:


        actual_dia = min(
            drill["max_d"] - 0.01,
            dia
        )

        actual_dia = round(actual_dia,2)


        if (
            actual_dia < drill["min_d"]
            or actual_dia >= drill["max_d"]
        ):
            continue


        d_params = get_parameters(
            actual_dia,
            material
        )


        if (
            d_params[0] is None
            or d_params[1] is None
        ):
            continue


        rpm = d_params[0]
        f_min = d_params[1]
        max_depth = d_params[2]  # ← get max_depth from table
        # Check depth against table max_depth
        if max_depth and depth > max_depth:
            continue  # skip this drill, depth exceeds table recommendation

        # power calculation
        p_req = (
            (
            (f_min/rpm)
            *
            (math.pi*actual_dia*rpm/1000)
            *
            actual_dia
            *
            kc
            )
            /192000
        )


        torque_req = (
            p_req * 9550
        ) / rpm



        if (
            p_req <= usable_power
            and torque_req <= usable_torque
        ):

            safe_drill_dia = actual_dia
            break


    if safe_drill_dia == 0:

        return {
    
            "time":0,
    
            "tools":0,
    
            "steps":[
                "No suitable drill found"
            ],
    
            "tool_rows": []
        }



    travel = (
        depth + 3
        if hole_type=="Blind Hole"
        else depth + 6
    )


    cut_time = (
        travel / f_min
    ) * 60 



    return {
        "time":cut_time,
        
        "tools":1,
        
        "drill_dia":safe_drill_dia,
        
        "steps":[
            f"Drill Ø{safe_drill_dia} | "
            f"Power {round(p_req,2)}kW | "
            f"Torque {round(torque_req,1)}Nm"
        ],
        "tool_rows": [{
            "operation": "Hole Drill",
            "tool_detail": f"Drill Ø{safe_drill_dia}mm",
            "machining_stock": "Solid",
            "vc": round((math.pi * safe_drill_dia * rpm) / 1000, 1),
            "rpm": round(rpm),
            "feed_rev": round(f_min / rpm, 3),
            "table_feed": round(f_min),
            "safety_length": 6 if hole_type == "Through Hole" else 3,
            "cut_length": round(depth, 1),
            "cut_time": round(cut_time, 2)
        }]

    }


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
    tool_rows = [] 
    current_dia = 0.0

    if e_mode == "Core Hole":
        current_dia = core_dia

    tol_band = tol_input * 2
    drill_only = (
        tol_band >= 0.4 and
        ra_input > 3.2
    )
    fine_boring_required = (
        tol_band < 0.2 or
        ra_input <= 1.6
    )
    if drill_only:
        fine_boring_required = False
        
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
    if fine_boring_required and rough_target_dia == current_dia:
        step_details.append(
            "Direct Fine Boring (No Rough Pass)"
        )

    # ==========================================
    # DEPTH VALIDATION
    # ==========================================
    if b_dep > 80 and not drill_only:
        st.error(
            f"Depth {b_dep}mm exceeds validated boring limit of 80mm."
        )
        st.warning(
            "Check tool weight, machine spindle capability, "
            "fixture rigidity and process feasibility manually."
        )
        return {
            "time": 0.0,
            "tools": 0,
            "steps": [f"Depth {b_dep}mm exceeds 80mm boring limit"],
            "tool_rows": []
        }
    
    # ==========================================
    # L/D VALIDATION
    # ==========================================
    ld_ratio = b_dep / f_dia
    if ld_ratio > 5 and not drill_only:
        st.error(
            f"L/D Ratio = {round(ld_ratio,1)} exceeds recommended limit of 5."
        )
        st.warning(
            "Check boring bar rigidity, machine capability "
            "and fixture stability."
        )
        return {
            "time": 0.0,
            "tools": 0,
            "steps": [f"L/D ratio {round(ld_ratio,1)} exceeds limit of 5"],
            "tool_rows": []
        }

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

    if f_dia <= 5:
        drill_stock = 0.5
    elif f_dia <= 10:
        drill_stock = 0.7
    else:
        drill_stock = 1.0

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
                        * (math.pi * actual_dia * d_rpm / 1000)
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
            d_time = ((d_travel / d_fmin) * 60) 

            # Add reposition time for each additional hole
            d_time = (
                (d_travel / d_fmin)
                * 60
            )
                
            total_time_sec += d_time
            
            step_details.append(f"Drill Ø{safe_drill_dia}")
            
            st.success(
                f"Step 1: Drilling Ø{safe_drill_dia} | "
                f"Power: {round(p_check,2)}kW | "
                f"Time: {round(d_time, 2)}s"
            )
            tool_rows.append({                          # ← ADD FROM HERE
                "operation": "Hole Drill",
                 "tool_detail": f"Drill Ø{safe_drill_dia}mm",
                "machining_stock": "Solid",
                "vc": round((math.pi * safe_drill_dia * d_rpm) / 1000, 1),
                "rpm": round(d_rpm),
                "feed_rev": round(d_fmin / d_rpm, 3),
                "table_feed": round(d_fmin),
                "safety_length": 6 if bor_ht == "Through Hole" else 3,
                "cut_length": round(b_dep, 1),
                "cut_time": round(d_time, 2)
            })                          
            current_dia = safe_drill_dia  # 👈 Line 712: Must have exactly 12 spaces before it
            
        else:
            st.error(f"❌ No suitable drill found for Ø{rough_target_dia:.1f} based on available machine capacity.")
            st.stop()            
    else:  # 👈 This else matches your original "if e_mode == 'Solid':" block
        current_dia = float(core_dia)  # 👈 Properly indented inside the else block

    # --- 4. STEP 2: ROUGH BORING (Stock-Aware Multi-Pass) ---
    if not drill_only:
        st.info(f"Step 2: Boring Sequence to Ø{rough_target_dia}")
        bor_travel = b_dep + (3 if bor_ht == "Blind Hole" else 6)
    
    while current_dia < rough_target_dia:
        tool = get_boring_params(current_dia, material)
        if not tool:
            st.warning(f"No boring data found for Ø{current_dia}.")
            break
        tool_count_bor += 1

        # Max stock increment from table
        max_dia_increment = tool['ap']
        d2 = round(min(
            rough_target_dia,
            current_dia + max_dia_increment
        ), 3)

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
        tool_rows.append({
            "operation": f"Rough Bore Ø{current_dia}→Ø{d2}",
            "tool_detail": f"Boring Bar Ø{d2}mm",
            "machining_stock": round(d2 - current_dia, 3),
            "vc": round((math.pi * d2 * tool['rpm']) / 1000, 1),
            "rpm": round(tool['rpm']),
            "feed_rev": round(tool['feed_min'] / tool['rpm'], 3),
            "table_feed": round(tool['feed_min']),
            "safety_length": 6 if bor_ht == "Through Hole" else 3,
            "cut_length": round(b_dep, 1),
            "cut_time": round(p_time, 2)
        })
        current_dia = round(d2, 3)

  
    # ==========================================
    # STEP 3 : FINAL BORING PASS
    # ==========================================
    if not drill_only and fine_boring_required:
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
            tool_rows.append({
                "operation": f"Fine Bore Ø{current_dia}→Ø{f_dia}",
                "tool_detail": f"Fine Boring Bar Ø{f_dia}mm",
                "machining_stock": round(finish_stock, 3),
                "vc": round((math.pi * f_dia * finish_rpm) / 1000, 1),
                "rpm": round(finish_rpm),
                "feed_rev": round(finish_feed_rev, 3),
                "table_feed": round(finish_feed, 1),
                "safety_length": 6 if bor_ht == "Through Hole" else 3,
                "cut_length": round(b_dep, 1),
                "cut_time": round(finish_time, 2)
            })
            step_details.append(
                f"Fine Bore Ø{current_dia} ➔ Ø{f_dia}"
            )
            st.success(
                f"Step 3: Fine Boring Ø{current_dia} ➔ Ø{f_dia} | "
                f"RPM: {round(finish_rpm)} | "
                f"Feed: {round(finish_feed,1)} mm/min | "    # ← fixed
                f"Time: {round(finish_time,1)}s"
            )
        else:
            st.error(
                "Fine boring data not available for this diameter/material."
            )

    return {    # ← fixed, 4 spaces
        "time": total_time_sec,
        "tools": tool_count_bor,
        "steps": step_details,
        "tool_rows": tool_rows 
    }
    
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
            cut_time = (actual_travel / f_min) * 60 
            total_op_time = cut_time
    
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
    # CORE HOLE HANDLING
    # ==========================================
    if e_mode == "Core Hole":
        core_dia = float(
            st.number_input(
                "Core Hole Diameter (mm)",
                value=max(5.0, f_dia - 3),
                step=0.1,
                key="bor_core_in"
            )
        )
    else:
        core_dia = 0.0

    if st.button("Calculate Boring Plan", key="bor_calc_btn"):
        results = calculate_boring_operation(
            f_dia=f_dia,
            b_dep=b_dep,
            bor_ht=bor_ht,
            e_mode=e_mode,
            bor_cnt=bor_cnt,
            tol_input=tol_input,
            ra_input=ra_input,
            material=material,
            core_dia=core_dia
        )
        st.divider()
        st.write(f"Total Time: {round(results['time'], 2)}s")
        st.write(f"Total Tools: {results['tools']}")
        for step in results['steps']:
            st.write(f"🔹 {step}")

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

if "summary_data" not in st.session_state:
    st.session_state.summary_data = []

if "tool_master" not in st.session_state:
    st.session_state.tool_master = {}

if "tool_counter" not in st.session_state:
    st.session_state.tool_counter = 1

def get_tool_no(tool_name):
    if tool_name not in st.session_state.tool_master:
        st.session_state.tool_master[tool_name] = st.session_state.tool_counter
        st.session_state.tool_counter += 1

    return st.session_state.tool_master[tool_name]
    
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
            tap_table = material_tables[material]["tap"]
            pitch_list = sorted(list(set(row["pitch"] for row in tap_table)))
            t_pitch = st.selectbox("Pitch (mm)", pitch_list, key=f"t_pitch_{i}")
            
            filtered = [row for row in tap_table if row["pitch"] == t_pitch]
            tap_options = sorted(list(set(row["tap"] for row in filtered)))
            t_size = st.selectbox("Tap Size", tap_options, key=f"t_size_{i}")
            
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

if st.button("🚀 Calculate Combined Cycle Time"):  
    total_combined_time = 0.0
    # 1. Clear previous results to prevent stacking duplicates
    st.session_state.combined_results = []
    st.session_state.summary_data = []
    st.session_state.tool_master = {}
    st.session_state.tool_counter = 1
    st.session_state.summary_tool_counter = 1
    
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
            
                            
                result = calculate_hole_feature(
                    op,
                    material
                )
                
                            
                op_time = result["time"]
                tool_count_bor = result["tools"]

                details = " | ".join(result["steps"])
                op["tool_count"] = tool_count_bor   
            
                # ==============================
                # TOOL CHANGE + POSITION TIME
                # ==============================
            
                tools_used = result["tools"]
            
                tool_change_total = (
                    tools_used * tool_change_time
                )
            
            
                position_total = (
                    (op["count"] - 1)
                    *
                    position_time
                    *
                    tools_used
                )
            
            
                # CUTTING TIME FOR ALL POSITIONS
                cut_time_total = (
                    op_time * op["count"]
                )
                
                
                # TOOL CHANGE FOR EACH TOOL
                tool_change_total = (
                    tools_used * tool_change_time
                )
                
                
                # POSITION MOVEMENT BETWEEN POSITIONS
                position_total = (
                    (op["count"] - 1)
                    *
                    position_time
                    *
                    tools_used
                )
                
                
                op_time = (
                    cut_time_total
                    +
                    tool_change_total
                    +
                    position_total
                )
                
                
                st.write("BEFORE ADDING TOTAL")
                st.write("Result time =", result["time"])
                st.write("Count =", op["count"])
                st.write("Final op time =", op_time)
                
                total_combined_time += op_time
      
                
            # ---- FACE MILL LOGIC PROCESSING ----
            elif op["type"] == "Face Mill":
                fm_result = calculate_facemill_time(op)
                op_time = fm_result["time"]
                details = (
                    f"Ø{fm_result['tool_dia']}mm cutter | "
                    f"RPM: {fm_result['rpm']} | "
                    f"Feed: {fm_result['feed']} mm/min | "
                    f"{fm_result['rough_passes']} rough pass(es) | "
                    f"Rough: {fm_result['time_rough_sec']}s | "
                    f"Finish: {fm_result['time_finish_sec']}s | "
                    f"{fm_result['finish_type']}"
                )


            # ---- TAP LOGIC PROCESSING ----
            elif op["type"] == "Tap":
            
                tap_result = calculate_tapping_time(op)
            
                # Drill + Tap cutting time already included
                op_time = tap_result["time"]
            
                # Two tools used:
                # 1. Drill
                # 2. Tap
            
                tap_tools_used = 2
            
                tap_tool_change = (
                    tap_tools_used * tool_change_time
                )
            
                tap_position_time = (
                    (op["t_cnt"] - 1)
                    *
                    position_time
                    *
                    tap_tools_used
                )
            
                op_time = (
                    op_time
                    +
                    tap_tool_change
                    +
                    tap_position_time
                )
            
            
                details = (
                    f"Drill Ø{tap_result['drill_dia']}mm | "
                    f"Drill RPM: {tap_result['drill_rpm']} | "
                    f"Drill Feed: {tap_result['drill_feed']} mm/min | "
                    f"Drill Time: {tap_result['drill_cut_time']}s\n"
                    f"{tap_result['process']} Ø{tap_result['tool_dia']}mm | "
                    f"RPM: {tap_result['rpm']} | "
                    f"Feed: {tap_result['feed']} mm/min | "
                    f"Cut Time: {tap_result['cut_time']}s"
                )
            st.session_state.combined_results.append({
                "op_num": i + 1,
                "type": op["type"],
                "details": details,
                "cycle_time": op_time
            })
            # ==============================
            # SIMPLE SUMMARY COLLECTION
            # ==============================

            if op["type"] == "Hole":
                for row in result["tool_rows"]:
                   
                    st.session_state.summary_data.append({
                        "Tool No": len(st.session_state.summary_data) + 1,
                        "Operation": row["operation"],
                        "Tool Details": row["tool_detail"],
                        "Machining Stock": row.get("machining_stock", "-"),
                        "Vc (m/min)": row.get("vc", "-"),
                        "RPM": row["rpm"],
                        "Feed/rev (mm)": row.get("feed_rev", "-"),
                        "Table Feed (mm/min)": row.get("table_feed", "-"),
                        "Safety Length (mm)": row.get("safety_length", "-"),
                        "Cut Length (mm)": row.get("cut_length", "-"),
                        "Cut Time (sec)": row["cut_time"],
                        "No of Positions": op.get("count", 1),
                        "Position Time (sec)": position_time,
                        "Tool Change (sec)": tool_change_time,                            
                        "Total Time (sec)": 0 if row["cut_time"] == 0 else round((row["cut_time"] * op.get("count", 1)) + tool_change_time + (op.get("count", 1) - 1) * position_time, 2)
                    })
                

            elif op["type"] == "Tap":
                # Drill row
                drill_dia_tap = tap_result['drill_dia']
                st.session_state.summary_data.append({
                    "Tool No": len(st.session_state.summary_data) + 1,
                    "Operation": "Tap Drill",
                    "Tool Details": f"Drill Ø{drill_dia_tap}mm",
                    "Machining Stock": "Solid",
                    "Vc (m/min)": round((math.pi * drill_dia_tap * tap_result['drill_rpm']) / 1000, 1),
                    "RPM": tap_result['drill_rpm'],
                    "Feed/rev (mm)": round(tap_result['drill_feed'] / tap_result['drill_rpm'], 3) if tap_result['drill_rpm'] > 0 else "-",
                    "Table Feed (mm/min)": tap_result['drill_feed'],
                    "Safety Length (mm)": 6 if op.get("t_ht") == "Through Hole" else 3,
                    "Cut Length (mm)": round(op.get("t_ddep", 0), 1),
                    "Cut Time (sec)": round(tap_result['drill_cut_time'], 2),
                    "No of Positions": op.get("t_cnt", 1),
                    "Position Time (sec)": position_time,
                    "Tool Change (sec)": tool_change_time,
                    "Total Time (sec)": 0 if tap_result['drill_cut_time'] == 0 else round((tap_result['drill_cut_time'] * op.get("t_cnt", 1)) + tool_change_time + (op.get("t_cnt", 1) - 1) * position_time, 2)
                })
                # Tap/Threadmill row
                tap_dia = tap_result['tool_dia']
                st.session_state.summary_data.append({
                    "Tool No": len(st.session_state.summary_data) + 1,
                    "Operation": tap_result['process'],
                    "Tool Details": f"{tap_result['process']} Ø{tap_dia}mm",
                    "Machining Stock": round(op.get("t_pitch", 0), 2),
                    "Vc (m/min)": round((math.pi * tap_dia * tap_result['rpm']) / 1000, 1),
                    "RPM": tap_result['rpm'],
                    "Feed/rev (mm)": round(op.get("t_pitch", 0), 2),
                    "Table Feed (mm/min)": tap_result['feed'],
                    "Safety Length (mm)": round((3 * 2 * op.get("t_pitch", 0)) + 4, 1),
                    "Cut Length (mm)": round(op.get("t_tdep", 0), 1),
                    "Cut Time (sec)": round(tap_result['cut_time'], 2),
                    "No of Positions": op.get("t_cnt", 1),
                    "Position Time (sec)": position_time,
                    "Tool Change (sec)": tool_change_time,
                    "Total Time (sec)": 0 if tap_result['cut_time'] == 0 else round((tap_result['cut_time'] * op.get("t_cnt", 1)) + tool_change_time + (op.get("t_cnt", 1) - 1) * position_time, 2)
                })
        

            elif op["type"] == "Face Mill":
                # Rough pass row
                st.session_state.summary_data.append({
                    "Tool No": len(st.session_state.summary_data) + 1,
                    "Operation": "Face Mill Rough",
                    "Tool Details": f"Ø{fm_result['tool_dia']}mm cutter",
                    "Machining Stock": round(op.get("stock", 0) - (0.5 if fm_result["finish_passes"] > 0 else 0), 2),
                    "Vc (m/min)": round((math.pi * fm_result['tool_dia'] * fm_result['rpm']) / 1000, 1),
                    "RPM": fm_result['rpm'],
                    "Feed/rev (mm)": round(fm_result['feed'] / fm_result['rpm'], 3) if fm_result['rpm'] > 0 else "-",
                    "Table Feed (mm/min)": fm_result['feed'],
                    "Safety Length (mm)": fm_result['tool_dia'],
                    "Cut Length (mm)": fm_result["cut_length"],
                    "Cut Time (sec)": fm_result["time_rough_sec"],
                    "No of Positions": op.get("fm_pos", 1),
                    "Position Time (sec)": position_time,
                    "Tool Change (sec)": tool_change_time,
                    "Total Time (sec)": 0 if fm_result["time_rough_sec"] == 0 else round((fm_result["time_rough_sec"] * op.get("fm_pos", 1)) + tool_change_time + (op.get("fm_pos", 1) - 1) * position_time, 2)
                })
                # Finish pass row
                if fm_result["finish_passes"] > 0:
                    st.session_state.summary_data.append({
                        "Tool No": len(st.session_state.summary_data) + 1,
                        "Operation": "Face Mill Finish",
                        "Tool Details": f"Ø{fm_result['tool_dia']}mm cutter",
                        "Machining Stock": 0.5,
                        "Vc (m/min)": round((math.pi * fm_result['tool_dia'] * fm_result['rpm']) / 1000, 1),
                        "RPM": fm_result['rpm'],
                        "Feed/rev (mm)": round(fm_result['feed'] / fm_result['rpm'], 3) if fm_result['rpm'] > 0 else "-",
                        "Table Feed (mm/min)": fm_result['feed'],
                        "Safety Length (mm)": fm_result['tool_dia'],
                        "Cut Length (mm)": fm_result["cut_length"],
                        "Cut Time (sec)": fm_result["time_finish_sec"],
                        "No of Positions": op.get("fm_pos", 1),
                        "Position Time (sec)": position_time,
                        "Tool Change (sec)": tool_change_time,
                        "Total Time (sec)": 0 if fm_result["time_finish_sec"] == 0 else round((fm_result["time_finish_sec"] * op.get("fm_pos", 1)) + tool_change_time + (op.get("fm_pos", 1) - 1) * position_time, 2)
                    })
           
            # 3. Append calculated data to your combined results list

            # ==============================
            # SUMMARY SHEET DATA COLLECTION
            # ==============================
            
            #tool_name = details.split("|")[0].strip()
            
            #tool_no = get_tool_no(tool_name)
            
            #st.session_state.summary_data.append({
            #    "Tool No": tool_no,
            #    "Tool Details": tool_name,
            #    "Cut Time (sec)": round(op_time,2),
            #    "Cycle Time (sec)": round(op_time,2)
            #})
            
            
            

        # ==========================================
        # DISPLAY RESULTS TABLE AND TOTAL TIME
        # ==========================================
        st.subheader("📊 Combined Cycle Time Report")
        
        # Calculate grand total
        total_cut_time = sum(item["cycle_time"] for item in st.session_state.combined_results)
        
        # Display as a neat summary table
        import pandas as pd
        report_df = pd.DataFrame(st.session_state.combined_results)
        report_df = report_df.rename(columns={
            "op_num": "Op #",
            "type": "Operation Type",
            "details": "Details",
            "cycle_time": "Cycle Time (sec)"
        })
        st.table(report_df)
        
        # Grand Total Message
        st.success(f"🏅 Total Combined Cycle Time = {total_cut_time:.2f} sec")

        # ==============================
        # TOOL SUMMARY REPORT
        # ==============================
        
        if st.session_state.summary_data:
        
            st.subheader("🛠 Tool Summary")
        
            summary_df = pd.DataFrame(
                st.session_state.summary_data
            )
        
            st.dataframe(summary_df)
        
        else:
            st.write("No tool summary data")
