import streamlit as st
import pandas as pd
import os
import base64
import requests
from sidebar import render_sidebar

# GitHub repository details
GITHUB_TOKEN = "your_personal_access_token"  # Replace with actual token
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Ensure database file exists
if not os.path.exists(DATABASE_FILE):
    pd.DataFrame(columns=["Tab", "SubTab", "Data"]).to_csv(DATABASE_FILE, index=False)

# Function to load database
def load_database():
    if os.path.exists(DATABASE_FILE):
        return pd.read_csv(DATABASE_FILE)
    return pd.DataFrame(columns=["Tab", "SubTab", "Data"])

# Function to save data to database
def save_to_database(tab, subtab, data):
    db = load_database()
    new_entry = pd.DataFrame({"Tab": [tab], "SubTab": [subtab], "Data": [data]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)
    updated_db.to_csv(DATABASE_FILE, index=False)

# Function to delete a row from database
def delete_from_database(index):
    db = load_database()
    db = db.drop(index)
    db.to_csv(DATABASE_FILE, index=False)

# Ensure uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

# Render Sidebar
selected_tab = render_sidebar()

# Tab Navigation
if selected_tab == "Home":
    import home
    home.run()
elif selected_tab == "Design and Analysis":
    import tabs.design_analysis as design_analysis
    design_analysis.run()
elif selected_tab == "Project Management":
    import tabs.project_management as project_management
    project_management.run()
elif selected_tab == "Compliance and Reporting":
    import tabs.compliance_reporting as compliance_reporting
    compliance_reporting.run()
elif selected_tab == "Tools and Utilities":
    import tabs.tools_utilities as tools_utilities
    tools_utilities.run()
elif selected_tab == "Collaboration and Documentation":
    import tabs.collaboration_documentation as collaboration_documentation
    collaboration_documentation.run()
