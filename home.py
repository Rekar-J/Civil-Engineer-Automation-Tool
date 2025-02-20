import streamlit as st
import os
import requests

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Two-column advanced UI layout
    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("""
        ### About This Application
        The **Civil Engineer Automation Tool** is a comprehensive platform designed 
        for civil engineers to automate tasks such as structural analysis, project 
        management, compliance checks, and collaboration.

        **Key Features**:
        - 🏗️ **Structural & Geotechnical Analysis**
        - 🌊 **Hydraulic & Hydrological Simulations**
        - 📅 **Project Management & Scheduling**
        - ✅ **Compliance Verification & Reporting**
        - 🔗 **Collaboration & Documentation Tools**
        
        This home section provides an overview of the app and allows you to customize 
        the welcome banner image below.
        """)

    # Path to the current home banner image
    HOME_BANNER_PATH = "uploads/home header image.jpg"
    placeholder_image = "uploads/content.txt"  # Some placeholder or fallback if no image exists

    with col2:
        st.subheader("Current Banner Image")
        # Check if the file exists
        if os.path.exists(HOME_BANNER_PATH):
            st.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            # Show a fallback or placeholder
            st.info("No banner image found. Please upload or set one below.")

    st.write("---")

    # Expander to manage the home banner image
    with st.expander("Manage Home Banner Image"):
        st.markdown("""
        You can **upload a local image** from your computer or **pull an image from the web** 
        using a URL. You can also **delete/reset** the current banner image.
        """)

        # --- Option 1: Upload from local desktop ---
        uploaded_file = st.file_uploader("Upload a local image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="home_local_image")
        if uploaded_file is not None:
            # Save the uploaded image to HOME_BANNER_PATH
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Home banner image updated from local file! Refresh the page to see changes.")

        st.write("---")

        # --- Option 2: Use a web image URL ---
        url_image = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set Image from URL", key="fetch_url_image"):
            if url_image.strip() == "":
                st.error("Please enter a valid URL.")
            else:
                try:
                    response = requests.get(url_image, timeout=10)
                    if response.status_code == 200 and response.headers["Content-Type"].startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(response.content)
                        st.success("Home banner image updated from web URL!")
                    else:
                        st.error("Could not fetch a valid image from the provided URL.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # --- Option 3: Delete/Reset the current banner ---
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.warning("The home banner image was deleted. A placeholder will be shown instead.")
            else:
                st.info("No home banner image found to delete.")

    # Final layout below the expander
    st.write("### Quick Start Guide")
    st.info("Use the left sidebar to navigate different sections of the tool. Explore the app to discover automated features for civil engineering tasks.")
