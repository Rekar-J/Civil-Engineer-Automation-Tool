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

# ------------------------------------------------------------------
# Cookie & User Management
# ------------------------------------------------------------------
COOKIES_PASSWORD = "MY_SUPER_SECRET_PASSWORD_1234"
cookies = EncryptedCookieManager(prefix="civil_eng_app", password=COOKIES_PASSWORD)
if not cookies.ready():
    st.stop()

def get_cookie(key):        return cookies.get(key)
def set_cookie(key, val):   cookies[key] = val; cookies.save()
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
    USERS_DF, USERS_SHA = ensure_columns(df), sha

def load_users_local():
    return USERS_DF.copy()

def save_users_local(df):
    global USERS_DF, USERS_SHA
    USERS_DF = df.copy()
    code = push_users(USERS_DF, USERS_SHA)
    if code in (200,201):
        new_df, new_sha = pull_users()
        USERS_DF, USERS_SHA = ensure_columns(new_df), new_sha

def user_exists(u):    return not load_users_local()[load_users_local()["username"]==u].empty
def check_credentials(u,p): 
    df = load_users_local()
    return not df[(df["username"]==u)&(df["password"]==p)].empty

def create_user(u,p):
    df = load_users_local()
    new = pd.DataFrame({"username":[u],"password":[p],"token":[""]})
    save_users_local(pd.concat([df,new],ignore_index=True))

def set_token_for_user(u,tok):
    df = load_users_local()
    df.loc[df["username"]==u,"token"] = tok
    save_users_local(df)

def find_user_by_token(tok):
    df = load_users_local()
    row = df[df["token"]==tok]
    return row.iloc[0] if not row.empty else None

def clear_token(tok):
    df = load_users_local()
    df.loc[df["token"]==tok,"token"] = ""
    save_users_local(df)

def sign_up_screen():
    st.title("Create a New Account")
    u = st.text_input("Username", key="signup_user")
    p = st.text_input("Password", type="password", key="signup_pw")
    if st.button("Sign Up"):
        if u and p and not user_exists(u):
            create_user(u,p)
            tok = str(uuid.uuid4())
            set_token_for_user(u,tok)
            st.session_state.update({
                "logged_in": True,
                "username": u,
                "session_token": tok
            })
            set_cookie("session_token", tok)
        st.stop()

def login_screen():
    st.title("🔒 Login")
    u = st.text_input("Username", key="login_user")
    p = st.text_input("Password", type="password", key="login_pw")
    c1,c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_credentials(u,p):
                tok = str(uuid.uuid4())
                set_token_for_user(u,tok)
                st.session_state.update({
                    "logged_in": True,
                    "username": u,
                    "session_token": tok
                })
                set_cookie("session_token", tok)
            st.stop()
    with c2:
        if st.button("Sign Up"):
            st.session_state["sign_up"] = True
            st.stop()

def logout():
    tok = st.session_state.get("session_token")
    if tok:
        clear_token(tok)
    clear_cookie("session_token")
    st.session_state.update({
        "logged_in": False,
        "username": None,
        "session_token": None
    })

# ------------------------------------------------------------------
# Banner & Persistence Helpers
# ------------------------------------------------------------------
HOME_BANNER_PATH = "uploads/home header image.jpg"

def sync_home_banner_after_pull():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    if "db_df" in st.session_state:
        df = st.session_state["db_df"]
        idx = df.index[df["Tab"]=="HomeBanner"].tolist()
        if idx:
            b64 = df.loc[idx[0],"Data"]
            if b64:
                try:
                    img = base64.b64decode(b64)
                    with open(HOME_BANNER_PATH,"wb") as f:
                        f.write(img)
                except:
                    pass

def save_home_banner_to_github():
    if not os.path.exists(HOME_BANNER_PATH):
        return
    with open(HOME_BANNER_PATH,"rb") as f:
        b = f.read()
    b64 = base64.b64encode(b).decode()
    df, sha = pull_database()
    idx = df.index[df["Tab"]=="HomeBanner"].tolist()
    if not idx:
        new = pd.DataFrame({
            "Tab":["HomeBanner"], "SubTab":[""], "Data":[b64]
        })
        df = pd.concat([df,new],ignore_index=True)
    else:
        df.loc[idx[0],"Data"] = b64
    push_database(df, sha)

def save_structural_analysis_to_github():
    if "structural_data" not in st.session_state:
        return
    df, sha = pull_database()
    csv = st.session_state.structural_data.to_csv(index=False)
    idx = df.index[
        (df["Tab"]=="DesignAnalysis") & (df["SubTab"]=="Structural")
    ].tolist()
    if not idx:
        new = pd.DataFrame({
            "Tab":["DesignAnalysis"],
            "SubTab":["Structural"],
            "Data":[csv]
        })
        df = pd.concat([df,new],ignore_index=True)
    else:
        df.loc[idx[0],"Data"] = csv
    push_database(df, sha)

