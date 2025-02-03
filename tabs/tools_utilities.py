import streamlit as st
import pandas as pd

def run():
    st.title("🔧 Tools and Utilities")

    st.write("This section provides tools for CAD design, cost estimation, and data visualization.")

    tabs = st.tabs(["Automated Design & Drafting", "Quantity Takeoff & Cost Estimation", "Data Visualization"])

    with tabs[0]:  
        st.header("Automated Design & Drafting")
        st.subheader("📌 About Automated Design & Drafting")
        st.info("This tool allows engineers to **upload and manage CAD files for engineering design**.")

        uploaded_file = st.file_uploader("Upload CAD File", type=["dwg", "dxf", "pdf"])
        if uploaded_file:
            st.success("CAD file uploaded successfully!")
