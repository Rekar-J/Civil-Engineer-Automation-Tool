# app.py
import streamlit as st
import os
import base64
import pandas as pd
import uuid

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

from pushpull import pull_database, push_database, pull_users, push_users

# ── Streamlit page config ───────────────────────────────────────────────────
st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

# ── Cookie & user management ────────────────────────────────────────────────
COOKIES_PASSWORD = "MY_SUPER_SECRET_PASSWORD_1234"
cookies = EncryptedCookieManager(prefix="civil_eng_app", password=COOKIES_PASSWORD)
if not cookies.ready():
    st.stop()

def get_cookie(k):       return cookies.get(k)
def set_cookie(k, v):    cookies[k] = v; cookies.save()
def clear_cookie(k):
    if k in cookies: del cookies[k]
    cookies.save()

# ── In‑memory users DataFrame ────────────────────────────────────────────────
USERS_DF = pd.DataFrame(columns=["username","password","token"])
USERS_SHA = None
def ensure_columns(df):
    for c in ["username","password","token"]:
        if c not in df.columns: df[c] = ""
    return df

def pull_users_init():
    global USERS_DF, USERS_SHA
    df, sha = pull_users()
    USERS_DF, USERS_SHA = ensure_columns(df), sha

def load_users_local(): return USERS_DF.copy()
def save_users_local(df):
    global USERS_DF, USERS_SHA
    code = push_users(df, USERS_SHA)
    if code in (200,201):
        new_df, new_sha = pull_users()
        USERS_DF, USERS_SHA = ensure_columns(new_df), new_sha

def user_exists(u): 
    return not load_users_local()[load_users_local()["username"]==u].empty
def check_credentials(u,p):
    df = load_users_local()
    return not df[(df["username"]==u)&(df["password"]==p)].empty

def create_user(u,p):
    df = load_users_local()
    new = pd.DataFrame({"username":[u],"password":[p],"token":[""]})
    save_users_local(pd.concat([df,new], ignore_index=True))

def set_token_for_user(u,token):
    df = load_users_local()
    df.loc[df["username"]==u,"token"] = token
    save_users_local(df)

def find_user_by_token(tok):
    df = load_users_local()
    row = df[df["token"]==tok]
    return row.iloc[0] if not row.empty else None

def clear_token(tok):
    df = load_users_local()
    df.loc[df["token"]==tok,"token"] = ""
    save_users_local(df)

# ── Banner file & GitHub sync ───────────────────────────────────────────────
HOME_BANNER_PATH = "home_banner.jpg"

def sync_home_banner_after_pull():
    """Pull the Base64 from session_state['db_df'] and write/erase local banner."""
    df = st.session_state.get("db_df", pd.DataFrame())
    idx = df.index[df["Tab"]=="HomeBanner"].tolist()
    # if there's data and non‑empty string, decode + write
    if idx and df.at[idx[0],"Data"]:
        b64 = df.at[idx[0],"Data"]
        try:
            img = base64.b64decode(b64)
            with open(HOME_BANNER_PATH, "wb") as f:
                f.write(img)
        except Exception:
            pass
    else:
        # no entry or empty Data → ensure file is removed
        if os.path.exists(HOME_BANNER_PATH):
            os.remove(HOME_BANNER_PATH)

