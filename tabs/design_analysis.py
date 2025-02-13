import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("🛠️ Design and Analysis")

    st.write("This section provides tools for analyzing structural loads, geotechnical properties, hydraulic models, and laboratory test results.")

    tabs = st.tabs([
        "Structural Analysis", 
        "Geotechnical Analysis", 
        "Hydraulic and Hydrological Modeling", 
        "Tests"
    ])

    ### GEOTECHNICAL ANALYSIS (RESTORED) ###
    with tabs[1]:  
        st.header("Geotechnical Analysis")
        st.subheader("📌 About Geotechnical Analysis")
        st.info("Geotechnical analysis assesses **soil properties** to determine foundation suitability.")

        soil_types = ["Clay", "Sand", "Gravel", "Silt", "Rock"]
        selected_soil = st.selectbox("Select Soil Type", soil_types)
        density = st.number_input("Enter Density (kg/m3)", min_value=1000, max_value=2500, step=10)
        cohesion = st.number_input("Enter Cohesion (kPa)", min_value=0, max_value=100, step=1)

        if "geotechnical_data" not in st.session_state:
            st.session_state.geotechnical_data = pd.DataFrame(columns=["Soil Type", "Density", "Cohesion"])

        if st.button("Add Soil Data"):
            new_row = pd.DataFrame({"Soil Type": [selected_soil], "Density": [density], "Cohesion": [cohesion]})
            st.session_state.geotechnical_data = pd.concat([st.session_state.geotechnical_data, new_row], ignore_index=True)

        st.write("### Soil Data")
        st.dataframe(st.session_state.geotechnical_data)

    ### HYDRAULIC AND HYDROLOGICAL MODELING (RESTORED) ###
    with tabs[2]:  
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

    ### TESTS (RESTORED) ###
    with tabs[3]:  
        st.header("Engineering Tests")
        st.subheader("📌 About Engineering Tests")
        st.info("Conduct laboratory tests on water, soil, and other materials.")

        test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"])
        
        if test_category == "Water Tests":
            test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids)", "pH Test"])

            if test_type == "TDS (Total Dissolved Solids)":
                ec = st.number_input("Enter Electrical Conductivity (µS/cm or mS/cm)")
                conversion_factor = st.slider("Conversion Factor (0.5 - 0.7)", min_value=0.5, max_value=0.7, step=0.01)

                if st.button("Calculate TDS"):
                    tds_value = ec * conversion_factor
                    st.write(f"**TDS: {tds_value:.2f} mg/L (ppm)**")
