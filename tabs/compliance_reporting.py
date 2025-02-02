import streamlit as st
import pandas as pd

def run():
    st.title("✅ Compliance and Reporting")
    st.write("Ensure adherence to standards and generate detailed reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:  # Standards Verification
        st.header("Standards Verification")
        st.write("Check compliance with building codes and regulations.")

        requirement = st.text_input("Enter Requirement Name")
        status_options = ["Pass", "Fail", "Pending"]
        compliance_status = st.selectbox("Select Compliance Status", status_options)

        if "compliance_data" not in st.session_state:
            st.session_state.compliance_data = pd.DataFrame(columns=["Requirement", "Status"])

        if st.button("Add Compliance Check"):
            new_row = pd.DataFrame({"Requirement": [requirement], "Status": [compliance_status]})
            st.session_state.compliance_data = pd.concat([st.session_state.compliance_data, new_row], ignore_index=True)

        st.write("### Compliance Data")
        st.dataframe(st.session_state.compliance_data)

        # Compliance Summary
        total_checks = len(st.session_state.compliance_data)
        failed_checks = (st.session_state.compliance_data["Status"] == "Fail").sum()
        passed_checks = (st.session_state.compliance_data["Status"] == "Pass").sum()

        st.write("### Compliance Summary")
        st.write(f"Total Checks: **{total_checks}**")
        st.write(f"Passed: **{passed_checks}**")
        st.write(f"Failed: **{failed_checks}** - Immediate Action Required!")

    with tabs[1]:  # Report Generation
        st.header("Report Generation")
        st.write("Generate detailed project compliance reports.")

        if "compliance_data" in st.session_state and not st.session_state.compliance_data.empty:
            st.download_button("Download Compliance Report", st.session_state.compliance_data.to_csv(index=False), "compliance_report.csv", "text/csv")
        else:
            st.write("No compliance data available.")
