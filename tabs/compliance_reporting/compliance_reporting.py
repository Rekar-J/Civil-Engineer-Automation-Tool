import streamlit as st
from tabs.compliance_reporting.standards_verification import run as standards_verification
from tabs.compliance_reporting.report_generation import run as report_generation

def run():
    # Title and description for the compliance reporting section
    st.title("Compliance Reporting")
    st.write("This section covers compliance verification and report generation.")

    # Tabs for standards verification and report generation
    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:  
        standards_verification()

    with tabs[1]:  
        report_generation()
