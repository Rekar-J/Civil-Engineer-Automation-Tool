import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run():
    st.title("🛠️ Design and Analysis")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling", "Tests"])

    with tabs[0]:  # Structural Analysis
        st.header("Structural Analysis")
        st.write("Structural analysis ensures structures can handle applied loads safely.")

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

    with tabs[3]:  # Tests (Fixed)
        st.header("Engineering Tests")
        st.write("Conduct laboratory tests for water, soil, and materials.")

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
