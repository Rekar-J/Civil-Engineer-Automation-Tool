import streamlit as st
import pandas as pd

def run():
    st.title("🤝 Collaboration and Documentation")
    st.write("Collaborate effectively and manage project documentation.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    with tabs[0]:  # Document Management
        st.header("Document Management")
        st.write("Manage project documents and track versions.")

        uploaded_file = st.file_uploader("Upload Project Document", type=["pdf", "docx", "xlsx"])
        if uploaded_file:
            st.success("Document uploaded successfully!")

        if "document_data" not in st.session_state:
            st.session_state.document_data = pd.DataFrame(columns=["File Name", "Version", "Last Updated"])

        document_name = st.text_input("Enter Document Name")
        version = st.number_input("Version", min_value=1)
        last_updated = st.date_input("Last Updated")

        if st.button("Add Document Record"):
            new_row = pd.DataFrame({"File Name": [document_name], "Version": [version], "Last Updated": [last_updated]})
            st.session_state.document_data = pd.concat([st.session_state.document_data, new_row], ignore_index=True)

        st.write("### Document Records")
        st.dataframe(st.session_state.document_data)

    with tabs[1]:  # Communication Tools
        st.header("Communication Tools")
        st.write("Schedule meetings and track discussions.")

        meeting_date = st.date_input("Meeting Date")
        meeting_topic = st.text_input("Enter Meeting Topic")
        attendees = st.text_area("Enter Attendees (comma-separated)")

        if "meeting_data" not in st.session_state:
            st.session_state.meeting_data = pd.DataFrame(columns=["Date", "Topic", "Attendees"])

        if st.button("Schedule Meeting"):
            new_row = pd.DataFrame({"Date": [meeting_date], "Topic": [meeting_topic], "Attendees": [attendees]})
            st.session_state.meeting_data = pd.concat([st.session_state.meeting_data, new_row], ignore_index=True)

        st.write("### Scheduled Meetings")
        st.dataframe(st.session_state.meeting_data)
