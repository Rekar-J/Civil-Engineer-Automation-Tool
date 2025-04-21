# home.py
import streamlit as st
import os
import requests

HOME_BANNER_PATH = "home_banner.jpg"

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool")

    # Greeting
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found—please log in again.")

    # Two‑column intro
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        ### About This Application
        The **Civil Engineer Automation Tool** helps automate:
        - 🏗️ Structural & Geotechnical Analysis  
        - 🌊 Hydraulic & Hydrological Simulations  
        - 📅 Project Management & Scheduling  
        - ✅ Compliance Verification & Reporting  
        - 🔗 Collaboration & Documentation  
        Use the sidebar to explore each feature.
        """)
    with col2:
        st.subheader("Current Banner")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No home banner image found.")

    st.markdown("---")

    # Banner manager
    with st.expander("Manage Home Banner Image"):
        st.write("Upload, fetch from URL, or delete the banner.")

        # 1) Upload
        uploaded = st.file_uploader("Upload image (PNG/JPG)", type=["png","jpg","jpeg"])
        if uploaded:
            os.makedirs(os.path.dirname(HOME_BANNER_PATH) or ".", exist_ok=True)
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("Image uploaded!")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.markdown("---")

        # 2) Fetch from URL
        url = st.text_input("Or enter an image URL:", key="banner_url")
        if st.button("Fetch & Set from URL"):
            if not url:
                st.error("Please enter a URL.")
            else:
                try:
                    resp = requests.get(url, timeout=10)
                    ctype = resp.headers.get("Content-Type","")
                    if resp.status_code == 200 and ctype.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(resp.content)
                        st.success("Fetched & saved!")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("That URL did not return an image.")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("---")

        # 3) Delete
        if st.button("Delete/Reset Banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("Banner deleted.")
            else:
                st.info("No banner to delete.")

    st.markdown("---")
    st.info("Use the left sidebar to navigate the rest of the app.")
