import streamlit as st
import pandas as pd
from datetime import datetime

def run():
    st.title("📅 Project Management")
    st.write("This section provides advanced tools for scheduling, resource allocation, and project tracking.")

    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])

    # ---------- Scheduling Tab ----------
    with tabs[0]:
        st.header("Scheduling")
        st.subheader("📌 About Scheduling")
        st.info("Plan project timelines with detailed task information and priority settings.")

        # Input fields for scheduling
        task = st.text_input("Enter Task Name", key="schedule_task_name")
        description = st.text_area("Task Description", key="schedule_task_desc")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"], key="schedule_priority")
        start_date = st.date_input("Start Date", key="schedule_start_date")
        end_date = st.date_input("End Date", key="schedule_end_date")
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"], key="schedule_status")

        # Initialize scheduling data in session state if not present
        if "scheduling_data" not in st.session_state:
            st.session_state.scheduling_data = pd.DataFrame(
                columns=["Task", "Description", "Priority", "Start Date", "End Date", "Status", "Created At"]
            )

        # Add a task button
        if st.button("Add Task", key="add_schedule_task"):
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame({
                "Task": [task],
                "Description": [description],
                "Priority": [priority],
                "Start Date": [start_date],
                "End Date": [end_date],
                "Status": [status],
                "Created At": [created_at]
            })
            st.session_state.scheduling_data = pd.concat(
                [st.session_state.scheduling_data, new_row], ignore_index=True
            )
        st.write("### Project Timeline")
        st.dataframe(st.session_state.scheduling_data)

    # ---------- Resource Allocation Tab ----------
    with tabs[1]:
        st.header("Resource Allocation")
        st.subheader("📌 About Resource Allocation")
        st.info("Assign labor, equipment, and materials to tasks with detailed resource information.")

        # Input fields for resource allocation
        resource = st.text_input("Enter Resource Name", key="resource_name")
        resource_type = st.selectbox("Resource Type", ["Labor", "Equipment", "Materials"], key="resource_type")
        assigned_task = st.text_input("Assigned Task", key="assigned_task")
        quantity = st.number_input("Quantity", min_value=0.0, step=1.0, key="resource_quantity")
        unit_cost = st.number_input("Unit Cost", min_value=0.0, step=0.1, key="resource_unit_cost")
        # Total cost calculated automatically if unit cost and quantity are given
        total_cost = quantity * unit_cost

        # Initialize resource allocation data
        if "resource_data" not in st.session_state:
            st.session_state.resource_data = pd.DataFrame(
                columns=["Resource", "Resource Type", "Assigned Task", "Quantity", "Unit Cost", "Total Cost", "Allocated At"]
            )

        # Add resource allocation entry
        if st.button("Allocate Resource", key="allocate_resource"):
            allocated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame({
                "Resource": [resource],
                "Resource Type": [resource_type],
                "Assigned Task": [assigned_task],
                "Quantity": [quantity],
                "Unit Cost": [unit_cost],
                "Total Cost": [total_cost],
                "Allocated At": [allocated_at]
            })
            st.session_state.resource_data = pd.concat(
                [st.session_state.resource_data, new_row], ignore_index=True
            )
        st.write("### Resource Allocation")
        st.dataframe(st.session_state.resource_data)

    # ---------- Progress Monitoring Tab ----------
    with tabs[2]:
        st.header("Progress Monitoring")
        st.subheader("📌 About Progress Monitoring")
        st.info("Monitor project progress with detailed status updates and remarks.")

        # Input fields for progress monitoring
        prog_task = st.text_input("Enter Task Name", key="progress_task_name")
        prog_status = st.selectbox("Task Status", ["Not Started", "In Progress", "Completed"], key="progress_status")
        progress_percentage = st.slider("Completion Percentage", 0, 100, step=5, key="progress_slider")
        remarks = st.text_area("Remarks", key="progress_remarks")

        # Initialize progress monitoring data
        if "progress_data" not in st.session_state:
            st.session_state.progress_data = pd.DataFrame(
                columns=["Task", "Status", "Progress (%)", "Remarks", "Updated At"]
            )

        # Add progress data entry
        if st.button("Add Progress Data", key="add_progress_task"):
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = pd.DataFrame({
                "Task": [prog_task],
                "Status": [prog_status],
                "Progress (%)": [progress_percentage],
                "Remarks": [remarks],
                "Updated At": [updated_at]
            })
            st.session_state.progress_data = pd.concat(
                [st.session_state.progress_data, new_row], ignore_index=True
            )
        st.write("### Task Progress")
        st.dataframe(st.session_state.progress_data)
