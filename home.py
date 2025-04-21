import streamlit as st
import os
import requests

# must match the path in app.py
HOME_BANNER_PATH = "uploads/home header image.jpg"

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Show username
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found—please log in again.")

    # Ensure uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

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
        
        Use the panel on the right to preview or update the home banner below.
        """)
    with col2:
        st.subheader("Current Banner Image")
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image found. Upload or fetch one below.")

    st.write("---")

    with st.expander("Manage Home Banner Image"):
        st.markdown("""
        You can **upload a local image** from your computer, **fetch from a URL**, 
        or **delete** the existing banner. Once you click **Save Home Banner** 
        (in the sidebar’s Home tab) it will be persisted to your GitHub‐backed DB.
        """)

        # --- Option 1: Upload from local desktop ---
        uploaded_file = st.file_uploader(
            "Upload a local image (PNG/JPG)", 
            type=["png", "jpg", "jpeg"], 
            key="home_local_image"
        )
        if uploaded_file is not None:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Local image uploaded!")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.write("---")

        # --- Option 2: Use a web image URL ---
        url_image = st.text_input(
            "Or enter an image URL:", 
            placeholder="https://example.com/your‐banner.jpg",
            key="home_web_image_url"
        )
        if st.button("Fetch & Set Image from URL", key="fetch_url_image"):
            if not url_image.strip():
                st.error("Please enter a valid URL.")
            else:
                try:
                    resp = requests.get(url_image, timeout=10)
                    ctype = resp.headers.get("Content-Type", "")
                    if resp.status_code == 200 and ctype.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(resp.content)
                        st.success("Fetched and saved banner from URL!")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("URL did not return a valid image.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # --- Option 3: Delete/Reset the current banner ---
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("Banner deleted.")
            else:
                st.info("No banner to delete.")

    st.write("---")
    st.write("🚀 **Get started by picking a tab on the left!**")
