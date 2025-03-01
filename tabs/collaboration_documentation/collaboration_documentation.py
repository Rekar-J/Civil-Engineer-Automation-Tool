import streamlit as st

def run():
    st.header("Document Management")
    st.subheader("📌 About Document Management")
    st.info("Manage your project documents, including designs, reports, and contracts.")
    
    # File uploader for document management
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "txt", "xls", "xlsx"], key="doc_upload")
    
    if uploaded_file:
        st.success(f"📁 {uploaded_file.name} uploaded successfully!")
