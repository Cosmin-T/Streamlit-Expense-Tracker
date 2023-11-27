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

        # Current Variables
        current_ing = 6429.67
        current_cec = 19125.11

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
            cols[0].write(f"{row['Months']}")
            st.divider()

            # Add checkboxes and input fields for the other columns
            for j, col in enumerate(dataframe.columns[1:-1]):
                col_widget = cols[j + 1]

                # Inside each column widget
                with col_widget:
                    # Generate unique keys for each input element
                    checkbox_key = f"{col}_{row['Months']}_checkbox"
                    input_key = f"{col}_{row['Months']}_input"

                    # Use data from the loaded JSON data or set default values
                    checkbox_value = st.checkbox("", key=checkbox_key, value=data.get(checkbox_key, False))
                    input_value = st.number_input("RON", key=input_key, value=float(data.get(input_key, 0.0)), step=0.1)

                    # Update the data dictionary with checkbox and input values
                    data[checkbox_key] = checkbox_value
                    data[input_key] = input_value

                    # Update the DataFrame with the input values
                    dataframe.at[i, col] = input_value

                     # Add input values to total for ING and CEC
                    if col == "ING":
                        total_ing += input_value
                    elif col == "CEC":
                        total_cec += input_value

            # Calculate "My Cut" dynamically for each row
            my_cut = row['Salary'] - (row['ING'] + row['CEC'] + row['Orange'])

            # Update the "My Cut" column in the DataFrame
            dataframe.at[i, "My Cut"] = my_cut

            # Display the "My Cut" value in the widget
            with cols[-1]:
                st.write("**RON**")
                st.number_input("", value=my_cut, step=0.1, key=f"My Cut_{row['Months']}")

        # Save the updated data to the JSON file
        print("Data before saving:", data)
        save_data(data)

        # Create a button to download the DataFrame as CSV
        if st.button("Download"):
            st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)


        # Generate 3 columns for Installments
        col1, col2, col3 = st.columns(3)

        # Generate total current data for CEC and ING
        with col1:
            st.markdown("## Current")
            st.number_input("ING", min_value=0.0, step = 0.1, value=current_ing, key="ING - Current")
            st.number_input("CEC", min_value=0.0, step = 0.1, value=current_cec, key="CEC - Current")
            st.markdown("---")

        # Generate total added value for CEC and ING
        with col2:
            st.markdown("## Added")
            st.number_input("ING", min_value=0.0, step = 0.1, value=total_ing, key="ING - Total Added")
            st.number_input("CEC", min_value=0.0, step = 0.1, value=total_cec, key="CEC - Total Added")
            st.markdown("---")

        # Generate total Remaining value for CEC and ING
        with col3:
            st.markdown("## Remaining")
            st.number_input("ING", min_value=0.0, step = 0.1, value=current_ing - total_ing, key="ING - Total Remaining")
            st.number_input("CEC", min_value=0.0, step = 0.1, value=current_cec - total_cec, key="CEC - Total Remaining")
            st.markdown("---")

        # Return the DataFrame
        return dataframe

    # Error handling in case of exceptions
    except Exception as e:
        st.error(f"Error: {e}")