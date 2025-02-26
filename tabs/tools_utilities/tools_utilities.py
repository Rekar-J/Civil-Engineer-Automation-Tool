import streamlit as st
from tabs.automated_design import run as automated_design
from tabs.quantity_takeoff import run as quantity_takeoff
from tabs.data_visualization import run as data_visualization

def run():
    st.title("🔧 Tools and Utilities")

    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    with tabs[0]:  
        automated_design()

    with tabs[1]:  
        quantity_takeoff()

    with tabs[2]:  
        data_visualization()
