import streamlit as st
import pandas as pd
import os

# Communication Tools Section
MESSAGES_FILE = "uploads/messages.csv"
MEETINGS_FILE = "uploads/meetings.csv"

def run_communication_tools():
    st.header("Communication Tools")
    st.subheader("📌 About Communication Tools")
    st.info("Facilitates team communication with **messaging, notifications, and meeting scheduling**.")

    # Ensure message storage exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if not os.path.exists(MESSAGES_FILE):
        pd.DataFrame(columns=["User", "Message"]).to_csv(MESSAGES_FILE, index=False)
    if not os.path.exists(MEETINGS_FILE):
        pd.DataFrame(columns=["Date", "Time"]).to_csv(MEETINGS_FILE, index=False)

    # Messaging System
    st.write("### Team Messaging")
    message = st.text_area("Send a Message", key="comm_message")
    if st.button("Send Message", key="send_message"):
        if message.strip():
            messages_df = pd.read_csv(MESSAGES_FILE)
            new_message = pd.DataFrame({"User": [st.session_state.get("username", "Unknown")], "Message": [message]})
            messages_df = pd.concat([messages_df, new_message], ignore_index=True)
            messages_df.to_csv(MESSAGES_FILE, index=False)

    st.write("### Previous Messages")
    messages_df = pd.read_csv(MESSAGES_FILE)
    if not messages_df.empty:
        for _, row in messages_df.iterrows():
            st.markdown(f"🗨️ **{row['User']}**: {row['Message']}")
    else:
        st.info("No messages yet.")

    # Meeting Scheduling
    st.write("### Schedule a Meeting")
    meeting_date = st.date_input("Select a Date", key="meeting_date")
    meeting_time = st.time_input("Select a Time", key="meeting_time")

    if st.button("Schedule Meeting", key="schedule_meeting"):
        meetings_df = pd.read_csv(MEETINGS_FILE)
        new_meeting = pd.DataFrame({"Date": [meeting_date], "Time": [meeting_time]})
        meetings_df = pd.concat([meetings_df, new_meeting], ignore_index=True)
        meetings_df.to_csv(MEETINGS_FILE, index=False)

    st.write("### Upcoming Meetings")
    meetings_df = pd.read_csv(MEETINGS_FILE)
    if not meetings_df.empty:
        for _, row in meetings_df.iterrows():
            st.markdown(f"📅 **{row['Date']} at {row['Time']}**")
    else:
        st.info("No meetings scheduled yet.")

# Document Management Section
UPLOADS_DIR = "uploads/documents"

def run_document_management():
    st.header("Document Management")
    st.subheader("📌 About Document Management")
    st.info("Upload, store, and manage project documents with **version control and sharing options**.")

    # Ensure the 'uploads/documents' directory exists
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    uploaded_file = st.file_uploader("Upload Project Document", type=["pdf", "docx", "xlsx"], key="doc_upload")

    if "document_data" not in st.session_state:
        st.session_state.document_data = pd.DataFrame(columns=["File Name", "File Path"])

    if uploaded_file:
        file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        new_row = pd.DataFrame({"File Name": [uploaded_file.name], "File Path": [file_path]})
        st.session_state.document_data = pd.concat([st.session_state.document_data, new_row], ignore_index=True)

    st.write("### Stored Documents")
    if not st.session_state.document_data.empty:
        for _, row in st.session_state.document_data.iterrows():
            st.markdown(f"📄 **{row['File Name']}**  |  [Download](/{row['File Path']})")
    else:
        st.info("No documents uploaded yet.")

# Merged Collaboration and Documentation Section
def run():
    st.title("📂 Collaboration and Documentation")

    st.write("This section provides tools for managing project documents and communication.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    with tabs[0]:
        run_document_management()

    with tabs[1]:
        run_communication_tools()
