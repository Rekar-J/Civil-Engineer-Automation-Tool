import streamlit as st
import os
import pandas as pd
import base64
import requests
import uuid

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
# We'll import the tabs, but we'll modify them to call back into app.py to do the pushing:
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting  # We skip auto-push here
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation
from home import run as run_home

# ------------------------ GITHUB DETAILS ------------------------
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"

DATABASE_FILE = "database.csv"
USERS_FILE = "users.csv"
HOME_BANNER_PATH = "uploads/home header image.jpg"

DATABASE_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
USERS_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{USERS_FILE}"

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# ------------------------ COOKIE MANAGER ------------------------
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

# ------------------------ GITHUB PULL/PUSH: database.csv ------------------------
def pull_database():
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
        df = pd.DataFrame(columns=["Tab","SubTab","Data"])
        df.to_csv(DATABASE_FILE, index=False)
        return df, None

def push_database(df, sha=None):
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

# ------------------------ GITHUB PULL/PUSH: users.csv ------------------------
def pull_users():
    resp = requests.get(USERS_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        content = resp.json().get("content","")
        sha = resp.json().get("sha","")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(USERS_FILE,"w",encoding="utf-8") as f:
            f.write(decoded)
    else:
        with open(USERS_FILE,"w",encoding="utf-8") as f:
            f.write("username,password,token\n")
        sha = None

    try:
        df = pd.read_csv(USERS_FILE)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["username","password","token"])
        df.to_csv(USERS_FILE, index=False)
    return df, sha

def push_users(df, sha=None):
    csv_data = df.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()
    data = {"message": "Update users.csv" if sha else "Create users.csv", "content": encoded}
    if sha:
        data["sha"] = sha
    r = requests.put(USERS_API_URL, headers=HEADERS, json=data)
    return r.status_code

# -------------- In-memory usage for users.csv --------------
USERS_DF = pd.DataFrame(columns=["username","password","token"])
USERS_SHA = None

def ensure_columns(df):
    for c in ["username","password","token"]:
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
    if code in (200,201):
        st.success("users.csv updated in GitHub successfully.")
        # Re-pull to refresh sha
        new_df, new_sha = pull_users()
        new_df = ensure_columns(new_df)
        USERS_DF = new_df.copy()
        USERS_SHA = new_sha
    else:
        st.error(f"Failed to push users.csv to GitHub. Status: {code}")

# -------------- Basic user management --------------
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
    if row.empty:
        return None
    return row.iloc[0]

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"]==token,"token"]=""
    save_users_local(df)

# -------------- Login/Logout/SignUp Flow --------------
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
            create_user(new_username, new_password)
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

    col1,col2 = st.columns(2)
    with col1:
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
    with col2:
        if st.button("Sign Up"):
            st.session_state["sign_up"]=True
            st.stop()

def logout():
    if "session_token" in st.session_state and st.session_state["session_token"]:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.info("Logged out successfully!")

# ----------------- Save Logic for Automatic GitHub push in tabs -----------------
def save_home_banner_to_github():
    # We'll store the home banner in your "database.csv" or a separate place.
    # For demonstration, let's say we do a 'home_image' row in database.csv
    # Then we push database.csv.
    # You could store the actual base64 image if you want, but for simplicity let's store a text pointer.

    # 1) Read local database
    df, sha = pull_database()
    # 2) Add or update row for 'home_banner'
    row_idx = df.index[df["Tab"]=="HomeBanner"].tolist()
    if not row_idx:
        # no row found
        new_row = pd.DataFrame({"Tab":["HomeBanner"], "SubTab":[""], "Data":[f"banner updated: {uuid.uuid4()}"]})
        df = pd.concat([df,new_row], ignore_index=True)
    else:
        df.loc[row_idx[0],"Data"] = f"banner updated: {uuid.uuid4()}"
    # 3) push
    code = push_database(df, sha)
    if code in (200,201):
        st.success("Home banner changes pushed to GitHub!")
    else:
        st.error(f"Failed to push. code {code}")

def save_structural_analysis_to_github():
    # For demonstration, we convert the st.session_state.structural_data to CSV and store in database.csv
    df, sha = pull_database()
    # let's store it in a row where Tab='DesignAnalysis', SubTab='Structural'
    data_str = st.session_state.structural_data.to_csv(index=False)
    row_idx = df.index[(df["Tab"]=="DesignAnalysis") & (df["SubTab"]=="Structural")].tolist()
    if not row_idx:
        new_row = pd.DataFrame({"Tab":["DesignAnalysis"],"SubTab":["Structural"],"Data":[data_str]})
        df = pd.concat([df,new_row], ignore_index=True)
    else:
        df.loc[row_idx[0],"Data"] = data_str

    code = push_database(df, sha)
    if code in (200,201):
        st.success("Structural Analysis changes pushed to GitHub!")
    else:
        st.error(f"Failed to push. code {code}")

