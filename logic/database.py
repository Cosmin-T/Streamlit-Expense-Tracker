# database.py

import os
import csv
from logic.util import *
import streamlit as st

# Ensure the database (CSV file) exists; if not, initialize it.
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Period', 'Incomes', 'Expenses', 'Comment'])

def load_all_data():

    # Load all data from the CSV and return as a list of dictionaries.
    data = []
    with open(FILE_NAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def save_all_data(data):

    # Save provided data back to the CSV.
    fieldnames = ['Period', 'Incomes', 'Expenses', 'Comment']
    with open(FILE_NAME, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def find_period_in_data(period, data):

    #Search for an entry with the provided period in the data. If found, return the entry, otherwise return None.
    for entry in data:
        if entry['Period'] == period:
            return entry
    return None

def insert_period(period, incomes, expenses, comment):

    # Load all data
    data = load_all_data()

    # Check if an entry with the provided period already exists.
    existing_entry = find_period_in_data(period, data)

    # Convert the string representation of the dictionary back to an actual dictionary.
    existing_incomes = eval(existing_entry['Incomes']) if existing_entry else {}
    existing_expenses = eval(existing_entry['Expenses']) if existing_entry else {}

    # Handle incomes
    for key, value in incomes.items():
        if key in existing_incomes:  # If key exists, we consider it an update
            # Your update logic here. For now, I'm just overwriting the value:
            existing_incomes[key] = value
        else:  # Else, it's a new category
            existing_incomes[key] = value

    # Handle expenses
    for key, value in expenses.items():
        if key in existing_expenses:
            existing_expenses[key] = value
        else:
            existing_expenses[key] = value

    # If the period exists, update the entry.
    if existing_entry:
        existing_entry['Incomes'] = str(existing_incomes)
        existing_entry['Expenses'] = str(existing_expenses)
        existing_entry['Comment'] = comment
    else:
        # If it doesn't exist, append a new entry.
        data.append({
            'Period': period,
            'Incomes': str(incomes),
            'Expenses': str(expenses),
            'Comment': comment
        })

    # Save the data back to the CSV.
    save_all_data(data)

def get_all_periods():

    # Retrieve all the unique periods (e.g., "January 2023") from the CSV database.
    periods = []
    with open(FILE_NAME, 'r') as file:
        reader = csv.reader(file)
        try:
            next(reader)  # skip the header row
            for row in reader:
                periods.append(row[0])
        except StopIteration:
            st.error('No data to show...')
    return periods

def get_period(period):

    # Retrieve the financial data for a specific period from the CSV database.
    with open(FILE_NAME, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'Period' in row and row['Period'] == period:
                incomes = eval(row['Incomes'])
                expenses = eval(row['Expenses'])
                comment = row['Comment']
                return {"incomes": incomes, "expenses": expenses, "comment": comment}
    return None

def clear_data():

    # Clear all entries except the header from the CSV database.
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Period", "Incomes", "Expenses", "Comment"])
