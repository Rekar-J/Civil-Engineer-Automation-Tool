# app.py
import streamlit as st
import os
import pandas as pd
import uuid
import base64

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

from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

HOME_BANNER_PATH = "uploads/home header image.jpg"

# In‑memory user store
USERS_DF = pd.DataFrame(columns=["username","password","token"])
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
    for c in ["username","password","token"]:
        if c not in df.columns:
            df[c] = ""
    return df

def pull_users_init():
    global USERS_DF, USERS_SHA
    df, sha = pull_users()
    USERS_DF = ensure_columns(df)
    USERS_SHA = sha

def load_users_local():
    return USERS_DF.copy()

def save_users_local(df):
    global USERS_DF, USERS_SHA
    USERS_DF = df.copy()
    code = push_users(USERS_DF, USERS_SHA)
    if code in (200,201):
        new_df, new_sha = pull_users()
        USERS_DF = ensure_columns(new_df)
        USERS_SHA = new_sha

def user_exists(username):
    df = load_users_local()
    return not df[df["username"]==username].empty

def check_credentials(username, password):
    df = load_users_local()
    return not df[(df["username"]==username)&(df["password"]==password)].empty

def create_user(username, password):
    df = load_users_local()
    new_row = pd.DataFrame({"username":[username],"password":[password],"token":[""]})
    df = pd.concat([df, new_row], ignore_index=True)
    save_users_local(df)

def set_token_for_user(username, token):
    df = load_users_local()
    df.loc[df["username"]==username, "token"] = token
    save_users_local(df)

def find_user_by_token(token):
    df = load_users_local()
    row = df[df["token"]==token]
    return row.iloc[0] if not row.empty else None

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"]==token, "token"] = ""
    save_users_local(df)

def sign_up_screen():
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.error("Both fields are required.")
        elif user_exists(new_username):
            st.error("Username already exists.")
        else:
            create_user(new_username, new_password)
            token = str(uuid.uuid4())
            set_token_for_user(new_username, token)
            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username
            st.session_state["session_token"] = token
            set_cookie("session_token", token)
            st.success("Account created!")
            st.experimental_rerun()

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
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.experimental_rerun()

def logout():
    if "session_token" in st.session_state and st.session_state["session_token"]:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.experimental_rerun()

def sync_home_banner_after_pull():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if "db_df" in st.session_state:
        df = st.session_state["db_df"]
        idx = df.index[df["Tab"]=="HomeBanner"].tolist()
        if idx:
            b64 = df.loc[idx[0], "Data"]
            if b64:
                try:
                    img = base64.b64decode(b64)
                    with open(HOME_BANNER_PATH, "wb") as f:
                        f.write(img)
                except:
                    pass

def save_home_banner_to_github():
    if not os.path.exists(HOME_BANNER_PATH):
        return
    with open(HOME_BANNER_PATH, "rb") as f:
        img = f.read()
    b64 = base64.b64encode(img).decode()
    df, sha = pull_database()
    idx = df.index[df["Tab"]=="HomeBanner"].tolist()
    if not idx:
        new = pd.DataFrame([{"Tab":"HomeBanner","SubTab":"","Data":b64}])
        df = pd.concat([df, new], ignore_index=True)
    else:
        df.loc[idx[0], "Data"] = b64
    push_database(df, sha)

def main_app():
    db_df, db_sha = pull_database()
    st.session_state["db_df"] = db_df
    st.session_state["db_sha"] = db_sha

    sync_home_banner_after_pull()

    if st.button("Logout"):
        logout()

    selected_tab = render_sidebar()

    if selected_tab == "Home":
        run_home()
        if st.button("Save Changes", key="save_home_banner"):
            save_home_banner_to_github()
            st.success("Banner saved!")
    elif selected_tab == "Design and Analysis":
        design_analysis.run()
    elif selected_tab == "Project Management":
        project_management.run()
    elif selected_tab == "Compliance and Reporting":
        compliance_reporting.run()
    elif selected_tab == "Tools and Utilities":
        tools_utilities.run()
    elif selected_tab == "Collaboration and Documentation":
        collaboration_documentation.run()

def check_cookie_session():
    tok = get_cookie("session_token")
    if tok:
        row = find_user_by_token(tok)
        if row is not None:
            st.session_state["logged_in"] = True
            st.session_state["username"] = row["username"]
            st.session_state["session_token"] = tok
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
