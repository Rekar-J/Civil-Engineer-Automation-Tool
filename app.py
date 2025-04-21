# app.py

import streamlit as st
import pandas as pd
import uuid

from streamlit_cookies_manager import EncryptedCookieManager
from sidebar import render_sidebar
from home import run as run_home, sync_home_banner_after_pull, save_home_banner_to_github
import tabs.design_analysis as design_analysis
import tabs.project_management as project_management
import tabs.compliance_reporting as compliance_reporting
import tabs.tools_utilities as tools_utilities
import tabs.collaboration_documentation as collaboration_documentation

from pushpull import pull_users, push_users, pull_database, push_database

# ── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

# ── Cookie & user‑management setup ───────────────────────────────────────────
COOKIES_PASSWORD = "MY_SUPER_SECRET_PASSWORD_1234"
cookies = EncryptedCookieManager(prefix="civil_eng_app", password=COOKIES_PASSWORD)
if not cookies.ready():
    st.stop()

def get_cookie(k): return cookies.get(k)
def set_cookie(k, v): cookies[k] = v; cookies.save()
def clear_cookie(k):
    if k in cookies: del cookies[k]
    cookies.save()

# ── In‑memory users DataFrame ─────────────────────────────────────────────────
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

def user_exists(u): return not load_users_local()[load_users_local()["username"] == u].empty
def check_credentials(u,p):
    df = load_users_local()
    return not df[(df["username"]==u)&(df["password"]==p)].empty

def create_user(u,p):
    df = load_users_local()
    new = pd.DataFrame({"username":[u],"password":[p],"token":[""]})
    save_users_local(pd.concat([df,new], ignore_index=True))

def set_token_for_user(u, tok):
    df = load_users_local()
    df.loc[df["username"]==u, "token"] = tok
    save_users_local(df)

def find_user_by_token(tok):
    df = load_users_local()
    row = df[df["token"]==tok]
    return row.iloc[0] if not row.empty else None

def clear_token(tok):
    df = load_users_local()
    df.loc[df["token"]==tok, "token"] = ""
    save_users_local(df)

# ── Authentication Screens ────────────────────────────────────────────────────
def sign_up_screen():
    st.title("Create a New Account")
    u = st.text_input("Username", key="signup_username")
    p = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if u and p and not user_exists(u):
            create_user(u,p)
            tok = str(uuid.uuid4())
            set_token_for_user(u, tok)
            st.session_state.update({"logged_in":True,"username":u,"session_token":tok})
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
                st.session_state.update({"logged_in":True,"username":u,"session_token":tok})
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
    st.session_state.update({"logged_in":False,"username":None,"session_token":None})

# ── Main App ────────────────────────────────────────────────────────────────
def main_app():
    # Pull & sync Home banner from GitHub
    db_df, db_sha = pull_database()
    st.session_state["db_df"], st.session_state["db_sha"] = db_df, db_sha
    sync_home_banner_after_pull()

    if st.button("Logout"):
        logout()
        st.stop()

    tab = render_sidebar()

    if tab == "Home":
        run_home()
        if st.button("Save Home Banner", key="save_home"):
            code = save_home_banner_to_github()
            if code in (200,201):
                st.success("✅ Home banner saved to GitHub!")
            else:
                st.error(f"❌ Save failed (status {code})")

    elif tab == "Design and Analysis":
        design_analysis.run()
        # … your existing “Save Design Analysis” button here …

    # … other tabs and their Save buttons …

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
