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

    ### TESTS SUB-TAB (RESTORED & IMPROVED) ###
    with tabs[3]:  
        st.header("Engineering Tests")
        st.subheader("📌 About Engineering Tests")
        st.info("This section provides **lab testing for water and soil** to assess material properties and ensure compliance with regulatory standards.")

        test_category = st.selectbox("Select Test Category", ["Water Tests", "Soil Tests"])
        
        if test_category == "Water Tests":
            test_type = st.selectbox("Select Water Test", ["TDS (Total Dissolved Solids)", "pH Test"])

            if test_type == "TDS (Total Dissolved Solids)":
                st.subheader("💧 TDS (Total Dissolved Solids) Test")
                st.write("This test determines the total amount of dissolved solids (minerals, salts, and metals) in water.")

                ec = st.number_input("Enter Electrical Conductivity (µS/cm or mS/cm)")
                conversion_factor = st.slider("Conversion Factor (0.5 - 0.7)", min_value=0.5, max_value=0.7, step=0.01)

                if st.button("Calculate TDS"):
                    tds_value = ec * conversion_factor
                    st.write(f"**TDS: {tds_value:.2f} mg/L (ppm)**")

                    # TDS Quality Interpretation
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

            elif test_type == "pH Test":
                st.subheader("⚖️ pH Test")
                st.write("This test determines the **acidity or alkalinity** of water.")

                ph_value = st.number_input("Enter Measured pH Value", min_value=0.0, max_value=14.0, step=0.1)

                if st.button("Analyze pH"):
                    st.write(f"**pH Value: {ph_value:.2f}**")

                    # pH Quality Interpretation
                    if ph_value < 6.5:
                        st.error("⚠️ **Acidic Water** (May cause corrosion in pipes and infrastructure).")
                    elif 6.5 <= ph_value <= 8.5:
                        st.success("✅ **Neutral Water** (Safe for drinking and industrial use).")
                    else:
                        st.warning("⚠️ **Alkaline Water** (May indicate excessive minerals, affecting taste and usability).")

        elif test_category == "Soil Tests":
            test_type = st.selectbox("Select Soil Test", ["Moisture Content", "Atterberg Limits"])

            if test_type == "Moisture Content":
                st.subheader("🌱 Moisture Content Test")
                st.write("Determines the **percentage of water** in soil.")

                weight_wet = st.number_input("Enter Wet Soil Weight (g)")
                weight_dry = st.number_input("Enter Dry Soil Weight (g)")

                if st.button("Calculate Moisture Content"):
                    if weight_dry > 0:
                        moisture_content = ((weight_wet - weight_dry) / weight_dry) * 100
                        st.write(f"**Moisture Content: {moisture_content:.2f}%**")

                        # Moisture Content Interpretation
                        if moisture_content < 10:
                            st.success("✅ **Low Moisture Content** (Ideal for compaction).")
                        elif 10 <= moisture_content < 25:
                            st.info("🔹 **Moderate Moisture Content** (Good for stability).")
                        else:
                            st.warning("⚠️ **High Moisture Content** (May cause settlement issues).")
                    else:
                        st.error("❌ **Invalid Input**: Dry soil weight must be greater than zero.")
