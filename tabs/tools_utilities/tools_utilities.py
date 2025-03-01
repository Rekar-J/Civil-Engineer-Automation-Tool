import streamlit as st
from tabs.automated_design import run as automated_design  # Ensure this path is correct
from tabs.quantity_takeoff import run as quantity_takeoff
from tabs.data_visualization import run as data_visualization

def run():
    st.title("🔧 Tools and Utilities")
    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    with tabs[0]:  
        automated_design()  # Call the run function from automated_design.py

    with tabs[1]:  
        quantity_takeoff()  # Call the run function from quantity_takeoff.py

    with tabs[2]:  
        data_visualization()  # Call the run function from data_visualization.py
