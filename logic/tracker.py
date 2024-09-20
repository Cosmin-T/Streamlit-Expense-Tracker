import streamlit as st
import pandas as pd
import base64
import pymysql
from logic.util import *
import datetime

def table() -> pd.DataFrame:
    """
    Generates an empty table with the 12 months of the year as the index and
    columns for ING, CEC, Orange, Salary and MyCut with all values set to 0.

    Returns
    -------
    pd.DataFrame
        An empty table with the specified columns and months as index.
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    return pd.DataFrame({'Months': months, 'ING': 0, 'CEC': 0, 'Orange': 0, 'Salary': 0, 'MyCut': 0})

def database_connection() -> pymysql.Connection:
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

def load_data() -> dict:
    """
    Loads the data from the database and returns it in a dictionary.

    The keys of the dictionary are in the format "ING_January_checkbox", and the
    values are the corresponding values from the database.

    Returns
    -------
    dict
        A dictionary with the data from the database.
    """
    connection = database_connection()
    try:
        with connection.cursor() as cursor:
            # Select all data from the ExpenseTrackerInstallments table
            sql = "SELECT * FROM ExpenseTrackerInstallments"
            cursor.execute(sql)
            # Fetch all the results
            results = cursor.fetchall()

            # Initialize an empty dictionary to store the data
            data = {}
            # Iterate over the months
            for row in results:
                # Get the month from the row
                month = row[1]
                # Add the data for each month to the dictionary
                data[f"ING_{month}_checkbox"] = bool(row[2])
                data[f"ING_{month}_input"] = float(row[2])
                data[f"CEC_{month}_checkbox"] = bool(row[3])
                data[f"CEC_{month}_input"] = float(row[3])
                data[f"Orange_{month}_checkbox"] = bool(row[4])
                data[f"Orange_{month}_input"] = float(row[4])
                data[f"Salary_{month}_input"] = float(row[5])
            # Return the dictionary
            return data
    finally:
        # Close the connection
        connection.close()

def save_data(data):
    """
    Saves the data to the database.

    The data is a dictionary with the keys in the format "ING_January_checkbox", and the
    values are the corresponding values from the database.

    Parameters
    ----------
    data : dict
        The dictionary with the data to be saved.

    Returns
    -------
    None
    """
    connection = database_connection()
    try:
        with connection.cursor() as cursor:
            # Iterate over the months
            for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December']:
                # Get the data for the current month
                ing = data.get(f"ING_{month}_input", 0)
                cec = data.get(f"CEC_{month}_input", 0)
                orange = data.get(f"Orange_{month}_input", 0)
                salary = data.get(f"Salary_{month}_input", 0)
                my_cut = salary - (ing + cec + orange)

                # Update the data in the database
                sql = """
                UPDATE ExpenseTrackerInstallments
                SET ING = %s, CEC = %s, Orange = %s, Salary = %s, MyCut = %s
                WHERE Months = %s
                """
                cursor.execute(sql, (ing, cec, orange, salary, my_cut, month))

                # Check if the row for the current month exists
                cursor.execute("SELECT * FROM ExpenseTrackerInstallments WHERE Months = %s", month)
                results = cursor.fetchone()
                if results is None:
                    # Insert the data if the row does not exist
                    sql = """
                    INSERT INTO ExpenseTrackerInstallments (Months, ING, CEC, Orange, Salary, MyCut)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (month, ing, cec, orange, salary, my_cut))
        connection.commit()
    finally:
        connection.close()

def get_table_download_link(df):
    """
    Generate a link allowing the user to download the given dataframe as a CSV file.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to export.

    Returns
    -------
    str
        A link with the download attribute set to "data.csv", which will allow the user
        to download the dataframe as a CSV file.
    """
    # Convert the dataframe to a CSV string
    csv = df.to_csv(index=False)

    # Encode the string as base64
    b64 = base64.b64encode(csv.encode()).decode()

    # Generate the link
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'

    # Return the link
    return href

