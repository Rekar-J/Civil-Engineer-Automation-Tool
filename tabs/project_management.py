import streamlit as st
import pandas as pd

def run():
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

    with tabs[1]:
        st.header("Resource Allocation")
        resource_data = pd.DataFrame({
            "Resource": ["Workers", "Equipment", "Materials"],
            "Assigned Task": ["Foundation", "Framing", "Roofing"]
        })
        st.dataframe(resource_data)

    with tabs[2]:
        st.header("Progress Monitoring")
        progress_data = pd.DataFrame({
            "Task": ["Foundation", "Framing", "Roofing"],
            "Completion (%)": [100, 75, 50]
        })
        st.dataframe(progress_data)
