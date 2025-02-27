import streamlit as st
import os
import pandas as pd
import uuid
import base64
import importlib  # Required for reloading modules

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

HOME_BANNER_PATH = "uploads/home header image.jpg"

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
        importlib.reload(design_analysis)  # Reload module before execution
        design_analysis.run()

    elif selected_tab == "Project Management":
        importlib.reload(project_management)
        project_management.run()

    elif selected_tab == "Compliance and Reporting":
        importlib.reload(compliance_reporting)
        compliance_reporting.run()

    elif selected_tab == "Tools and Utilities":
        importlib.reload(tools_utilities)
        tools_utilities.run()

    elif selected_tab == "Collaboration and Documentation":
        importlib.reload(collaboration_documentation)
        collaboration_documentation.run()

def run():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_screen()
    else:
        main_app()

if __name__=="__main__":
    run()
