import streamlit as st
from tabs.standards_verification import run as standards_verification
from tabs.report_generation import run as report_generation

def run():
    st.title("✅ Compliance and Reporting")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:  
        standards_verification()

    with tabs[1]:  
        report_generation()
