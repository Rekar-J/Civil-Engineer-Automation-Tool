import streamlit as st
import pandas as pd

def run():
    st.header("Scheduling")
    st.subheader("📌 About Scheduling")
    st.info("This tool helps engineers **plan project timelines**, ensuring tasks are scheduled efficiently.")

    task = st.text_input("Enter Task Name", key="schedule_task_name")
    start_date = st.date_input("Start Date", key="schedule_start_date")
    end_date = st.date_input("End Date", key="schedule_end_date")

    if "scheduling_data" not in st.session_state:
        st.session_state.scheduling_data = pd.DataFrame(columns=["Task", "Start Date", "End Date"])

    if st.button("Add Task", key="add_schedule_task"):
        new_row = pd.DataFrame({"Task": [task], "Start Date": [start_date], "End Date": [end_date]})
        st.session_state.scheduling_data = pd.concat([st.session_state.scheduling_data, new_row], ignore_index=True)

    st.write("### Project Timeline")
    st.dataframe(st.session_state.scheduling_data)
