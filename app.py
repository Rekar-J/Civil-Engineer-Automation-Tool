import streamlit as st
import os
import pandas as pd
import uuid
import base64
import importlib

# Must be the first Streamlit command
st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

# ---- Import push/pull functions from pushpull.py ----
from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

HOME_BANNER_PATH = "uploads/home header image.jpg"

# -------------- In-memory usage for users.csv --------------
USERS_DF = pd.DataFrame(columns=["username","password","token"])
USERS_SHA = None

DATABASE_DF = pd.DataFrame()

COOKIES_PASSWORD = "MY_SUPER_SECRET_PASSWORD_1234"
cookies = EncryptedCookieManager(prefix="civil_eng_app", password=COOKIES_PASSWORD)
if not cookies.ready():
    st.stop()

def get_cookie(key):
    return cookies.get(key)
def set_cookie(key, value):
    cookies[key] = value
    cookies.save()
def clear_cookie(key):
    if key in cookies:
        del cookies[key]
    cookies.save()

def ensure_columns(df):
    for c in ["username","password","token"]:
        if c not in df.columns:
            df[c] = ""
    return df

def pull_users_init():
    """Pull users.csv from GitHub at app startup and store in memory."""
    global USERS_DF, USERS_SHA
    df, sha = pull_users()
    df = ensure_columns(df)
    USERS_DF = df.copy()
    USERS_SHA = sha

def load_users_local():
    return USERS_DF.copy()

def save_users_local(df):
    """Save user data and push to GitHub."""
    global USERS_DF, USERS_SHA
    USERS_DF = df.copy()
    code = push_users(USERS_DF, USERS_SHA)
    if code in (200,201):
        new_df, new_sha = pull_users()
        new_df = ensure_columns(new_df)
        USERS_DF = new_df.copy()
        USERS_SHA = new_sha

def user_exists(username):
    df = load_users_local()
    return not df[df["username"]==username].empty

def check_credentials(username, password):
    df = load_users_local()
    row = df[(df["username"]==username) & (df["password"]==password)]
    return not row.empty

def create_user(username, password):
    df = load_users_local()
    new_row = pd.DataFrame({"username":[username],"password":[password],"token":[""]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_users_local(df)

def set_token_for_user(username, token):
    df = load_users_local()
    df.loc[df["username"]==username,"token"]=token
    save_users_local(df)

def find_user_by_token(token):
    df = load_users_local()
    row = df[df["token"]==token]
    return None if row.empty else row.iloc[0]

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"]==token,"token"]=""
    save_users_local(df)

def logout():
    """Log the user out and clear session cookies."""
    if "session_token" in st.session_state and st.session_state["session_token"]:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None

def main_app():
    """Main application logic after login."""
    from pushpull import pull_database
    db_df, db_sha = pull_database()
    st.session_state["db_df"] = db_df
    st.session_state["db_sha"] = db_sha

    if st.button("Logout"):
        logout()
        st.stop()

    selected_tab = render_sidebar()

    if selected_tab == "Home":
        run_home()
    elif selected_tab == "Design and Analysis":
        importlib.reload(design_analysis)
        design_analysis.run()
    elif selected_tab == "Project Management":
        importlib.reload(project_management)
        project_management.run()
    elif selected_tab == "Compliance and Reporting":
        importlib.reload(compliance_reporting)
        compliance_reporting.run()
    elif selected_tab == "Tools and Utilities":
        importlib.reload(tools_utilities)
        tools_utilities.run()
    elif selected_tab == "Collaboration and Documentation":
        importlib.reload(collaboration_documentation)
        collaboration_documentation.run()

def run():
    pull_users_init()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "sign_up" not in st.session_state:
        st.session_state["sign_up"] = False
    if "session_token" not in st.session_state:
        st.session_state["session_token"] = None

    if not st.session_state["logged_in"]:
        st.title("🔒 Login to Civil Engineer Automation Tool")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.stop()
    else:
        main_app()

if __name__ == "__main__":
    run()
