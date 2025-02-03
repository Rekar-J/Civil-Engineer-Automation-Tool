import streamlit as st

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")

    st.markdown("""
    ### **What is this application?**
    The **Civil Engineer Automation Tool** is a comprehensive platform designed for civil engineers to automate structural analysis, project management, compliance checks, and collaboration.

    ### **Key Features:**
    - 🏗️ **Structural & Geotechnical Analysis**
    - 🌊 **Hydraulic & Hydrological Simulations**
    - 📅 **Project Management & Scheduling**
    - ✅ **Compliance Verification & Reporting**
    - 🔗 **Collaboration & Documentation Tools**
    """)

    # Image Banner
    st.image("https://via.placeholder.com/800x400.png?text=Civil+Engineering+Automation", use_column_width=True)

    # Quick Navigation Guide
    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate different sections of the tool.")
