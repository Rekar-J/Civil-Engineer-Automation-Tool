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

    ### STRUCTURAL ANALYSIS (RESTORED) ###
    with tabs[0]:  
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

    ### TESTS SUB-TAB (FIXED RESULTS FOR TDS & PH) ###
    with tabs[3]:  
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

                        # TDS Water Quality Interpretation
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

            elif test_type == "pH Test":
                st.subheader("⚖️ pH Test")
                st.write("Determines the **acidity or alkalinity** of water.")

                ph_value = st.number_input("Enter Measured pH Value", min_value=0.0, max_value=14.0, step=0.1, key="ph_value")

                if st.button("Analyze pH", key="analyze_ph"):
                    if ph_value > 0:
                        st.write(f"**pH Value: {ph_value:.2f}**")

                        # pH Water Quality Interpretation
                        if ph_value < 6.5:
                            st.error("⚠️ **Acidic Water** (May cause corrosion in pipes and infrastructure).")
                        elif 6.5 <= ph_value <= 8.5:
                            st.success("✅ **Neutral Water** (Safe for drinking and industrial use).")
                        else:
                            st.warning("⚠️ **Alkaline Water** (May indicate excessive minerals, affecting taste and usability).")
                    else:
                        st.error("⚠️ Please enter a valid pH value.")

