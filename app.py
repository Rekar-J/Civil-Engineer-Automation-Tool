import streamlit as st
import os
import pandas as pd
import requests
from sidebar import render_sidebar
from tabs import design_analysis, project_management, compliance_reporting, tools_utilities, collaboration_documentation

# GitHub repository details
GITHUB_TOKEN = "your_personal_access_token"  # Replace with your actual token
GITHUB_REPO = "your_username/your_repository"  # Replace with your GitHub repo
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Ensure the 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

# Render Sidebar
selected_tab = render_sidebar()

if selected_tab == "Home":
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")
    st.write("Upload and manage your project media files.")

    uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])
    if uploaded_file:
        file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{file_type} uploaded successfully!")

# Ensure tabs execute properly
try:
    if selected_tab == "Design and Analysis":
        design_analysis.run()
    elif selected_tab == "Project Management":
        project_management.run()
    elif selected_tab == "Compliance and Reporting":
        compliance_reporting.run()
    elif selected_tab == "Tools and Utilities":
        tools_utilities.run()
    elif selected_tab == "Collaboration and Documentation":
        collaboration_documentation.run()
except Exception as e:
    st.error(f"Error loading tab: {str(e)}")
