# navigation.py

import streamlit as st
from streamlit_option_menu import option_menu

def nav():

    # Create a menu for users to select either Data Entry or Data Visualization.
    selected = option_menu(
        menu_title=None,
        options=["Data-Entry", "Data-Visualization", "Data-Tracker"],
        icons=["pencil-fill", "bar-chart-fill", "box-seam-fill"],
        orientation="horizontal"
    )
    return selected