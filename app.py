import streamlit as st
from streamlit_option_menu import option_menu
import os
from database import load_database, save_to_database, delete_from_database

def main():
    st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide")

    with st.sidebar:
        selected_tab = option_menu(
            "Main Menu",
            ["Home", "Design and Analysis", "Project Management", "Compliance and Reporting", "Tools and Utilities", "Collaboration and Documentation"],
            icons=["house", "tools", "calendar", "file-check", "gear", "people"],
            menu_icon="menu-button",
            default_index=0,
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
    st.title("Welcome to the Civil Engineer Automation Tool")
    st.write("Upload and manage your project media files (images/videos).")

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    database = load_database()

    uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])

    if uploaded_file:
        file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        save_to_database(uploaded_file.name, file_type)
        st.success(f"{file_type} uploaded successfully!")

    st.write("### Uploaded Media")
    for _, row in database.iterrows():
        file_path = os.path.join("uploads", row["Uploaded File"])
        if row["Type"] == "Image":
            st.image(file_path, caption=row["Uploaded File"], use_column_width=True)
        elif row["Type"] == "Video":
            st.video(file_path)

        if st.button(f"Delete {row['Uploaded File']}"):
            delete_from_database(row["Uploaded File"])
            os.remove(file_path)
            st.experimental_rerun()

# Placeholder functions for other tabs
def design_and_analysis():
    st.title("Design and Analysis")

def project_management():
    st.title("Project Management")

def compliance_and_reporting():
    st.title("Compliance and Reporting")

def tools_and_utilities():
    st.title("Tools and Utilities")

def collaboration_and_documentation():
    st.title("Collaboration and Documentation")

if __name__ == "__main__":
    main()
