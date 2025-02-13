import streamlit as st
import pandas as pd
import plotly.express as px

def run():
    st.title("🔧 Tools and Utilities")

    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    ### AUTOMATED DESIGN & DRAFTING (RESTORED) ###
    with tabs[0]:  
        st.header("Automated Design & Drafting")
        st.subheader("📌 About Automated Design & Drafting")
        st.info("This tool allows engineers to **upload and manage CAD files for engineering design**.")

    ### DATA VISUALIZATION (RESTORED) ###
    with tabs[2]:  
        st.header("Data Visualization")
        st.subheader("📌 About Data Visualization")
        st.info("This tool helps engineers visualize project data using interactive charts and graphs.")
