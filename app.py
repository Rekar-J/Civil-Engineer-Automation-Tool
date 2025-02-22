import streamlit as st
import os
import pandas as pd
import base64
import requests
import uuid

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
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"  # MUST match your repo exactly

# Filenames
DATABASE_FILE = "database.csv"
USERS_FILE = "users.csv"

# GitHub API endpoints for each file
DATABASE_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
USERS_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{USERS_FILE}"

# GitHub headers
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

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

# -------------- Pull/Push database.csv --------------
def pull_database():
    """Pull database.csv from GitHub and store locally."""
    resp = requests.get(DATABASE_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        content = resp.json().get("content","")
        sha = resp.json().get("sha","")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(DATABASE_FILE,"w",encoding="utf-8") as f:
            f.write(decoded)
        df = pd.read_csv(DATABASE_FILE)
        return df, sha
    else:
        empty_df = pd.DataFrame(columns=["Tab","SubTab","Data"])
        empty_df.to_csv(DATABASE_FILE, index=False)
        return empty_df, None

def push_database(df, sha=None):
    """Push the updated database.csv to GitHub."""
    csv_data = df.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()

    data = {
        "message": "Update database.csv" if sha else "Create database.csv",
        "content": encoded
    }
    if sha:
        data["sha"] = sha

    r = requests.put(DATABASE_API_URL, headers=HEADERS, json=data)
    return r.status_code

# -------------- Pull/Push users.csv --------------
def pull_users():
    """Pull users.csv from GitHub and store locally."""
    resp = requests.get(USERS_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        content = resp.json().get("content","")
        sha = resp.json().get("sha","")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(USERS_FILE,"w",encoding="utf-8") as f:
            f.write(decoded)
        df = pd.read_csv(USERS_FILE)
        return df, sha
    else:
        # Create empty
        df = pd.DataFrame(columns=["username","password","token"])
        df.to_csv(USERS_FILE, index=False)
        return df, None

def push_users(df, sha=None):
    """Push updated users.csv to GitHub."""
    csv_data = df.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()

    data = {
        "message": "Update users.csv" if sha else "Create users.csv",
        "content": encoded
    }
    if sha:
        data["sha"] = sha

    r = requests.put(USERS_API_URL, headers=HEADERS, json=data)
    return r.status_code

# -------------- Load/save users in memory --------------
# We keep a local copy of users in memory to avoid repeated pull requests.
USERS_DF = pd.DataFrame(columns=["username","password","token"])
USERS_SHA = None

def load_users_local():
    """Return the in-memory users DataFrame."""
    global USERS_DF
    return USERS_DF.copy()

def save_users_local(df):
    """Update the in-memory users and also push changes to GitHub."""
    global USERS_DF, USERS_SHA
    USERS_DF = df.copy()  # update in-memory
    # push to GitHub
    status = push_users(USERS_DF, sha=USERS_SHA)
    if status in [200,201]:
        st.success("users.csv updated in GitHub successfully.")
    else:
        st.error(f"Failed to push users.csv to GitHub. Status code: {status}")

def ensure_columns(df):
    for col in ["username","password","token"]:
        if col not in df.columns:
            df[col] = ""
    return df

# -------------- In-memory setup --------------
def pull_users_init():
    """Pull users.csv from GitHub at startup."""
    global USERS_DF, USERS_SHA
    df, sha = pull_users()
    df = ensure_columns(df)
    USERS_DF = df
    USERS_SHA = sha

# -------------- Basic user mgmt --------------
def user_exists(username):
    df = load_users_local()
    return not df[df["username"] == username].empty

def check_credentials(username,password):
    df = load_users_local()
    row = df[(df["username"] == username) & (df["password"] == password)]
    return not row.empty

def create_user(username,password):
    df = load_users_local()
    new_row = pd.DataFrame({
        "username":[username],
        "password":[password],
        "token":[""]
    })
    df = pd.concat([df,new_row], ignore_index=True)
    save_users_local(df)

def set_token_for_user(username, token):
    df = load_users_local()
    df.loc[df["username"]==username,"token"]=token
    save_users_local(df)

def find_user_by_token(token):
    df = load_users_local()
    row = df[df["token"]==token]
    if row.empty:
        return None
    return row.iloc[0]

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"]==token,"token"] = ""
    save_users_local(df)

# -------------- Sign Up / Login / Logout Flow --------------
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

    c1,c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_credentials(username,password):
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
    if "session_token" in st.session_state:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")

    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.info("Logged out successfully!")

# -------------- Main App --------------
def main_app():
    # pull database.csv each time in case changes
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

# -------------- Check Cookie on Refresh --------------
def check_cookie_session():
    token_in_cookie = get_cookie("session_token")
    if token_in_cookie:
        row = find_user_by_token(token_in_cookie)
        if row is not None:
            st.session_state["logged_in"] = True
            st.session_state["username"] = row["username"]
            st.session_state["session_token"] = token_in_cookie
        else:
            clear_cookie("session_token")
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["session_token"] = None

def run():
    # 1) Pull users.csv from GitHub at startup
    pull_users_init()

    # 2) Initialize session
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "sign_up" not in st.session_state:
        st.session_state["sign_up"] = False
    if "session_token" not in st.session_state:
        st.session_state["session_token"] = None

    # 3) Check cookie for existing session
    check_cookie_session()

    # 4) Route to login or main app
    if not st.session_state["logged_in"]:
        if st.session_state["sign_up"]:
            sign_up_screen()
        else:
            login_screen()
    else:
        main_app()

def pull_users_init():
    """Pull users.csv from GitHub at app startup so we have the latest data in memory."""
    global USERS_DF, USERS_SHA
    df, sha = pull_users()
    # store in memory
    df = ensure_columns(df)
    # But we can store it in a global or pass around
    # We'll do that in memory approach with "load_users_local", but let's do it here:
    # We'll just store globally for demonstration:
    # But let's do it the simpler way for demonstration:
    global _USERS_DF
    global _USERS_SHA
    _USERS_DF = df.copy()
    _USERS_SHA = sha

def pull_users():
    """Pull from GitHub to local 'users.csv'."""
    resp = requests.get(USERS_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        content = resp.json().get("content","")
        sha = resp.json().get("sha","")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(USERS_FILE,"w",encoding="utf-8") as f:
            f.write(decoded)
        df = pd.read_csv(USERS_FILE)
        return df, sha
    else:
        df = pd.DataFrame(columns=["username","password","token"])
        df.to_csv(USERS_FILE,index=False)
        return df, None

def push_users_local():
    """Push the local 'users.csv' to GitHub."""
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE)
        # We'll need to keep track of the 'sha' for users.csv if we want to update it
        # We can do the same approach as database. This is a simplified approach w/o sha.
        csv_data = df.to_csv(index=False)
        encoded = base64.b64encode(csv_data.encode()).decode()
        data = {"message":"Update users.csv","content":encoded}
        r = requests.put(USERS_API_URL, headers=HEADERS, json=data)
        return r.status_code
    return None

def ensure_columns(df):
    for c in ["username","password","token"]:
        if c not in df.columns:
            df[c] = ""
    return df

if __name__ == "__main__":
    run()
