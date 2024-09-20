# database.py
import os
from deta import Deta
from collections import OrderedDict
from logic.util import *
import pymysql
import json


def database() -> pymysql.Connection:
    """
    Connects to the database and returns a database connection object.

    Raises:
        pymysql.Error: If there is an error connecting to the database.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=int(PORT),
            database=DATABASE,
        )
        print(f'Connected to database: {connection} ')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ExpenseTrackerDetails (
                id INT AUTO_INCREMENT PRIMARY KEY,
                period VARCHAR(255) NOT NULL,
                incomes JSON NOT NULL,
                expenses JSON NOT NULL,
                comment TEXT
            )
        ''')
    except pymysql.Error as e:
        print(f'Error connecting to database: {e}')
        raise

    return connection

def load_all_data():
    """
    Load all data from the database.

    This function fetches all the entries from the ExpenseTrackerDetails table in the database and
    returns them as a list of dictionaries.

    The dictionaries contain the following keys:
        - id (int): The unique identifier for the entry.
        - period (str): The period for the expenses/incomes (e.g. "January 2022").
        - incomes (dict): A dictionary of incomes where the keys are the income names and the values are the amounts.
        - expenses (dict): A dictionary of expenses where the keys are the expense names and the values are the amounts.
        - comment (str): A comment associated with the period.

    :return: A list of dictionaries containing the data loaded from the database.
    """
    connection = database()
    cursor = connection.cursor()
    # Fetch all the entries from the ExpenseTrackerDetails table
    query = 'SELECT * FROM ExpenseTrackerDetails'
    cursor.execute(query)
    rows = cursor.fetchall()
    data = []
    for row in rows:
        # Create a dictionary for each entry with the relevant keys
        data.append({
            'id': row[0],
            'period': row[1],
            'incomes': json.loads(row[2]),
            'expenses': json.loads(row[3]),
            'comment': row[4]
        })
    # Close the connection
    connection.close()
    return data

def save_all_data(data):
    """
    Save all data to the database.

    This function iterates over the data list and inserts each dictionary into the
    ExpenseTrackerDetails table in the database.

    Args:
        data (list): A list of dictionaries containing the data to be saved.
    """
    connection = database()
    cursor = connection.cursor()

    # Iterate over each dictionary in the data list
    for item in data:
        # Create a query to insert the data into the database
        query = 'INSERT INTO ExpenseTrackerDetails (period, incomes, expenses, comment) VALUES (%s, %s, %s, %s)'
        # Execute the query with the data from the dictionary
        cursor.execute(query, (item['period'], json.dumps(item['incomes']),
                               json.dumps(item['expenses']), item['comment']))

    # Commit the changes to the database
    connection.commit()
    # Close the database connection
    connection.close()

def find_period_in_data(period, data):
    """
    Find an entry in the data list with the given period.

    Args:
        period (str): The period to search for.
        data (list): A list of dictionaries containing the data to search in.

    Returns:
        dict or None: The entry with the given period, or None if not found.
    """
    # Iterate over the data list
    for entry in data:
        # Check if the period matches
        if entry['period'] == period:
            # Return the matching entry
            return entry

    # Return None if no matching entry was found
    return None

def insert_period(period, incomes, expenses, comment):
    """
    Insert a new period into the database, or update an existing one.

    If an existing entry is found, the incomes, expenses, and comment fields will be updated.
    If no existing entry is found, a new entry will be inserted.

    Args:
        period (str): The period to insert or update.
        incomes (dict): A dictionary of incomes for the period.
        expenses (dict): A dictionary of expenses for the period.
        comment (str): A comment associated with the period.
    """
    connection = database()
    cursor = connection.cursor()

    # Check if an existing entry exists
    query = 'SELECT * FROM ExpenseTrackerDetails WHERE period = %s'
    cursor.execute(query, (period,))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # Update the existing entry
        query = 'UPDATE ExpenseTrackerDetails SET incomes = %s, expenses = %s, comment = %s WHERE period = %s'
        cursor.execute(query, (json.dumps(incomes), json.dumps(expenses), comment, period))
    else:
        # Insert a new entry
        query = 'INSERT INTO ExpenseTrackerDetails (period, incomes, expenses, comment) VALUES (%s, %s, %s, %s)'
        cursor.execute(query, (period, json.dumps(incomes), json.dumps(expenses), comment))

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    connection.close()

def update_period(period, incomes, expenses):
    """
    Update an existing period in the database.

    Args:
        period (str): The period to update.
        incomes (dict): A dictionary of updated incomes for the period.
        expenses (dict): A dictionary of updated expenses for the period.
    """
    # Connect to the database
    connection = database()
    cursor = connection.cursor()

    # Update the period in the database
    query = 'UPDATE ExpenseTrackerDetails SET incomes = %s, expenses = %s WHERE period = %s'
    cursor.execute(query, (json.dumps(incomes), json.dumps(expenses), period))

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    connection.close()

def get_all_periods():
    """
    Get all the periods stored in the database.

    Returns:
        list: A list of all the periods.
    """
    # Connect to the database
    connection = database()
    cursor = connection.cursor()

    # Execute the query to get all periods
    query = 'SELECT period FROM ExpenseTrackerDetails'
    cursor.execute(query)

    # Fetch all the periods
    rows = cursor.fetchall()

    # Extract the periods from the query results
    periods = [row[0] for row in rows]

    # Close the database connection
    connection.close()

    # Return the list of periods
    return periods

def get_period(period):
    """
    Get the details for a specific period from the database.

    Args:
        period (str): The period to retrieve details for.

    Returns:
        dict: A dictionary containing the details for the period.
            The dictionary contains the following keys:
            - incomes (dict): A dictionary of incomes for the period.
            - expenses (dict): A dictionary of expenses for the period.
            - comment (str): A comment associated with the period.
                If no comment is found, an empty string is returned.
    """
    # Connect to the database
    connection = database()
    # Create a cursor object to execute queries
    cursor = connection.cursor()
    # Execute the query to get the period details
    query = 'SELECT * FROM ExpenseTrackerDetails WHERE period = %s'
    cursor.execute(query, (period,))
    # Fetch the query result
    entry = cursor.fetchone()
    # Close the database connection
    connection.close()
    # If a result was found, return a dictionary with the details
    if entry:
        return {
            "incomes": json.loads(entry[2]),
            "expenses": json.loads(entry[3]),
            "comment": entry[4] if entry[4] else ""
        }
    # If no result was found, return an empty dictionary
    return {"incomes": {}, "expenses": {}, "comment": ""}

def clear_data():
    """
    Clear all data from the database.

    This function truncates the ExpenseTrackerDetails table, which will delete all rows.
    """
    # Connect to the database
    connection = database()
    # Create a cursor object to execute queries
    cursor = connection.cursor()
    # Execute the query to truncate the table
    query = 'TRUNCATE TABLE ExpenseTrackerDetails'
    cursor.execute(query)
    # Commit the changes to the database
    connection.commit()
    # Close the database connection
    connection.close()

def update_comment(period: str, edited_comment: str) -> None:
    """
    Update the comment associated with a given period.

    Args:
        period (str): The period to update the comment for.
        edited_comment (str): The new comment to associate with the period.
    """

    # Connect to the database
    connection = database()
    # Create a cursor object to execute queries
    cursor = connection.cursor()

    # Execute the query to update the comment
    query = 'UPDATE ExpenseTrackerDetails SET comment = %s WHERE period = %s'
    cursor.execute(query, (edited_comment, period))

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    connection.close()
