# core/config.py
"""
Application configuration and setup.
Handles Streamlit page configuration and CSS application.
"""

import streamlit as st
from ui.styles import css as ui_css


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Social Analytics Hub",
        layout="wide",
        page_icon="📊",
        initial_sidebar_state="expanded",
    )


def apply_css():
    """Apply custom CSS styling to the app."""
    st.markdown(ui_css(), unsafe_allow_html=True)
