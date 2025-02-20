import streamlit as st
import os
import pandas as pd
import base64
import requests
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
    """Initialize an empty users.csv if it doesn't exist."""
    if not os.path.exists(USERS_FILE):
        # Create an empty CSV with columns: username, password
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USERS_FILE, index=False)

def load_users():
    """Load all users into a DataFrame."""
    if not os.path.exists(USERS_FILE):
        ensure_users_csv()
        return pd.DataFrame(columns=["username", "password"])
    return pd.read_csv(USERS_FILE)

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
    users_df = load_users()
    row = users_df[(users_df["username"] == username) & (users_df["password"] == password)]
    return not row.empty

# ------------------------ GITHUB DATABASE OPERATIONS ------------------------
def pull_database():
    """Pull database.csv from GitHub and store locally."""
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
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

    if sha:
        data = {
            "message": "Update database.csv",
            "content": encoded_content,
            "sha": sha
        }
    else:
        data = {
            "message": "Create database.csv",
            "content": encoded_content
        }

    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=data)
    return response.status_code

# ------------------------ STREAMLIT APP ------------------------
def sign_up_screen():
    """Sign Up Page: Create a new account."""
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if new_username == "" or new_password == "":
            st.error("Username/Password cannot be empty.")
        elif user_exists(new_username):
            st.error("Username already exists. Please choose a different one.")
        else:
            save_user(new_username, new_password)
            st.success("Account created! Please go back to login.")
            # Stop execution here; next run will see updated session state
            st.stop()

def login_screen():
    """Login Page: Verify existing account."""
    st.title("🔒 Login to Civil Engineer Automation Tool")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful!")
                # Stop execution so the next run will pick up the new session state
                st.stop()
            else:
                st.error("Invalid username or password.")
    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            # Stop execution here to reflect new session state
            st.stop()

def main_app():
    """Main application after successful login."""
    st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")
    # Pull database from GitHub
    st.session_state["db_df"], st.session_state["db_sha"] = pull_database()

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

    # Example "Save to GitHub" button
    st.write("---")
    if st.button("Push Changes to GitHub"):
        local_df = pd.read_csv(DATABASE_FILE) if os.path.exists(DATABASE_FILE) else st.session_state["db_df"]
        status_code = push_database(local_df, sha=st.session_state["db_sha"])
        if status_code in (200, 201):
            st.success("Database successfully pushed to GitHub!")
        else:
            st.error(f"Failed to push to GitHub. Status code: {status_code}")

def run():
    """Entry point of the app."""
    # Ensure we have an empty users.csv if not present
    ensure_users_csv()

    # Initialize session variables if not set
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "sign_up" not in st.session_state:
        st.session_state["sign_up"] = False

    # If not logged in, show login or sign-up screen
    if not st.session_state["logged_in"]:
        if st.session_state["sign_up"]:
            sign_up_screen()
        else:
            login_screen()
    else:
        main_app()

if __name__ == "__main__":
    run()