def save_home_banner_to_github():
    """
    Read the local banner file if it exists (or empty string if not),
    then update the `HomeBanner` row in database.csv on GitHub.
    """
    df, sha = pull_database()
    # prepare new Base64 or empty
    if os.path.exists(HOME_BANNER_PATH):
        with open(HOME_BANNER_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    else:
        b64 = ""
    # upsert
    idx = df.index[df["Tab"]=="HomeBanner"].tolist()
    if not idx:
        new = pd.DataFrame([{"Tab":"HomeBanner","SubTab":"","Data":b64}])
        df = pd.concat([df, new], ignore_index=True)
    else:
        df.at[idx[0],"Data"] = b64
    return push_database(df, sha)

# ── “Save” handlers for other tabs ──────────────────────────────────────────
def save_structural_analysis_to_github():
    if "structural_data" not in st.session_state:
        st.error("No structural data to save.")
        return None
    df_data, sha = pull_database()
    csv = st.session_state.structural_data.to_csv(index=False)
    idx = df_data.index[
        (df_data["Tab"]=="Design and Analysis") & (df_data["SubTab"]=="Structural Analysis")
    ].tolist()
    if not idx:
        new = pd.DataFrame([{
            "Tab":"Design and Analysis",
            "SubTab":"Structural Analysis",
            "Data":csv
        }])
        df_data = pd.concat([df_data, new], ignore_index=True)
    else:
        df_data.at[idx[0],"Data"] = csv
    return push_database(df_data, sha)

def save_project_management_to_github():
    df_data, sha = pull_database()
    if "scheduling_data" in st.session_state:
        csv = st.session_state.scheduling_data.to_csv(index=False)
        idx = df_data.index[
            (df_data["Tab"]=="Project Management") & (df_data["SubTab"]=="Scheduling")
        ].tolist()
        if not idx:
            new = pd.DataFrame([{
                "Tab":"Project Management",
                "SubTab":"Scheduling",
                "Data":csv
            }])
            df_data = pd.concat([df_data,new], ignore_index=True)
        else:
            df_data.at[idx[0],"Data"] = csv
    return push_database(df_data, sha)

def save_tools_utilities_to_github():
    df_data, sha = pull_database()
    if "cost_estimation_data" in st.session_state:
        csv = st.session_state.cost_estimation_data.to_csv(index=False)
        idx = df_data.index[
            (df_data["Tab"]=="Tools and Utilities") & (df_data["SubTab"]=="Cost Estimation")
        ].tolist()
        if not idx:
            new = pd.DataFrame([{
                "Tab":"Tools and Utilities",
                "SubTab":"Cost Estimation",
                "Data":csv
            }])
            df_data = pd.concat([df_data,new], ignore_index=True)
        else:
            df_data.at[idx[0],"Data"] = csv
    return push_database(df_data, sha)

def save_collaboration_docs_to_github():
    df_data, sha = pull_database()
    if "document_data" in st.session_state:
        csv = st.session_state.document_data.to_csv(index=False)
        idx = df_data.index[
            (df_data["Tab"]=="Collaboration and Documentation") & (df_data["SubTab"]=="Documents")
        ].tolist()
        if not idx:
            new = pd.DataFrame([{
                "Tab":"Collaboration and Documentation",
                "SubTab":"Documents",
                "Data":csv
            }])
            df_data = pd.concat([df_data,new], ignore_index=True)
        else:
            df_data.at[idx[0],"Data"] = csv
    return push_database(df_data, sha)

# ── Authentication Screens ─────────────────────────────────────────────────
def sign_up_screen():
    st.title("Create a New Account")
    u = st.text_input("Username", key="signup_username")
    p = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if u and p and not user_exists(u):
            create_user(u,p)
            tok = str(uuid.uuid4())
            set_token_for_user(u, tok)
            st.session_state.update(logged_in=True, username=u, session_token=tok)
            set_cookie("session_token", tok)
        st.stop()

def login_screen():
    st.title("🔒 Login")
    u = st.text_input("Username", key="login_username")
    p = st.text_input("Password", type="password", key="login_password")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login"):
            if check_credentials(u,p):
                tok = str(uuid.uuid4())
                set_token_for_user(u, tok)
                st.session_state.update(logged_in=True, username=u, session_token=tok)
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
    st.session_state.update(logged_in=False, username=None, session_token=None)

# ── Main App ───────────────────────────────────────────────────────────────
def main_app():
    # 1) pull DB, store in session, sync banner  
    df, sha = pull_database()
    st.session_state["db_df"], st.session_state["db_sha"] = df, sha
    sync_home_banner_after_pull()

    if st.button("Logout"):
        logout(); st.stop()

    tab = render_sidebar()
    if tab == "Home":
        run_home()
        if st.button("Save Home Banner"):
            code = save_home_banner_to_github()
            if code in (200,201):
                st.success("✅ Home banner saved!")
            else:
                st.error(f"❌ Save failed (status {code})")
    elif tab == "Design and Analysis":
        design_analysis.run()
        if st.button("Save Design & Analysis", key="save_design"):
            code = save_structural_analysis_to_github()
            if code in (200,201): st.success("✅ Design & Analysis saved!")
            else: st.error(f"❌ Save failed (status {code})")
    elif tab == "Project Management":
        project_management.run()
        if st.button("Save Project Management", key="save_pm"):
            code = save_project_management_to_github()
            if code in (200,201): st.success("✅ Project Management saved!")
            else: st.error(f"❌ Save failed (status {code})")
    elif tab == "Compliance and Reporting":
        compliance_reporting.run()
    elif tab == "Tools and Utilities":
        tools_utilities.run()
        if st.button("Save Tools & Utilities", key="save_tools"):
            code = save_tools_utilities_to_github()
            if code in (200,201): st.success("✅ Tools & Utilities saved!")
            else: st.error(f"❌ Save failed (status {code})")
    elif tab == "Collaboration and Documentation":
        collaboration_documentation.run()
        if st.button("Save Collaboration Docs", key="save_collab"):
            code = save_collaboration_docs_to_github()
            if code in (200,201): st.success("✅ Collaboration Docs saved!")
            else: st.error(f"❌ Save failed (status {code})")

# ── Cookie/session bootstrap ───────────────────────────────────────────────
def check_cookie_session():
    tok = get_cookie("session_token")
    if tok:
        user = find_user_by_token(tok)
        if user is not None:  # explicit check
            st.session_state.update(logged_in=True, username=user["username"], session_token=tok)
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

if __name__=="__main__":
    run()
