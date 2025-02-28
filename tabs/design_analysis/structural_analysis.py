import streamlit as st
import pandas as pd

def run():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info("Structural analysis evaluates loads acting on a structure to ensure **stability** and **compliance with ACI standards**.")

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

    if not st.session_state.structural_data.empty:
        total_load = st.session_state.structural_data["Load Value (kN)"].sum()
        max_load = st.session_state.structural_data["Load Value (kN)"].max()

        st.write("### Analysis Results")
        st.write(f"- **Total Load:** {total_load} kN")
        st.write(f"- **Maximum Load:** {max_load} kN")
        st.success("Ensure compliance with **ACI design load requirements**.")
    else:
        st.info("No load data available. Please add loads to perform analysis.")
