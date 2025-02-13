import streamlit as st
import pandas as pd

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

        st.write("### Foundation Recommendation")
        if cohesion > 20:
            st.success("Suitable for **shallow foundations**.")
        else:
            st.warning("Consider **deep foundations** due to low cohesion.")

    ### HYDRAULIC AND HYDROLOGICAL MODELING (RESTORED) ###
    with tabs[2]:  
        st.header("Hydraulic and Hydrological Modeling")
        st.subheader("📌 About Hydrological Modeling")
        st.info("This tool simulates **water flow and drainage systems**, helping engineers design effective stormwater management, drainage, and sewage networks.")

        simulation_time = st.number_input("Enter Simulation Time (s)", min_value=1)
        flow_rate = st.number_input("Enter Flow Rate (L/s)", min_value=1)

        if "hydraulic_data" not in st.session_state:
            st.session_state.hydraulic_data = pd.DataFrame(columns=["Time (s)", "Flow Rate (L/s)"])

        if st.button("Add Simulation Data"):
            new_row = pd.DataFrame({"Time (s)": [simulation_time], "Flow Rate (L/s)": [flow_rate]})
            st.session_state.hydraulic_data = pd.concat([st.session_state.hydraulic_data, new_row], ignore_index=True)

        st.write("### Flow Simulation Data")
        st.dataframe(st.session_state.hydraulic_data)

        st.write("### Drainage Design Recommendation")
        if flow_rate > 250:
            st.warning("Consider using **larger drainage pipes** to accommodate high flow rates.")
        else:
            st.success("Standard drainage pipes are sufficient.")

    ### TESTS (RESTORED) ###
    with tabs[3]:  
        st.header("Engineering Tests")
        st.subheader("📌 About Engineering Tests")
        st.info("This section provides **lab testing for water and soil** to assess material properties and ensure compliance with regulatory standards.")

        test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"])
        
        if test_category == "Water Tests":
            test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids)", "pH Test"])
