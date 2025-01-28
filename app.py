import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import numpy as np
import plotly.express as px
from database import load_database, save_to_database, delete_from_database

def main():
    # Ensure the 'uploads' directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

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
            st.image(file_path, caption=row["Uploaded File"], use_container_width=True)
        elif row["Type"] == "Video":
            st.video(file_path)

        if st.button(f"Delete {row['Uploaded File']}"):
            delete_from_database(row["Uploaded File"])
            os.remove(file_path)
            st.experimental_rerun()

def design_and_analysis():
    st.title("Design and Analysis")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling"])

    with tabs[0]:
        st.header("Structural Analysis")
        st.write("Example: Load Calculations")
        sample_data = pd.DataFrame({
            "Load Type": ["Dead Load", "Live Load", "Wind Load", "Seismic Load"],
            "Load Value (kN)": [500, 300, 150, 200]
        })
        st.dataframe(sample_data)
        st.bar_chart(sample_data.set_index("Load Type"))

    with tabs[1]:
        st.header("Geotechnical Analysis")
        st.write("Example: Soil Properties")
        sample_soil_data = pd.DataFrame({
            "Soil Type": ["Clay", "Sand", "Gravel", "Silt"],
            "Density (kg/m3)": [1600, 1800, 2000, 1500],
            "Cohesion (kPa)": [25, 5, 0, 15]
        })
        st.dataframe(sample_soil_data)
        fig = px.scatter(sample_soil_data, x="Density (kg/m3)", y="Cohesion (kPa)", color="Soil Type", title="Soil Properties")
        st.plotly_chart(fig)

    with tabs[2]:
        st.header("Hydraulic and Hydrological Modeling")
        st.write("Example: Water Flow Simulation")
        time = np.arange(0, 10, 0.1)
        flow_rate = np.sin(time) * 100 + 200
        st.line_chart(pd.DataFrame({"Time (s)": time, "Flow Rate (L/s)": flow_rate}))

def project_management():
    st.title("Project Management")

    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])

    with tabs[0]:
        st.header("Scheduling")
        st.write("Example: Project Timeline")
        sample_timeline = pd.DataFrame({
            "Task": ["Foundation", "Framing", "Roofing", "Finishing"],
            "Start Date": ["2025-01-01", "2025-01-15", "2025-02-01", "2025-02-15"],
            "End Date": ["2025-01-14", "2025-01-31", "2025-02-14", "2025-02-28"]
        })
        st.dataframe(sample_timeline)

    with tabs[1]:
        st.header("Resource Allocation")
        st.write("Example: Labor Assignment")
        labor_data = pd.DataFrame({
            "Worker": ["John", "Jane", "Paul", "Anna"],
            "Role": ["Engineer", "Foreman", "Technician", "Supervisor"],
            "Assigned Task": ["Foundation", "Framing", "Roofing", "Finishing"]
        })
        st.dataframe(labor_data)

    with tabs[2]:
        st.header("Progress Monitoring")
        st.write("Example: Task Completion Status")
        progress_data = pd.DataFrame({
            "Task": ["Foundation", "Framing", "Roofing", "Finishing"],
            "Completion (%)": [100, 75, 50, 25]
        })
        st.dataframe(progress_data)
        st.bar_chart(progress_data.set_index("Task"))

def compliance_and_reporting():
    st.title("Compliance and Reporting")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:
        st.header("Standards Verification")
        st.write("Example: Building Code Checklist")
        compliance_data = pd.DataFrame({
            "Requirement": ["Fire Safety", "Structural Integrity", "Electrical Standards", "Environmental Impact"],
            "Status": ["Pass", "Pass", "Fail", "Pending"]
        })
        st.dataframe(compliance_data)

    with tabs[1]:
        st.header("Report Generation")
        st.write("Example: Analysis Summary")
        report_summary = """
        - **Total Load Analysis**: 1150 kN
        - **Critical Soil Type**: Clay
        - **Environmental Impact**: Pending
        """
        st.markdown(report_summary)

def tools_and_utilities():
    st.title("Tools and Utilities")

    tabs = st.tabs(["Automated Design and Drafting", "Quantity Takeoff and Cost Estimation", "Data Visualization"])

    with tabs[0]:
        st.header("Automated Design and Drafting")
        st.write("Example: CAD Design Overview")
        st.image("https://via.placeholder.com/600x400?text=CAD+Preview", caption="Sample CAD Design")

    with tabs[1]:
        st.header("Quantity Takeoff and Cost Estimation")
        st.write("Example: Material Quantification")
        quantity_data = pd.DataFrame({
            "Material": ["Concrete", "Steel", "Bricks", "Wood"],
            "Quantity": [100, 50, 500, 200],
            "Unit": ["m3", "tons", "pieces", "pieces"]
        })
        st.dataframe(quantity_data)

    with tabs[2]:
        st.header("Data Visualization")
        st.write("Example: Project Cost Breakdown")
        cost_data = pd.DataFrame({
            "Category": ["Materials", "Labor", "Equipment", "Miscellaneous"],
            "Cost (USD)": [5000, 3000, 2000, 1000]
        })
        fig = px.pie(cost_data, names="Category", values="Cost (USD)", title="Project Cost Breakdown")
        st.plotly_chart(fig)

def collaboration_and_documentation():
    st.title("Collaboration and Documentation")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    with tabs[0]:
        st.header("Document Management")
        st.write("Example: Version Control")
        version_data = pd.DataFrame({
            "File": ["Design_v1.pdf", "Design_v2.pdf", "Report_v1.docx"],
            "Version": [1, 2, 1],
            "Last Updated": ["2025-01-01", "2025-01-15", "2025-01-20"]
        })
        st.dataframe(version_data)

    with tabs[1]:
        st.header("Communication Tools")
        st.write("Example: Meeting Schedule")
        meetings = pd.DataFrame({
            "Date": ["2025-01-10", "2025-01-17", "2025-01-24"],
            "Topic": ["Design Review", "Progress Update", "Final Presentation"],
            "Attendees": ["Team A", "Team B", "Team C"]
        })
        st.dataframe(meetings)

if __name__ == "__main__":
    main()
