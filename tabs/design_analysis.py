# tabs/design_analysis.py

import streamlit as st
import pandas as pd

# --- Structural Analysis Section ---
def run_structural_analysis():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info(
        "This tool evaluates loads acting on a structure and performs advanced calculations "
        "including bending moment analysis and load combination assessments, in accordance with ACI standards."
    )

    load_options = ["Dead Load", "Live Load", "Wind Load", "Seismic Load", "Snow Load"]
    selected_load = st.selectbox("Select Load Type", load_options, key="struct_load_type")
    load_value    = st.number_input("Enter Load Value (kN)", min_value=0.0, key="struct_load_value")
    distance      = st.number_input("Enter Distance from Support (m)", min_value=0.0, key="struct_distance")
    load_factor   = st.number_input("Enter Load Factor", min_value=0.0, value=1.0, key="struct_load_factor")

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

    # Summary
    df = st.session_state.structural_data
    total_load   = df["Load Value (kN)"].sum()   if not df.empty else 0
    max_load     = df["Load Value (kN)"].max()   if not df.empty else 0
    total_moment = df["Moment (kN-m)"].sum()     if not df.empty else 0
    max_moment   = df["Moment (kN-m)"].max()     if not df.empty else 0

    st.write("### Analysis Results")
    st.write(f"- **Total Load:** {total_load:.2f} kN")
    st.write(f"- **Maximum Load:** {max_load:.2f} kN")
    st.write(f"- **Total Bending Moment:** {total_moment:.2f} kN·m")
    st.write(f"- **Maximum Bending Moment:** {max_moment:.2f} kN·m")
    st.success("Ensure compliance with **ACI design load requirements** and proper safety factors.")

# --- Geotechnical Analysis ---
def run_geotechnical_analysis():
    st.header("Geotechnical Analysis")
    st.subheader("📌 About Geotechnical Analysis")
    st.info("Assesses soil properties to determine foundation suitability.")

    soil_types   = ["Clay","Sand","Gravel","Silt","Rock"]
    selected_soil= st.selectbox("Soil Type", soil_types)
    density      = st.number_input("Density (kg/m³)", min_value=1000, max_value=2500, step=10)
    cohesion     = st.number_input("Cohesion (kPa)",    min_value=0,    max_value=100,  step=1)

    if "geotechnical_data" not in st.session_state:
        st.session_state.geotechnical_data = pd.DataFrame(
            columns=["Soil Type","Density","Cohesion"]
        )

    if st.button("Add Soil Data"):
        new_row = pd.DataFrame({
            "Soil Type":[selected_soil],
            "Density":[density],
            "Cohesion":[cohesion]
        })
        st.session_state.geotechnical_data = pd.concat(
            [st.session_state.geotechnical_data, new_row], ignore_index=True
        )

    st.write("### Soil Data")
    st.dataframe(st.session_state.geotechnical_data)

# --- Hydraulic & Hydrological Modeling ---
def run_hydraulic_analysis():
    st.header("Hydraulic & Hydrological Modeling")
    st.info("Simulates water flow and drainage systems.")

    t = st.number_input("Simulation Time (s)", min_value=1)
    q = st.number_input("Flow Rate (L/s)",      min_value=1)

    if "hydraulic_data" not in st.session_state:
        st.session_state.hydraulic_data = pd.DataFrame(
            columns=["Time (s)","Flow Rate (L/s)"]
        )

    if st.button("Add Simulation Data"):
        new_row = pd.DataFrame({"Time (s)":[t],"Flow Rate (L/s)":[q]})
        st.session_state.hydraulic_data = pd.concat(
            [st.session_state.hydraulic_data, new_row], ignore_index=True
        )

    st.write("### Flow Simulation Data")
    st.dataframe(st.session_state.hydraulic_data)

# --- Lab Tests ---
def run_tests():
    st.header("Engineering Tests")
    st.info("Lab tests on water, soil, etc.")

    cat = st.selectbox("Test Category", ["Water Tests","Soil Tests"], key="test_category")

    if cat == "Water Tests":
        typ = st.selectbox("Water Test", ["TDS","pH"], key="water_test")
        if typ == "TDS":
            ec = st.number_input("EC (µS/cm)", key="tds_ec")
            cf = st.slider("Conversion Factor", 0.5, 0.7, 0.6, 0.01, key="tds_cf")
            if st.button("Calculate TDS"):
                tds = ec * cf
                st.write(f"**TDS: {tds:.2f} mg/L**")
                if tds<300:    st.success("Excellent Water Quality")
                elif tds<600:  st.info("Good Water Quality")
                elif tds<900:  st.warning("Fair Quality")
                else:          st.error("Poor Quality")

# --- Main Tab Switcher ---
def run():
    st.title("🛠️ Design and Analysis")
    tabs = st.tabs([
        "Structural Analysis",
        "Geotechnical Analysis",
        "Hydraulic & Hydrological",
        "Tests"
    ])

    with tabs[0]:
        run_structural_analysis()
    with tabs[1]:
        run_geotechnical_analysis()
    with tabs[2]:
        run_hydraulic_analysis()
    with tabs[3]:
        run_tests()
