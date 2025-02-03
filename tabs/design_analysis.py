import streamlit as st
import pandas as pd
import numpy as np
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

    with tabs[0]:  # Structural Analysis
        st.header("Structural Analysis")
        st.write("### About")
        st.write("Structural analysis involves evaluating loads acting on a structure to ensure stability and compliance with ACI standards.")

        # Load options dropdown
        load_options = ["Dead Load", "Live Load", "Wind Load", "Seismic Load", "Snow Load"]
        selected_load = st.selectbox("Select Load Type", load_options)
        load_value = st.number_input("Enter Load Value (kN)", min_value=0)

        if "structural_data" not in st.session_state:
            st.session_state.structural_data = pd.DataFrame(columns=["Load Type", "Load Value (kN)"])

        if st.button("Add Load"):
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
        st.write("Ensure compliance with ACI standards for safe design.")

    with tabs[1]:  # Geotechnical Analysis (Restored & Improved)
        st.header("Geotechnical Analysis")
        st.write("### About")
        st.write("Geotechnical analysis evaluates soil properties to determine foundation suitability.")

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

        # Foundation Recommendation
        st.write("### Foundation Recommendation")
        if cohesion > 20:
            st.write("Suitable for shallow foundations.")
        else:
            st.write("Consider deep foundations due to low cohesion.")

    with tabs[2]:  # Hydraulic and Hydrological Modeling (Restored & Improved)
        st.header("Hydraulic and Hydrological Modeling")
        st.write("### About")
        st.write("Simulates water flow for drainage and hydrological system design.")

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
            st.write("Consider larger drainage pipes.")
        else:
            st.write("Standard drainage pipes are sufficient.")

    with tabs[3]:  # Water & Soil Tests (Enhanced)
        st.header("Engineering Tests")
        st.write("### About")
        st.write("Conduct laboratory tests on water, soil, and other materials.")

        test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"])
        
        if test_category == "Water Tests":
            test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids)", "pH Test"])

            if test_type == "TDS (Total Dissolved Solids)":
                ec = st.number_input("Enter Electrical Conductivity (µS/cm or mS/cm)")
                conversion_factor = st.slider("Conversion Factor (0.5 - 0.7)", min_value=0.5, max_value=0.7, step=0.01)

                if st.button("Calculate TDS"):
                    tds_value = ec * conversion_factor
                    st.write(f"**TDS: {tds_value:.2f} mg/L**")

            elif test_type == "pH Test":
                ph_value = st.number_input("Enter Measured pH Value", min_value=0.0, max_value=14.0, step=0.1)

                if st.button("Analyze pH"):
                    st.write(f"**pH Value: {ph_value:.2f}**")

        elif test_category == "Soil Tests":
            test_type = st.selectbox("Select Soil Test", ["Moisture Content", "Atterberg Limits"])
            
            if test_type == "Moisture Content":
                weight_wet = st.number_input("Enter Wet Soil Weight (g)")
                weight_dry = st.number_input("Enter Dry Soil Weight (g)")
                
                if st.button("Calculate Moisture Content"):
                    moisture_content = ((weight_wet - weight_dry) / weight_dry) * 100
                    st.write(f"**Moisture Content: {moisture_content:.2f}%**")

---
### **Updated Home Tab (UI & Content)**
```python
import streamlit as st

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")
    
    st.markdown("""
    ### About This Application
    This tool automates key civil engineering calculations, compliance checks, and collaboration tasks.
    
    **Key Features**:
    - 📊 **Structural & Geotechnical Analysis**
    - 🚰 **Hydraulic & Hydrological Simulations**
    - 🏗️ **Project Management & Scheduling**
    - ✅ **Compliance Verification & Reporting**
    - 📎 **Collaboration & Documentation Tools**
    """)

    st.image("https://via.placeholder.com/800x400.png?text=Civil+Engineering+Automation", use_column_width=True)
    
    st.write("### Quick Start")
    st.info("Use the left sidebar to navigate different sections of the tool.")
