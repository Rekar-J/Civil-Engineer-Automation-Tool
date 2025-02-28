import streamlit as st
from .structural_analysis import run as structural_analysis
from .geotechnical_analysis import run as geotechnical_analysis
from .hydraulic_analysis import run as hydraulic_analysis
from .test import run as test

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
        test()
