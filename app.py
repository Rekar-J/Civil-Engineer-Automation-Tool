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
    if code in (200, 201):
        new_df, new_sha = pull_users()
        USERS_DF, USERS_SHA = ensure_columns(new_df), new_sha

def user_exists(username):
    return not load_users_local()[load_users_local()["username"] == username].empty

def check_credentials(username, password):
    df = load_users_local()
    return not df[(df["username"] == username) & (df["password"] == password)].empty

def create_user(username, password):
    df = load_users_local()
    new = pd.DataFrame({"username":[username], "password":[password], "token":[""]})
    save_users_local(pd.concat([df, new], ignore_index=True))

def set_token_for_user(username, token):
    df = load_users_local()
    df.loc[df["username"] == username, "token"] = token
    save_users_local(df)

def find_user_by_token(token):
    row = load_users_local()[load_users_local()["token"] == token]
    return row.iloc[0] if not row.empty else None

def clear_token(token):
    df = load_users_local()
    df.loc[df["token"] == token, "token"] = ""
    save_users_local(df)

def sign_up_screen():
    st.title("Create a New Account")
    user = st.text_input("Choose a Username", key="signup_username")
    pw   = st.text_input("Choose a Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if user and pw and not user_exists(user):
            create_user(user, pw)
            tok = str(uuid.uuid4())
            set_token_for_user(user, tok)
            st.session_state["logged_in"] = True
            st.session_state["username"]  = user
            st.session_state["session_token"] = tok
            set_cookie("session_token", tok)
        st.stop()

def login_screen():
    st.title("🔒 Login to Civil Engineer Automation Tool")
    user = st.text_input("Username", key="login_username")
    pw   = st.text_input("Password", type="password", key="login_password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_credentials(user, pw):
                tok = str(uuid.uuid4())
                set_token_for_user(user, tok)
                st.session_state["logged_in"] = True
                st.session_state["username"]  = user
                st.session_state["session_token"] = tok
                set_cookie("session_token", tok)
            st.stop()
    with c2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.stop()

def logout():
    if st.session_state.get("session_token"):
        clear_token(st.session_state["session_token"])
    clear_cookie("session_token")
    st.session_state.update({
        "logged_in": False,
        "username": None,
        "session_token": None
    })

# --- Persistence Helpers ---
def sync_home_banner_after_pull():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if "db_df" in st.session_state and st.session_state["db_df"] is not None:
        df = st.session_state["db_df"]
        idx = df.index[df["Tab"] == "HomeBanner"].tolist()
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
        b64 = base64.b64encode(f.read()).decode()
    df, sha = pull_database()
    idx = df.index[df["Tab"] == "HomeBanner"].tolist()
    if not idx:
        new = pd.DataFrame({"Tab":["HomeBanner"], "SubTab":[""], "Data":[b64]})
        df = pd.concat([df, new], ignore_index=True)
    else:
        df.loc[idx[0], "Data"] = b64
    push_database(df, sha)

def save_structural_analysis_to_github():
    if "structural_data" not in st.session_state:
        return
    df_data, sha = pull_database()
    csv = st.session_state.structural_data.to_csv(index=False)
    idx = df_data.index[(df_data["Tab"]=="DesignAnalysis") & (df_data["SubTab"]=="Structural")].tolist()
    if not idx:
        new = pd.DataFrame({"Tab":["DesignAnalysis"], "SubTab":["Structural"], "Data":[csv]})
        df_data = pd.concat([df_data, new], ignore_index=True)
    else:
        df_data.loc[idx[0], "Data"] = csv
    push_database(df_data, sha)

def save_project_management_to_github():
    df_data, sha = pull_database()
    if "scheduling_data" in st.session_state:
        csv = st.session_state.scheduling_data.to_csv(index=False)
        idx = df_data.index[(df_data["Tab"]=="ProjectManagement") & (df_data["SubTab"]=="Scheduling")].tolist()
        if not idx:
            new = pd.DataFrame({"Tab":["ProjectManagement"], "SubTab":["Scheduling"], "Data":[csv]})
            df_data = pd.concat([df_data, new], ignore_index=True)
        else:
            df_data.loc[idx[0], "Data"] = csv
    if "resource_data" in st.session_state:
        csv = st.session_state.resource_data.to_csv(index=False)
        idx = df_data.index[(df_data["Tab"]=="ProjectManagement") & (df_data["SubTab"]=="Resource")].tolist()
        if not idx:
            new = pd.DataFrame({"Tab":["ProjectManagement"], "SubTab":["Resource"], "Data":[csv]})
            df_data = pd.concat([df_data, new], ignore_index=True)
        else:
            df_data.loc[idx[0], "Data"] = csv
    if "progress_data" in st.session_state:
        csv = st.session_state.progress_data.to_csv(index=False)
        idx = df_data.index[(df_data["Tab"]=="ProjectManagement") & (df_data["SubTab"]=="Progress")].tolist()
        if not idx:
            new = pd.DataFrame({"Tab":["ProjectManagement"], "SubTab":["Progress"], "Data":[csv]})
            df_data = pd.concat([df_data, new], ignore_index=True)
        else:
            df_data.loc[idx[0], "Data"] = csv
    push_database(df_data, sha)

def save_tools_utilities_to_github():
    df_data, sha = pull_database()
    if "cost_estimation_data" in st.session_state:
        csv = st.session_state.cost_estimation_data.to_csv(index=False)
        idx = df_data.index[(df_data["Tab"]=="ToolsUtilities") & (df_data["SubTab"]=="CostEstimation")].tolist()
        if not idx:
            new = pd.DataFrame({"Tab":["ToolsUtilities"], "SubTab":["CostEstimation"], "Data":[csv]})
            df_data = pd.concat([df_data, new], ignore_index=True)
        else:
            df_data.loc[idx[0], "Data"] = csv
        push_database(df_data, sha)

def save_collaboration_docs_to_github():
    df_data, sha = pull_database()
    if "document_data" in st.session_state:
        csv = st.session_state.document_data.to_csv(index=False)
        idx = df_data.index[(df_data["Tab"]=="CollaborationDocs") & (df_data["SubTab"]=="Documents")].
