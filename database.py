import base64
import pandas as pd
import requests
import io

# ✅ GitHub repository details
GITHUB_TOKEN = "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"
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

# ✅ Function to load database from GitHub
def load_database():
    response = requests.get(GITHUB_API_URL, headers=HEADERS)

    if response.status_code == 200:
        file_data = response.json()
        file_content = base64.b64decode(file_data["content"]).decode("utf-8")
        df = pd.read_csv(io.StringIO(file_content))

        # Ensure correct columns exist
        expected_columns = ["Tab", "SubTab", "Data"]
        if not all(col in df.columns for col in expected_columns):
            df = pd.DataFrame(columns=expected_columns)

        return df, file_data["sha"]

    else:
        # If file doesn't exist, create empty database
        return pd.DataFrame(columns=["Tab", "SubTab", "Data"]), None

# ✅ Function to save data to GitHub
def save_to_database(tab, subtab, data):
    db, sha = load_database()

    if isinstance(data, dict):
        data = str(data)  # Convert dictionary to string before saving

    # Append new entry
    new_entry = pd.DataFrame({"Tab": [tab], "SubTab": [subtab], "Data": [data]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)

    # Convert DataFrame to CSV string
    csv_data = updated_db.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()

    payload = {
        "message": "Updated database.csv",
        "content": encoded_content
    }

    if sha:
        payload["sha"] = sha  # Required for updating an existing file

    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        print("✅ Database successfully updated on GitHub.")
    else:
        print("❌ Failed to update database on GitHub:", response.json())

    return response.status_code

