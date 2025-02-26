import streamlit as st
from tabs.standards_verification import run as standards_verification
from tabs.report_generation import run as report_generation

def run():
    st.title("✅ Compliance and Reporting")

    st.write("This section ensures compliance with regulations and generates engineering reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:  
        standards_verification()

    with tabs[1]:  
        report_generation()
