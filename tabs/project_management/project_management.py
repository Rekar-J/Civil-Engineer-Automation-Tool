import streamlit as st
from tabs.project_management.scheduling import run as scheduling
from tabs.project_management.resource_allocation import run as resource_allocation
from tabs.project_management.progress_monitoring import run as progress_monitoring

def run():
    st.title("📅 Project Management")

    st.write("This section provides tools for scheduling, resource allocation, and project tracking.")

    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])

    with tabs[0]:  
        scheduling()

    with tabs[1]:  
        resource_allocation()

    with tabs[2]:  
        progress_monitoring()
