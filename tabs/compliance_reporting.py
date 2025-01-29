import streamlit as st
import pandas as pd

def run():
    st.title("✅ Compliance and Reporting")
    st.write("Ensure adherence to standards and generate detailed reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:
        st.header("Standards Verification")
        compliance_data = pd.DataFrame({
            "Requirement": ["Fire Safety", "Structural Integrity", "Electrical Standards", "Environmental Impact"],
            "Status": ["Pass", "Pass", "Fail", "Pending"]
        })
        st.dataframe(compliance_data)
        st.write("### Result: Compliance Status")
        if "Fail" in compliance_data["Status"].values:
            st.write("Some requirements are not met. Address the failures immediately.")
        else:
            st.write("All requirements are met. The project complies with standards.")

    with tabs[1]:
        st.header("Report Generation")
        st.write("Generate detailed project reports for stakeholders.")
