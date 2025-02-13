import streamlit as st
import os
from sidebar import render_sidebar
from database import load_database, save_to_database
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

# ✅ Ensure the 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

# ✅ Render Sidebar
selected_tab = render_sidebar()

### 🚀 HOME TAB (UPDATED) ###
if selected_tab == "Home":
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")

    st.markdown("""
    ### About This Application
    This tool automates **civil engineering calculations**, compliance checks, cost estimation, and collaboration.
    
    **Key Features**:
    - 🏗️ **Structural & Geotechnical Analysis**
    - 🚰 **Hydraulic & Hydrological Simulations**
    - ✅ **Compliance Verification & Reporting**
    - 📊 **Project Management & Scheduling**
    - 🔧 **Tools for Quantity Takeoff & Cost Estimation**
    - 🤝 **Collaboration & Documentation Management**
    """)

    uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])

    if uploaded_file:
        file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # ✅ Save uploaded file m
