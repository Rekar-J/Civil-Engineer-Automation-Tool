import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import numpy as np
import plotly.express as px

# Initialize database
if not os.path.exists("database.csv"):
    pd.DataFrame(columns=["Tab", "SubTab", "Data"]).to_csv("database.csv", index=False)

def load_database():
    return pd.read_csv("database.csv")

def save_to_database(tab, subtab, data):
    db = load_database()
    new_entry = pd.DataFrame({"Tab": [tab], "SubTab": [subtab], "Data": [data]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)
    updated_db.to_csv("database.csv", index=False)

def main():
    # Ensure uploads directory exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    st.set_page_config(page_title="Civil Engineer Automation Tool", layout="wide", page_icon="🛠️")

    with st.sidebar:
        selected_tab = option_menu(
            "Main Menu",
            ["Home", "Design and Analysis", "Project Management", "Compliance and Reporting", "Tools and Utilities", "Collaboration and Documentation"],
            icons=["house", "tools", "calendar", "file-check", "gear", "people"],
            menu_icon="menu-button",
            default_index=0
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

    with st.expander("Upload Media Files"):
        uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov"])
        if uploaded_file:
            file_type = "Video" if uploaded_file.type.startswith("video/") else "Image"
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"{file_type} uploaded successfully!")

def design_and_analysis():
    st.title("🛠️ Design and Analysis")
    st.write("Analyze and design structures with the tools provided.")

    tabs = st.tabs(["Structural Analysis", "Geotechnical Analysis", "Hydraulic and Hydrological Modeling"])

    with tabs[0]:
        st.header("Structural Analysis")
        st.write("Example: Load Calculations")
        sample_data = pd.DataFrame({
            "Load Type": ["Dead Load", "Live Load", "Wind Load", "Seismic Load"],
            "Load Value (kN)": [500, 300, 150, 200]
        })
        st.dataframe(sample_data)
        st.write("Add your own data:")
        load_type = st.text_input("Enter Load Type")
        load_value = st.number_input("Enter Load Value (kN)", min_value=0)
        if st.button("Add Load"):
            new_row = pd.DataFrame({"Load Type": [load_type], "Load Value (kN)": [load_value]})
            sample_data = pd.concat([sample_data, new_row], ignore_index=True)
            st.dataframe(sample_data)
        st.write("### Result: Total Load")
        total_load = sample_data["Load Value (kN)"].sum()
        st.write(f"The total load is **{total_load} kN**. Ensure this value meets the design criteria per ACI standards.")

    with tabs[1]:
        st.header("Geotechnical Analysis")
        st.write("Evaluate soil properties for foundation design.")
        sample_soil_data = pd.DataFrame({
            "Soil Type": ["Clay", "Sand", "Gravel", "Silt"],
            "Density (kg/m3)": [1600, 1800, 2000, 1500],
            "Cohesion (kPa)": [25, 5, 0, 15]
        })
        st.dataframe(sample_soil_data)
        st.write("Add your own data:")
        soil_type = st.text_input("Enter Soil Type")
        density = st.number_input("Enter Density (kg/m3)", min_value=0)
        cohesion = st.number_input("Enter Cohesion (kPa)", min_value=0)
        if st.button("Add Soil Data"):
            new_row = pd.DataFrame({"Soil Type": [soil_type], "Density (kg/m3)": [density], "Cohesion (kPa)": [cohesion]})
            sample_soil_data = pd.concat([sample_soil_data, new_row], ignore_index=True)
            st.dataframe(sample_soil_data)
        st.write("### Result: Foundation Recommendation")
        if cohesion > 20:
            st.write("The soil is suitable for shallow foundations.")
        else:
            st.write("Consider deep foundations due to low cohesion.")

    with tabs[2]:
        st.header("Hydraulic and Hydrological Modeling")
        st.write("Simulate water flow and design drainage systems.")
        time = np.arange(0, 10, 0.1)
        flow_rate = np.sin(time) * 100 + 200
        st.line_chart(pd.DataFrame({"Time (s)": time, "Flow Rate (L/s)": flow_rate}))
        st.write("Add your flow simulation data:")
        simulation_time = st.number_input("Enter Simulation Time (s)", min_value=0)
        flow = st.number_input("Enter Flow Rate (L/s)", min_value=0)
        if st.button("Add Simulation Data"):
            st.write(f"Added data: Time = {simulation_time}s, Flow Rate = {flow}L/s")
        st.write("### Result: Drainage Design")
        if flow > 250:
            st.write("The flow rate exceeds typical capacity. Design larger drainage pipes.")
        else:
            st.write("The flow rate is within acceptable limits for standard drainage systems.")

def project_management():
    st.title("📅 Project Management")
    st.write("Plan, allocate resources, and monitor project progress.")

    tabs = st.tabs(["Scheduling", "Resource Allocation", "Progress Monitoring"])

    with tabs[0]:
        st.header("Scheduling")
        sample_timeline = pd.DataFrame({
            "Task": ["Foundation", "Framing", "Roofing", "Finishing"],
            "Start Date": ["2025-01-01", "2025-01-15", "2025-02-01", "2025-02-15"],
            "End Date": ["2025-01-14", "2025-01-31", "2025-02-14", "2025-02-28"]
        })
        st.dataframe(sample_timeline)
        st.write("### Result: Project Duration")
        duration = pd.to_datetime(sample_timeline["End Date"]).max() - pd.to_datetime(sample_timeline["Start Date"]).min()
        st.write(f"The total project duration is **{duration.days} days**.")

def compliance_and_reporting():
    st.title("✅ Compliance and Reporting")
    st.write("Ensure adherence to standards and generate detailed reports.")

    tabs = st.tabs(["Standards Verification", "Report Generation"])

    with tabs[0]:
        st.header("Standards Verification")
        compliance_data = pd.DataFrame({
            "Requirement": ["Fire Safety", "Structural Integrity", "Electrical Standards", "Environmental Impact"],
            "Status": ["Pass", "Pass", "Fail", "Pending"]
        })
        st.dataframe(compliance_data)
        st.write("### Result: Compliance Status")
        if "Fail" in compliance_data["Status"].values:
            st.write("Some requirements are not met. Address the failures immediately.")
        else:
            st.write("All requirements are met. The project complies with standards.")

def tools_and_utilities():
    st.title("🔧 Tools and Utilities")
    st.write("Use advanced tools for drafting, cost estimation, and visualization.")

    tabs = st.tabs(["Automated Design and Drafting", "Quantity Takeoff and Cost Estimation", "Data Visualization"])

    with tabs[0]:
        st.header("Automated Design and Drafting")
        st.image("https://via.placeholder.com/600x400?text=CAD+Preview", caption="Sample CAD Design")
        st.write("Upload and manage your CAD designs.")

    with tabs[1]:
        st.header("Quantity Takeoff and Cost Estimation")
        sample_materials = pd.DataFrame({
            "Material": ["Concrete", "Steel", "Bricks", "Wood"],
            "Quantity": [100, 50, 500, 200],
            "Unit": ["m3", "tons", "pieces", "pieces"]
        })
        st.dataframe(sample_materials)
        st.write("### Result: Total Material Quantities")
        total_materials = sample_materials.groupby("Unit")["Quantity"].sum()
        for unit, quantity in total_materials.items():
            st.write(f"{quantity} {unit}")

    with tabs[2]:
        st.header("Data Visualization")
        cost_data = pd.DataFrame({
            "Category": ["Materials", "Labor", "Equipment", "Miscellaneous"],
            "Cost (USD)": [5000, 3000, 2000, 1000]
        })
        fig = px.pie(cost_data, names="Category", values="Cost (USD)", title="Project Cost Breakdown")
        st.plotly_chart(fig)

def collaboration_and_documentation():
    st.title("🤝 Collaboration and Documentation")
    st.write("Collaborate effectively and manage project documentation.")
    tabs = st.tabs(["Document Management", "Communication Tools"])

    with tabs[0]:
        st.header("Document Management")
        version_data = pd.DataFrame({
            "File": ["Design_v1.pdf", "Design_v2.pdf", "Report_v1.docx"],
            "Version": [1, 2, 1],
            "Last Updated": ["2025-01-01", "2025-01-15", "2025-01-20"]
        })
        st.dataframe(version_data)

    with tabs[1]:
        st.header("Communication Tools")
        meetings = pd.DataFrame({
            "Date": ["2025-01-10", "2025-01-17", "2025-01-24"],
            "Topic": ["Design Review", "Progress Update", "Final Presentation"],
            "Attendees": ["Team A", "Team B", "Team C"]
        })
        st.dataframe(meetings)

if __name__ == "__main__":
    main()
