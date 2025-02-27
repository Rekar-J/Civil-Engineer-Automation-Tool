import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load combination factors (ACI 318)
LOAD_COMBINATIONS = {
    "DL + LL": (1.2, 1.6),    # Dead Load + Live Load
    "DL + WL": (1.2, 1.0),    # Dead Load + Wind Load
    "DL + LL + WL": (1.2, 1.6, 1.0),  # DL + LL + Wind Load
    "Seismic Load": (1.0, 1.0) # Simplified seismic factor
}

def run():
    st.header("Structural Analysis")
    st.subheader("📌 About Structural Analysis")
    st.info("Analyze loads, calculate structural response, and check compliance with ACI 318 standards.")

    # Define Load Types
    load_options = ["Dead Load (DL)", "Live Load (LL)", "Wind Load (WL)", "Seismic Load (SL)", "Snow Load (SN)"]
    selected_load = st.selectbox("Select Load Type", load_options, key="struct_load_type")
    load_value = st.number_input("Enter Load Value (kN)", min_value=0.0, step=1.0, key="struct_load_value")

    # Initialize session storage for structural data
    if "structural_data" not in st.session_state:
        st.session_state.structural_data = pd.DataFrame(columns=["Load Type", "Load Value (kN)"])

    # Add Load
    if st.button("Add Load", key="add_struct_load"):
        new_row = pd.DataFrame({"Load Type": [selected_load], "Load Value (kN)": [load_value]})
        st.session_state.structural_data = pd.concat([st.session_state.structural_data, new_row], ignore_index=True)

    # Display Load Data
    st.write("### Load Data")
    st.dataframe(st.session_state.structural_data)

    # **Step 1: Load Calculation & Combination**
    total_load = st.session_state.structural_data["Load Value (kN)"].sum()
    max_load = st.session_state.structural_data["Load Value (kN)"].max()

    st.write("### Load Summary")
    st.write(f"- **Total Applied Load:** {total_load} kN")
    st.write(f"- **Maximum Load Applied:** {max_load} kN")

    # Load Combination Selection
    st.write("### Load Combinations (ACI 318)")
    selected_combination = st.selectbox("Select Load Combination", list(LOAD_COMBINATIONS.keys()), key="load_combo")
    factors = LOAD_COMBINATIONS[selected_combination]

    combined_load = sum(f * total_load / len(factors) for f in factors)
    st.write(f"🔹 **Applied Combined Load:** {combined_load:.2f} kN")
    st.success("Ensure compliance with **ACI 318 load combinations** for safety.")

    # **Step 2: Structural Member Design**
    st.write("## Beam & Column Design")
    beam_length = st.number_input("Enter Beam Length (m)", min_value=1.0, step=0.1, key="beam_length")
    material = st.selectbox("Select Material", ["Concrete (f'c = 30 MPa)", "Steel (Fy = 250 MPa)"], key="beam_material")

    # Approximate Section Properties
    if material.startswith("Concrete"):
        allowable_stress = 0.45 * 30  # 45% of f'c (Concrete strength)
    else:
        allowable_stress = 0.6 * 250  # 60% of Fy (Steel yield strength)

    moment = (combined_load * beam_length**2) / 8  # Approximate simply supported beam formula
    shear_force = combined_load / 2  # Max shear at supports
    stress = moment / (0.5 * beam_length)  # Simplified bending stress calc

    # **Step 3: Safety Check**
    st.write("### Structural Safety Check")
    st.write(f"🔹 **Calculated Bending Moment:** {moment:.2f} kN·m")
    st.write(f"🔹 **Calculated Shear Force:** {shear_force:.2f} kN")
    st.write(f"🔹 **Calculated Bending Stress:** {stress:.2f} MPa")
    st.write(f"🔹 **Allowable Stress for {material}:** {allowable_stress:.2f} MPa")

    if stress <= allowable_stress:
        st.success("✅ Beam/Column is safe under applied loading.")
    else:
        st.error("⚠️ WARNING: Beam/Column may fail under applied loads. Consider increasing section size.")

    # **Step 4: Visualization of Load Distribution**
    st.write("### Load Distribution Chart")
    fig = px.bar(st.session_state.structural_data, x="Load Type", y="Load Value (kN)", title="Load Distribution on Structure")
    st.plotly_chart(fig, use_container_width=True)

    # **Step 5: Saving Analysis Report**
    st.write("### Save Analysis Report")
    if st.button("Save Structural Analysis Report"):
        report = f"""
        **Structural Analysis Report**
        ------------------------------
        - **Total Load:** {total_load} kN
        - **Maximum Load:** {max_load} kN
        - **Selected Load Combination:** {selected_combination}
        - **Applied Combined Load:** {combined_load:.2f} kN
        - **Beam/Column Material:** {material}
        - **Beam Length:** {beam_length} m
        - **Bending Moment:** {moment:.2f} kN·m
        - **Shear Force:** {shear_force:.2f} kN
        - **Bending Stress:** {stress:.2f} MPa
        - **Allowable Stress:** {allowable_stress:.2f} MPa
        - **Structural Safety:** {"SAFE ✅" if stress <= allowable_stress else "UNSAFE ⚠️"}
        """

        # Save to file
        with open("uploads/structural_analysis_report.txt", "w") as file:
            file.write(report)
        st.success("📄 Report saved successfully. Find it in the 'uploads' folder.")

