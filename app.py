import streamlit as st
import os
import sys
import pandas as pd
import uuid
import base64
import importlib

# Ensure the repository root (where app.py lives) is on the PYTHONPATH.
repo_root = os.path.abspath(os.path.dirname(__file__))
if repo_root not in sys.path:
    sys.path.append(repo_root)

# st.set_page_config must be the first Streamlit command.
st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home

# Use absolute imports for your packages.
from design_analysis import run as run_design_analysis
from project_management import run as run_project_management
from compliance_reporting import run as run_compliance_reporting
from tools_utilities import run as run_tools_utilities
from collaboration_documentation import run as run_collaboration_documentation

from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

HOME_BANNER_PATH = "uploads/home header image.jpg"

# In-memory storage for users.csv
USERS_DF = pd.DataFrame(columns=["username", "password", "token"])
USERS_SHA = None

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
    for c in ["username", "password", "token"]:
        if c not in df.columns:
            df[c] = ""
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
    return None if row.empty else row.iloc[0]

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"] == token, "token"] = ""
    save_users_local(df)

def sign_up_screen():
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.stop()
        elif user_exists(new_username):
            st.stop()
        else:
            create_user(new_username, new_password)
            token = str(uuid.uuid4())
            set_token_for_user(new_username, token)
            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username
            st.session_state["session_token"] = token
            set_cookie("session_token", token)
            st.stop()

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
            st.stop()
    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.stop()

def logout():
    if "session_token" in st.session_state and st.session_state["session_token"]:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None

def main_app():
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
        importlib.reload(run_design_analysis)
        run_design_analysis()
    elif selected_tab == "Project Management":
        importlib.reload(run_project_management)
        run_project_management()
    elif selected_tab == "Compliance and Reporting":
        importlib.reload(run_compliance_reporting)
        run_compliance_reporting()
    elif selected_tab == "Tools and Utilities":
        importlib.reload(run_tools_utilities)
        run_tools_utilities()
    elif selected_tab == "Collaboration and Documentation":
        importlib.reload(run_collaboration_documentation)
        run_collaboration_documentation()

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
            st.session_state["username"] = None
            st.session_state["session_token"] = None

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
