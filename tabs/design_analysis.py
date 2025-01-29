import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run():
    st.title("🛠️ Design and Analysis")
    st.write("Analyze and design structures with the tools provided.")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling"])

    with tabs[0]:
        st.header("Structural Analysis")
        st.write("Example: Load Calculations")
        sample_data = pd.DataFrame({
            "Load Type": ["Dead Load", "Live Load", "Wind Load", "Seismic Load"],
            "Load Value (kN)": [500, 300, 150, 200]
        })
        st.dataframe(sample_data)
        st.write("Add your own data:")
        load_type = st.text_input("Enter Load Type")
        load_value = st.number_input("Enter Load Value (kN)", min_value=0)
        if st.button("Add Load"):
            new_row = pd.DataFrame({"Load Type": [load_type], "Load Value (kN)": [load_value]})
            sample_data = pd.concat([sample_data, new_row], ignore_index=True)
            st.dataframe(sample_data)
        st.write("### Result: Total Load")
        total_load = sample_data["Load Value (kN)"].sum()
        st.write(f"The total load is **{total_load} kN**. Ensure this value meets the design criteria per ACI standards.")

    with tabs[1]:
        st.header("Geotechnical Analysis")
        st.write("Evaluate soil properties for foundation design.")
        sample_soil_data = pd.DataFrame({
            "Soil Type": ["Clay", "Sand", "Gravel", "Silt"],
            "Density (kg/m3)": [1600, 1800, 2000, 1500],
            "Cohesion (kPa)": [25, 5, 0, 15]
        })
        st.dataframe(sample_soil_data)
        st.write("Add your own data:")
        soil_type = st.text_input("Enter Soil Type")
        density = st.number_input("Enter Density (kg/m3)", min_value=0)
        cohesion = st.number_input("Enter Cohesion (kPa)", min_value=0)
        if st.button("Add Soil Data"):
            new_row = pd.DataFrame({"Soil Type": [soil_type], "Density (kg/m3)": [density], "Cohesion (kPa)": [cohesion]})
            sample_soil_data = pd.concat([sample_soil_data, new_row], ignore_index=True)
            st.dataframe(sample_soil_data)
        st.write("### Result: Foundation Recommendation")
        if cohesion > 20:
            st.write("The soil is suitable for shallow foundations.")
        else:
            st.write("Consider deep foundations due to low cohesion.")

    with tabs[2]:
        st.header("Hydraulic and Hydrological Modeling")
        st.write("Simulate water flow and design drainage systems.")
        time = np.arange(0, 10, 0.1)
        flow_rate = np.sin(time) * 100 + 200
        st.line_chart(pd.DataFrame({"Time (s)": time, "Flow Rate (L/s)": flow_rate}))
        st.write("Add your flow simulation data:")
        simulation_time = st.number_input("Enter Simulation Time (s)", min_value=0)
        flow = st.number_input("Enter Flow Rate (L/s)", min_value=0)
        if st.button("Add Simulation Data"):
            st.write(f"Added data: Time = {simulation_time}s, Flow Rate = {flow}L/s")
        st.write("### Result: Drainage Design")
        if flow > 250:
            st.write("The flow rate exceeds typical capacity. Design larger drainage pipes.")
        else:
            st.write("The flow rate is within acceptable limits for standard drainage systems.")
