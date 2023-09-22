# settings.py

import streamlit as st

def settings():

    # Set basic configurations for the Streamlit page.
    page_title = "Expense Tracker"
    page_icon = ":money_with_wings:"
    st.set_page_config(page_title=page_title, page_icon=page_icon)
    st.title(f"{page_title} {page_icon}")

    # Use custom CSS to hide the Streamlit's default menu, footer, and header for cleaner UI.
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
