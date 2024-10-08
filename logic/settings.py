# settings.py

import streamlit as st

def settings():
    """
    Set up the Streamlit page with custom CSS styles and hide unwanted components.
    """
    # Set basic configurations for the Streamlit page.
    page_title = "Expense Tracker"
    st.set_page_config(page_title=page_title,)
    st.title(f"{page_title} ")

    # Use custom CSS to hide the Streamlit's default menu, footer, and header for cleaner UI.
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Insert your CSS style
    custom_css = """
    <style>
        /* Set the background color to a dark blue. */
        body {
            background-color: #002b36;
        }

        /* Set the color and font weight of the headings. */
        h1, h2, h3, h4, h5, h6 {
            color: #999;
            font-weight: 500;
            transition: color 0.3s;
        }

        /* Set the background color of the main content area to a gradient. */
        .stApp {
            background: linear-gradient(200deg, #002b36 20%, #1e1e1e 90%);
            border-radius: 10px;
            box-shadow: 3px 3px 20px rgba(0, 0, 0, 0.3);
            padding: 50px;
        }

        /* Set the style of the buttons. */
        .stButton>button {
            background-color: #6a2336;
            color: #FFF;
            border: none;
            border-radius: 12px;
        }

        /* Change the button color on hover. */
        .stButton>button:hover {
            background-color: #5E0000;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
