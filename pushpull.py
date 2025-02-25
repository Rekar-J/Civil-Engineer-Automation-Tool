import streamlit as st
import requests
import base64
import pandas as pd

# We read GITHUB_TOKEN from Streamlit secrets
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"

DATABASE_FILE = "database.csv"
USERS_FILE = "users.csv"

DATABASE_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
USERS_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{USERS_FILE}"

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def pull_database():
    """
    Pull database.csv from GitHub and save to local 'database.csv'.
    Returns (df, sha).
    """
    resp = requests.get(DATABASE_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        content = resp.json().get("content", "")
        sha = resp.json().get("sha", "")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            f.write(decoded)
        df = pd.read_csv(DATABASE_FILE)
        return df, sha
    else:
        df = pd.DataFrame(columns=["Tab","SubTab","Data"])
        df.to_csv(DATABASE_FILE, index=False)
        return df, None

def push_database(df, sha=None):
    """
    Push local 'database.csv' DataFrame to GitHub.
    If sha is provided, updates existing file; otherwise creates it.
    """
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

def pull_users():
    """
    Pull users.csv from GitHub and save to local 'users.csv'.
    Returns (df, sha).
    """
    resp = requests.get(USERS_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        content = resp.json().get("content","")
        sha = resp.json().get("sha","")
        decoded = base64.b64decode(content).decode("utf-8")
        with open(USERS_FILE,"w",encoding="utf-8") as f:
            f.write(decoded)
    else:
        # minimal CSV
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
    """
    Push local 'users.csv' DataFrame to GitHub.
    If sha is provided, updates existing file; otherwise creates it.
    """
    csv_data = df.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()
    data = {"message": "Update users.csv" if sha else "Create users.csv", "content": encoded}
    if sha:
        data["sha"] = sha
    r = requests.put(USERS_API_URL, headers=HEADERS, json=data)
    return r.status_code
