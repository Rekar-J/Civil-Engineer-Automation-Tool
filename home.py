import streamlit as st
import os

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")

    st.markdown("""
    ### About This Application
    The **Civil Engineer Automation Tool** is a comprehensive platform designed for civil engineers to automate structural analysis, project management, compliance checks, and collaboration.

    **Key Features**:
    - 🏗️ **Structural & Geotechnical Analysis**
    - 🌊 **Hydraulic & Hydrological Simulations**
    - 📅 **Project Management & Scheduling**
    - ✅ **Compliance Verification & Reporting**
    - 🔗 **Collaboration & Documentation Tools**
    """)

    # Ensure the 'uploads' directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Display a header image
    st.image("uploads/home header image.jpg", use_container_width=True)

    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate different sections of the tool.")
