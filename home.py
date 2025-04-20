import streamlit as st
import os
import requests

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Show username
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found—please log in again.")

    # Two‑column layout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### About This Application
        The **Civil Engineer Automation Tool** helps automate:
        - 🏗️ Structural & Geotechnical Analysis  
        - 🌊 Hydraulic & Hydrological Simulations  
        - 📅 Project Management & Scheduling  
        - ✅ Compliance Verification & Reporting  
        - 🔗 Collaboration & Documentation  
        Use the sidebar to explore each section.
        """)
    with col2:
        st.write("## Quick Tips")
        st.info("Navigate via the left sidebar.")

    st.write("---")
    st.write("🚀 **Get started by picking a tab on the left!**")
