import streamlit as st
import pandas as pd

def run():
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
    if not st.session_state.structural_data.empty:
        total_load = st.session_state.structural_data["Load Value (kN)"].sum()
        max_load = st.session_state.structural_data["Load Value (kN)"].max()
        avg_load = st.session_state.structural_data["Load Value (kN)"].mean()
        min_load = st.session_state.structural_data["Load Value (kN)"].min()

        st.write("### Analysis Results")
        st.write(f"- **Total Load:** {total_load:.2f} kN")
        st.write(f"- **Maximum Load:** {max_load:.2f} kN")
        st.write(f"- **Minimum Load:** {min_load:.2f} kN")
        st.write(f"- **Average Load:** {avg_load:.2f} kN")

        # Load Classification System
        if max_load > 500:
            st.warning("⚠️ **High Load Warning**: Ensure structure is designed to handle heavy loads.")
        elif max_load < 100:
            st.success("✅ **Light Load**: Structure is under minimal stress.")

        # Load Distribution Visualization
        st.write("### Load Distribution")
        st.bar_chart(st.session_state.structural_data.set_index("Load Type"))

        # Structural Safety Check based on Load Factor
        st.write("### Safety Factor Analysis")
        load_factor = st.number_input("Enter Load Factor (Typical: 1.5 for Ultimate Load)", min_value=1.0, max_value=3.0, step=0.1, key="load_factor")
        
        ultimate_load = total_load * load_factor
        st.write(f"🔹 **Ultimate Design Load (kN):** {ultimate_load:.2f}")

        if ultimate_load > 1000:
            st.error("❌ **Overloaded Structure!** Consider re-evaluating the design.")
        elif 500 <= ultimate_load <= 1000:
            st.warning("⚠️ **Moderate Load**: Ensure structural integrity checks are performed.")
        else:
            st.success("✅ **Safe Load Design**: The structure is within safe limits.")

        st.success("Ensure compliance with **ACI design load requirements**.")

    else:
        st.info("No load data available. Please enter values to begin analysis.")
