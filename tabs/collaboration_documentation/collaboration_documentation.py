import streamlit as st
from tabs.document_management import run as document_management
from tabs.communication_tools import run as communication_tools

def run():
    st.title("📂 Collaboration and Documentation")

    st.write("This section provides tools for managing project documents and communication.")

    tabs = st.tabs(["Document Management", "Communication Tools"])

    with tabs[0]:  
        document_management()

    with tabs[1]:  
        communication_tools()
