import streamlit as st
import pandas as pd

def run():
    st.header("Resource Allocation")
    st.subheader("📌 About Resource Allocation")
    st.info("This tool helps engineers assign **labor, equipment, and materials** to different tasks.")

    resource = st.text_input("Enter Resource Name", key="resource_name")
    assigned_task = st.text_input("Assigned Task", key="assigned_task")

    if "resource_data" not in st.session_state:
        st.session_state.resource_data = pd.DataFrame(columns=["Resource", "Assigned Task"])

    if st.button("Allocate Resource", key="allocate_resource"):
        new_row = pd.DataFrame({"Resource": [resource], "Assigned Task": [assigned_task]})
        st.session_state.resource_data = pd.concat([st.session_state.resource_data, new_row], ignore_index=True)

    st.write("### Resource Allocation")
    st.dataframe(st.session_state.resource_data)
