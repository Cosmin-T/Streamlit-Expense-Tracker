import os
from deta import Deta
from collections import OrderedDict
from logic.util import *



def database():
    """
    Returns a Deta base object for the 'Details' collection.

    This function initializes the Deta SDK and creates a new base object for the 'Details' collection.
    The returned base object can be used to interact with the 'Details' collection.

    Returns:
        deta.Base: A Deta base object for the 'Details' collection.
    """
    # Initialize the Deta SDK
    deta = Deta(DETA_KEY)

    # Create a new base object for the 'Details' collection
    db = deta.Base('Details')

    return db

def load_all_data():
    """
    Load all data from the database.

    Returns:
        list: A list of dictionaries containing the data loaded from the database.
    """
    # Initialize the Deta SDK and get the 'Details' collection
    db = database()

    # Fetch all items from the 'Details' collection
    data = db.fetch().items

    # Return the fetched data
    return data

def save_all_data(data):
    """
    Save all data to the database.

    Args:
        data (list): A list of dictionaries containing the data to be saved.
    """
    # Initialize the Deta SDK and get the 'Details' collection
    db = database()

    # Iterate over each item in the data list
    for item in data:
        # Put the item in the 'Details' collection
        db.put(item)

def find_period_in_data(period, data):
    """
    Find an entry in the data list with the given period.

    Args:
        period (str): The period to search for.
        data (list): A list of dictionaries containing the data to search in.

    Returns:
        dict or None: The entry with the given period, or None if not found.
    """
    # Iterate over each entry in the data list
    for entry in data:
        # Check if the period of the entry matches the given period
        if entry['Period'] == period:
            # Return the entry if found
            return entry
    # Return None if the entry is not found
    return None

def insert_period(period, incomes, expenses, comment):
    """
    Insert a new period into the database, or update an existing one.

    Args:
        period (str): The period to insert or update.
        incomes (dict): A dictionary of incomes for the period.
        expenses (dict): A dictionary of expenses for the period.
        comment (str): A comment associated with the period.
    """
    db = database()
    existing_entry = db.get(period)

    # If the period already exists, update it
    if existing_entry:
        # Update the incomes and expenses dictionaries
        existing_incomes = existing_entry['Incomes']
        existing_expenses = existing_entry['Expenses']
        for key, value in incomes.items():
            existing_incomes[key] = existing_incomes.get(key, 0) + value
        for key, value in expenses.items():
            existing_expenses[key] = existing_expenses.get(key, 0) + value

        # Update the comment
        existing_entry['Comment'] = comment
        db.put(existing_entry)

    # If the period doesn't exist, create a new entry
    else:
        new_entry = {
            'key': period,
            'Period': period,
            'Incomes': incomes,
            'Expenses': expenses,
            'Comment': comment
        }
        db.put(new_entry)

def update_period(period, incomes, expenses):
    """
    Update an existing period in the database.

    Args:
        period (str): The period to update.
        incomes (dict): A dictionary of updated incomes for the period.
        expenses (dict): A dictionary of updated expenses for the period.
    """
    db = database()
    existing_entry = db.get(period)
    if existing_entry:
        # Update the incomes and expenses dictionaries
        existing_entry['Incomes'] = incomes
        existing_entry['Expenses'] = expenses
        db.put(existing_entry)
    else:
        # If the period doesn't exist, create a new entry
        new_entry = {
            'key': period,
            'Period': period,
            'Incomes': incomes,
            'Expenses': expenses,
            'Comment': ''
        }
        db.put(new_entry)

def get_all_periods():
    """
    Get all the periods stored in the database.

    Returns:
        list: A list of all the periods.
    """
    # Initialize the Deta SDK and get the 'Details' collection
    db = database()

    # Fetch all the entries from the 'Details' collection
    data = db.fetch().items

    # Extract the periods from the entries
    periods = [entry['Period'] for entry in data]

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
    # Initialize the Deta SDK and get the 'Details' collection
    db = database()

    # Convert the period to a string
    period_str = str(period)

    # Retrieve the entry for the given period from the database
    entry = db.get(period_str)

    # If the entry exists, extract the details
    if entry:
        return {
            "incomes": entry['Incomes'],
            "expenses": entry['Expenses'],
            "comment": entry['Comment'] if 'Comment' in entry else ""
        }

    # If the entry doesn't exist, return an empty dictionary with the correct keys
    return {"incomes": {}, "expenses": {}, "comment": ""}

def clear_data():
    """
    Clear all data from the database.

    This function initializes the Deta SDK and fetches all entries from the 'Details' collection.
    It then deletes each entry from the database.
    """
    # Initialize the Deta SDK and get the 'Details' collection
    db = database()

    # Fetch all entries from the 'Details' collection
    items = db.fetch().items

    # Iterate over each entry and delete it from the database
    for item in items:
        # Delete the entry from the 'Details' collection
        db.delete(item['key'])

def update_comment(period, edited_comment):
    """
    Update the comment associated with a given period.

    Args:
        period (str): The period to update the comment for.
        edited_comment (str): The new comment to associate with the period.
    """
    # Initialize the Deta SDK and get the 'Details' collection
    db = database()

    # Retrieve the entry for the given period from the database
    existing_entry = db.get(period)

    # If the entry exists, update the comment and save the entry
    if existing_entry:
        existing_entry['Comment'] = edited_comment
        db.put(existing_entry)

