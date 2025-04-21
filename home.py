# home.py

import streamlit as st
import os
import requests

# Banner image file path (in repo root)
HOME_BANNER_PATH = "home header image.jpg"

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Greet the user
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found in session state. Please log in again.")

    # Two‑column layout: About on the left, banner on the right
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
        
        Use the panel on the right to manage your home banner image.
        """)
    with col2:
        st.subheader("Current Banner Image")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image found. Manage it below.")

    st.write("---")

    # Expander to manage the banner
    with st.expander("Manage Home Banner Image"):
        st.markdown("""
        You can **upload** a local image, **fetch** one from a URL, or **delete/reset** 
        the current banner. Changes take effect immediately.
        """)

        # 1) Upload from local
        uploaded_file = st.file_uploader(
            "Upload a local image (PNG/JPG)", 
            type=["png", "jpg", "jpeg"],
            key="home_local_image"
        )
        if uploaded_file:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✅ Banner uploaded!")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.write("---")

        # 2) Fetch from URL
        url = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set from URL", key="fetch_url_image"):
            if not url.strip():
                st.error("Please enter a valid URL.")
            else:
                try:
                    resp = requests.get(url, timeout=10)
                    ctype = resp.headers.get("Content-Type", "")
                    if resp.status_code == 200 and ctype.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(resp.content)
                        st.success("✅ Banner fetched!")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("URL did not return a valid image.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # 3) Delete / Reset
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("🗑️ Banner deleted.")
            else:
                st.info("No banner to delete.")

    st.write("---")
    st.write("🚀 **Get started by picking a tab on the left!**")
