import streamlit as st
import pandas as pd
import os

MESSAGES_FILE = "uploads/messages.csv"
MEETINGS_FILE = "uploads/meetings.csv"

def run():
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
