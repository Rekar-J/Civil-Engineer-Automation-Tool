import streamlit as st
import os
import requests

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Ensure username is displayed
    if "username" in st.session_state and st.session_state["username"]:
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found in session state. Try logging in again.")

    # Two-column advanced UI layout
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

    # Path to the current home banner image
    HOME_BANNER_PATH = "uploads/home header image.jpg"

    with col2:
        st.subheader("Profile Image")
        # Check if the file exists or if a new image was just uploaded
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            st.info("No banner image found. Please upload or set one below.")

    st.write("---")

    # Expander to manage the home banner image
    with st.expander("Manage Home Banner Image"):
        st.markdown("""
        You can **upload a local image** from your computer or **pull an image from the web** 
        using a URL. You can also **delete/reset** the current banner image.
        
        Once updated, the new banner will appear **immediately** below, 
        and your session remains active without requiring a refresh.
        """)

        # --- Option 1: Upload from local desktop ---
        uploaded_file = st.file_uploader("Upload a local image (PNG/JPG)", 
                                         type=["png", "jpg", "jpeg"], 
                                         key="home_local_image")
        if uploaded_file is not None:
            # Save the uploaded image
            file_path = HOME_BANNER_PATH
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.image(file_path, use_container_width=True)

        st.write("---")

        # --- Option 2: Use a web image URL ---
        url_image = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set Image from URL", key="fetch_url_image"):
            if url_image.strip() == "":
                st.error("Please enter a valid URL.")
            else:
                try:
                    response = requests.get(url_image, timeout=10)
                    content_type = response.headers.get("Content-Type", "")
                    if response.status_code == 200 and content_type.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(response.content)
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("Could not fetch a valid image from the provided URL.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # --- Option 3: Delete/Reset the current banner ---
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
            else:
                st.info("No home banner image found to delete.")

        st.write("---")

    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate different sections of the tool.")
