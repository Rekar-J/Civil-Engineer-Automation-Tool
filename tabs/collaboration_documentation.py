import streamlit as st
import pandas as pd
from database import save_to_database

def run():
    st.title("🤝 Collaboration and Documentation")

    st.write("This section helps engineers share documents, track revisions, and manage team communication.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    ### DOCUMENT MANAGEMENT ###
    with tabs[0]:  
        st.header("Document Management")
        uploaded_file = st.file_uploader("Upload Project Document", type=["pdf", "docx", "xlsx"])
        if uploaded_file:
            st.success("Document uploaded successfully!")

            # Save document metadata to GitHub
            new_entry = pd.DataFrame({"Document Name": [uploaded_file.name], "File Type": [uploaded_file.type]})
            save_to_database("Collaboration and Documentation", "Document Management", new_entry.to_dict(orient="records"))
