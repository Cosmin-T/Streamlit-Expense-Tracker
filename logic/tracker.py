import streamlit as st
import pandas as pd
import base64
from deta import Deta
from logic.util import *

def table():
    """
    Returns an empty DataFrame with the following columns:
    "ING", "CEC", "Orange", "Salary", "My Cut"
    """
    # Create a new DataFrame with the specified columns
    df = pd.DataFrame(columns=["ING", "CEC", "Orange", "Salary", "My Cut"])

    return df

def database_installments():
    """
    Returns a Deta base object for the 'installments' collection.

    This function initializes the Deta SDK and creates a new base object for the 'installments' collection.
    The returned base object can be used to interact with the 'installments' collection.

    Returns:
        deta.Base: A Deta base object for the 'installments' collection.
    """
    # Initialize the Deta SDK
    deta = Deta(DETA_KEY)

    # Create a new base object for the 'installments' collection
    db = deta.Base('installments')

    return db

def load_data():
    """
    Load data from the 'installments' collection and return it as a dictionary.

    This function initializes the Deta SDK and retrieves all items from the 'installments' collection.
    The returned data is a dictionary where the keys are the 'key' field of each item and the values are the 'value' field.

    Returns:
        dict: A dictionary containing the data loaded from the 'installments' collection.
    """
    # Initialize the Deta SDK and get the 'installments' collection
    db = database_installments()

    # Fetch all items from the 'installments' collection
    data = db.fetch().items

    # Create a dictionary where the keys are the 'key' field of each item and the values are the 'value' field
    return {item['key']: item['value'] for item in data}



def save_data(data):
    """
    Save the given data to the 'installments' collection.

    This function initializes the Deta SDK and iterates over the key-value pairs in the given data.
    For each key-value pair, it creates a new item with the 'key' and 'value' fields set accordingly.
    The new item is then inserted into the 'installments' collection using the 'put' method.

    Args:
        data (dict): A dictionary containing the data to be saved.
                     The keys are the 'key' field of each item and the values are the 'value' field.
    """
    # Initialize the Deta SDK and get the 'installments' collection
    db = database_installments()

    # Iterate over the key-value pairs in the given data
    for key, value in data.items():
        # Create a new item with the 'key' and 'value' fields set accordingly
        item = {"key": key, "value": value}

        # Insert the new item into the 'installments' collection
        db.put(item)



def get_table_download_link(df):
    """
    Generate a download link for the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame to be downloaded.

    Returns:
        str: The HTML link for downloading the DataFrame as a CSV file.
    """
    # Convert the DataFrame to CSV format
    csv = df.to_csv(index=False)

    # Encode the CSV data in base64 format
    b64 = base64.b64encode(csv.encode()).decode()

    # Generate the HTML link for downloading the CSV data
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'

    return href

