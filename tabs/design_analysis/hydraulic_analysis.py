import streamlit as st
import pandas as pd

def run():
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
