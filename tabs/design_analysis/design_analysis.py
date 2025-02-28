import streamlit as st
from tabs.design_analysis.structural_analysis import run as structural_analysis
from tabs.design_analysis.geotechnical_analysis import run as geotechnical_analysis
from tabs.design_analysis.hydraulic_analysis import run as hydraulic_analysis
from tabs.design_analysis.test import run as test  # Use absolute import from design_analysis/test.py

def run():
    st.title("🛠️ Design and Analysis")
    st.write("This section provides tools for analyzing structural loads, geotechnical properties, hydraulic models, and laboratory test results.")

    tabs = st.tabs([
        "Structural Analysis", 
        "Geotechnical Analysis", 
        "Hydraulic and Hydrological Modeling", 
        "Tests"
    ])

    with tabs[0]:
        structural_analysis()

    with tabs[1]:
        geotechnical_analysis()

    with tabs[2]:
        hydraulic_analysis()

    with tabs[3]:
        tests()