def f_instalments():
    """
    This function is a Streamlit app for managing installments.
    It displays a table with input fields for each month and allows the user to input expenses for each month.
    The function also calculates the total expenses for each month and provides an option to download the table as a CSV file.
    """
    try:
        # Load the data from the session state
        data = load_data()

        # Create an empty DataFrame with the required columns
        dataframe = table()

        # Display the title for the installments section
        st.markdown("## Installments")
        st.markdown("---")

        # Create a DataFrame with the months
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        months_df = pd.DataFrame(months, columns=['Months'])

        # Concatenate the months DataFrame with the existing DataFrame
        dataframe = pd.concat([months_df, dataframe], axis=1)

        # Initialize the total expenses for each month
        total_ing = 0.0
        total_cec = 0.0

        # Create columns for the table headers
        header_columns = st.columns(len(dataframe.columns))
        st.write("---")
        header_columns[0].write("Current Year")
        for col_index, col_name in enumerate(dataframe.columns[1:], start=1):
            header_columns[col_index].write(col_name)

        # Iterate over each row in the DataFrame
        for i, row in dataframe.iterrows():
            # Create columns for the input fields
            cols = st.columns(len(dataframe.columns))
            month = row['Months']
            cols[0].write(f"{month}")
            st.divider()

            # Initialize the expense values for each month
            ing_value = cec_value = orange_value = salary_value = 0.0

            # Iterate over each column in the DataFrame
            for j, col in enumerate(dataframe.columns[1:-1]):
                col_widget = cols[j + 1]

                with col_widget:
                    # Create keys for the checkbox and input fields
                    checkbox_key = f"{col}_{month}_checkbox"
                    input_key = f"{col}_{month}_input"

                    # Display the checkbox and input fields
                    checkbox_value = st.checkbox("", key=checkbox_key, value=data.get(checkbox_key, False))
                    if col == "Salary":
                        salary_value = float(data.get(input_key, 0.0))
                        input_value = st.number_input("RON", key=input_key, value=salary_value, step=0.1)
                    else:
                        input_value = st.number_input("RON", key=input_key, value=float(data.get(input_key, 0.0)), step=0.1)

                    # Update the data dictionary with the new values
                    data[checkbox_key] = checkbox_value
                    data[input_key] = input_value

                    # Update the DataFrame with the new values
                    dataframe.at[i, col] = input_value

                    # Update the expense values based on the column name
                    if col == "ING":
                        ing_value = input_value
                    elif col == "CEC":
                        cec_value = input_value
                    elif col == "Orange":
                        orange_value = input_value

            # Calculate the total expenses for the month
            my_cut = salary_value - (ing_value + cec_value + orange_value)

            # Update the DataFrame with the total expenses
            dataframe.at[i, "My Cut"] = my_cut

            # Display the total expenses
            with cols[-1]:
                st.write("**RON**")
                st.number_input("", value=my_cut, step=0.1, key=f"My Cut_{month}")

            # Update the total expenses for each month
            total_ing += ing_value
            total_cec += cec_value

        # Display the download button
        if st.button("Download"):
            st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

        # Define the maximum funds for each expense category
        all_ing = 13529.00
        all_cec = 38660.00

        # Calculate the current funds for each expense category
        current_ing = 4356.34 + total_ing
        current_cec = 891.37 + total_cec

        # Create columns for the current funds display
        col1, col2, col3 = st.columns(3)

        # Display the current funds for each expense category
        with col1:
            st.markdown("## Current")
            st.number_input("ING Current", min_value=0.0, step=0.1, value=current_ing, key="ING - Current")
            st.number_input("CEC Current", min_value=0.0, step=0.1, value=current_cec, key="CEC - Current")
            st.markdown("---")

        # Calculate the remaining funds for each expense category
        remaining_ing = all_ing - current_ing
        remaining_cec = all_cec - current_cec

        # Display the remaining funds for each expense category
        with col2:
            st.markdown("## Added")
            st.number_input("ING Added", min_value=0.0, step=0.1, value=total_ing, key="ING - Total Added")
            st.number_input("CEC Added", min_value=0.0, step=0.1, value=total_cec, key="CEC - Total Added")
            st.markdown("---")

        # Display the remaining funds for each expense category
        with col3:
            st.markdown("## Remaining")
            st.number_input("ING Remaining", min_value=0.0, step=0.1, value=remaining_ing, key="ING - Total Remaining")
            st.number_input("CEC Remaining", min_value=0.0, step=0.1, value=remaining_cec, key="CEC - Total Remaining")
            st.markdown("---")

        # Display the maximum funds for each expense category
        st.markdown("## Max Funds")
        st.number_input("ING Funds", min_value=0.0, step=0.1, value=all_ing, key="ING - Total")
        st.number_input("CEC Funds", min_value=0.0, step=0.1, value=all_cec, key="CEC - Total")
        st.markdown("---")

        # Save the data to the session state
        save_data(data)

        return dataframe

    except Exception as e:
        st.error(f"Error: {e}")
