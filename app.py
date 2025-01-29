### app.py ###

import streamlit as st
from sidebar import render_sidebar
from tabs import design_analysis, project_management, compliance_reporting, tools_utilities, collaboration_documentation
import os


# Initialize uploads directory
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Main Application
st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide", page_icon="🛠️")

# Render Sidebar
selected_tab = render_sidebar()

if selected_tab == "Home":
    st.title("🏠 Home")
    st.write("Welcome to the Civil Engineer Automation Tool. Upload and manage your project media files.")

    with st.expander("Upload Media Files"):
        uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])
        if uploaded_file:
            file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"{file_type} uploaded successfully!")

elif selected_tab == "Design and Analysis":
    design_analysis.run()

elif selected_tab == "Project Management":
    project_management.run()

elif selected_tab == "Compliance and Reporting":
    compliance_reporting.run()

elif selected_tab == "Tools and Utilities":
    tools_utilities.run()

elif selected_tab == "Collaboration and Documentation":
    collaboration_documentation.run()
