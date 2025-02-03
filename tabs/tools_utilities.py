import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("🔧 Tools and Utilities")

    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    ### AUTOMATED DESIGN & DRAFTING ###
    with tabs[0]:  
        st.header("Automated Design & Drafting")
        st.subheader("📌 About Automated Design & Drafting")
        st.info("This tool allows engineers to **upload and manage CAD files for engineering design**.")

        uploaded_file = st.file_uploader("Upload CAD File", type=["dwg", "dxf", "pdf"])
        if uploaded_file:
            st.success("CAD file uploaded successfully!")

    ### QUANTITY TAKEOFF & COST ESTIMATION (ENHANCED) ###
    with tabs[1]:  
        st.header("Quantity Takeoff & Cost Estimation")
        st.subheader("📌 About Quantity Takeoff & Cost Estimation")
        st.info("This tool helps engineers estimate material quantities and costs for construction projects.")

        # Predefined list of construction materials
        material_options = [
            "Concrete", "Steel", "Bricks", "Wood", "Glass", "Rebar", "Cement", 
            "Gravel", "Sand", "Asphalt", "Plywood", "Tiles", "Paint", "Pipes", "Other"
        ]
        
        selected_material = st.selectbox("Select Material", material_options, key="qt_material_select")

        # If "Other" is selected, allow manual entry
        material = selected_material if selected_material != "Other" else st.text_input("Enter Custom Material", key="qt_custom_material")

        # Currency selection
        currency_options = ["USD ($)", "IQD (Iraqi Dinar)", "EUR (€)", "GBP (£)", "Other"]
        selected_currency = st.selectbox("Select Currency", currency_options, key="qt_currency")

        # Allow user to enter custom currency if "Other" is selected
        currency_symbol = selected_currency if selected_currency != "Other" else st.text_input("Enter Custom Currency", key="qt_custom_currency")

        unit_price = st.number_input(f"Enter Unit Price ({currency_symbol}/unit)", min_value=0.0, key="qt_unit_price")
        quantity = st.number_input("Enter Quantity Needed", min_value=0, key="qt_quantity")

        # Notes input
        note = st.text_area("Add Notes (Optional)", key="qt_notes")

        if "cost_estimation_data" not in st.session_state:
            st.session_state.cost_estimation_data = pd.DataFrame(columns=["Material", "Unit Price", "Quantity", "Total Cost", "Currency", "Notes"])

        if st.button("Add Material", key="add_qt_material"):
            total_cost = unit_price * quantity
            new_row = pd.DataFrame({
                "Material": [material], 
                "Unit Price": [unit_price], 
                "Quantity": [quantity], 
                "Total Cost": [total_cost], 
                "Currency": [currency_symbol], 
                "Notes": [note]
            })
            st.session_state.cost_estimation_data = pd.concat([st.session_state.cost_estimation_data, new_row], ignore_index=True)

        st.write("### Cost Estimation Breakdown")
        st.dataframe(st.session_state.cost_estimation_data)

        # Total Cost Summary
        total_project_cost = st.session_state.cost_estimation_data["Total Cost"].sum()
        st.write(f"**Total Project Cost:** {total_project_cost:,.2f} {currency_symbol}")

    ### DATA VISUALIZATION (UNCHANGED) ###
    with tabs[2]:  
        st.header("Data Visualization")
        st.subheader("📌 About Data Visualization")
        st.info("This tool helps engineers visualize project data using interactive charts and graphs.")

        # Sample dataset for visualization
        st.write("### Upload CSV Data for Visualization")
        uploaded_data = st.file_uploader("Upload CSV File", type=["csv"], key="data_viz_upload")

        if uploaded_data:
            df = pd.read_csv(uploaded_data)
            st.write("### Uploaded Data")
            st.dataframe(df)

            # Select column for visualization
            column_options = list(df.columns)
            selected_column = st.selectbox("Select Column for Visualization", column_options, key="data_viz_column")

            # Generate Bar Chart
            st.write("### Data Distribution")
            fig = px.histogram(df, x=selected_column, title=f"Distribution of {selected_column}")
            st.plotly_chart(fig, use_container_width=True)
