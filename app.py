import streamlit as st
import os
import pandas as pd
import base64
import requests
import uuid

# --- Must be first Streamlit command ---
st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

# ------------------------ GitHub Details ------------------------
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Must be in your Streamlit secrets
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"

# ------------------------ Users CSV ------------------------
USERS_FILE = "users.csv"

def ensure_users_csv():
    """
    Create 'users.csv' if missing or empty, with columns: username, password, token
    """
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        df = pd.DataFrame(columns=["username","password","token"])
        df.to_csv(USERS_FILE, index=False)

def load_users():
    """
    Load users into a DataFrame with columns: username, password, token
    """
    ensure_users_csv()
    try:
        df = pd.read_csv(USERS_FILE)
        for col in ["username","password","token"]:
            if col not in df.columns:
                df[col] = ""
        return df
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["username","password","token"])
        df.to_csv(USERS_FILE, index=False)
        return df

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

def check_credentials(username, password):
    """
    Return True if there's a user row matching (username,password).
    """
    df = load_users()
    row = df[(df["username"] == username) & (df["password"] == password)]
    return not row.empty

def user_exists(username):
    df = load_users()
    return not df[df["username"] == username].empty

def create_user(username, password):
    """
    Create a new user row with empty token
    """
    df = load_users()
    new_row = pd.DataFrame({"username":[username],"password":[password],"token":[""]})
    df = pd.concat([df,new_row], ignore_index=True)
    save_users(df)

def set_token_for_user(username, token):
    """
    Sets or updates the token for a given user row
    """
    df = load_users()
    df.loc[df["username"] == username, "token"] = token
    save_users(df)

def find_user_by_token(token):
    df = load_users()
    row = df[df["token"] == token]
    if row.empty:
        return None
    return row.iloc[0]

# ------------------------ GitHub Database Ops ------------------------
def pull_database():
    resp = requests.get(
        GITHUB_API_URL,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    if resp.status_code == 200:
        content = resp.json().get("content","")
        sha = resp.json().get("sha","")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(DATABASE_FILE,"w",encoding="utf-8") as f:
            f.write(decoded)
        df = pd.read_csv(DATABASE_FILE)
        return df, sha
    else:
        # Create empty
        empty_df = pd.DataFrame(columns=["Tab","SubTab","Data"])
        empty_df.to_csv(DATABASE_FILE, index=False)
        return empty_df, None

def push_database(df, sha=None):
    csv_data = df.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()

    if sha:
        data = {"message":"Update database.csv","content":encoded,"sha":sha}
    else:
        data = {"message":"Create database.csv","content":encoded}
    r = requests.put(
        GITHUB_API_URL,
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
        json=data
    )
    return r.status_code

# ------------------------ Cookie Manager ------------------------
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

# ------------------------ Auth Flow: Sign Up, Login, Logout ------------------------
def sign_up_screen():
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.error("Username/Password cannot be empty.")
        elif user_exists(new_username):
            st.error("Username already exists. Please choose a different one.")
        else:
            create_user(new_username,new_password)
            st.success("Account created! You're now logged in.")

            # Generate random token
            token = str(uuid.uuid4())
            set_token_for_user(new_username, token)

            # Mark user as logged in
            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username
            st.session_state["session_token"] = token

            # Save token in cookie
            set_cookie("session_token", token)

            st.stop()

def login_screen():
    st.title("🔒 Login to Civil Engineer Automation Tool")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    col1,col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if check_credentials(username,password):
                # Generate new token
                token = str(uuid.uuid4())
                set_token_for_user(username, token)

                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["session_token"] = token
                set_cookie("session_token", token)

                st.success("Login successful!")
                st.stop()
            else:
                st.error("Invalid username or password.")

    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.stop()

def logout():
    # If user has a token, remove it from CSV
    if "session_token" in st.session_state and st.session_state["session_token"]:
        df = load_users()
        df.loc[df["token"] == st.session_state["session_token"], "token"] = ""
        save_users(df)

    # Clear cookie
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.info("Logged out successfully!")

# ------------------------ Main App & Session Check ------------------------
def main_app():
    st.session_state["db_df"], st.session_state["db_sha"] = pull_database()

    if st.button("Logout"):
        logout()
        st.stop()

    selected_tab = render_sidebar()

    if selected_tab == "Home":
        run_home()
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

    st.write("---")
    if st.button("Push Changes to GitHub"):
        local_df = pd.read_csv(DATABASE_FILE) if os.path.exists(DATABASE_FILE) else st.session_state["db_df"]
        code = push_database(local_df, sha=st.session_state["db_sha"])
        if code in (200,201):
            st.success("Database successfully pushed to GitHub!")
        else:
            st.error(f"Failed to push to GitHub. Status code: {code}")

def check_cookie_session():
    """
    On page reload, if there's a session_token in cookies, find matching user in CSV.
    If found, auto-login them.
    """
    token_in_cookie = get_cookie("session_token")
    if token_in_cookie:
        user_row = find_user_by_token(token_in_cookie)
        if user_row is not None:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user_row["username"]
            st.session_state["session_token"] = token_in_cookie
        else:
            # No row found, remove invalid cookie
            clear_cookie("session_token")
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["session_token"] = None

def run():
    ensure_users_csv()

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

if __name__=="__main__":
    run()
