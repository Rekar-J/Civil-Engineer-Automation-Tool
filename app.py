import streamlit as st
import os
import sys
import pandas as pd
import uuid
import base64
from sidebar import render_sidebar
from home import run as run_home
from tabs.design_analysis.design_analysis import run as run_design_analysis
from tabs.project_management.project_management import run as run_project_management
from tabs.compliance_reporting.compliance_reporting import run as run_compliance_reporting
from tabs.tools_utilities.tools_utilities import run as run_tools_utilities
from tabs.collaboration_documentation.collaboration_documentation import run as run_collaboration_documentation
from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

# ... (rest of the code remains the same)

def main_app():
    from pushpull import pull_database
    db_df, db_sha = pull_database()
    st.session_state["db_df"] = db_df
    st.session_state["db_sha"] = db_sha

    if st.button("Logout"):
        logout()
        st.stop()

    selected_tab = render_sidebar()

    if selected_tab == "Home":
        run_home()
    elif selected_tab == "Design and Analysis":
        run_design_analysis()  # Directly calling the function here without reloading
    elif selected_tab == "Project Management":
        run_project_management()  # Directly calling the function here without reloading
    elif selected_tab == "Compliance and Reporting":
        run_compliance_reporting()  # Directly calling the function here without reloading
    elif selected_tab == "Tools and Utilities":
        run_tools_utilities()  # Directly calling the function here without reloading
    elif selected_tab == "Collaboration and Documentation":
        run_collaboration_documentation()  # Directly calling the function here without reloading

# ... (rest of the code remains the same)
