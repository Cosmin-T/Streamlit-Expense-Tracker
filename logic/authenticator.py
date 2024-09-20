# authenticator

import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import re
from deta import Deta
from logic.util import *
from cryptography.fernet import Fernet
import time
import pymysql

def database() -> pymysql.Connection:
    """
    Connects to the database and returns a database connection object.

    Raises:
        pymysql.Error: If there is an error connecting to the database.
    """
    connection = None
    try:
        connection = pymysql.connect(
            # Database connection parameters
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=int(PORT),
            database=DATABASE,
        )
        print(f'Connected to database: {connection} ')
    except pymysql.Error as e:
        # Print error message if there is an error connecting to the database
        print(f'Error connecting to database: {e}')
        # Raise the exception so it can be handled by the caller
        raise

    return connection

# Encrypt password
def encrypt_password(password: str) -> str:
    """
    Encrypts the given password using Fernet key.

    Args:
        password (str): The password to encrypt.

    Returns:
        str: The encrypted password.
    """
    cipher = Fernet(KEY)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

# Decrypt password
def decrypt_password(encrypted_password: str) -> str:
    """
    Decrypts the given password using Fernet key.

    Args:
        encrypted_password (str): The password to decrypt.

    Returns:
        str: The decrypted password.
    """
    cipher = Fernet(KEY)
    # Decode the encrypted password from bytes to string
    return cipher.decrypt(encrypted_password.encode()).decode()

def insert_user(email: str, username: str, hashed_password: str) -> None:
    """
    Inserts a new user into the database.

    Args:
        email (str): The email address of the user.
        username (str): The username of the user.
        hashed_password (str): The hashed password of the user.
    """
    # Establish a connection to the database
    conn = database()

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    # Get the current date and time
    date_joined = str(datetime.now())

    # Execute the query to insert the user
    query = "INSERT INTO ExpenseTrackerAuth (email, username, password, date_joined) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (email, username, hashed_password, date_joined))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def fetch_users():
    """
    Fetches all users from the database.

    Returns:
        list: A list of dictionaries where each dictionary represents a user.
    """
    # Establish a connection to the database
    conn = database()

    # Create a cursor object to execute queries
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Execute the query to get all users
    query = "SELECT * FROM ExpenseTrackerAuth"
    cursor.execute(query)

    # Fetch all the users
    users = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return users

def get_user_emails():
    """
    Fetches all the emails from the database.

    Returns:
        list: A list of all the emails in the database.
    """
    # Fetch all the users from the database
    users = fetch_users()

    # Extract the emails from the users
    emails = [user['email'] for user in users]

    # Return the list of emails
    return emails

def get_usernames():
    """
    Fetches all the usernames from the database.

    Returns:
        list: A list of all the usernames in the database.
    """
    # Fetch all the users from the database
    users = fetch_users()

    # Extract the usernames from the users
    usernames = [user['username'] for user in users]

    # Return the list of usernames
    return usernames

def validate_email(email):
    """
    Validates if the given email is in a valid format or not.

    The pattern for the email is as follows:
        - The email should contain one '@' symbol
        - The email should contain at least one '.' symbol
        - The email should not contain any spaces or special characters
        - The email should not be empty

    Args:
        email (str): The email to be validated

    Returns:
        bool: True if the email is valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return bool(re.match(pattern, email))

def validate_username(username: str) -> bool:
    """
    Validates if the given username is in a valid format or not.

    The pattern for the username is as follows:
        - The username should contain only alphanumeric characters
        - The username should not contain any spaces or special characters
        - The username should not be empty

    Args:
        username (str): The username to be validated

    Returns:
        bool: True if the username is valid, False otherwise
    """
    pattern = "^[a-zA-Z0-9]*$"
    return bool(re.match(pattern, username))

def register():
    """
    Handles the user registration process.

    It creates a form that takes an email, username, password and confirm password.
    It validates the input, checks for any errors, encrypts the password and
    inserts the user data into the MySQL database.

    If the registration is successful, it displays a success message, shows a
    balloon animation and redirects the user to the login page after 2 seconds.

    If the user clicks on the login button, it redirects the user to the login page.
    """
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

            # Encrypt the password
            encrypted_password = encrypt_password(password)

            # Insert the user data into the MySQL database
            insert_user(email, username, encrypted_password)
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

def check_login(username: str, entered_password: str) -> bool:
    """
    Check if the entered login credentials match the stored ones.

    Args:
        username (str): The username entered by the user.
        entered_password (str): The password entered by the user.

    Returns:
        bool: True if the credentials match, False otherwise.
    """
    # Fetch the users from the database
    users = fetch_users()
    # Find the user with the matching username
    user = next((u for u in users if u['username'] == username), None)
    if user:
        # Get the stored encrypted password
        stored_encrypted_password = user['password']
        # Decrypt the stored password
        decrypted_password = decrypt_password(stored_encrypted_password)
        # Check if the entered password matches the decrypted one
        return entered_password == decrypted_password
    # If no user is found, return False
    return False

def login() -> str:
    """
    Handles the login process using the Streamlit Authenticator library.

    Returns:
        str: The username of the logged-in user.
    """
    try:
        # Fetch the users from the database
        users = fetch_users()
        # Extract the usernames and emails from the users list
        emails = [user['email'] for user in users]
        usernames = [user['username'] for user in users]
        passwords = [user['password'] for user in users]

        # Create a dictionary of usernames and their respective emails and passwords
        credentials = {'usernames': {}}
        for i in range(len(emails)):
            credentials['usernames'][usernames[i]] = {'name': emails[i], 'password': passwords[i]}

        # Create an instance of the Streamlit Authenticator class
        Authenticator = stauth.Authenticate(credentials, cookie_name='expense', key='abcdef')
        # Get the email, authentication status, and username from the Authenticator
        email, auth_status, username = Authenticator.login(':green[Login]', 'main')

        # Check if the username exists in the database
        if username:
            if username not in usernames:
                # If the username does not exist, show a warning message
                st.warning('Username does not exist, Please Register.')
            if not auth_status:
                # If the authentication is not successful, show an error message
                register()
                st.error('Incorrect Password or Username!')

        # Return the username of the logged-in user
        return username

    except:
        # If any exception occurs, show a success message to refresh the page
        st.success('Refresh Page')
