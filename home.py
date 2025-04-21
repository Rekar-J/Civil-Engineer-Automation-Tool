# home.py

import streamlit as st
import os
import requests
import base64
from pushpull import pull_database, push_database

# Path to banner image in repo root
HOME_BANNER_PATH = "home header image.jpg"

def sync_home_banner_after_pull():
    """
    Pulls the Base64 banner from database.csv (GitHub) and
    writes it over HOME_BANNER_PATH locally.
    """
    df, sha = pull_database()
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
        # if decoding fails, leave any existing file untouched
        pass

def save_home_banner_to_github():
    """
    Reads HOME_BANNER_PATH, encodes it to Base64, and
    pushes (or creates) the HomeBanner row in database.csv.
    Returns the HTTP status code from GitHub.
    """
    if not os.path.exists(HOME_BANNER_PATH):
        st.error("No banner image found to save.")
        return None

    with open(HOME_BANNER_PATH, "rb") as f:
        img = f.read()
    b64 = base64.b64encode(img).decode()

    df, sha = pull_database()
    idx = df.index[df["Tab"] == "HomeBanner"].tolist()

    if not idx:
        # create new row
        new = {
            "Tab": "HomeBanner",
            "SubTab": "",
            "Data": b64
        }
        df = df.append(new, ignore_index=True)
    else:
        df.at[idx[0], "Data"] = b64

    return push_database(df, sha)

def run():
    st.title("🏠 Welcome to the Civil Engineer Automation Tool (Home)")

    # Greet
    if st.session_state.get("username"):
        st.write(f"### 🔵 Welcome, **{st.session_state['username']}!**")
    else:
        st.warning("⚠️ Username not found in session. Please log in again.")

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
        
        Use the panel on the right to manage your home banner image.
        """)
    with col2:
        st.subheader("Current Banner Image")
        placeholder = st.empty()
        if os.path.exists(HOME_BANNER_PATH):
            placeholder.image(HOME_BANNER_PATH, use_container_width=True)
        else:
            placeholder.info("No banner image found.")

    st.write("---")

    # Expander to manage the banner
    with st.expander("Manage Home Banner Image"):
        # 1) Upload local
        upload = st.file_uploader(
            "Upload a local image (PNG/JPG)", 
            type=["png", "jpg", "jpeg"],
            key="home_local_image"
        )
        if upload:
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(upload.getbuffer())
            st.success("✅ Banner uploaded locally.")
            placeholder.image(HOME_BANNER_PATH, use_container_width=True)

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
                        st.success("✅ Banner fetched from URL.")
                        placeholder.image(HOME_BANNER_PATH, use_container_width=True)
                    else:
                        st.error("URL did not return an image.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")

        st.write("---")

        # 3) Delete / Reset
        if st.button("Delete/Reset Banner", key="delete_banner"):
            if os.path.exists(HOME_BANNER_PATH):
                os.remove(HOME_BANNER_PATH)
                st.success("🗑️ Banner deleted locally.")
                placeholder.info("No banner image found.")
            else:
                st.info("No banner to delete.")

    st.write("---")
    st.write("🚀 **Get started by picking a tab on the left!**")
