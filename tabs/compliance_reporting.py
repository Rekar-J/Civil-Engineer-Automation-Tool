import streamlit as st
import pandas as pd

# Report Generation Section
def run_report_generation():
    st.header("Report Generation")
    st.subheader("📌 About Report Generation")
    st.info("Generate **detailed compliance and engineering reports** for documentation and legal approval.")

    report_title = st.text_input("Enter Report Title", key="report_title")
    report_content = st.text_area("Enter Report Content", key="report_content")

    if "report_data" not in st.session_state:
        st.session_state.report_data = pd.DataFrame(columns=["Title", "Content"])

    if st.button("Generate Report", key="generate_report"):
        new_row = pd.DataFrame({"Title": [report_title], "Content": [report_content]})
        st.session_state.report_data = pd.concat([st.session_state.report_data, new_row], ignore_index=True)

    st.write("### Generated Reports")
    st.dataframe(st.session_state.report_data)

# Standards Verification Section
def run_standards_verification():
    st.header("Standards Verification")
    st.subheader("📌 About Compliance Verification")
    st.info("Check if your project **meets safety codes and legal requirements**.")

    requirement = st.text_input("Enter Requirement Name", key="requirement_name")
    status_options = ["Pass", "Fail", "Pending"]
    compliance_status = st.selectbox("Select Compliance Status", status_options, key="compliance_status")

    if "compliance_data" not in st.session_state:
        st.session_state.compliance_data = pd.DataFrame(columns=["Requirement", "Status"])

    if st.button("Add Compliance Check", key="add_compliance"):
        new_row = pd.DataFrame({"Requirement": [requirement], "Status": [compliance_status]})
        st.session_state.compliance_data = pd.concat([st.session_state.compliance_data, new_row], ignore_index=True)

    st.write("### Compliance Data")
    st.dataframe(st.session_state.compliance_data)

# Merged Compliance and Reporting Section
def run():
    st.title("✅ Compliance and Reporting")

    st.write("This section ensures compliance with regulations and generates engineering reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:
        run_standards_verification()

    with tabs[1]:
        run_report_generation()
