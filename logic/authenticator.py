# authenticator

import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
from logic.util import *
import bcrypt
import time

# DETA_KEY = 'a0jtvvxnh2x_7Dxsy9FxkYMvoZjtxeCAvQFjJgh1adZ2'

def database():
    deta = Deta(DETA_KEY)
    db = deta.Base('ExpenseTrackerAuth')
    return db

def insert_user(email, username, hashed_password):
    db = database()
    date_joined = str(datetime.datetime.now())
    return db.put({
        'key': email,
        'username': username,
        'password': hashed_password,
        'date_joined': date_joined
    })

def fetch_users():
    db = database()
    fetch = db.fetch()
    users = fetch.items
    return users

def get_user_emails():
    db = database()
    fetch = db.fetch()
    users = fetch.items
    emails = []
    for user in users:
        emails.append(user['key'])
    return emails

def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pattern, email):
        return True
    return False

def get_usernames():
    db = database()
    fetch = db.fetch()
    users = fetch.items
    usernames = []
    for user in users:
        usernames.append(user['username'])
    return usernames

def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def register():
    with st.form(key='register', clear_on_submit=True):
        st.subheader(':green[Register]')
        email = st.text_input(':blue[Email]', placeholder='Enter your email')
        username = st.text_input(':blue[Username]', placeholder='Enter your username')
        password = st.text_input(':blue[Password]', placeholder='Enter your password', type='password')
        confirm_password = st.text_input(':blue[Confirm Password]', placeholder='Confirm your password', type='password')

        b1, b2, b3, b4, b5 = st.columns(5)
        with b4:
            submit = st.form_submit_button('Register')

        if submit:
            if not email or not validate_email(email):
                st.warning('Invalid or missing Email!')
                return

            if email in get_user_emails():
                st.warning('Email Already Exists!')
                return

            if not validate_username(username):
                st.warning('Invalid Username!')
                return

            if username in get_usernames():
                st.warning('Username Already Exists!')
                return

            if len(username) < 2:
                st.warning('Username Too Short')
                return

            if len(password) < 6:
                st.warning('Password Too Short')
                return

            if password != confirm_password:
                st.warning('Passwords Do Not Match!')
                return

            # Hash the password once
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Decode the hashed password to store it as a string
            decoded_hashed_password = hashed_password.decode('utf-8')

            # Debug print here (Make sure to remove after debugging)
            print(f"Debug: Hashed password during registration: {hashed_password}")  # For debugging only!

            # Pass the decoded hashed password to the insert_user function
            user_record = insert_user(email, username, decoded_hashed_password)

            # Debug print here (Make sure to remove after debugging)
            print(f"Debug: Stored user record: {user_record}")  # For debugging only!
            st.success('Account Created Successfully')
            st.balloons()
            time.sleep(2)

            # Redirect user to the login page
            st.session_state['mode'] = 'login'
            st.experimental_rerun()

        with b2:
            login = st.form_submit_button('Login')
        if login:
            st.session_state['mode'] = 'login'
            st.experimental_rerun()

def check_login(username, entered_password):
    db = database()
    users = fetch_users()

    user = next((u for u in users if u['username'] == username), None)
    if user:
        stored_hashed_password = user['password'].encode('utf-8')
        login_attempt = bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)
        print(f"Debug: Stored hashed password: {stored_hashed_password}")  # For debugging only!
        print(f"Debug: Login attempt result: {login_attempt}")  # For debugging only!
        return login_attempt
    return False

def login():

    try:

        users = fetch_users()
        emails = []
        usernames = []
        passwords = []

        for user in users:
            emails.append(user['key'])
            usernames.append(user['username'])
            passwords.append(user['password'])

        credentials = {
            'usernames': {}
        }

        for i in range(len(emails)):
            credentials['usernames'][usernames[i]] = {'name': emails[i], 'password': passwords[i]}

        Authenticator = stauth.Authenticate(credentials, cookie_name='expense', key ='abcdef')
        email, auth_stauts, username = Authenticator.login(':green[Login]', 'main')

        info, info1 = st.columns(2)


        if username:
            if username not in usernames:
                st.warning('Username does not exist, Please Register.')

            if not auth_stauts:
                register()
                st.error('Incorrect Password or Username!')

    except:
        st.success('Refersh Page')