import streamlit as st
import pandas as pd
import os

UPLOADS_DIR = "uploads/documents"

def run():
    st.header("Document Management")
    st.subheader("📌 About Document Management")
    st.info("Upload, store, and manage project documents with **version control and sharing options**.")

    # Ensure the 'uploads/documents' directory exists
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)

    uploaded_file = st.file_uploader("Upload Project Document", type=["pdf", "docx", "xlsx"], key="doc_upload")

    if "document_data" not in st.session_state:
        st.session_state.document_data = pd.DataFrame(columns=["File Name", "File Path"])

    if uploaded_file:
        file_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        new_row = pd.DataFrame({"File Name": [uploaded_file.name], "File Path": [file_path]})
        st.session_state.document_data = pd.concat([st.session_state.document_data, new_row], ignore_index=True)

    st.write("### Stored Documents")
    if not st.session_state.document_data.empty:
        for _, row in st.session_state.document_data.iterrows():
            st.markdown(f"📄 **{row['File Name']}**  |  [Download](/{row['File Path']})")
    else:
        st.info("No documents uploaded yet.")
