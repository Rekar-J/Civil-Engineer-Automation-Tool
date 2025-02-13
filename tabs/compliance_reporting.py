import streamlit as st
import pandas as pd

def run():
    st.title("✅ Compliance and Reporting")

    st.write("This section ensures compliance with regulations and generates engineering reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    ### STANDARDS VERIFICATION (RESTORED) ###
    with tabs[0]:  
        st.header("Standards Verification")
        st.subheader("📌 About Compliance Verification")
        st.info("Check if your project **meets safety codes and legal requirements**.")

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
