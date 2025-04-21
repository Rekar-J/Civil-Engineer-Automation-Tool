# pushpull.py
import requests
import base64
import pandas as pd
import streamlit as st

# Read from Streamlit secrets
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO  = "Rekar-J/Civil-Engineer-Automation-Tool"

DATABASE_FILE = "database.csv"
USERS_FILE    = "users.csv"

DATABASE_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
USERS_API_URL    = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{USERS_FILE}"

HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}


def pull_database():
    """Pull database.csv from GitHub. Returns (df, sha)."""
    resp = requests.get(DATABASE_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        payload = resp.json()
        sha     = payload.get("sha")
        content = base64.b64decode(payload.get("content", "")).decode("utf-8")
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        df = pd.read_csv(DATABASE_FILE)
        return df, sha

    # not found or error → start fresh
    df = pd.DataFrame(columns=["Tab","SubTab","Data"])
    df.to_csv(DATABASE_FILE, index=False)
    return df, None


def push_database(df, sha=None):
    """
    Push local 'database.csv' DataFrame to GitHub.
    If sha is None, we first fetch the real SHA so we update instead of create.
    Returns HTTP status code.
    """
    # 1) prepare content
    csv_data = df.to_csv(index=False)
    b64      = base64.b64encode(csv_data.encode()).decode()

    # 2) if we don’t already have a sha, fetch it so we update rather than create
    if sha is None:
        head = requests.get(DATABASE_API_URL, headers=HEADERS)
        if head.status_code == 200:
            sha = head.json().get("sha")

    payload = {
        "message": "Update database.csv" if sha else "Create database.csv",
        "content": b64,
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(DATABASE_API_URL, headers=HEADERS, json=payload)
    return r.status_code


def pull_users():
    """Pull users.csv from GitHub. Returns (df, sha)."""
    resp = requests.get(USERS_API_URL, headers=HEADERS)
    if resp.status_code == 200:
        payload = resp.json()
        sha     = payload.get("sha")
        content = base64.b64decode(payload.get("content", "")).decode("utf-8")
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        df = pd.read_csv(USERS_FILE)
        return df, sha

    # not found or error → start fresh
    df = pd.DataFrame(columns=["username","password","token"])
    df.to_csv(USERS_FILE, index=False)
    return df, None


def push_users(df, sha=None):
    """
    Push local 'users.csv' DataFrame to GitHub.
    If sha is None, fetch it so we update the existing file.
    Returns HTTP status code.
    """
    csv_data = df.to_csv(index=False)
    b64      = base64.b64encode(csv_data.encode()).decode()

    if sha is None:
        head = requests.get(USERS_API_URL, headers=HEADERS)
        if head.status_code == 200:
            sha = head.json().get("sha")

    payload = {
        "message": "Update users.csv" if sha else "Create users.csv",
        "content": b64,
    }
    if sha:
        payload["sha"] = sha

    r = requests.put(USERS_API_URL, headers=HEADERS, json=payload)
    return r.status_code
