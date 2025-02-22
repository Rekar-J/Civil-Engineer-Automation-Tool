import streamlit as st

def apply_sidebar_styles():
    """
    Returns a dict for the 'option_menu' styles param.
    Additional styling can be done here for the sidebar. 
    """
    return {
        "container": {
            "padding": "5px",
            "background-color": "#111111",  # Dark sidebar
        },
        "icon": {
            "color": "#ff9800",   # Brighter orange icon
            "font-size": "25px"
        },
        "nav-link": {
            "font-size": "20px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#333333", # Slightly lighter hover
            "color": "#ffffff",        # White text in sidebar
        },
        "nav-link-selected": {
            "background-color": "#444444",
            "color": "#ffffff",
        },
    }

def load_global_style():
    """
    Injects global CSS to make the entire app's background black,
    text lighter, and headings bold with a bright color.
    """
    st.markdown(
        """
        <style>
        /* Make main background black, text a grayish color */
        body, .main, .block-container {
            background-color: #000000 !important;
            color: #dddddd !important;
        }
        /* Adjust default text color for Streamlit widgets */
        .stTextInput, .stCheckbox, .stButton, .stSlider {
            color: #dddddd !important;
        }
        /* Headings (H1-H5) in bold and bright color (orange) */
        h1, h2, h3, h4, h5 {
            color: #ffa500 !important;
            font-weight: bold !important;
        }
        /* 
        Optionally style code blocks or other elements 
        for a dark theme if you prefer. 
        */
        code, pre {
            background-color: #222222 !important;
            color: #ffffff !important;
        }
        /* Adjust text for Streamlit 'success', 'warning', 'error', 'info' blocks */
        .stAlert, .st-expander {
            background-color: #111111 !important;
            color: #dddddd !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
