import streamlit as st
import pandas as pd

def run():
    st.title("📅 Project Management")

    st.write("This section provides tools for scheduling, resource allocation, and project tracking.")

    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])

    ### RESOURCE ALLOCATION (RESTORED) ###
    with tabs[1]:  
        st.header("Resource Allocation")
        st.subheader("📌 About Resource Allocation")
        st.info("Assign **labor, equipment, and materials** to different tasks.")

        resource = st.text_input("Enter Resource Name", key="resource_name")
        assigned_task = st.text_input("Assigned Task", key="assigned_task")

        if "resource_data" not in st.session_state:
            st.session_state.resource_data = pd.DataFrame(columns=["Resource", "Assigned Task"])

        if st.button("Allocate Resource"):
            new_row = pd.DataFrame({"Resource": [resource], "Assigned Task": [assigned_task]})
            st.session_state.resource_data = pd.concat([st.session_state.resource_data, new_row], ignore_index=True)

        st.write("### Resource Allocation")
        st.dataframe(st.session_state.resource_data)

    ### PROGRESS MONITORING (RESTORED) ###
    with tabs[2]:  
        st.header("Progress Monitoring")
        st.subheader("📌 About Progress Monitoring")
        st.info("Track **project completion and task status**.")

        task_name = st.text_input("Enter Task Name", key="progress_task_name")
        progress_percentage = st.slider("Completion Percentage", 0, 100, step=5, key="progress_slider")

        if "progress_data" not in st.session_state:
            st.session_state.progress_data = pd.DataFrame(columns=["Task", "Progress (%)"])

        if st.button("Add Progress Data"):
            new_row = pd.DataFrame({"Task": [task_name], "Progress (%)": [progress_percentage]})
            st.session_state.progress_data = pd.concat([st.session_state.progress_data, new_row], ignore_index=True)

        st.write("### Task Progress")
        st.dataframe(st.session_state.progress_data)
