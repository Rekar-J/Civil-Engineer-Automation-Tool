import base64
import pandas as pd
import requests
import io

# GitHub repository details
GITHUB_TOKEN = "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"
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Function to load database from GitHub
def load_database():
    response = requests.get(GITHUB_API_URL, headers=HEADERS)

    if response.status_code == 200:
        file_data = response.json()
        file_content = base64.b64decode(file_data["content"]).decode("utf-8")
        df = pd.read_csv(io.StringIO(file_content))

        # Ensure the correct columns exist
        expected_columns = ["Tab", "SubTab", "Data"]
        if not all(col in df.columns for col in expected_columns):
            df = pd.DataFrame(columns=expected_columns)

        return df, file_data["sha"]

    else:
        # If file doesn't exist, return an empty DataFrame
        return pd.DataFrame(columns=["Tab", "SubTab", "Data"]), None

# Function to save data to GitHub
def save_to_database(tab, subtab, data):
    db, sha = load_database()

    # Convert dictionary to string if data is a dictionary
    if isinstance(data, dict):
        data = str(data)

    # Add new entry
    new_entry = pd.DataFrame({"Tab": [tab], "SubTab": [subtab], "Data": [data]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)

    # Convert DataFrame to CSV string
    csv_data = updated_db.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()

    # Prepare GitHub payload
    payload = {
        "message": "Updated database.csv",
        "content": encoded_content
    }

    # If the file exists, include SHA to update it
    if sha:
        payload["sha"] = sha

    response = requests.put(GITHUB_API_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200 or response.status_code == 201:
        print("✅ Database successfully updated on GitHub.")
    else:
        print("❌ Failed to update database on GitHub:", response.json())

    return response.status_code
