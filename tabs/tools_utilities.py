import streamlit as st
import pandas as pd

def run():
    st.title("🔧 Tools and Utilities")

    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    ### QUANTITY TAKEOFF & COST ESTIMATION (RESTORED) ###
    with tabs[1]:  
        st.header("Quantity Takeoff & Cost Estimation")
        st.subheader("📌 About Quantity Takeoff & Cost Estimation")
        st.info("This tool helps engineers estimate material quantities and costs for construction projects.")

        material = st.text_input("Enter Material Name", key="qt_material_name")
        unit_price = st.number_input("Enter Unit Price ($/unit)", min_value=0.0, key="qt_unit_price")
        quantity = st.number_input("Enter Quantity Needed", min_value=0, key="qt_quantity")

        if "cost_estimation_data" not in st.session_state:
            st.session_state.cost_estimation_data = pd.DataFrame(columns=["Material", "Unit Price ($)", "Quantity", "Total Cost ($)"])

        if st.button("Add Material", key="add_qt_material"):
            total_cost = unit_price * quantity
            new_row = pd.DataFrame({"Material": [material], "Unit Price ($)": [unit_price], "Quantity": [quantity], "Total Cost ($)": [total_cost]})
            st.session_state.cost_estimation_data = pd.concat([st.session_state.cost_estimation_data, new_row], ignore_index=True)

        st.write("### Cost Estimation Breakdown")
        st.dataframe(st.session_state.cost_estimation_data)

        # Total Cost Summary
        total_project_cost = st.session_state.cost_estimation_data["Total Cost ($)"].sum()
        st.write(f"**Total Project Cost:** ${total_project_cost:,.2f}")
