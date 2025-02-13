import streamlit as st
import pandas as pd
from database import save_to_database

def run():
    st.title("🛠️ Design and Analysis")

    st.write("This section provides tools for analyzing structural loads, geotechnical properties, hydraulic models, and laboratory test results.")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling", "Tests"])

    ### STRUCTURAL ANALYSIS ###
    with tabs[0]:  
        st.header("Structural Analysis")
        st.subheader("📌 About Structural Analysis")
        st.info("Structural analysis evaluates loads acting on a structure to ensure compliance with **ACI standards**.")

        load_options = ["Dead Load", "Live Load", "Wind Load", "Seismic Load", "Snow Load"]
        selected_load = st.selectbox("Select Load Type", load_options)
        load_value = st.number_input("Enter Load Value (kN)", min_value=0)

        if "structural_data" not in st.session_state:
            st.session_state.structural_data = pd.DataFrame(columns=["Load Type", "Load Value (kN)"])

        if st.button("Add Load"):
            new_row = pd.DataFrame({"Load Type": [selected_load], "Load Value (kN)": [load_value]})
            st.session_state.structural_data = pd.concat([st.session_state.structural_data, new_row], ignore_index=True)

            # Save data to GitHub
            save_to_database("Design and Analysis", "Structural Analysis", new_row.to_dict(orient="records"))

        st.write("### Load Data")
        st.dataframe(st.session_state.structural_data)
