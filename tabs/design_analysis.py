import pandas as pd
import numpy as np

# Structural Analysis Section
def run_structural_analysis():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info("Structural analysis evaluates loads acting on a structure to ensure **stability** and **compliance with ACI standards**.")

    # Load options dropdown
    load_options = ["Dead Load", "Live Load", "Wind Load", "Seismic Load", "Snow Load"]
    selected_load = st.selectbox("Select Load Type", load_options, key="struct_load_type")
    load_value = st.number_input("Enter Load Value (kN)", min_value=0, key="struct_load_value")

    if "structural_data" not in st.session_state:
        st.session_state.structural_data = pd.DataFrame(columns=["Load Type", "Load Value (kN)"])

    if st.button("Add Load", key="add_struct_load"):
        new_row = pd.DataFrame({"Load Type": [selected_load], "Load Value (kN)": [load_value]})
        st.session_state.structural_data = pd.concat([st.session_state.structural_data, new_row], ignore_index=True)

    st.write("### Load Data")
    st.dataframe(st.session_state.structural_data)

    # Perform calculations
    total_load = st.session_state.structural_data["Load Value (kN)"].sum()
    max_load = st.session_state.structural_data["Load Value (kN)"].max()

    st.write("### Analysis Results")
    st.write(f"- **Total Load:** {total_load} kN")
    st.write(f"- **Maximum Load:** {max_load} kN")
    st.success("Ensure compliance with **ACI design load requirements**.")
    

# Geotechnical Analysis Section
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
        new_row = pd.DataFrame({"Soil Type": [selected_soil], "Density": [density], "Cohesion": [cohesion]})
        st.session_state.geotechnical_data = pd.concat([st.session_state.geotechnical_data, new_row], ignore_index=True)

    st.write("### Soil Data")
    st.dataframe(st.session_state.geotechnical_data)

# Hydraulic and Hydrological Modeling Section
def run_hydraulic_analysis():
    st.header("Hydraulic and Hydrological Modeling")
    st.subheader("📌 About Hydrological Modeling")
    st.info("Simulates **water flow and drainage systems**, helping engineers design stormwater, drainage, and sewage networks.")

    simulation_time = st.number_input("Enter Simulation Time (s)", min_value=1)
    flow_rate = st.number_input("Enter Flow Rate (L/s)", min_value=1)

    if "hydraulic_data" not in st.session_state:
        st.session_state.hydraulic_data = pd.DataFrame(columns=["Time (s)", "Flow Rate (L/s)"])

    if st.button("Add Simulation Data"):
        new_row = pd.DataFrame({"Time (s)": [simulation_time], "Flow Rate (L/s)": [flow_rate]})
        st.session_state.hydraulic_data = pd.concat([st.session_state.hydraulic_data, new_row], ignore_index=True)

    st.write("### Flow Simulation Data")
    st.dataframe(st.session_state.hydraulic_data)

# Engineering Tests Section
def run_tests():
    st.header("Engineering Tests")
    st.subheader("📌 About Engineering Tests")
    st.info("Conduct laboratory tests on **water, soil, and other materials**.")

    test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"], key="test_category")

    if test_category == "Water Tests":
        test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids)", "pH Test"], key="water_test_type")

        if test_type == "TDS (Total Dissolved Solids)":
            st.subheader("💧 TDS (Total Dissolved Solids) Test")
            st.write("Determines the total amount of dissolved solids (minerals, salts, and metals) in water.")

            ec = st.number_input("Enter Electrical Conductivity (µS/cm or mS/cm)", key="tds_ec")
            conversion_factor = st.slider("Conversion Factor (0.5 - 0.7)", min_value=0.5, max_value=0.7, step=0.01, key="tds_conversion")

            if st.button("Calculate TDS", key="calc_tds"):
                if ec > 0:
                    tds_value = ec * conversion_factor
                    st.write(f"**TDS: {tds_value:.2f} mg/L (ppm)**")

                    if tds_value < 300:
                        st.success("💧 **Excellent Water Quality** (Ideal for drinking and industrial use).")
                    elif 300 <= tds_value < 600:
                        st.info("✅ **Good Water Quality** (Suitable for most uses).")
                    elif 600 <= tds_value < 900:
                        st.warning("⚠️ **Fair Water Quality** (May require treatment for sensitive applications).")
                    elif 900 <= tds_value < 1200:
                        st.error("❌ **Poor Water Quality** (Not recommended for drinking).")
                    else:
                        st.error("🚫 **Not Suitable for Drinking** (Exceeds safe limits).")
                else:
                    st.error("⚠️ Please enter a valid Electrical Conductivity value.")

# Merged Design and Analysis Section
def run():
    st.title("🛠️ Design and Analysis")

    st.write("This section provides tools for analyzing structural loads, geotechnical properties, hydraulic models, and laboratory test results.")

    tabs = st.tabs([
        "Structural Analysis", 
        "Geotechnical Analysis", 
        "Hydraulic and Hydrological Modeling", 
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
