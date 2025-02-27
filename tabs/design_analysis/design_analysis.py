import streamlit as st
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
        # Force reload of structural_analysis.py
        import importlib
        import tabs.structural_analysis
        importlib.reload(tabs.structural_analysis)
        structural_analysis()

    with tabs[1]:  
        import tabs.geotechnical_analysis
        importlib.reload(tabs.geotechnical_analysis)
        geotechnical_analysis()

    with tabs[2]:  
        import tabs.hydraulic_analysis
        importlib.reload(tabs.hydraulic_analysis)
        hydraulic_analysis()

    with tabs[3]:  
        import tabs.tests
        importlib.reload(tabs.tests)
        tests()
