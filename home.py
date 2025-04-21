# home.py

import streamlit as st
import os
import requests

# Path must match what app.py expects
HOME_BANNER_PATH = "home_banner.jpg"

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Greet the user
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found—please log in again.")

    # Two‑column layout: description + current banner
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
        st.subheader("Current Banner")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image set. Upload one below.")

    st.write("---")

    # Banner management UI
    with st.expander("Manage Home Banner"):
        st.markdown("""
        - Upload from your computer  
        - Fetch from an external URL  
        - Delete current banner  
        """)

        uploaded_file = st.file_uploader("Upload a local image", type=["png","jpg","jpeg"])
        if uploaded_file:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("✅ Uploaded local image!")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        url = st.text_input("Or enter an image URL", key="home_url")
        if st.button("Fetch & Upload from URL"):
            if url:
                try:
                    r = requests.get(url, timeout=10)
                    ct = r.headers.get("Content-Type", "")
                    if r.status_code == 200 and ct.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(r.content)
                        st.success("✅ Fetched image from URL!")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("URL did not return a valid image.")
                except Exception as e:
                    st.error(f"Error fetching URL: {e}")
            else:
                st.error("Enter a valid URL.")

        if st.button("Delete Banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("✅ Banner deleted.")
            else:
                st.info("No banner to delete.")

    st.write("---")
    st.info("Use the sidebar to navigate different sections of the tool.")
