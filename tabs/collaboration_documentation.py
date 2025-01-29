import streamlit as st
import pandas as pd

def run():
    st.title("🤝 Collaboration and Documentation")
    st.write("Collaborate effectively and manage project documentation.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    with tabs[0]:
        st.header("Document Management")
        version_data = pd.DataFrame({
            "File": ["Design_v1.pdf", "Design_v2.pdf", "Report_v1.docx"],
            "Version": [1, 2, 1],
            "Last Updated": ["2025-01-01", "2025-01-15", "2025-01-20"]
        })
        st.dataframe(version_data)

    with tabs[1]:
        st.header("Communication Tools")
        meetings = pd.DataFrame({
            "Date": ["2025-01-10", "2025-01-17", "2025-01-24"],
            "Topic": ["Design Review", "Progress Update", "Final Presentation"],
            "Attendees": ["Team A", "Team B", "Team C"]
        })
        st.dataframe(meetings)
