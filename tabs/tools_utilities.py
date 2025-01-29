import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("🔧 Tools and Utilities")
    st.write("Use advanced tools for drafting, cost estimation, and visualization.")

    tabs = st.tabs(["Automated Design and Drafting", "Quantity Takeoff and Cost Estimation", "Data Visualization"])

    with tabs[0]:
        st.header("Automated Design and Drafting")
        st.image("https://via.placeholder.com/600x400?text=CAD+Preview", caption="Sample CAD Design")
        st.write("Upload and manage your CAD designs.")

    with tabs[1]:
        st.header("Quantity Takeoff and Cost Estimation")
        sample_materials = pd.DataFrame({
            "Material": ["Concrete", "Steel", "Bricks", "Wood"],
            "Quantity": [100, 50, 500, 200],
            "Unit": ["m3", "tons", "pieces", "pieces"]
        })
        st.dataframe(sample_materials)

    with tabs[2]:
        st.header("Data Visualization")
        cost_data = pd.DataFrame({
            "Category": ["Materials", "Labor", "Equipment", "Miscellaneous"],
            "Cost (USD)": [5000, 3000, 2000, 1000]
        })
        fig = px.pie(cost_data, names="Category", values="Cost (USD)", title="Project Cost Breakdown")
        st.plotly_chart(fig)
