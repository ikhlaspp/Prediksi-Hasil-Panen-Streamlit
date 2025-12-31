"""
Styling utilities
"""
import streamlit as st
from config.theme import get_custom_css


def apply_custom_css():
    """Apply custom CSS styling to the app"""
    st.markdown(get_custom_css(), unsafe_allow_html=True)