def save_project_management_to_github():
    df, sha = pull_database()
    # Scheduling
    if "scheduling_data" in st.session_state:
        sched = st.session_state.scheduling_data.to_csv(index=False)
        idx = df.index[
            (df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Scheduling")
        ].tolist()
        if not idx:
            new = pd.DataFrame({
                "Tab":["ProjectManagement"],
                "SubTab":["Scheduling"],
                "Data":[sched]
            })
            df = pd.concat([df,new],ignore_index=True)
        else:
            df.loc[idx[0],"Data"] = sched
    # Resource
    if "resource_data" in st.session_state:
        res = st.session_state.resource_data.to_csv(index=False)
        idx = df.index[
            (df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Resource")
        ].tolist()
        if not idx:
            new = pd.DataFrame({
                "Tab":["ProjectManagement"],
                "SubTab":["Resource"],
                "Data":[res]
            })
            df = pd.concat([df,new],ignore_index=True)
        else:
            df.loc[idx[0],"Data"] = res
    # Progress
    if "progress_data" in st.session_state:
        prog = st.session_state.progress_data.to_csv(index=False)
        idx = df.index[
            (df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Progress")
        ].tolist()
        if not idx:
            new = pd.DataFrame({
                "Tab":["ProjectManagement"],
                "SubTab":["Progress"],
                "Data":[prog]
            })
            df = pd.concat([df,new],ignore_index=True)
        else:
            df.loc[idx[0],"Data"] = prog
    push_database(df, sha)

def save_tools_utilities_to_github():
    df, sha = pull_database()
    if "cost_estimation_data" in st.session_state:
        csv = st.session_state.cost_estimation_data.to_csv(index=False)
        idx = df.index[
            (df["Tab"]=="ToolsUtilities") & (df["SubTab"]=="CostEstimation")
        ].tolist()
        if not idx:
            new = pd.DataFrame({
                "Tab":["ToolsUtilities"],
                "SubTab":["CostEstimation"],
                "Data":[csv]
            })
            df = pd.concat([df,new],ignore_index=True)
        else:
            df.loc[idx[0],"Data"] = csv
    push_database(df, sha)

def save_collaboration_docs_to_github():
    df, sha = pull_database()
    if "document_data" in st.session_state:
        csv = st.session_state.document_data.to_csv(index=False)
        idx = df.index[
            (df["Tab"]=="CollaborationDocs") & (df["SubTab"]=="Documents")
        ].tolist()
        if not idx:
            new = pd.DataFrame({
                "Tab":["CollaborationDocs"],
                "SubTab":["Documents"],
                "Data":[csv]
            })
            df = pd.concat([df,new],ignore_index=True)
        else:
            df.loc[idx[0],"Data"] = csv
    push_database(df, sha)

# ------------------------------------------------------------------
# Main Application Logic
# ------------------------------------------------------------------
def main_app():
    # Get the latest database
    db_df, db_sha = pull_database()
    st.session_state["db_df"], st.session_state["db_sha"] = db_df, db_sha

    # Sync existing banner into uploads/
    sync_home_banner_after_pull()

    if st.button("Logout"):
        logout()
        st.stop()

    tab = render_sidebar()

    if tab == "Home":
        run_home()
        if st.button("Save Home Banner", key="save_home"):
            save_home_banner_to_github()
            st.success("Home banner saved!")
            # refresh if supported
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.stop()

    elif tab == "Design and Analysis":
        design_analysis.run()
        if st.button("Save Structural Analysis", key="save_design"):
            save_structural_analysis_to_github()
            st.success("Structural analysis saved!")
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.stop()

    elif tab == "Project Management":
        project_management.run()
        if st.button("Save Project Management", key="save_proj"):
            save_project_management_to_github()
            st.success("Project management saved!")
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.stop()

    elif tab == "Compliance and Reporting":
        compliance_reporting.run()
        # no save button for this tab

    elif tab == "Tools and Utilities":
        tools_utilities.run()
        if st.button("Save Utilities Data", key="save_utils"):
            save_tools_utilities_to_github()
            st.success("Utilities data saved!")
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.stop()

    elif tab == "Collaboration and Documentation":
        collaboration_documentation.run()
        if st.button("Save Documents Data", key="save_docs"):
            save_collaboration_docs_to_github()
            st.success("Documents saved!")
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.stop()

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
