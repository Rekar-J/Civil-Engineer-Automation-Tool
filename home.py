import streamlit as st

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")

    st.markdown("""
    ### **What is this application?**
    The **Civil Engineer Automation Tool** automates civil engineering calculations, project management, compliance checks, and collaboration.

    ### **Key Features:**
    - 🏗️ **Structural & Geotechnical Analysis**
    - 🌊 **Hydraulic & Hydrological Simulations**
    - 📅 **Project Management & Scheduling**
    - ✅ **Compliance Verification & Reporting**
    - 🔗 **Collaboration & Documentation Tools**
    """)

    st.image("https://via.placeholder.com/800x400.png?text=Civil+Engineering+Automation", use_column_width=True)

    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate different sections.")
