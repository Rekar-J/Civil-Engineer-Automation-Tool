import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def run():
    st.title("🛠️ Design and Analysis")
    st.write("Analyze and design structures with the tools provided.")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling", "Tests"])

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

    with tabs[3]:  # Water Tests
        st.header("Water Quality Tests")
        st.write("Analyze water quality parameters such as TDS and pH.")

        # Select Test Type
        test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids) Test", "pH Test"])

        if test_type == "TDS (Total Dissolved Solids) Test":
            st.subheader("TDS (Total Dissolved Solids) Test")
            temp = st.number_input("Enter Sample Temperature (°C)", min_value=0, max_value=100, step=1)
            ec = st.number_input("Enter Electrical Conductivity (EC) (µS/cm or mS/cm)", min_value=0.0, format="%.2f")
            conversion_factor = st.slider("Conversion Factor (0.5 - 0.7)", min_value=0.5, max_value=0.7, step=0.01, value=0.65)

            if st.button("Calculate TDS"):
                tds_value = ec * conversion_factor
                st.write(f"**Total Dissolved Solids (TDS): {tds_value:.2f} mg/L (ppm)**")

                # TDS Classification
                st.write("### Water Quality Based on TDS:")
                if tds_value < 300:
                    st.success("Excellent Water Quality")
                elif 300 <= tds_value < 600:
                    st.info("Good Water Quality")
                elif 600 <= tds_value < 900:
                    st.warning("Fair Water Quality")
                elif 900 <= tds_value < 1200:
                    st.error("Poor Water Quality")
                else:
                    st.error("Not Suitable for Drinking")

        elif test_type == "pH Test":
            st.subheader("pH Test")
            ph_value = st.number_input("Enter Measured pH Value", min_value=0.0, max_value=14.0, step=0.1, format="%.1f")
            temp_pH = st.number_input("Enter Water Sample Temperature (°C) (Optional)", min_value=0, max_value=100, step=1)

            if st.button("Analyze pH"):
                st.write(f"**pH Value: {ph_value:.2f}**")

                # pH Classification
                st.write("### Water Quality Based on pH:")
                if ph_value < 6.5:
                    st.error("Acidic (May cause corrosion)")
                elif 6.5 <= ph_value <= 8.5:
                    st.success("Neutral (Safe for Drinking)")
                else:
                    st.warning("Alkaline (May indicate mineral deposits)")

                # Graphical Representation of pH Scale
                ph_scale = pd.DataFrame({
                    "pH Range": ["Acidic", "Neutral", "Alkaline"],
                    "pH Value": [4.0, 7.0, 10.0]
                })
                fig = px.bar(ph_scale, x="pH Range", y="pH Value", title="pH Scale (0-14)")
                st.plotly_chart(fig)

        # Additional Features
        st.write("### Additional Features")
        upload_report = st.file_uploader("Upload Test Report (CSV/PDF)", type=["csv", "pdf"])
        if upload_report:
            st.success("Test Report Uploaded Successfully!")

        # Historical Data Storage
        if "water_test_data" not in st.session_state:
            st.session_state.water_test_data = pd.DataFrame(columns=["Test Type", "Result"])

        if test_type == "TDS (Total Dissolved Solids) Test" and st.button("Save TDS Result"):
            st.session_state.water_test_data = pd.concat([st.session_state.water_test_data, 
                pd.DataFrame({"Test Type": ["TDS"], "Result": [tds_value]})], ignore_index=True)
            st.success("TDS Test Result Saved!")

        if test_type == "pH Test" and st.button("Save pH Result"):
            st.session_state.water_test_data = pd.concat([st.session_state.water_test_data, 
                pd.DataFrame({"Test Type": ["pH"], "Result": [ph_value]})], ignore_index=True)
            st.success("pH Test Result Saved!")

        st.write("### Historical Water Test Data")
        st.dataframe(st.session_state.water_test_data)
