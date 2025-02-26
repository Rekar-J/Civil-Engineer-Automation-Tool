import streamlit as st

def run():
    st.header("Automated Design & Drafting")
    st.subheader("📌 About Automated Design & Drafting")
    st.info("This tool allows engineers to **upload and manage CAD files for engineering design**.")

    uploaded_file = st.file_uploader("Upload CAD File", type=["dwg", "dxf", "pdf"], key="cad_upload")
    
    if uploaded_file:
        st.success(f"📁 {uploaded_file.name} uploaded successfully!")
