import streamlit as st
import pandas as pd

def run():
    # Title and subheader for the section
    st.header("Standards Verification")
    st.subheader("📌 About Compliance Verification")
    st.info("Check if your project **meets safety codes and legal requirements**.")

    # Input fields for the requirement name and compliance status
    requirement = st.text_input("Enter Requirement Name", key="requirement_name")
    status_options = ["Pass", "Fail", "Pending"]
    compliance_status = st.selectbox("Select Compliance Status", status_options, key="compliance_status")

    # Initialize session state to store compliance data if not already done
    if "compliance_data" not in st.session_state:
        st.session_state.compliance_data = pd.DataFrame(columns=["Requirement", "Status"])

    # Button to add the compliance check entry
    if st.button("Add Compliance Check", key="add_compliance"):
        # Create a new row of data to add
        new_row = pd.DataFrame({"Requirement": [requirement], "Status": [compliance_status]})
        # Append the new row to the session state DataFrame
        st.session_state.compliance_data = pd.concat([st.session_state.compliance_data, new_row], ignore_index=True)

    # Display the compliance data in a table
    st.write("### Compliance Data")
    st.dataframe(st.session_state.compliance_data)
