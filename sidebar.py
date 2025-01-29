import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        selected_tab = option_menu(
            "Main Menu",
            ["Home", "Design and Analysis", "Project Management", "Compliance and Reporting", "Tools and Utilities", "Collaboration and Documentation"],
            icons=["house", "tools", "calendar", "file-check", "gear", "people"],
            menu_icon="menu-button",
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#FF5733"},
            }
        )
    return selected_tab
