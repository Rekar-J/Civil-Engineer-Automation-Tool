import streamlit as st
import pandas as pd

def run():
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
