# home.py

import streamlit as st
import os
import requests

# Path to banner file at repo root
HOME_BANNER_PATH = "home_banner.jpg"

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Greet user
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found—please log in again.")

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
        
        Use the right panel below to manage your home banner image.
        """)
    with col2:
        st.subheader("Current Banner Image")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image found. Manage it below.")

    st.write("---")

    # Expander for managing banner
    with st.expander("Manage Home Banner Image"):
        # --- 1) Upload local file ---
        uploaded = st.file_uploader(
            "Upload a local image (PNG/JPG)", 
            type=["png", "jpg", "jpeg"],
            key="home_local_image"
        )
        if uploaded:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("✅ Banner uploaded!")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.write("---")

        # --- 2) Fetch from URL ---
        url = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set from URL", key="fetch_url_image"):
            if not url:
                st.error("Please enter a URL.")
            else:
                try:
                    r = requests.get(url, timeout=10)
                    ct = r.headers.get("Content-Type", "")
                    if r.status_code == 200 and ct.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(r.content)
                        st.success("✅ Banner fetched!")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("URL did not return an image.")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.write("---")

        # --- 3) Delete/Reset Banner ---
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("🗑️ Banner deleted.")
            else:
                st.info("No banner to delete.")

    st.write("---")
    st.write("🚀 **Get started by picking a tab on the left!**")
