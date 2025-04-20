import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        return option_menu(
            "Main Menu",
            ["Home", "Design and Analysis", "Project Management",
             "Compliance and Reporting","Tools and Utilities","Collaboration and Documentation"],
            icons=["house","tools","calendar","file-check","gear","people"],
            menu_icon="menu-button",
            default_index=0,
        )
