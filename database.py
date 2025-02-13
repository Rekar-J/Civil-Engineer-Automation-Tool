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

# Load database from GitHub
def load_database():
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        file_data = response.json()
        file_content = base64.b64decode(file_data["content"]).decode("utf-8")
        return pd.read_csv(io.StringIO(file_content)), file_data["sha"]
    else:
        return pd.DataFrame(columns=["Tab", "SubTab", "Data"]), None

# Save data to GitHub
def save_to_database(tab, subtab, data):
    db, sha = load_database()
    new_entry = pd.DataFrame({"Tab": [tab], "SubTab": [subtab], "Data": [data]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)

    # Convert DataFrame to CSV
    csv_data = updated_db.to_csv(index=False)
    encoded_content = base64.b64encode(csv_data.encode()).decode()

    payload = {
        "message": "Updated database.csv",
        "content": encoded_content
    }

    if sha:
        payload["sha"] = sha  # Required for updating an existing file

    update_response = requests.put(GITHUB_API_URL, headers=HEADERS, json=payload)
    
    return update_response.status_code
