# main.py

import streamlit as st
from logic.settings import *
from logic.app import *
from logic.authenticator import *

def main():
    """
    The main entry point for the expense tracker app.

    Handles the user's choice between the login, register, and app sections.
    """
    # Configure the page with title and icon
    settings()

    # Check if the mode is set in the session state, if not, set it to login
    if 'mode' not in st.session_state:
        st.session_state['mode'] = 'login'

    # If the mode is set to login, display the login form
    if st.session_state['mode'] == 'login':
        with st.form('login_form'):
            st.subheader(':green[Login]')

            # Get the username and password from the user
            username = st.text_input(':blue[Username]')
            password = st.text_input(':blue[Password]', type='password')

            # Add buttons for the login form
            b1, b2, b3, b4, b5 = st.columns(5)
            with b2:
                submitted = st.form_submit_button('Login')

            # If the form is submitted, check the login credentials
            if submitted:
                if validate_username(username):
                    if username in get_usernames():
                        if check_login(username, password):
                            st.session_state['username'] = username  # Save username in session state
                            st.session_state['mode'] = 'app'  # Login successful
                            st.rerun()
                        else:
                            st.error('Incorrect password. Please try again.')  # Wrong password
                    else:
                        st.error('Username does not exist.')  # Username does not exist
                else:
                    st.error('Invalid username format.')  # Username format is wrong

            # Add a button to switch to the register form
            with b4:
                registering = st.form_submit_button('Register')
                if registering:
                    st.session_state['mode'] = 'register'  # Switch to register form
                    st.rerun()

    # Display the registration form
    if st.session_state['mode'] == 'register':
        register()

    # If the mode is set to app, run the main application
    if st.session_state['mode'] == 'app':
        og_app()

if __name__ == '__main__':
    main()