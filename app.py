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

# --- Cookie & User Management ---
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

# In‑memory users table
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
        new_df, new_sha = pull_users()
        USERS_DF, USERS_SHA = ensure_columns(new_df), new_sha

def user_exists(username):
    return not load_users_local()[load_users_local()["username"]==username].empty

def check_credentials(username, password):
    df = load_users_local()
    return not df[(df["username"]==username)&(df["password"]==password)].empty

def create_user(username, password):
    df = load_users_local()
    new = pd.DataFrame({"username":[username],"password":[password],"token":[""]})
    save_users_local(pd.concat([df, new], ignore_index=True))

def set_token_for_user(username, token):
    df = load_users_local()
    df.loc[df["username"]==username, "token"] = token
    save_users_local(df)

def find_user_by_token(token):
    row = load_users_local()[load_users_local()["token"]==token]
    return row.iloc[0] if not row.empty else None

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"]==token, "token"] = ""
    save_users_local(df)

def sign_up_screen():
    st.title("Create a New Account")
    user = st.text_input("Choose a Username", key="signup_username")
    pw = st.text_input("Choose a Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if user and pw and not user_exists(user):
            create_user(user, pw)
            tok = str(uuid.uuid4())
            set_token_for_user(user, tok)
            st.session_state.update({
                "logged_in": True,
                "username": user,
                "session_token": tok
            })
            set_cookie("session_token", tok)
        st.experimental_rerun()

def login_screen():
    st.title("🔒 Login")
    user = st.text_input("Username", key="login_username")
    pw   = st.text_input("Password", type="password", key="login_password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_credentials(user, pw):
                tok = str(uuid.uuid4())
                set_token_for_user(user, tok)
                st.session_state.update({
                    "logged_in": True,
                    "username": user,
                    "session_token": tok
                })
                set_cookie("session_token", tok)
            st.experimental_rerun()
    with c2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.experimental_rerun()

def logout():
    if st.session_state.get("session_token"):
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state.update({
        "logged_in": False,
        "username": None,
        "session_token": None
    })

# --- Home Banner Persistence ---
def sync_home_banner_after_pull():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    df = st.session_state.get("db_df")
    if df is not None:
        rows = df.index[df["Tab"]=="HomeBanner"].tolist()
        if rows:
            b64 = df.loc[rows[0], "Data"]
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
        b64 = base64.b64encode(f.read()).decode()
    df, sha = pull_database()
    rows = df.index[df["Tab"]=="HomeBanner"].tolist()
    if rows:
        df.loc[rows[0], "Data"] = b64
    else:
        df = pd.concat([df, pd.DataFrame([{"Tab":"HomeBanner","SubTab":"","Data":b64}])], ignore_index=True)
    push_database(df, sha)

# --- Design & Analysis Persistence ---
def save_structural_analysis_to_github():
    if "structural_data" not in st.session_state:
        return
    df, sha = pull_database()
    data_csv = st.session_state.structural_data.to_csv(index=False)
    rows = df.index[(df["Tab"]=="DesignAnalysis")&(df["SubTab"]=="Structural")].tolist()
    if rows:
        df.loc[rows[0], "Data"] = data_csv
    else:
        df = pd.concat([df, pd.DataFrame([{"Tab":"DesignAnalysis","SubTab":"Structural","Data":data_csv}])], ignore_index=True)
    push_database(df, sha)

# --- Project Management Persistence ---
def save_project_management_to_github():
    df, sha = pull_database()
    # scheduling
    if "scheduling_data" in st.session_state:
        csv = st.session_state.scheduling_data.to_csv(index=False)
        rows = df.index[(df["Tab"]=="ProjectManagement")&(df["SubTab"]=="Scheduling")].tolist()
        if rows:
            df.loc[rows[0], "Data"] = csv
        else:
            df = pd.concat([df, pd.DataFrame([{"Tab":"ProjectManagement","SubTab":"Scheduling","Data":csv}])], ignore_index=True)
    # resource
    if "resource_data" in st.session_state:
        csv = st.session_state.resource_data.to_csv(index=False)
        rows = df.index[(df["Tab"]=="ProjectManagement")&(df["SubTab"]=="Resource")].tolist()
        if rows:
            df.loc[rows[0], "Data"] = csv
        else:
            df = pd.concat([df, pd.DataFrame([{"Tab":"ProjectManagement","SubTab":"Resource","Data":csv}])], ignore_index=True)
    # progress
    if "progress_data" in st.session_state:
        csv = st.session_state.progress_data.to_csv(index=False)
        rows = df.index[(df["Tab"]=="ProjectManagement")&(df["SubTab"]=="Progress")].tolist()
        if rows:
            df.loc[rows[0], "Data"] = csv
        else:
            df = pd.concat([df, pd.DataFrame([{"Tab":"ProjectManagement","SubTab":"Progress","Data":csv}])], ignore_index=True)
    push_database(df, sha)

# --- Tools & Utilities Persistence ---
def save_tools_utilities_to_github():
    df, sha = pull_database()
    if "cost_estimation_data" in st.session_state:
        csv = st.session_state.cost_estimation_data.to_csv(index=False)
        rows = df.index[(df["Tab"]=="ToolsUtilities")&(df["SubTab"]=="CostEstimation")].tolist()
        if rows:
            df.loc[rows[0], "Data"] = csv
        else:
            df = pd.concat([df, pd.DataFrame([{"Tab":"ToolsUtilities","SubTab":"CostEstimation","Data":csv}])], ignore_index=True)
    push_database(df, sha)

# --- Collaboration Docs Persistence ---
def save_collaboration_docs_to_github():
    df, sha = pull_database()
    if "document_data" in st.session_state:
        csv = st.session_state.document_data.to_csv(index=False)
        rows = df.index[(df["Tab"]=="CollaborationDocs")&(df["SubTab"]=="Documents")].tolist()
        if rows:
            df.loc[rows[0], "Data"] = csv
        else:
            df = pd.concat([df, pd.DataFrame([{"Tab":"CollaborationDocs","SubTab":"Documents","Data":csv}])], ignore_index=True)
    push_database(df, sha)

# --- Main App ---
def main_app():
    # Pull latest database and sync banner
    db_df, db_sha = pull_database()
    st.session_state["db_df"], st.session_state["db_sha"] = db_df, db_sha
    sync_home_banner_after_pull()

    # Logout button
    if st.button("Logout"):
        logout()
        st.experimental_rerun()

    tab = render_sidebar()

    if tab == "Home":
        run_home()
        if st.button("Save Home Banner", key="save_home"):
            save_home_banner_to_github()
            st.experimental_rerun()

    elif tab == "Design and Analysis":
        design_analysis.run()
        if st.button("Save Structural Analysis", key="save_design"):
            save_structural_analysis_to_github()
            st.experimental_rerun()

    elif tab == "Project Management":
        project_management.run()
        if st.button("Save Project Management", key="save_projects"):
            save_project_management_to_github()
            st.experimental_rerun()

    elif tab == "Compliance and Reporting":
        compliance_reporting.run()
        # no persistent data here

    elif tab == "Tools and Utilities":
        tools_utilities.run()
        if st.button("Save Tools & Utilities", key="save_tools"):
            save_tools_utilities_to_github()
            st.experimental_rerun()

    elif tab == "Collaboration and Documentation":
        collaboration_documentation.run()
        if st.button("Save Collaboration Docs", key="save_collab"):
            save_collaboration_docs_to_github()
            st.experimental_rerun()

def check_cookie_session():
    tok = get_cookie("session_token")
    if tok:
        user = find_user_by_token(tok)
        if user is not None:
            st.session_state.update({
                "logged_in": True,
                "username": user["username"],
                "session_token": tok
            })
        else:
            clear_cookie("session_token")

def run():
    pull_users_init()
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("sign_up", False)
    st.session_state.setdefault("session_token", None)

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
