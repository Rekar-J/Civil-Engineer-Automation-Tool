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

    ### DATA VISUALIZATION (RESTORED) ###
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
