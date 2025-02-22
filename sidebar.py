import streamlit as st
from streamlit_option_menu import option_menu
from style import apply_sidebar_styles

def render_sidebar():
    """
    Renders the sidebar with a black background, 
    bright icons, and any styles from style.py.
    """
    with st.sidebar:
        selected_tab = option_menu(
            "Main Menu",
            ["Home", "Design and Analysis", "Project Management", "Compliance and Reporting", "Tools and Utilities", "Collaboration and Documentation"],
            icons=["house", "tools", "calendar", "file-check", "gear", "people"],
            menu_icon="menu-button",
            default_index=0,
            styles=apply_sidebar_styles()  # KEY line
        )
    return selected_tab