def f_instalments():
    """
    Function to display the installments table, allowing the user to input values
    and download the table as a CSV file.

    The function also displays the total added, current, and remaining balance for
    each of the two accounts.
    """
    try:
        data = load_data()
        dataframe = table()

        st.markdown("## Installments")
        st.markdown("---")

        total_ing = 0.0
        total_cec = 0.0

        # Display the months and column names
        header_columns = st.columns(len(dataframe.columns))
        st.write("---")
        current_year = datetime.datetime.now().year
        header_columns[0].write(f'##### {current_year}')
        for col_index, col_name in enumerate(dataframe.columns[1:], start=1):
            header_columns[col_index].write(col_name)

        # Iterate over the dataframe rows
        for i, row in dataframe.iterrows():
            cols = st.columns(len(dataframe.columns))
            month = row['Months']
            cols[0].write(f"{month}")
            st.divider()

            ing_value = cec_value = orange_value = salary_value = 0.0

            # Iterate over the columns, displaying a checkbox and a number input
            # for each column
            for j, col in enumerate(dataframe.columns[1:-1]):
                col_widget = cols[j + 1]

                with col_widget:
                    checkbox_key = f"{col}_{month}_checkbox"
                    input_key = f"{col}_{month}_input"

                    checkbox_value = st.checkbox("", key=checkbox_key, value=data.get(checkbox_key, False))
                    if col == "Salary":
                        salary_value = float(data.get(input_key, 0.0))
                        input_value = st.number_input("RON", key=input_key, value=salary_value, step=0.1)
                    else:
                        input_value = st.number_input("RON", key=input_key, value=float(data.get(input_key, 0.0)), step=0.1)

                    data[checkbox_key] = checkbox_value
                    data[input_key] = input_value
                    dataframe.at[i, col] = input_value

                    if col == "ING":
                        ing_value = input_value
                    elif col == "CEC":
                        cec_value = input_value
                    elif col == "Orange":
                        orange_value = input_value

            # Calculate the "MyCut" value
            my_cut = salary_value - (ing_value + cec_value + orange_value)
            dataframe.at[i, "MyCut"] = my_cut

            # Display the "MyCut" value
            with cols[-1]:
                st.write("**RON**")
                st.number_input("", value=my_cut, step=0.1, key=f"MyCut_{month}")

            # Sum up the total added values
            total_ing += ing_value
            total_cec += cec_value

        # Add a download button
        if st.button("Download"):
            st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

        # Calculate the remaining balance for each account
        all_ing = 13529.00
        all_cec = 38660.00

        current_ing = 3699.81 + total_ing
        current_cec = 594.35 + total_cec

        remaining_ing = all_ing - current_ing
        remaining_cec = all_cec - current_cec

        # Display the current and remaining balance for each account
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("## Current")
            st.number_input("ING Current", min_value=0.0, step=0.1, value=current_ing, key="ING - Current")
            st.number_input("CEC Current", min_value=0.0, step=0.1, value=current_cec, key="CEC - Current")
            st.markdown("---")

        with col2:
            st.markdown("## Added")
            st.number_input("ING Added", min_value=0.0, step=0.1, value=total_ing, key="ING - Total Added")
            st.number_input("CEC Added", min_value=0.0, step=0.1, value=total_cec, key="CEC - Total Added")
            st.markdown("---")

        with col3:
            st.markdown("## Remaining")
            st.number_input("ING Remaining", min_value=0.0, step=0.1, value=remaining_ing, key="ING - Total Remaining")
            st.number_input("CEC Remaining", min_value=0.0, step=0.1, value=remaining_cec, key="CEC - Total Remaining")
            st.markdown("---")

        # Display the maximum balance for each account
        st.markdown("## Max Funds")
        st.number_input("ING Funds", min_value=0.0, step=0.1, value=all_ing, key="ING - Total")
        st.number_input("CEC Funds", min_value=0.0, step=0.1, value=all_cec, key="CEC - Total")
        st.markdown("---")

        # Save the data
        save_data(data)

        # Return the dataframe
        return dataframe

    except Exception as e:
        st.error(f"Error: {e}")
