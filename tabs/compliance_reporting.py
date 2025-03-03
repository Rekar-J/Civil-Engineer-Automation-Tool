import streamlit as st
import pandas as pd
from datetime import date

# --- Enhanced Standards Verification Section ---
def run_standards_verification():
    st.header("Standards Verification")
    st.subheader("📌 About Compliance Verification")
    st.info("Verify that your project meets applicable safety codes and legal requirements with detailed inputs.")

    # Inputs for compliance check
    requirement = st.text_input("Enter Compliance Requirement", key="comp_requirement")
    regulation_options = ["ACI 318", "IBC", "Local Code", "Custom"]
    regulation = st.selectbox("Select Regulation/Code", regulation_options, key="comp_regulation")
    if regulation == "Custom":
        regulation = st.text_input("Enter Custom Regulation/Code", key="comp_custom_regulation")
    project_component = st.text_input("Project Component (e.g., Beam, Column, Foundation)", key="comp_component")
    risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"], key="comp_risk")
    check_date = st.date_input("Compliance Check Date", value=date.today(), key="comp_date")
    status_options = ["Pass", "Fail", "Pending"]
    compliance_status = st.selectbox("Compliance Status", status_options, key="comp_status")

    # Initialize session state DataFrame if not exists
    if "compliance_data" not in st.session_state:
        st.session_state.compliance_data = pd.DataFrame(columns=[
            "Requirement", "Regulation", "Project Component", "Risk Level", "Date", "Status"
        ])

    if st.button("Add Compliance Check", key="add_compliance"):
        new_row = pd.DataFrame({
            "Requirement": [requirement],
            "Regulation": [regulation],
            "Project Component": [project_component],
            "Risk Level": [risk_level],
            "Date": [check_date],
            "Status": [compliance_status]
        })
        st.session_state.compliance_data = pd.concat(
            [st.session_state.compliance_data, new_row], ignore_index=True
        )
        st.success("Compliance check added!")

    st.write("### Compliance Checks")
    st.dataframe(st.session_state.compliance_data)


# --- Enhanced Report Generation Section ---
def run_report_generation():
    st.header("Report Generation")
    st.subheader("📌 About Report Generation")
    st.info("Generate detailed compliance and engineering reports for documentation and legal approval.")

    # Inputs for report generation
    report_title = st.text_input("Enter Report Title", key="report_title")
    report_date = st.date_input("Report Date", value=date.today(), key="report_date")
    report_author = st.text_input("Report Author", key="report_author")
    report_summary = st.text_area("Enter Report Summary", key="report_summary")
    report_content = st.text_area("Enter Detailed Report Content", key="report_content")
    template_options = ["Standard", "Executive Summary", "Detailed Analysis"]
    report_template = st.selectbox("Select Report Template", template_options, key="report_template")

    # Initialize session state DataFrame if not exists
    if "report_data" not in st.session_state:
        st.session_state.report_data = pd.DataFrame(columns=[
            "Title", "Date", "Author", "Template", "Summary", "Content"
        ])

    if st.button("Generate Report", key="generate_report"):
        new_row = pd.DataFrame({
            "Title": [report_title],
            "Date": [report_date],
            "Author": [report_author],
            "Template": [report_template],
            "Summary": [report_summary],
            "Content": [report_content]
        })
        st.session_state.report_data = pd.concat(
            [st.session_state.report_data, new_row], ignore_index=True
        )
        st.success("Report generated successfully!")

    st.write("### Generated Reports")
    st.dataframe(st.session_state.report_data)

    # Report Preview (Optional)
    if not st.session_state.report_data.empty:
        selected_index = st.selectbox("Select Report to Preview", st.session_state.report_data.index, key="report_preview_index")
        selected_report = st.session_state.report_data.loc[selected_index]
        st.markdown("## Report Preview")
        st.markdown(f"**Title:** {selected_report['Title']}")
        st.markdown(f"**Date:** {selected_report['Date']}")
        st.markdown(f"**Author:** {selected_report['Author']}")
        st.markdown(f"**Template:** {selected_report['Template']}")
        st.markdown(f"**Summary:** {selected_report['Summary']}")
        st.markdown("---")
        st.markdown(f"{selected_report['Content']}")

# --- Merged Compliance and Reporting Section ---
def run():
    st.title("✅ Compliance and Reporting")
    st.write("This section ensures compliance with regulations and generates detailed engineering reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:
        run_standards_verification()
    with tabs[1]:
        run_report_generation()
