from logic.navigation import *
from logic.database import *
import streamlit as st
import pandas as pd
import os
from logic.util import *
import json

def load_data():
    try:
        # Attempt to open the JSON file for reading
        with open(INSTALMENTS_PATH, 'r') as file:
            # Load the JSON data into a Python dictionary
            data = json.load(file)

    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty dictionary
        data = {}

    # Return the json dictionary
    return data

def save_data(data):
    # Open the JSON file for writing
    with open(INSTALMENTS_PATH, 'w') as file:
        # Write the data dictionary to the JSON file
        json.dump(data, file)

def table():
    # Create a dataframe that has "ING, CEC, Orange" as columns
    df = pd.DataFrame(columns=["ING", "CEC", "Orange"])
    # Return the dataframe
    return df

def f_instalments():
    try:
        # Load data from the JSON file
        data = load_data()

        # Call the table() function to generate an empty DataFrame
        dataframe = table()

        # Display a title for the section
        st.markdown("## Installments")
        st.markdown("---")

        # Create a DataFrame with month names
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        months_df = pd.DataFrame(months, columns=['Months'])

        # Concatenate the months DataFrame with the existing one
        dataframe = pd.concat([months_df, dataframe], axis=1)

        # Create a row for the header
        header_columns = st.columns(len(dataframe.columns))
        st.write("---")
        header_columns[0].write("Current Year")
        for col_index, col_name in enumerate(dataframe.columns[1:], start=1):
            header_columns[col_index].write(col_name)  # Write column names

        # Create rows for each month
        for i, row in dataframe.iterrows():
            # Create columns for each row
            cols = st.columns(len(dataframe.columns))

            # Display the month in the first column
            cols[0].write(f"{row['Months']}")
            st.divider()  # Add a divider line

            # Add checkboxes and input fields for the other columns
            for j, col in enumerate(dataframe.columns[1:]):
                col_widget = cols[j + 1]

                # Inside each column widget
                with col_widget:
                    # Generate unique keys for each input element
                    checkbox_key = f"{col}_{row['Months']}_checkbox"
                    input_key = f"{col}_{row['Months']}_input"

                    # Use data from the loaded JSON data or set default values
                    checkbox_value = st.checkbox("", key=checkbox_key, value=data.get(checkbox_key, False))
                    input_value = st.number_input("RON", key=input_key, value=data.get(input_key, 0))

                    # Update the data dictionary with checkbox and input values
                    data[checkbox_key] = checkbox_value
                    data[input_key] = input_value

        # Save the updated data to the JSON file
        save_data(data)

        # Return the DataFrame
        return dataframe

    # Error handling in case of exceptions
    except Exception as e:
        st.error(f"Error: {e}")