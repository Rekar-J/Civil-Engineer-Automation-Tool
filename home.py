# home.py

import streamlit as st
import os
import requests

HOME_BANNER_PATH = "uploads/home header image.jpg"

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")

    # Ensure username is displayed
    if "username" in st.session_state and st.session_state["username"]:
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found in session state. Try logging in again.")

    # Two‑column layout: about text + current banner
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### About This Application  
        The **Civil Engineer Automation Tool** is a comprehensive platform 
        designed for civil engineers to automate tasks such as structural 
        analysis, project management, compliance checks, and collaboration.

        **Key Features**:
        - 🏗️ **Structural & Geotechnical Analysis**
        - 🌊 **Hydraulic & Hydrological Simulations**
        - 📅 **Project Management & Scheduling**
        - ✅ **Compliance Verification & Reporting**
        - 🔗 **Collaboration & Documentation Tools**
        
        Use the panel on the left to navigate the different sections of the tool.
        """)

    with col2:
        st.subheader("Current Banner Image")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image found. Please upload or set one below.")

    st.write("---")

    # Expander for banner management
    with st.expander("Manage Home Banner Image"):
        st.markdown("""
        You can **upload** a local image, **fetch** one from a URL, 
        or **delete/reset** the current banner. Changes will appear immediately.
        """)

        # 1) Upload local file
        uploaded_file = st.file_uploader(
            "Upload a local image (PNG/JPG)", 
            type=["png", "jpg", "jpeg"], 
            key="home_local_image"
        )
        if uploaded_file:
            os.makedirs(os.path.dirname(HOME_BANNER_PATH), exist_ok=True)
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Banner uploaded!")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.write("---")

        # 2) Fetch from URL
        url = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set Image from URL", key="fetch_url_image"):
            if not url.strip():
                st.error("Please enter a valid URL.")
            else:
                try:
                    resp = requests.get(url, timeout=10)
                    ctype = resp.headers.get("Content-Type", "")
                    if resp.status_code == 200 and ctype.startswith("image"):
                        os.makedirs(os.path.dirname(HOME_BANNER_PATH), exist_ok=True)
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(resp.content)
                        st.success("Banner fetched from URL!")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("Failed to fetch a valid image.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # 3) Delete/reset
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("Banner deleted.")
            else:
                st.info("No banner to delete.")

    st.write("---")
    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate to **Design & Analysis**, **Project Management**, **Compliance**, and other tools.")
