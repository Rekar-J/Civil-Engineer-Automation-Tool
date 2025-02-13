import streamlit as st
import pandas as pd
import os

def run():
    st.title("📂 Collaboration and Documentation")

    st.write("This section provides tools for managing project documents and communication.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    ### DOCUMENT MANAGEMENT (RESTORED) ###
    with tabs[0]:  
        st.header("Document Management")
        st.subheader("📌 About Document Management")
        st.info("Upload, store, and manage project documents with **version control and sharing options**.")

        # Ensure the 'uploads' directory exists
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        uploaded_file = st.file_uploader("Upload Project Document", type=["pdf", "docx", "xlsx"], key="doc_upload")

        if "document_data" not in st.session_state:
            st.session_state.document_data = pd.DataFrame(columns=["File Name", "File Path"])

        if uploaded_file:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            new_row = pd.DataFrame({"File Name": [uploaded_file.name], "File Path": [file_path]})
            st.session_state.document_data = pd.concat([st.session_state.document_data, new_row], ignore_index=True)
            st.success(f"📄 {uploaded_file.name} uploaded successfully!")

        st.write("### Stored Documents")
        st.dataframe(st.session_state.document_data)

    ### COMMUNICATION TOOLS (UNCHANGED) ###
    with tabs[1]:  
        st.header("Communication Tools")
        st.subheader("📌 About Communication Tools")
        st.info("Facilitates team communication with **messaging, notifications, and meeting scheduling**.")

        message = st.text_area("Send a Message", key="comm_message")
        if st.button("Send Message", key="send_message"):
            st.success("📩 Message sent successfully!")

        meeting_date = st.date_input("Schedule a Meeting", key="meeting_date")
        meeting_time = st.time_input("Meeting Time", key="meeting_time")

        if st.button("Schedule Meeting", key="schedule_meeting"):
            st.success(f"📅 Meeting scheduled on {meeting_date} at {meeting_time}")
