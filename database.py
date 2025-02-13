import base64
import pandas as pd
import requests
import os

# GitHub repository details
GITHUB_TOKEN = "your_github_token_here"  # Replace with your actual token
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"  # Replace with your GitHub repo
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Load database from GitHub
def load_database():
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        return pd.read_csv(pd.compat.StringIO(decoded_content))
    else:
        return pd.DataFrame(columns=["Tab", "SubTab", "Data"])

# Save data to GitHub
def save_to_database(tab, subtab, data):
    db = load_database()
    new_entry = pd.DataFrame({"Tab": [tab], "SubTab": [subtab], "Data": [data]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)
    
    # Convert DataFrame to CSV string
    csv_data = updated_db.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()

    # Update file on GitHub
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        sha = response.json()["sha"]
        update_response = requests.put(
            GITHUB_API_URL,
            headers=HEADERS,
            json={
                "message": "Updated database.csv",
                "content": encoded_content,
                "sha": sha,
            },
        )
    else:
        update_response = requests.put(
            GITHUB_API_URL,
            headers=HEADERS,
            json={
                "message": "Created database.csv",
                "content": encoded_content,
            },
        )
    return update_response.status_code
