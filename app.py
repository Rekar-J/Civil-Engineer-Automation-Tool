import streamlit as st
from tabs import design_analysis, project_management, compliance_reporting, tools_utilities, collaboration_documentation
import os
import pandas as pd
import requests
from sidebar import render_sidebar

# GitHub repository details
GITHUB_TOKEN = "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"  # Replace this with your actual token
GITHUB_REPO = "Rekar-J/Civil-Engineer-Automation-Tool"  # Replace with your GitHub repo
DATABASE_FILE = "database.csv"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATABASE_FILE}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}


# Function to load the database from GitHub
def load_database():
    response = requests.get(GITHUB_API_URL, headers=HEADERS)
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        return pd.read_csv(pd.compat.StringIO(decoded_content))
    else:
        return pd.DataFrame(columns=["Tab", "SubTab", "Data"])


# Function to save data to the database
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


# Ensure the 'uploads' directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

# Render Sidebar
selected_tab = render_sidebar()

if selected_tab == "Home":
    st.title("Welcome to the Civil Engineer Automation Tool")
    st.write("Upload and manage your project media files (images/videos).")

    uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])

    if uploaded_file:
        file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"{file_type} uploaded successfully!")

elif selected_tab == "Design and Analysis":
    design_analysis.run()

elif selected_tab == "Project Management":
    project_management.run()

elif selected_tab == "Compliance and Reporting":
    compliance_reporting.run()

elif selected_tab == "Tools and Utilities":
    tools_utilities.run()

elif selected_tab == "Collaboration and Documentation":
    collaboration_documentation.run()
