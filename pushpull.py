import streamlit as st
import requests
import base64
import pandas as pd

GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO  = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
USERS_FILE    = "users.csv"

DB_URL   = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
USERS_URL= f"https://api.github.com/repos/{GITHUB_REPO}/contents/{USERS_FILE}"
HEADERS  = {"Authorization": f"token {GITHUB_TOKEN}"}

def pull_database():
    resp = requests.get(DB_URL, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        content = base64.b64decode(data["content"]).decode()
        sha     = data["sha"]
        with open(DATABASE_FILE,"w") as f: f.write(content)
        return pd.read_csv(DATABASE_FILE), sha
    # fallback
    df = pd.DataFrame(columns=["Tab","SubTab","Data"])
    df.to_csv(DATABASE_FILE,index=False)
    return df, None

def push_database(df, sha=None):
    csv = df.to_csv(index=False)
    content = base64.b64encode(csv.encode()).decode()
    payload = {"message": "Update database.csv", "content": content}
    if sha: payload["sha"] = sha
    return requests.put(DB_URL, headers=HEADERS, json=payload).status_code

def pull_users():
    resp = requests.get(USERS_URL, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        content = base64.b64decode(data["content"]).decode()
        sha     = data["sha"]
        with open(USERS_FILE,"w") as f: f.write(content)
    else:
        with open(USERS_FILE,"w") as f:
            f.write("username,password,token\n")
        sha = None
    try:
        df = pd.read_csv(USERS_FILE)
    except:
        df = pd.DataFrame(columns=["username","password","token"])
        df.to_csv(USERS_FILE,index=False)
    return df, sha

def push_users(df, sha=None):
    csv = df.to_csv(index=False)
    content = base64.b64encode(csv.encode()).decode()
    payload = {"message":"Update users.csv","content":content}
    if sha: payload["sha"] = sha
    return requests.put(USERS_URL, headers=HEADERS, json=payload).status_code
