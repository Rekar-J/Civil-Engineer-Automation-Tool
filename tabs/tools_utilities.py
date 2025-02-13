import streamlit as st
import pandas as pd
import plotly.express as px
from database import save_to_database

def run():
    st.title("🔧 Tools and Utilities")

    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    ### QUANTITY TAKEOFF & COST ESTIMATION ###
    with tabs[1]:  
        st.header("Quantity Takeoff & Cost Estimation")
        st.subheader("📌 About Quantity Takeoff & Cost Estimation")
        st.info("This tool helps engineers estimate material quantities and costs for construction projects.")

        # Predefined list of construction materials
        material_options = ["Concrete", "Steel", "Bricks", "Wood", "Glass", "Other"]
        selected_material = st.selectbox("Select Material", material_options, key="qt_material_select")
        material = selected_material if selected_material != "Other" else st.text_input("Enter Custom Material", key="qt_custom_material")

        # Predefined quantity units
        unit_options = {"Concrete": "m³", "Steel": "kg", "Bricks": "pieces", "Other": "Other"}
        selected_unit = st.selectbox("Select Quantity Unit", list(unit_options.values()), key="qt_unit_select")
        if selected_unit == "Other":
            selected_unit = st.text_input("Enter Custom Unit", key="qt_custom_unit")

        # Currency selection
        currency_options = ["USD ($)", "IQD (Iraqi Dinar)", "Other"]
        selected_currency = st.selectbox("Select Currency", currency_options, key="qt_currency")
        currency_symbol = selected_currency if selected_currency != "Other" else st.text_input("Enter Custom Currency", key="qt_custom_currency")

        unit_price = st.number_input(f"Enter Unit Price ({currency_symbol}/{selected_unit})", min_value=0.0, key="qt_unit_price")
        quantity = st.number_input(f"Enter Quantity Needed ({selected_unit})", min_value=0, key="qt_quantity")
        note = st.text_area("Add Notes (Optional)", key="qt_notes")

        if "cost_estimation_data" not in st.session_state:
            st.session_state.cost_estimation_data = pd.DataFrame(columns=["Material", "Unit Price", "Quantity", "Unit", "Total Cost", "Currency", "Notes"])

        if st.button("Add Material", key="add_qt_material"):
            total_cost = unit_price * quantity
            new_row = pd.DataFrame({
                "Material": [material], 
                "Unit Price": [unit_price], 
                "Quantity": [quantity], 
                "Unit": [selected_unit],
                "Total Cost": [total_cost], 
                "Currency": [currency_symbol], 
                "Notes": [note]
            })
            st.session_state.cost_estimation_data = pd.concat([st.session_state.cost_estimation_data, new_row], ignore_index=True)

            # Save data to GitHub
            save_to_database("Tools and Utilities", "Quantity Takeoff & Cost Estimation", new_row.to_dict(orient="records"))

        st.write("### Cost Estimation Breakdown")
        st.dataframe(st.session_state.cost_estimation_data)

        # Total Cost Summary
        total_project_cost = st.session_state.cost_estimation_data["Total Cost"].sum()
        st.write(f"**Total Project Cost:** {total_project_cost:,.2f} {currency_symbol}")
