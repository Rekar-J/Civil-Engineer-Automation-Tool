import streamlit as st
import os
import base64
import requests
import pandas as pd
from pushpull import pull_database, push_database

# Local filename for the banner
HOME_BANNER_PATH = "home_banner.jpg"

def sync_home_banner():
    """Pull the banner from the GitHub‐backed database into a local file."""
    # Remove any existing local copy
    if os.path.exists(HOME_BANNER_PATH):
        os.remove(HOME_BANNER_PATH)

    df, _ = pull_database()
    idx = df.index[df["Tab"] == "HomeBanner"].tolist()
    if not idx:
        return
    b64 = df.loc[idx[0], "Data"]
    if not b64:
        return
    try:
        img = base64.b64decode(b64)
        with open(HOME_BANNER_PATH, "wb") as f:
            f.write(img)
    except Exception:
        st.error("🔴 Could not decode the banner image from the database.")

def save_home_banner_to_github():
    """Read the local banner file and push it to the GitHub‐backed database."""
    if not os.path.exists(HOME_BANNER_PATH):
        st.error("⚠️ No banner image to save.")
        return None

    with open(HOME_BANNER_PATH, "rb") as f:
        img_data = f.read()
    b64 = base64.b64encode(img_data).decode()

    df, sha = pull_database()
    idx = df.index[df["Tab"] == "HomeBanner"].tolist()
    if not idx:
        new = pd.DataFrame({
            "Tab": ["HomeBanner"],
            "SubTab": [""],
            "Data": [b64]
        })
        df = pd.concat([df, new], ignore_index=True)
    else:
        df.loc[idx[0], "Data"] = b64

    code = push_database(df, sha)
    return code

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Greeting
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found—please log in again.")

    # Two-column intro
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
        st.subheader("Quick Tips")
        st.info("Navigate via the left sidebar.")

    st.write("---")

    # Show the current banner (pulled fresh from GitHub)
    sync_home_banner()
    if os.path.exists(HOME_BANNER_PATH):
        st.image(HOME_BANNER_PATH, use_container_width=True)
    else:
        st.info("No banner image set. Expand below to add one.")

    # Banner management UI
    with st.expander("Manage Home Banner Image"):
        # 1) Upload local file
        uploaded = st.file_uploader(
            "Upload a local image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="home_local_image"
        )
        if uploaded is not None:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success("Local banner updated.")
            st.image(HOME_BANNER_PATH, use_container_width=True)

        st.write("---")

        # 2) Fetch from URL
        url = st.text_input("Or enter an image URL:", key="home_web_image_url")
        if st.button("Fetch & Set from URL", key="home_fetch_url"):
            if not url.strip():
                st.error("Please enter a valid URL.")
            else:
                try:
                    resp = requests.get(url, timeout=10)
                    ctype = resp.headers.get("Content-Type", "")
                    if resp.status_code == 200 and ctype.startswith("image"):
                        with open(HOME_BANNER_PATH, "wb") as f:
                            f.write(resp.content)
                        st.success("Banner fetched from URL.")
                        st.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("Could not fetch a valid image from that URL.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # 3) Delete/reset
        if st.button("Delete/Reset Banner", key="home_delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("Local banner deleted.")
            else:
                st.info("No banner to delete.")

        st.write("---")

        # 4) Push up to GitHub
        if st.button("Save Banner to GitHub", key="home_save_banner"):
            code = save_home_banner_to_github()
            if code in (200, 201):
                st.success("✅ Home banner saved to GitHub!")
            else:
                st.error(f"❌ Failed to save banner (GitHub status {code}).")

    st.write("---")
    st.write("🚀 **Get started by picking a tab on the left!**")
