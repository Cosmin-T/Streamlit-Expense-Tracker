# navigation.py

import streamlit as st
from streamlit_option_menu import option_menu

def nav() -> str:
    """
    Create a menu for users to select either Data Entry, Data Visualization, or Data Tracker.

    This function returns the selected option as a string.
    """

    # Create a menu for users to select either Data Entry or Data Visualization.
    selected = option_menu(
        menu_title=None,
        options=["Data-Entry", "Data-Visualization", "Data-Tracker"],
        icons=["pencil-fill", "bar-chart-fill", "box-seam-fill"],
        orientation="horizontal"
    )

    # Return the selected option as a string.
    return selected
