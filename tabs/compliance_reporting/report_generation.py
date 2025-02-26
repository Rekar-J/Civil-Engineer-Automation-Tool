import streamlit as st
import pandas as pd

def run():
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
