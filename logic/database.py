# database.py

import os
import json
from collections import OrderedDict
from logic.util import *

# Ensure the database (JSON file) exists; if not, initialize it.
if not os.path.exists(get_json_file_path()):
    with open(get_json_file_path(), 'w') as file:
        # Initialize an empty JSON array if the file doesn't exist.
        json.dump([], file)

def load_all_data():

    # Load all data from the JSON file and return as a list of dictionaries.
    with open(get_json_file_path(), 'r') as file:
        data = json.load(file)
    return data

def save_all_data(data):

    # Save provided data back to the JSON file.
    with open(get_json_file_path(), 'w') as file:
        json.dump(data, file)

def find_period_in_data(period, data):

    # Search for an entry with the provided period in the data.
    # If found, return the entry; otherwise, return None.
    for entry in data:
        if entry['Period'] == period:
            return entry
    return None

def insert_period(period, incomes, expenses, comment):

    # Function to insert or update financial data for a specific period
    # Load all existing financial data from the database
    data = load_all_data()

    if not data:
        # If the database is empty, create a new entry for the given period
        new_entry = {
            'Period': period,
            'Incomes': incomes,
            'Expenses': expenses,
            'Comment': comment
        }
        data.append(new_entry)
    else:
        # Check if there is an existing entry for the given period
        existing_entry = find_period_in_data(period, data)
        if existing_entry:
            # Update the existing entry by adding new incomes and expenses
            existing_incomes = existing_entry['Incomes']
            existing_expenses = existing_entry['Expenses']

            # Add the new incomes to the existing incomes
            for key, value in incomes.items():
                existing_incomes[key] += value

            # Add the new expenses to the existing expenses
            for key, value in expenses.items():
                existing_expenses[key] = existing_expenses.get(key, 0) + value


            # Update the comment for the existing entry
            existing_entry['Comment'] = comment
        else:
            # If there is no existing entry for the period, create a new one
            new_entry = {
                'Period': period,
                'Incomes': incomes,
                'Expenses': expenses,
                'Comment': comment
            }
            data.append(new_entry)

    # Save the updated data back to the database
    save_all_data(data)

def update_period(period, incomes, expenses):

    # Function to update financial data for a specific period
    # Load all existing financial data from the database
    data = load_all_data()

    # Find the existing entry for the given period
    existing_entry = find_period_in_data(period, data)

    if existing_entry:
        # Update the existing entry by replacing incomes and expenses
        existing_entry['Incomes'] = incomes
        existing_entry['Expenses'] = expenses
    else:
        # If there is no existing entry for the period, create a new one
        new_entry = {
            'Period': period,
            'Incomes': incomes,
            'Expenses': expenses,
            'Comment': ''
        }
        data.append(new_entry)

    # Save the updated data back to the database
    save_all_data(data)

def get_all_periods():

    # Function to retrieve all unique financial periods from the database
    # Load all existing financial data from the database
    data = load_all_data()

    # Extract the periods from the data and return them as a list
    periods = [entry['Period'] for entry in data]
    return periods

def get_period(period):

    # Function to retrieve financial data for a specific period
    # Load all existing financial data from the database
    data = load_all_data()

    # Search for the entry corresponding to the specified period
    for entry in data:
        if entry['Period'] == period:
            return {
                "incomes": entry['Incomes'],
                "expenses": entry['Expenses'],
                "comment": entry['Comment'] if 'Comment' in entry else ""
            }

    # If no entry is found for the period, return empty data
    return {"incomes": {}, "expenses": {}, "comment": ""}

def clear_data():

    # Function to clear all financial data from the database
    # Save an empty list to clear all entries in the database
    save_all_data([])

def update_comment(period, edited_comment):
    # Function to update the comment for a specific period
    # Load all existing financial data from the database
    data = load_all_data()

    # Find the existing entry for the given period
    existing_entry = find_period_in_data(period, data)

    if existing_entry:
        # Update the comment for the existing entry
        existing_entry['Comment'] = edited_comment

    # Save the updated data back to the database
    save_all_data(data)