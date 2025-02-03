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

    ### STRUCTURAL ANALYSIS ###
    with tabs[0]:  
        st.header("Structural Analysis")
        st.write("### About")
        st.write("Structural analysis involves evaluating loads acting on a structure to ensure stability and compliance with ACI standards.")

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

        total_load = st.session_state.structural_data["Load Value (kN)"].sum()
        max_load = st.session_state.structural_data["Load Value (kN)"].max()

        st.write("### Structural Analysis Results")
        st.write(f"- **Total Load:** {total_load} kN")
        st.write(f"- **Maximum Load:** {max_load} kN")
        st.write("Ensure compliance with ACI load design standards.")

        if total_load > 5000:
            st.warning("Warning: The total load exceeds recommended design limits. Consider load redistribution or structural reinforcement.")
        elif total_load > 3000:
            st.info("The structure is within acceptable limits but should be reviewed for safety factors.")

    ### TESTS SUB-TAB (RESTORED & IMPROVED) ###
    with tabs[3]:  
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
                ph_value = st.number_input("Enter Measured pH Value", min_value=0.0, max_value=14.0, step=0.1)

                if st.button("Analyze pH"):
                    st.write(f"**pH Value: {ph_value:.2f}**")

                    if ph_value < 6.5:
                        st.error("Acidic (May cause corrosion)")
                    elif 6.5 <= ph_value <= 8.5:
                        st.success("Neutral (Safe for Drinking)")
                    else:
                        st.warning("Alkaline (May indicate mineral deposits)")
