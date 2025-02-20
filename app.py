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
# Replace with your actual secrets or environment variables
GITHUB_TOKEN = "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"
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ------------------------ LOCAL USERS CSV ------------------------
# A minimal example "users.csv" with columns: username,password
# e.g.:
# username,password
# alice,1234
# bob,abcd
# Make sure you have users.csv in the same directory or handle creation below
USERS_FILE = "users.csv"

def ensure_users_csv():
    """Initialize users.csv if it doesn't exist."""
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame({"username": ["alice", "bob"], "password": ["1234", "abcd"]})
        df.to_csv(USERS_FILE, index=False)

def check_credentials(username, password):
    """Check if the given username/password is in users.csv."""
    if not os.path.exists(USERS_FILE):
        return False
    users_df = pd.read_csv(USERS_FILE)
    row = users_df[(users_df["username"] == username) & (users_df["password"] == password)]
    return not row.empty

# ------------------------ GITHUB DATABASE OPERATIONS ------------------------
def pull_database():
    """
    Pull database.csv from GitHub and store locally.
    Returns a DataFrame of the pulled CSV.
    """
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        file_content = response.json().get("content", "")
        sha = response.json().get("sha", "")
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            f.write(decoded_content)
        return pd.read_csv(DATABASE_FILE), sha
    else:
        # If file not found or any other error, create an empty file
        pd.DataFrame(columns=["Tab", "SubTab", "Data"]).to_csv(DATABASE_FILE, index=False)
        return pd.DataFrame(columns=["Tab", "SubTab", "Data"]), None

def push_database(df, sha=None):
    """
    Push the updated database.csv to GitHub.
    If sha is known (file already exists), we update. Otherwise we create a new file.
    """
    csv_data = df.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()
    if sha:
        # Update existing file
        data = {
            "message": "Update database.csv",
            "content": encoded_content,
            "sha": sha
        }
    else:
        # Create new file
        data = {
            "message": "Create database.csv",
            "content": encoded_content
        }
    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=data)
    return response.status_code

# ------------------------ STREAMLIT APP ------------------------
def login_screen():
    """Display the login screen and return True if logged in."""
    st.title("🔒 Login to Civil Engineer Automation Tool")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")
    return st.session_state.get("logged_in", False)

def main_app():
    """
    Main application after successful login.
    Pull database from GitHub, sync changes upon user actions, 
    and show main interface with sidebar navigation.
    """
    st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")
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

    # Example of a "Save to GitHub" button to push changes
    if st.button("Push Changes to GitHub"):
        # Re-read local CSV if changed
        local_df = pd.read_csv(DATABASE_FILE) if os.path.exists(DATABASE_FILE) else st.session_state["db_df"]
        status_code = push_database(local_df, sha=st.session_state["db_sha"])
        if status_code == 200 or status_code == 201:
            st.success("Database successfully pushed to GitHub!")
        else:
            st.error(f"Failed to push to GitHub. Status code: {status_code}")

# ------------------------ MAIN EXECUTION ------------------------
def run():
    ensure_users_csv()  # Ensure users.csv exists
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # If not logged in, show login screen
    if not st.session_state["logged_in"]:
        login_screen()
    else:
        main_app()

if __name__ == "__main__":
    run()
