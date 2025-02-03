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
        st.subheader("📌 About Structural Analysis")
        st.info("Structural analysis involves evaluating loads acting on a structure to ensure stability, safety, and compliance with **ACI standards**. This tool helps engineers assess load effects on buildings, bridges, and other structures.")

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
        st.success("Ensure compliance with ACI design load requirements.")

    ### GEOTECHNICAL ANALYSIS ###
    with tabs[1]:  
        st.header("Geotechnical Analysis")
        st.subheader("📌 About Geotechnical Analysis")
        st.info("Geotechnical analysis assesses **soil properties** to determine foundation suitability. The soil's density, cohesion, and type are key factors in designing safe and stable structures.")

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

    ### HYDRAULIC AND HYDROLOGICAL MODELING ###
    with tabs[2]:  
        st.header("Hydraulic and Hydrological Modeling")
        st.subheader("📌 About Hydrological Modeling")
        st.info("This tool simulates **water flow and drainage systems**, helping engineers design effective stormwater management, drainage, and sewage networks.")

        simulation_time = st.number_input("Enter Simulation Time (s)", min_value=1)
        flow_rate = st.number_input("Enter Flow Rate (L/s)", min_value=1)

        if "hydraulic_data" not in st.session_state:
            st.session_state.hydraulic_data = pd.DataFrame(columns=["Time (s)", "Flow Rate (L/s)"])

        if st.button("Add Simulation Data"):
            new_row = pd.DataFrame({"Time (s)": [simulation_time], "Flow Rate (L/s)"]})
            st.session_state.hydraulic_data = pd.concat([st.session_state.hydraulic_data, new_row], ignore_index=True)

        st.write("### Flow Simulation Data")
        st.dataframe(st.session_state.hydraulic_data)

        st.write("### Drainage Design Recommendation")
        if flow_rate > 250:
            st.warning("Consider using **larger drainage pipes** to accommodate high flow rates.")
        else:
            st.success("Standard drainage pipes are sufficient.")

    ### TESTS SUB-TAB (RESTORED & IMPROVED) ###
    with tabs[3]:  
        st.header("Engineering Tests")
        st.subheader("📌 About Engineering Tests")
        st.info("This section provides **lab testing for water and soil** to assess material properties and ensure compliance with regulatory standards.")

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
