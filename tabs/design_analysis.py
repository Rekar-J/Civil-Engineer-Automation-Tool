# tabs/design_analysis.py

import streamlit as st
import pandas as pd
import numpy as np
from core import Beam
from plots import plot_beam_diagram, plot_sfd, plot_bmd

# --- Enhanced Structural Analysis Section ---
def run_structural_analysis():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info(
        "This tool evaluates loads acting on a structure and performs advanced calculations "
        "including bending moment analysis and load combination assessments, in accordance with ACI standards."
    )

    # … your existing Structural Analysis code here …
    load_options = ["Dead Load", "Live Load", "Wind Load", "Seismic Load", "Snow Load"]
    selected_load = st.selectbox("Select Load Type", load_options, key="struct_load_type")
    load_value = st.number_input("Enter Load Value (kN)", min_value=0.0, key="struct_load_value")
    distance = st.number_input("Enter Distance from Support (m)", min_value=0.0, key="struct_distance")
    load_factor = st.number_input("Enter Load Factor", min_value=0.0, value=1.0, key="struct_load_factor")

    if "structural_data" not in st.session_state:
        st.session_state.structural_data = pd.DataFrame(
            columns=["Load Type", "Load Value (kN)", "Distance (m)", "Load Factor", "Moment (kN-m)"]
        )

    if st.button("Add Load", key="add_struct_load"):
        moment = load_value * distance * load_factor
        new_row = pd.DataFrame({
            "Load Type": [selected_load],
            "Load Value (kN)": [load_value],
            "Distance (m)": [distance],
            "Load Factor": [load_factor],
            "Moment (kN-m)": [moment]
        })
        st.session_state.structural_data = pd.concat(
            [st.session_state.structural_data, new_row], ignore_index=True
        )

    st.write("### Load Data")
    st.dataframe(st.session_state.structural_data)

    total_load = st.session_state.structural_data["Load Value (kN)"].sum() if not st.session_state.structural_data.empty else 0
    max_load   = st.session_state.structural_data["Load Value (kN)"].max() if not st.session_state.structural_data.empty else 0
    total_mom  = st.session_state.structural_data["Moment (kN-m)"].sum() if not st.session_state.structural_data.empty else 0
    max_mom    = st.session_state.structural_data["Moment (kN-m)"].max() if not st.session_state.structural_data.empty else 0

    st.write("### Analysis Results")
    st.write(f"- **Total Load:** {total_load:.2f} kN")
    st.write(f"- **Maximum Load:** {max_load:.2f} kN")
    st.write(f"- **Total Bending Moment:** {total_mom:.2f} kN·m")
    st.write(f"- **Maximum Bending Moment:** {max_mom:.2f} kN·m")
    st.success("Ensure compliance with **ACI design load requirements** and proper safety factors.")

# --- Geotechnical Analysis Section ---
def run_geotechnical_analysis():
    st.header("Geotechnical Analysis")
    st.subheader("📌 About Geotechnical Analysis")
    st.info("Geotechnical analysis assesses **soil properties** to determine foundation suitability.")

    soil_types = ["Clay", "Sand", "Gravel", "Silt", "Rock"]
    selected_soil = st.selectbox("Select Soil Type", soil_types)
    density = st.number_input("Enter Density (kg/m³)", min_value=1000, max_value=2500, step=10)
    cohesion = st.number_input("Enter Cohesion (kPa)", min_value=0, max_value=100, step=1)

    if "geotechnical_data" not in st.session_state:
        st.session_state.geotechnical_data = pd.DataFrame(columns=["Soil Type", "Density", "Cohesion"])

    if st.button("Add Soil Data"):
        new_row = pd.DataFrame({
            "Soil Type": [selected_soil],
            "Density": [density],
            "Cohesion": [cohesion]
        })
        st.session_state.geotechnical_data = pd.concat([st.session_state.geotechnical_data, new_row], ignore_index=True)

    st.write("### Soil Data")
    st.dataframe(st.session_state.geotechnical_data)

# --- Hydraulic and Hydrological Modeling Section ---
def run_hydraulic_analysis():
    st.header("Hydraulic and Hydrological Modeling")
    st.subheader("📌 About Hydrological Modeling")
    st.info("Simulates **water flow and drainage systems**, helping engineers design stormwater, drainage, and sewage networks.")

    simulation_time = st.number_input("Enter Simulation Time (s)", min_value=1)
    flow_rate = st.number_input("Enter Flow Rate (L/s)", min_value=1)

    if "hydraulic_data" not in st.session_state:
        st.session_state.hydraulic_data = pd.DataFrame(columns=["Time (s)", "Flow Rate (L/s)"])

    if st.button("Add Simulation Data"):
        new_row = pd.DataFrame({
            "Time (s)": [simulation_time],
            "Flow Rate (L/s)": [flow_rate]
        })
        st.session_state.hydraulic_data = pd.concat([st.session_state.hydraulic_data, new_row], ignore_index=True)

    st.write("### Flow Simulation Data")
    st.dataframe(st.session_state.hydraulic_data)

