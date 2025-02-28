import streamlit as st
from design_analysis.structural_analysis import run as structural_analysis
from design_analysis.geotechnical_analysis import run as geotechnical_analysis
from design_analysis.hydraulic_analysis import run as hydraulic_analysis
from tests import run as tests  # Since tests.py is outside `design_analysis/`

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
