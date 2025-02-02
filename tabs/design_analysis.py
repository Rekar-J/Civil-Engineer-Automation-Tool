import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run():
    st.title("🛠️ Design and Analysis")
    st.write("Analyze and design structures with the tools provided.")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling"])

    with tabs[0]:  # Structural Analysis
        st.header("Structural Analysis")
        st.write("Perform load calculations and evaluate structural integrity.")

        # Load options dropdown
        load_options = ["Dead Load", "Live Load", "Wind Load", "Seismic Load", "Snow Load"]
        selected_load = st.selectbox("Select Load Type", load_options)
        load_value = st.number_input("Enter Load Value (kN)", min_value=0)

        # Existing sample data
        if "structural_data" not in st.session_state:
            st.session_state.structural_data = pd.DataFrame(columns=["Load Type", "Load Value (kN)"])

        if st.button("Add Load"):
            new_row = pd.DataFrame({"Load Type": [selected_load], "Load Value (kN)": [load_value]})
            st.session_state.structural_data = pd.concat([st.session_state.structural_data, new_row], ignore_index=True)

        st.write("### Load Data")
        st.dataframe(st.session_state.structural_data)

        # Perform calculations
        total_load = st.session_state.structural_data["Load Value (kN)"].sum()
        average_load = st.session_state.structural_data["Load Value (kN)"].mean()
        max_load = st.session_state.structural_data["Load Value (kN)"].max()

        st.write(f"### Analysis Results")
        st.write(f"- **Total Load:** {total_load} kN")
        st.write(f"- **Average Load:** {average_load:.2f} kN")
        st.write(f"- **Maximum Load:** {max_load} kN")
        st.write("Ensure these values comply with ACI and structural safety limits.")

    with tabs[1]:  # Geotechnical Analysis
        st.header("Geotechnical Analysis")
        st.write("Evaluate soil properties for foundation design.")

        soil_types = ["Clay", "Sand", "Gravel", "Silt", "Rock"]
        selected_soil = st.selectbox("Select Soil Type", soil_types)
        density = st.number_input("Enter Density (kg/m3)", min_value=1000, max_value=2500, step=10)
        cohesion = st.number_input("Enter Cohesion (kPa)", min_value=0, max_value=100, step=1)

        if "geotechnical_data" not in st.session_state:
            st.session_state.geotechnical_data = pd.DataFrame(columns=["Soil Type", "Density (kg/m3)", "Cohesion (kPa)"])

        if st.button("Add Soil Data"):
            new_row = pd.DataFrame({"Soil Type": [selected_soil], "Density (kg/m3)": [density], "Cohesion (kPa)": [cohesion]})
            st.session_state.geotechnical_data = pd.concat([st.session_state.geotechnical_data, new_row], ignore_index=True)

        st.write("### Soil Data")
        st.dataframe(st.session_state.geotechnical_data)

        # Foundation Recommendation
        st.write("### Foundation Recommendation")
        if cohesion > 20:
            st.write("The soil is suitable for shallow foundations.")
        else:
            st.write("Consider deep foundations due to low cohesion.")

    with tabs[2]:  # Hydraulic and Hydrological Modeling
        st.header("Hydraulic and Hydrological Modeling")
        st.write("Simulate water flow and design drainage systems.")

        simulation_time = st.number_input("Enter Simulation Time (s)", min_value=1)
        flow_rate = st.number_input("Enter Flow Rate (L/s)", min_value=1)

        if "hydraulic_data" not in st.session_state:
            st.session_state.hydraulic_data = pd.DataFrame(columns=["Time (s)", "Flow Rate (L/s)"])

        if st.button("Add Simulation Data"):
            new_row = pd.DataFrame({"Time (s)": [simulation_time], "Flow Rate (L/s)": [flow_rate]})
            st.session_state.hydraulic_data = pd.concat([st.session_state.hydraulic_data, new_row], ignore_index=True)

        st.write("### Flow Simulation Data")
        st.dataframe(st.session_state.hydraulic_data)

        # Drainage Design Recommendation
        st.write("### Drainage Design Recommendation")
        if flow_rate > 250:
            st.write("The flow rate exceeds typical capacity. Design larger drainage pipes.")
        else:
            st.write("The flow rate is within acceptable limits for standard drainage systems.")