def save_project_management_to_github():
    # We'll store scheduling_data, resource_data, progress_data in database.csv
    df, sha = pull_database()
    # scheduling
    if "scheduling_data" in st.session_state:
        sched_csv = st.session_state.scheduling_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Scheduling")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ProjectManagement"],"SubTab":["Scheduling"],"Data":[sched_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = sched_csv
    # resource_data
    if "resource_data" in st.session_state:
        res_csv = st.session_state.resource_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Resource")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ProjectManagement"],"SubTab":["Resource"],"Data":[res_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = res_csv
    # progress_data
    if "progress_data" in st.session_state:
        prog_csv = st.session_state.progress_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Progress")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ProjectManagement"],"SubTab":["Progress"],"Data":[prog_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = prog_csv

    code = push_database(df, sha)
    if code in (200,201):
        st.success("Project Management data pushed to GitHub!")
    else:
        st.error(f"Failed to push. code {code}")

def save_tools_utilities_to_github():
    # We'll store cost_estimation_data, etc.
    df, sha = pull_database()
    if "cost_estimation_data" in st.session_state:
        cost_csv = st.session_state.cost_estimation_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ToolsUtilities") & (df["SubTab"]=="CostEstimation")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ToolsUtilities"],"SubTab":["CostEstimation"],"Data":[cost_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = cost_csv

    code = push_database(df, sha)
    if code in (200,201):
        st.success("Tools & Utilities data pushed to GitHub!")
    else:
        st.error(f"Failed to push. code {code}")

def save_collaboration_docs_to_github():
    # We'll store document_data from session_state
    df, sha = pull_database()
    if "document_data" in st.session_state:
        docs_csv = st.session_state.document_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="CollaborationDocs") & (df["SubTab"]=="Documents")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["CollaborationDocs"],"SubTab":["Documents"],"Data":[docs_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = docs_csv

    code = push_database(df, sha)
    if code in (200,201):
        st.success("Collaboration & Docs data pushed to GitHub!")
    else:
        st.error(f"Failed to push. code {code}")
# ----------------------------------------------------------------

def logout():
    if "session_token" in st.session_state and st.session_state["session_token"]:
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["session_token"] = None
    st.info("Logged out successfully!")

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
            st.session_state["username"] = None
            st.session_state["session_token"] = None

def main_app():
    # We always pull database here
    st.session_state["db_df"], st.session_state["db_sha"] = pull_database()

    if st.button("Logout"):
        logout()
        st.stop()

    selected_tab = render_sidebar()
    if selected_tab == "Home":
        run_home()
        # Add a "Save to GitHub" button for the banner
        if st.button("Save Home Banner to GitHub"):
            save_home_banner_to_github()

    elif selected_tab == "Design and Analysis":
        design_analysis.run()
        # sub tab "Structural Analysis" auto
        if st.button("Save Structural Analysis to GitHub"):
            save_structural_analysis_to_github()

    elif selected_tab == "Project Management":
        project_management.run()
        if st.button("Save Project Management to GitHub"):
            save_project_management_to_github()

    elif selected_tab == "Compliance and Reporting":
        compliance_reporting.run()
        st.info("No auto-push for compliance tab as requested.")

    elif selected_tab == "Tools and Utilities":
        tools_utilities.run()
        if st.button("Save Tools & Utilities to GitHub"):
            save_tools_utilities_to_github()

    elif selected_tab == "Collaboration and Documentation":
        collaboration_documentation.run()
        if st.button("Save Collaboration Docs to GitHub"):
            save_collaboration_docs_to_github()

    st.write("---")
    if st.button("Push Changes to GitHub (database.csv)"):
        # If you want a global push for database.csv
        local_df = pd.read_csv(DATABASE_FILE) if os.path.exists(DATABASE_FILE) else st.session_state["db_df"]
        code = push_database(local_df, sha=st.session_state["db_sha"])
        if code in (200,201):
            st.success("database.csv successfully pushed to GitHub!")
        else:
            st.error(f"Failed to push database.csv. Status code: {code}")

def run():
    pull_users_init()  # load users from GitHub
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "sign_up" not in st.session_state:
        st.session_state["sign_up"] = False
    if "session_token" not in st.session_state:
        st.session_state["session_token"] = None

    check_cookie_session()

    if not st.session_state["logged_in"]:
        # Show login or signup
        if st.session_state["sign_up"]:
            sign_up_screen()
        else:
            login_screen()
    else:
        main_app()

if __name__=="__main__":
    run()
