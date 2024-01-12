from logic.navigation import *
from logic.database import *
import streamlit as st
import pandas as pd
import os
from logic.util import *
import json
import base64

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
    df = pd.DataFrame(columns=["ING", "CEC", "Orange", "Salary", "My Cut"])
    # Return the dataframe
    return df

def get_table_download_link(df):
    # Convert and download dataframe
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'
    return href

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

        # Total Variables
        total_ing = 0.0
        total_cec = 0.0

        # Create a row for the header
        header_columns = st.columns(len(dataframe.columns))
        st.write("---")
        header_columns[0].write("Current Year")
        for col_index, col_name in enumerate(dataframe.columns[1:], start=1):
            header_columns[col_index].write(col_name)

        # Create rows for each month
        for i, row in dataframe.iterrows():
            # Create columns for each row
            cols = st.columns(len(dataframe.columns))

            # Display the month in the first column
            month = row['Months']
            cols[0].write(f"{month}")
            st.divider()

            # Initialize the values for ING, CEC, Orange, and Salary for the current month
            ing_value = cec_value = orange_value = salary_value = 0.0

            # Add checkboxes and input fields for the other columns
            for j, col in enumerate(dataframe.columns[1:-1]):
                col_widget = cols[j + 1]

                # Inside each column widget
                with col_widget:
                    # Generate unique keys for each input element
                    checkbox_key = f"{col}_{month}_checkbox"
                    input_key = f"{col}_{month}_input"

                    # Use data from the loaded JSON data or set default values
                    checkbox_value = st.checkbox("", key=checkbox_key, value=data.get(checkbox_key, False))
                    if col == "Salary":
                        # For Salary, set the default value from the JSON data if available
                        salary_value = float(data.get(input_key, 0.0))
                        input_value = st.number_input("RON", key=input_key, value=salary_value, step=0.1)
                    else:
                        # For other columns, use 0.0 as the default value
                        input_value = st.number_input("RON", key=input_key, value=float(data.get(input_key, 0.0)), step=0.1)

                    # Update the data dictionary with checkbox and input values
                    data[checkbox_key] = checkbox_value
                    data[input_key] = input_value

                    # Update the DataFrame with the input values
                    dataframe.at[i, col] = input_value

                    # Update the variable values for ING, CEC, and Orange
                    if col == "ING":
                        ing_value = input_value
                    elif col == "CEC":
                        cec_value = input_value
                    elif col == "Orange":
                        orange_value = input_value

            # Calculate "My Cut" for each row using the updated values
            my_cut = salary_value - (ing_value + cec_value + orange_value)

            # Update the "My Cut" column in the DataFrame
            dataframe.at[i, "My Cut"] = my_cut

            # Display the "My Cut" value in the widget
            with cols[-1]:
                st.write("**RON**")
                st.number_input("", value=my_cut, step=0.1, key=f"My Cut_{month}")

            # Add input values to total for ING and CEC
            total_ing += ing_value
            total_cec += cec_value

        # Create a button to download the DataFrame as CSV
        if st.button("Download"):
            st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

        # Generate the 100% values for ING and CEC
        all_ing = 13529.00
        all_cec = 38660.00

        # Generate the current values for ING and CEC
        current_ing = 6042.86 + total_ing
        current_cec = 3448.43 + total_cec

        # Generate 3 columns for Installments, including the updated remaining values
        col1, col2, col3 = st.columns(3)


        # Generate Current Instance
        with col1:
            st.markdown("## Current")
            st.number_input("ING Current", min_value=0.0, step=0.1, value=current_ing, key="ING - Current")
            st.number_input("CEC Current", min_value=0.0, step=0.1, value=current_cec, key="CEC - Current")
            st.markdown("---")

        # Calculate the remaining values after all months have been processed
        remaining_ing = all_ing - current_ing
        remaining_cec = all_cec - current_cec

        # Generate Added Instance
        with col2:
            st.markdown("## Added")
            st.number_input("ING Added", min_value=0.0, step=0.1, value=total_ing, key="ING - Total Added")
            st.number_input("CEC Added", min_value=0.0, step=0.1, value=total_cec, key="CEC - Total Added")
            st.markdown("---")

        # Generate Remaining Instance
        with col3:
            st.markdown("## Remaining")
            st.number_input("ING Remaining", min_value=0.0, step=0.1, value=remaining_ing, key="ING - Total Remaining")
            st.number_input("CEC Remaining", min_value=0.0, step=0.1, value=remaining_cec, key="CEC - Total Remaining")
            st.markdown("---")

        # Generate Total Load
        st.markdown("## Max Funds")

        st.number_input("ING Funds", min_value=0.0, step=0.1, value=all_ing, key="ING - Total")
        st.number_input("CEC Funds", min_value=0.0, step=0.1, value=all_cec, key="CEC - Total")
        st.markdown("---")

        # Save the updated data to the JSON file
        save_data(data)

        # Return the DataFrame
        return dataframe

    # Error handling in case of exceptions
    except Exception as e:
        st.error(f"Error: {e}")
