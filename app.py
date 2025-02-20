import streamlit as st
import os
import pandas as pd
import base64
import requests
import uuid

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

# ------------------------ GITHUB DETAILS ------------------------
GITHUB_TOKEN = "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"
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ------------------------ USERS CSV (STORES LOGINS + TOKENS) ------------------------
USERS_FILE = "users.csv"

def ensure_users_csv():
    """
    Create 'users.csv' if it doesn't exist or is empty.
    We'll ensure columns: username, password, token
    """
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        df = pd.DataFrame(columns=["username", "password", "token"])
        df.to_csv(USERS_FILE, index=False)

def load_users():
    """
    Load all users into a DataFrame; ensure columns: username, password, token
    """
    ensure_users_csv()
    try:
        df = pd.read_csv(USERS_FILE)
        missing_cols = {"username", "password", "token"} - set(df.columns)
        if missing_cols:
            for col in missing_cols:
                df[col] = ""
            df.to_csv(USERS_FILE, index=False)
        return df
    except pd.errors.EmptyDataError:
        # Re-create with proper columns
        df = pd.DataFrame(columns=["username", "password", "token"])
        df.to_csv(USERS_FILE, index=False)
        return df

def save_users(df):
    """
    Overwrite 'users.csv' with the given DataFrame (username, password, token).
    """
    df.to_csv(USERS_FILE, index=False)

def user_exists(username):
    df = load_users()
    return not df[df["username"] == username].empty

def check_credentials(username, password):
    """
    Return True if there's a row matching (username, password).
    """
    df = load_users()
    row = df[(df["username"] == username) & (df["password"] == password)]
    return not row.empty

def save_user(username, password):
    """
    Add a new user row: (username, password, token="").
    Uses pd.concat(...) instead of .append() to avoid AttributeError in pandas 2.x.
    """
    df = load_users()
    new_row = pd.DataFrame({
        "username": [username],
        "password": [password],
        "token": [""]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_users(df)

def set_token_for_user(username, token):
    """
    Update the 'token' column for this user in 'users.csv'.
    """
    df = load_users()
    df.loc[df["username"] == username, "token"] = token
    save_users(df)

def find_user_by_token(token):
    """
    Return the row matching this token, or None if not found.
    """
    df = load_users()
    match = df[df["token"] == token]
    if match.empty:
        return None
    return match.iloc[0]  # first row

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
        empty_df = pd.DataFrame(columns=["Tab", "SubTab", "Data"])
        empty_df.to_csv(DATABASE_FILE, index=False)
        return empty_df, None

def push_database(df, sha=None):
    """Push updated database.csv to GitHub."""
    csv_data = df.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()
    if sha:
        data = {"message": "Update database.csv", "content": encoded_content, "sha": sha}
    else:
        data = {"message": "Create database.csv", "content": encoded_content}
    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=data)
    return response.status_code

# ------------------------ COOKIE MANAGER ------------------------
COOKIES_PASSWORD = "MY_SUPER_SECRET_PASSWORD_1234"

from streamlit_cookies_manager import EncryptedCookieManager
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

# ------------------------ AUTH FLOW ------------------------
def sign_up_screen():
    """Sign up new user -> auto login -> store token in cookie."""
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.error("Username/Password cannot be empty.")
        elif user_exists(new_username):
            st.error("Username already exists. Please choose a different one.")
        else:
            save_user(new_username, new_password)
            st.success("Account created! You're now logged in.")

            # Generate token
            token = str(uuid.uuid4())
            set_token_for_user(new_username, token)

            st.session_state["logged_in"] = True
            st.session_state["username"] = new_username
            st.session_state["session_token"] = token
            set_cookie("session_token", token)

            st.stop()

def login_screen():
    """Login existing user. If valid, set new token -> cookie."""
    st.title("🔒 Login to Civil Engineer Automation Tool")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_credentials(username, password):
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

    with c2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.stop()

def logout():
    """Remove token from CSV, clear cookie & session state."""
    if "session_token" in st.session_state and st.session_state["session_token"]:
        df = load_users()
        df.loc[df["token"] == st.session_state["session_token"], "token"] = ""
        save_users(df)

    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.info("Logged out successfully!")

def main_app():
    """Main app after login."""
    # Pull database from GitHub
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
        status_code = push_database(local_df, sha=st.session_state["db_sha"])
        if status_code in (200, 201):
            st.success("Database successfully pushed to GitHub!")
        else:
            st.error(f"Failed to push to GitHub. Status code: {status_code}")

def check_cookie_session():
    """
    On reload, if there's a 'session_token' cookie, find the user with that token.
    If found, log them in automatically.
    """
    token_in_cookie = get_cookie("session_token")
    if token_in_cookie:
        user_row = find_user_by_token(token_in_cookie)
        if user_row is not None:
            st.session_state["logged_in"] = True
            st.session_state["username"] = user_row["username"]
            st.session_state["session_token"] = token_in_cookie
        else:
            # No matching user -> remove invalid cookie
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

    # Check for cookie-based session
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
