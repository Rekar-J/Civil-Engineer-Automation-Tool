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

# ---- We import push/pull from pushpull.py ----
from pushpull import (
    pull_database, push_database,
    pull_users, push_users,
    DATABASE_FILE, USERS_FILE
)

HOME_BANNER_PATH = "uploads/home header image.jpg"

# -------------- In-memory usage for users.csv --------------
USERS_DF = pd.DataFrame(columns=["username","password","token"])
USERS_SHA = None

DATABASE_DF = pd.DataFrame()  # We'll store DB in session_state, or we can do so here

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

def ensure_columns(df):
    for c in ["username","password","token"]:
        if c not in df.columns:
            df[c] = ""
    return df

def pull_users_init():
    """
    Pull users.csv from GitHub at app startup, store in memory.
    """
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
        new_df = ensure_columns(new_df)
        USERS_DF = new_df.copy()
        USERS_SHA = new_sha
    else:
        pass

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

def sign_up_screen():
    st.title("Create a New Account")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.stop()
        elif user_exists(new_username):
            st.stop()
        else:
            create_user(new_username, new_password)
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
            st.stop()
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

# --- Banner Storage in database.csv as base64 so it persists ---
def sync_home_banner_after_pull():
    """
    Called after we do pull_database().
    If there's a row with Tab='HomeBanner', decode it into 'uploads/home header image.jpg'.
    """
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    if "db_df" in st.session_state and st.session_state["db_df"] is not None:
        df = st.session_state["db_df"]
        row_idx = df.index[df["Tab"]=="HomeBanner"].tolist()
        if row_idx:
            b64_str = df.loc[row_idx[0],"Data"]
            if b64_str:
                try:
                    img_bin = base64.b64decode(b64_str)
                    with open(HOME_BANNER_PATH,"wb") as f:
                        f.write(img_bin)
                except:
                    pass

def save_home_banner_to_github():
    """
    If 'uploads/home header image.jpg' changed, store it in database.csv row Tab='HomeBanner'.
    """
    if not os.path.exists(HOME_BANNER_PATH):
        return
    with open(HOME_BANNER_PATH,"rb") as f:
        img_bin = f.read()
    b64_str = base64.b64encode(img_bin).decode()

    from pushpull import pull_database, push_database
    df, sha = pull_database()
    row_idx = df.index[df["Tab"]=="HomeBanner"].tolist()
    if not row_idx:
        new_row = pd.DataFrame({"Tab":["HomeBanner"], "SubTab":[""], "Data":[b64_str]})
        df = pd.concat([df,new_row], ignore_index=True)
    else:
        df.loc[row_idx[0],"Data"] = b64_str

    push_database(df, sha)

def save_structural_analysis_to_github():
    from pushpull import pull_database, push_database
    if "structural_data" not in st.session_state:
        return
    df, sha = pull_database()
    data_str = st.session_state.structural_data.to_csv(index=False)
    row_idx = df.index[(df["Tab"]=="DesignAnalysis") & (df["SubTab"]=="Structural")].tolist()
    if not row_idx:
        new_row = pd.DataFrame({"Tab":["DesignAnalysis"],"SubTab":["Structural"],"Data":[data_str]})
        df = pd.concat([df,new_row], ignore_index=True)
    else:
        df.loc[row_idx[0],"Data"] = data_str
    push_database(df, sha)

def save_project_management_to_github():
    from pushpull import pull_database, push_database
    df, sha = pull_database()
    if "scheduling_data" in st.session_state:
        sched_csv = st.session_state.scheduling_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Scheduling")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ProjectManagement"],"SubTab":["Scheduling"],"Data":[sched_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = sched_csv
    if "resource_data" in st.session_state:
        res_csv = st.session_state.resource_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Resource")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ProjectManagement"],"SubTab":["Resource"],"Data":[res_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = res_csv
    if "progress_data" in st.session_state:
        prog_csv = st.session_state.progress_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ProjectManagement") & (df["SubTab"]=="Progress")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ProjectManagement"],"SubTab":["Progress"],"Data":[prog_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = prog_csv
    push_database(df, sha)

def save_tools_utilities_to_github():
    from pushpull import pull_database, push_database
    df, sha = pull_database()
    if "cost_estimation_data" in st.session_state:
        cost_csv = st.session_state.cost_estimation_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="ToolsUtilities") & (df["SubTab"]=="CostEstimation")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["ToolsUtilities"],"SubTab":["CostEstimation"],"Data":[cost_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = cost_csv
    push_database(df, sha)

def save_collaboration_docs_to_github():
    from pushpull import pull_database, push_database
    df, sha = pull_database()
    if "document_data" in st.session_state:
        docs_csv = st.session_state.document_data.to_csv(index=False)
        row_idx = df.index[(df["Tab"]=="CollaborationDocs") & (df["SubTab"]=="Documents")].tolist()
        if not row_idx:
            new_row = pd.DataFrame({"Tab":["CollaborationDocs"],"SubTab":["Documents"],"Data":[docs_csv]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            df.loc[row_idx[0],"Data"] = docs_csv
    push_database(df, sha)

def main_app():
    from pushpull import pull_database
    db_df, db_sha = pull_database()
    st.session_state["db_df"] = db_df
    st.session_state["db_sha"] = db_sha

    sync_home_banner_after_pull()

    if st.button("Logout"):
        logout()
        st.stop()

    selected_tab = render_sidebar()

    if selected_tab == "Home":
        run_home()
        if st.button("Save Changes", key="save_home_banner"):
            save_home_banner_to_github()
            st.stop()

    elif selected_tab == "Design and Analysis":
        design_analysis.run()
        if st.button("Save Changes", key="save_struct_analysis"):
            save_structural_analysis_to_github()
            st.stop()

    elif selected_tab == "Project Management":
        project_management.run()
        if st.button("Save Changes", key="save_project_mgmt"):
            save_project_management_to_github()
            st.stop()

    elif selected_tab == "Compliance and Reporting":
        compliance_reporting.run()

    elif selected_tab == "Tools and Utilities":
        tools_utilities.run()
        if st.button("Save Changes", key="save_tools_utils"):
            save_tools_utilities_to_github()
            st.stop()

    elif selected_tab == "Collaboration and Documentation":
        collaboration_documentation.run()
        if st.button("Save Changes", key="save_collab_docs"):
            save_collaboration_docs_to_github()
            st.stop()

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

def run():
    pull_users_init()
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
