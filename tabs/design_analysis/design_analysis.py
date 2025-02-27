import streamlit as st
import importlib
from tabs.structural_analysis import run as structural_analysis
from tabs.geotechnical_analysis import run as geotechnical_analysis
from tabs.hydraulic_analysis import run as hydraulic_analysis
from tabs.tests import run as tests

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
        importlib.reload(structural_analysis)  # Ensure latest version is loaded
        structural_analysis()

    with tabs[1]:  
        importlib.reload(geotechnical_analysis)
        geotechnical_analysis()

    with tabs[2]:  
        importlib.reload(hydraulic_analysis)
        hydraulic_analysis()

    with tabs[3]:  
        importlib.reload(tests)
        tests()
