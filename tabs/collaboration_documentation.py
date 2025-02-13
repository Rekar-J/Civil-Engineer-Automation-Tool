import streamlit as st

def run():
    st.title("🗂️ Collaboration and Documentation")

    st.write("This section provides tools for document management and team communication.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    ### COMMUNICATION TOOLS (RESTORED) ###
    with tabs[1]:  
        st.header("Communication Tools")
        st.subheader("📌 About Communication Tools")
        st.info("This tool provides **real-time messaging and meeting scheduling** for engineering teams.")

        st.write("💬 **Team Messaging**")
        message = st.text_area("Send a message to the team")
        if st.button("Send Message"):
            st.success("Message sent successfully!")

        st.write("📅 **Meeting Scheduling**")
        meeting_date = st.date_input("Select Meeting Date")
        meeting_time = st.time_input("Select Meeting Time")
        if st.button("Schedule Meeting"):
            st.success(f"Meeting scheduled on {meeting_date} at {meeting_time}.")
