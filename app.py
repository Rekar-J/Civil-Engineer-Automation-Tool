import streamlit as st
import os
import pandas as pd
import base64
import requests
import uuid

# IMPORTANT: Ensure "streamlit-cookies-manager" is in your requirements.txt
# pip install streamlit-cookies-manager

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

# ------------------------ GITHUB DETAILS ------------------------
GITHUB_TOKEN = "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"
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ------------------------ USERS CSV (STORES LOGINS) ------------------------
USERS_FILE = "users.csv"

def ensure_users_csv():
    """Create an empty users.csv if missing or empty."""
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USERS_FILE, index=False)

def load_users():
    """Load all users into a DataFrame, handle if file is empty."""
    ensure_users_csv()
    try:
        df = pd.read_csv(USERS_FILE)
        if df.empty or "username" not in df.columns or "password" not in df.columns:
            ensure_users_csv()
            return pd.DataFrame(columns=["username", "password"])
        return df
    except pd.errors.EmptyDataError:
        ensure_users_csv()
        return pd.DataFrame(columns=["username", "password"])

def save_user(username, password):
    """Add a new user to the users.csv file."""
    users_df = load_users()
    new_row = pd.DataFrame({"username": [username], "password": [password]})
    updated_df = pd.concat([users_df, new_row], ignore_index=True)
    updated_df.to_csv(USERS_FILE, index=False)

def user_exists(username):
    """Check if a username already exists."""
    users_df = load_users()
    return not users_df[users_df["username"] == username].empty

def check_credentials(username, password):
    """Validate if the given username/password is correct."""
    df = load_users()
    row = df[(df["username"] == username) & (df["password"] == password)]
    return not row.empty

# ------------------------ GITHUB DATABASE OPERATIONS ------------------------
def pull_database():
    """Pull database.csv from GitHub and store locally."""
    response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        file_content = response.json().get("content", "")
        sha = response.json().get("sha", "")
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            f.write(decoded_content)
        df = pd.read_csv(DATABASE_FILE)
        return df, sha
    else:
        # If file not found or any other error, create an empty file
        empty_df = pd.DataFrame(columns=["Tab", "SubTab", "Data"])
        empty_df.to_csv(DATABASE_FILE, index=False)
        return empty_df, None

def push_database(df, sha=None):
    """Push the updated database.csv to GitHub."""
    csv_data = df.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()
    data = {
        "message": "Update database.csv" if sha else "Create database.csv",
        "content": encoded_content
    }
    if sha:
        data["sha"] = sha

    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=data)
    return response.status_code

# ------------------------ COOKIE MANAGER (WITH A PASSWORD) ------------------------
# Provide a random string as password. In production, store it in secrets or env var.
COOKIES_PASSWORD = "MY_SUPER_SECRET_PASSWORD_1234"

cookies = EncryptedCookieManager(
    prefix="civil_eng_app", 
    password=COOKIES_PASSWORD  # <--- Provide a password here
)
# If the cookie manager isn't ready, stop execution
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

# ------------------------ LOGIN/LOGOUT & SIGNUP LOGIC ------------------------
def sign_up_screen():
    """Sign up for a new account; auto-login user."""
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if new_username == "" or new_password == "":
            st.error("Username/Password cannot be empty.")
        elif user_exists(new_username):
            st.error("Username already exists. Please choose a different one.")
        else:
            # Save new user locally
            save_user(new_username, new_password)
            st.success("Account created! You're now logged in.")

            # Generate a random token for the new user, store it in cookies
            session_token = str(uuid.uuid4())
            set_cookie("session_token", session_token)

            # Mark them as logged_in in session_state
            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username
            st.session_state["session_token"] = session_token

            st.stop()

def login_screen():
    """Login existing user. If credentials match, store a session token in cookies."""
    st.title("🔒 Login to Civil Engineer Automation Tool")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username

                # Generate new session token
                session_token = str(uuid.uuid4())
                st.session_state["session_token"] = session_token
                # Store in cookie so user remains logged in on reload
                set_cookie("session_token", session_token)

                st.success("Login successful!")
                st.stop()
            else:
                st.error("Invalid username or password.")

    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.stop()

def logout():
    """Clear cookies and session state, forcing user to log in again."""
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.info("Logged out successfully!")

# ------------------------ MAIN APP ------------------------
def main_app():
    """Main application after successful login."""
    st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

    st.session_state["db_df"], st.session_state["db_sha"] = pull_database()

    # Logout button
    if st.button("Logout"):
        logout()
        st.stop()

    # Render Sidebar
    selected_tab = render_sidebar()

    # Navigation
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
        status_code = push_database(local_df, sha=st.session_state["db_sha"])
        if status_code in (200, 201):
            st.success("Database successfully pushed to GitHub!")
        else:
            st.error(f"Failed to push to GitHub. Status code: {status_code}")

def check_cookie_session():
    """
    If a valid session token is stored in the cookie, mark the user as logged_in.
    This runs before the UI to keep the user logged in after reload.
    """
    token_in_cookie = get_cookie("session_token")
    if token_in_cookie and "session_token" in st.session_state:
        # Compare cookie token with in-memory session token
        if token_in_cookie == st.session_state["session_token"]:
            st.session_state["logged_in"] = True
    elif token_in_cookie and "session_token" not in st.session_state:
        # If there's a token in cookie but not in session, adopt it
        st.session_state["session_token"] = token_in_cookie
        st.session_state["logged_in"] = True
        # If you want to track user -> token, you'd need a real DB approach

def run():
    # Ensure we have an empty users.csv if not present
    ensure_users_csv()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "sign_up" not in st.session_state:
        st.session_state["sign_up"] = False
    if "session_token" not in st.session_state:
        st.session_state["session_token"] = None

    # Check cookie-based session before showing login screen
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
