import streamlit as st
import pandas as pd

def run():
    st.title("📅 Project Management")
    st.write("Plan, allocate resources, and monitor project progress.")

    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])

    with tabs[0]:  # Scheduling
        st.header("Scheduling")
        st.write("Plan your project's timeline.")

        task = st.text_input("Enter Task Name")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

        if "scheduling_data" not in st.session_state:
            st.session_state.scheduling_data = pd.DataFrame(columns=["Task", "Start Date", "End Date"])

        if st.button("Add Task"):
            new_row = pd.DataFrame({"Task": [task], "Start Date": [start_date], "End Date": [end_date]})
            st.session_state.scheduling_data = pd.concat([st.session_state.scheduling_data, new_row], ignore_index=True)

        st.write("### Project Timeline")
        st.dataframe(st.session_state.scheduling_data)

    with tabs[1]:  # Resource Allocation
        st.header("Resource Allocation")
        st.write("Assign resources effectively.")

        resource = st.text_input("Enter Resource Name")
        assigned_task = st.text_input("Assigned Task")

        if "resource_data" not in st.session_state:
            st.session_state.resource_data = pd.DataFrame(columns=["Resource", "Assigned Task"])

        if st.button("Allocate Resource"):
            new_row = pd.DataFrame({"Resource": [resource], "Assigned Task": [assigned_task]})
            st.session_state.resource_data = pd.concat([st.session_state.resource_data, new_row], ignore_index=True)

        st.write("### Resource Allocation")
        st.dataframe(st.session_state.resource_data)

    with tabs[2]:  # Progress Monitoring
        st.header("Progress Monitoring")
        st.write("Track project progress.")

        task_name = st.text_input("Task Name")
        completion = st.slider("Completion Percentage", 0, 100)

        if "progress_data" not in st.session_state:
            st.session_state.progress_data = pd.DataFrame(columns=["Task", "Completion (%)"])

        if st.button("Update Progress"):
            new_row = pd.DataFrame({"Task": [task_name], "Completion (%)": [completion]})
            st.session_state.progress_data = pd.concat([st.session_state.progress_data, new_row], ignore_index=True)

        st.write("### Project Progress")
        st.dataframe(st.session_state.progress_data)
