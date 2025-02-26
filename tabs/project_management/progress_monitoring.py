import streamlit as st
import pandas as pd

def run():
    st.header("Progress Monitoring")
    st.subheader("📌 About Progress Monitoring")
    st.info("Track **project completion, performance metrics, and task status** to ensure projects stay on schedule.")

    task_name = st.text_input("Enter Task Name", key="progress_task_name")
    progress_percentage = st.slider("Completion Percentage", 0, 100, step=5, key="progress_slider")

    if "progress_data" not in st.session_state:
        st.session_state.progress_data = pd.DataFrame(columns=["Task", "Progress (%)"])

    if st.button("Add Progress Data", key="add_progress_task"):
        new_row = pd.DataFrame({"Task": [task_name], "Progress (%)": [progress_percentage]})
        st.session_state.progress_data = pd.concat([st.session_state.progress_data, new_row], ignore_index=True)

    st.write("### Task Progress")
    st.dataframe(st.session_state.progress_data)
