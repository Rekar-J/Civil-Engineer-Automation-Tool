import streamlit as st
import pandas as pd
from database import save_to_database

def run():
    st.title("✅ Compliance and Reporting")

    st.write("This section ensures compliance with regulations and generates engineering reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    ### REPORT GENERATION ###
    with tabs[1]:  
        st.header("Report Generation")
        report_title = st.text_input("Enter Report Title")
        report_content = st.text_area("Enter Report Content")

        if "report_data" not in st.session_state:
            st.session_state.report_data = pd.DataFrame(columns=["Title", "Content"])

        if st.button("Generate Report"):
            new_row = pd.DataFrame({"Title": [report_title], "Content": [report_content]})
            st.session_state.report_data = pd.concat([st.session_state.report_data, new_row], ignore_index=True)

            # Save data to GitHub
            save_to_database("Compliance and Reporting", "Report Generation", new_row.to_dict(orient="records"))

        st.write("### Generated Reports")
        st.dataframe(st.session_state.report_data)
