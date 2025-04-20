# home.py

import streamlit as st
import os
import requests

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Display username
    if "username" in st.session_state and st.session_state["username"]:
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found in session state. Try logging in again.")

    # Two‑column layout
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

        Use the panel on the right to customize the home banner image below 
        without leaving or refreshing this page.
        """)

    HOME_BANNER_PATH = "uploads/home header image.jpg"
    with col2:
        st.subheader("Current Banner Image")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image found. Please upload or set one below.")

    st.write("---")

    with st.expander("Manage Home Banner Image"):
        st.markdown("""
        You can **upload a local image** from your computer or **pull an image from the web** 
        using a URL. You can also **delete/reset** the current banner image.
        
        Once updated, the new banner will appear **immediately** below, 
        and your session remains active without requiring a refresh.
        """)

        # Upload local file
        uploaded_file = st.file_uploader(
            "Upload a local image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="home_local_image"
        )
        if uploaded_file:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.write("---")

        # Fetch from URL
        url_image = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set Image from URL", key="fetch_url_image"):
            if not url_image.strip():
                st.error("Please enter a valid URL.")
            else:
                try:
                    resp = requests.get(url_image, timeout=10)
                    ct = resp.headers.get("Content-Type", "")
                    if resp.status_code == 200 and ct.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(resp.content)
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("Could not fetch a valid image from the provided URL.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # Delete/reset
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.info("Banner image deleted.")
            else:
                st.info("No banner image to delete.")

    st.write("---")
    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate different sections of the tool.")
