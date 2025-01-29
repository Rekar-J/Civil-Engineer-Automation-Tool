import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import numpy as np
import plotly.express as px

# Initialize database
def initialize_database():
    if not os.path.exists("database.csv"):
        data = {
            "Tab": [],
            "SubTab": [],
            "Data": []
        }
        pd.DataFrame(data).to_csv("database.csv", index=False)

def load_database():
    initialize_database()
    return pd.read_csv("database.csv")

def save_to_database(tab, subtab, data):
    db = load_database()
    new_entry = pd.DataFrame({
        "Tab": [tab],
        "SubTab": [subtab],
        "Data": [data]
    })
    updated_db = pd.concat([db, new_entry], ignore_index=True)
    updated_db.to_csv("database.csv", index=False)

def delete_data_from_database(tab, subtab):
    db = load_database()
    updated_db = db[~((db["Tab"] == tab) & (db["SubTab"] == subtab))]
    updated_db.to_csv("database.csv", index=False)

def main():
    # Ensure uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Initialize database
    initialize_database()

    st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide", page_icon="🛠️")

    with st.sidebar:
        selected_tab = option_menu(
            "Main Menu",
            ["Home", "Design and Analysis", "Project Management", "Compliance and Reporting", "Tools and Utilities", "Collaboration and Documentation"],
            icons=["house", "tools", "calendar", "file-check", "gear", "people"],
            menu_icon="menu-button",
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#FF5733"},
            }
        )

    if selected_tab == "Home":
        home()
    elif selected_tab == "Design and Analysis":
        design_and_analysis()
    elif selected_tab == "Project Management":
        project_management()
    elif selected_tab == "Compliance and Reporting":
        compliance_and_reporting()
    elif selected_tab == "Tools and Utilities":
        tools_and_utilities()
    elif selected_tab == "Collaboration and Documentation":
        collaboration_and_documentation()

def home():
    st.title("🏠 Home")
    st.write("Welcome to the Civil Engineer Automation Tool. Upload and manage your project media files.")

    database = load_database()

    with st.expander("Upload Media Files"):
        uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])
        if uploaded_file:
            file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            save_to_database("Home", "Media Files", {"file_name": uploaded_file.name, "type": file_type})
            st.success(f"{file_type} uploaded successfully!")

    st.write("### Uploaded Media")
    for _, row in database[database["Tab"] == "Home"].iterrows():
        media_data = eval(row["Data"])
        file_path = os.path.join("uploads", media_data["file_name"])
        col1, col2 = st.columns([3, 1])
        with col1:
            if media_data["type"] == "Image":
                st.image(file_path, caption=media_data["file_name"], use_container_width=True)
            elif media_data["type"] == "Video":
                st.video(file_path)
        with col2:
            if st.button(f"Delete {media_data['file_name']}", key=row["Data"]):
                delete_data_from_database("Home", "Media Files")
                os.remove(file_path)
                st.experimental_rerun()

def design_and_analysis():
    st.title("🛠️ Design and Analysis")
    st.write("Analyze and design structures with the tools provided.")
    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling"])
    handle_tab_input("Design and Analysis", tabs)

def project_management():
    st.title("📅 Project Management")
    st.write("Plan, allocate resources, and monitor project progress.")
    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])
    handle_tab_input("Project Management", tabs)

def compliance_and_reporting():
    st.title("✅ Compliance and Reporting")
    st.write("Ensure adherence to standards and generate detailed reports.")
    tabs = st.tabs(["Standards Verification", "Report Generation"])
    handle_tab_input("Compliance and Reporting", tabs)

def tools_and_utilities():
    st.title("🔧 Tools and Utilities")
    st.write("Use advanced tools for drafting, cost estimation, and visualization.")
    tabs = st.tabs(["Automated Design and Drafting", "Quantity Takeoff and Cost Estimation", "Data Visualization"])
    handle_tab_input("Tools and Utilities", tabs)

def collaboration_and_documentation():
    st.title("🤝 Collaboration and Documentation")
    st.write("Collaborate effectively and manage project documentation.")
    tabs = st.tabs(["Document Management", "Communication Tools"])
    handle_tab_input("Collaboration and Documentation", tabs)

def handle_tab_input(tab_name, tabs):
    for i, tab in enumerate(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling"]):
        with tabs[i]:
            st.header(tab)
            db = load_database()
            existing_data = db[(db["Tab"] == tab_name) & (db["SubTab"] == tab)]
            if not existing_data.empty:
                data = pd.DataFrame([eval(existing_data.iloc[0]["Data"])])
                st.write("### Current Data")
                st.dataframe(data.reset_index(drop=True))
            with st.form(f"form_{tab}"):
                st.write("### Add Data")
                new_data = st.text_area("Enter data as a dictionary (e.g., {'key': 'value'})")
                if st.form_submit_button("Save"):
                    save_to_database(tab_name, tab, new_data)
                    st.success("Data saved successfully!")
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