# --- Engineering Tests Section ---
def run_tests():
    st.header("Engineering Tests")
    st.subheader("📌 About Engineering Tests")
    st.info("Conduct laboratory tests on **water, soil, and other materials**.")

    test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"], key="test_category")

    if test_category == "Water Tests":
        test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids)", "pH Test"], key="water_test_type")
        if test_type == "TDS (Total Dissolved Solids)":
            st.subheader("💧 TDS (Total Dissolved Solids) Test")
            ec = st.number_input("Enter Electrical Conductivity (µS/cm)", key="tds_ec")
            cf = st.slider("Conversion Factor (0.5–0.7)", min_value=0.5, max_value=0.7, step=0.01, key="tds_conversion")
            if st.button("Calculate TDS", key="calc_tds"):
                tds = ec * cf if ec > 0 else 0
                st.write(f"**TDS: {tds:.2f} mg/L (ppm)**")
                if tds < 300:
                    st.success("💧 Excellent Water Quality")
                elif tds < 600:
                    st.info("✅ Good Water Quality")
                elif tds < 900:
                    st.warning("⚠️ Fair Water Quality")
                else:
                    st.error("🚫 Poor Water Quality")

# --- New Beam Analysis Sub‑Tab ---
def run_beam_analysis():
    st.header("Beam Analysis")
    st.info("Analyze simply supported beams with point loads and UDLs.")

    length = st.number_input("Beam Length (m)", min_value=0.1, value=5.0, key="beam_len")

    # Supports (exactly two)
    st.write("#### Supports")
    supports = []
    for i in range(2):
        pos = st.number_input(
            f"Support #{i+1} Position (m)",
            min_value=0.0, max_value=length,
            value=(0.0 if i == 0 else length),
            key=f"beam_sup_pos_{i}"
        )
        sup_type = st.selectbox(
            f"Support #{i+1} Type",
            ["pin", "roller"],
            key=f"beam_sup_type_{i}"
        )
        supports.append({"pos": pos, "type": sup_type})

    # Point Loads
    st.write("#### Point Loads")
    point_loads = []
    n_pl = st.number_input("How many point loads?", min_value=0, value=0, step=1, key="beam_pl_num")
    for i in range(int(n_pl)):
        pos = st.number_input(
            f"Load #{i+1} Position (m)",
            min_value=0.0, max_value=length,
            value=length / 2,
            key=f"beam_pl_pos_{i}"
        )
        mag = st.number_input(
            f"Load #{i+1} Magnitude (kN)",
            value=10.0,
            key=f"beam_pl_mag_{i}"
        )
        point_loads.append({"pos": pos, "mag": mag})

    # UDLs
    st.write("#### Uniformly Distributed Loads")
    udls = []
    n_udl = st.number_input("How many UDLs?", min_value=0, value=0, step=1, key="beam_udl_num")
    for i in range(int(n_udl)):
        start = st.number_input(
            f"UDL #{i+1} Start (m)",
            min_value=0.0, max_value=length,
            value=0.0,
            key=f"beam_udl_start_{i}"
        )
        end = st.number_input(
            f"UDL #{i+1} End (m)",
            min_value=0.0, max_value=length,
            value=length,
            key=f"beam_udl_end_{i}"
        )
        intensity = st.number_input(
            f"UDL #{i+1} Intensity (kN/m)",
            value=5.0,
            key=f"beam_udl_int_{i}"
        )
        udls.append({"start": start, "end": end, "int": intensity})

    # Build and solve beam
    beam = Beam(length)
    for sup in supports:
        beam.add_support(sup["pos"], sup["type"])
    for pl in point_loads:
        beam.add_point_load(pl["pos"], pl["mag"])
    for ud in udls:
        beam.add_distributed_load(ud["start"], ud["end"], ud["int"])

    if st.button("🔎 Analyze Beam", key="analyze_beam"):
        beam.analyze()

        # Reactions
        st.write("#### Support Reactions")
        for i, R in enumerate(beam.reactions):
            st.write(f"> Support #{i+1} at {supports[i]['pos']} m → **{R:.2f} kN**")

        # Max moment
        xs = np.linspace(0, beam.length, 200)
        max_M = max(abs(beam.moment_at(x)) for x in xs)
        st.write(f"#### Maximum Bending Moment: **{max_M:.2f} kN·m**")

        # Plots
        st.write("#### Beam Schematic")
        st.pyplot(plot_beam_diagram(beam))
        st.write("#### Shear Force Diagram")
        st.pyplot(plot_sfd(beam))
        st.write("#### Bending Moment Diagram")
        st.pyplot(plot_bmd(beam))

# --- Combined Tabs for Design & Analysis ---
def run():
    st.title("🛠️ Design and Analysis")
    tabs = st.tabs([
        "Structural Analysis",
        "Beam Analysis",
        "Geotechnical Analysis",
        "Hydraulic and Hydrological Modeling",
        "Tests"
    ])
    with tabs[0]:
        run_structural_analysis()
    with tabs[1]:
        run_beam_analysis()
    with tabs[2]:
        run_geotechnical_analysis()
    with tabs[3]:
        run_hydraulic_analysis()
    with tabs[4]:
        run_tests()
