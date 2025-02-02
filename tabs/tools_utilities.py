import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("🔧 Tools and Utilities")
    st.write("Use advanced tools for drafting, cost estimation, and visualization.")

    tabs = st.tabs(["Automated Design and Drafting", "Quantity Takeoff and Cost Estimation", "Data Visualization"])

    with tabs[0]:  # Automated Design and Drafting
        st.header("Automated Design and Drafting")
        st.image("https://via.placeholder.com/600x400?text=CAD+Preview", caption="Sample CAD Design")
        st.write("Upload and manage your CAD designs.")
        uploaded_file = st.file_uploader("Upload CAD File", type=["dwg", "dxf", "pdf"])
        if uploaded_file:
            st.success("CAD file uploaded successfully!")

    with tabs[1]:  # Quantity Takeoff and Cost Estimation
        st.header("Quantity Takeoff and Cost Estimation")
        st.write("Calculate material quantities and project costs.")

        material = st.text_input("Enter Material Name")
        quantity = st.number_input("Enter Quantity", min_value=1)
        unit_price = st.number_input("Enter Unit Price (USD)", min_value=1)

        if "cost_estimation_data" not in st.session_state:
            st.session_state.cost_estimation_data = pd.DataFrame(columns=["Material", "Quantity", "Unit Price", "Total Cost"])

        if st.button("Add Material"):
            total_cost = quantity * unit_price
            new_row = pd.DataFrame({"Material": [material], "Quantity": [quantity], "Unit Price": [unit_price], "Total Cost": [total_cost]})
            st.session_state.cost_estimation_data = pd.concat([st.session_state.cost_estimation_data, new_row], ignore_index=True)

        st.write("### Material Cost Estimation")
        st.dataframe(st.session_state.cost_estimation_data)

        # Total Project Cost
        total_project_cost = st.session_state.cost_estimation_data["Total Cost"].sum()
        st.write(f"### Total Project Cost: **${total_project_cost:,.2f}**")

    with tabs[2]:  # Data Visualization
        st.header("Data Visualization")
        st.write("Visualize project data with interactive charts.")

        if "cost_estimation_data" in st.session_state and not st.session_state.cost_estimation_data.empty:
            fig = px.pie(st.session_state.cost_estimation_data, names="Material", values="Total Cost", title="Material Cost Breakdown")
            st.plotly_chart(fig)
        else:
            st.write("No data available for visualization.")
