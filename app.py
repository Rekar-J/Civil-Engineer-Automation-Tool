import streamlit as st
import os
import pandas as pd
import uuid
import base64
import importlib

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

HOME_BANNER_PATH = "uploads/home header image.jpg"

# ----------------- Initialize Cookies -----------------
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

# ----------------- User Authentication -----------------
USERS_DF = pd.DataFrame(columns=["username", "password", "token"])
USERS_SHA = None

def ensure_columns(df):
    for col in ["username", "password", "token"]:
        if col not in df.columns:
            df[col] = ""
    return df

def pull_users_init():
    global USERS_DF, USERS_SHA
    df, sha = pull_users()
    df = ensure_columns(df)
    USERS_DF = df.copy()
    USERS_SHA = sha

def load_users_local():
    return USERS_DF.copy()

def save_users_local(df):
    global USERS_DF, USERS_SHA
    USERS_DF = df.copy()
    code = push_users(USERS_DF, USERS_SHA)
    if code in (200, 201):
        new_df, new_sha = pull_users()
        new_df = ensure_columns(new_df)
        USERS_DF = new_df.copy()
        USERS_SHA = new_sha

def user_exists(username):
    df = load_users_local()
    return not df[df["username"] == username].empty

def check_credentials(username, password):
    df = load_users_local()
    row = df[(df["username"] == username) & (df["password"] == password)]
    return not row.empty

def create_user(username, password):
    df = load_users_local()
    new_row = pd.DataFrame({"username": [username], "password": [password], "token": [""]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_users_local(df)

def set_token_for_user(username, token):
    df = load_users_local()
    df.loc[df["username"] == username, "token"] = token
    save_users_local(df)

def find_user_by_token(token):
    df = load_users_local()
    row = df[df["token"] == token]
    return row.iloc[0] if not row.empty else None

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"] == token, "token"] = ""
    save_users_local(df)

# ----------------- Authentication Screens -----------------
def sign_up_screen():
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.warning("Username and password cannot be empty.")
        elif user_exists(new_username):
            st.warning("Username already exists. Choose another one.")
        else:
            create_user(new_username, new_password)
            token = str(uuid.uuid4())
            set_token_for_user(new_username, token)
            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username
            st.session_state["session_token"] = token
            set_cookie("session_token", token)
            st.rerun()

def login_screen():
    st.title("🔒 Login to Civil Engineer Automation Tool")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if check_credentials(username, password):
                token = str(uuid.uuid4())
                set_token_for_user(username, token)
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["session_token"] = token
                set_cookie("session_token", token)
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.rerun()

def logout():
    if "session_token" in st.session_state and st.session_state["session_token"]:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.rerun()

# ----------------- Main Application -----------------
def main_app():
    from pushpull import pull_database
    db_df, db_sha = pull_database()
    st.session_state["db_df"] = db_df
    st.session_state["db_sha"] = db_sha

    if st.button("Logout"):
        logout()

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

# ----------------- Check Session and Run App -----------------
def check_cookie_session():
    token = get_cookie("session_token")
    if token:
        user = find_user_by_token(token)
        if user is not None:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user["username"]
            st.session_state["session_token"] = token
        else:
            clear_cookie("session_token")
            st.session_state["logged_in"] = False

def run():
    pull_users_init()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "sign_up" not in st.session_state:
        st.session_state["sign_up"] = False
    if "session_token" not in st.session_state:
        st.session_state["session_token"] = None

    check_cookie_session()

    if not st.session_state["logged_in"]:
        if st.session_state["sign_up"]:
            sign_up_screen()
        else:
            login_screen()
    else:
        main_app()

if __name__ == "__main__":
    run()
