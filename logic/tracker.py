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
    db = database_installments()
    for key, value in data.items():
        db.put({"key": key, "value": value})

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV</a>'
    return href

def f_instalments():
    try:
        data = load_data()
        dataframe = table()

        st.markdown("## Installments")
        st.markdown("---")

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        months_df = pd.DataFrame(months, columns=['Months'])

        dataframe = pd.concat([months_df, dataframe], axis=1)

        total_ing = 0.0
        total_cec = 0.0

        header_columns = st.columns(len(dataframe.columns))
        st.write("---")
        header_columns[0].write("Current Year")
        for col_index, col_name in enumerate(dataframe.columns[1:], start=1):
            header_columns[col_index].write(col_name)

        for i, row in dataframe.iterrows():
            cols = st.columns(len(dataframe.columns))
            month = row['Months']
            cols[0].write(f"{month}")
            st.divider()

            ing_value = cec_value = orange_value = salary_value = 0.0

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

            my_cut = salary_value - (ing_value + cec_value + orange_value)

            dataframe.at[i, "My Cut"] = my_cut

            with cols[-1]:
                st.write("**RON**")
                st.number_input("", value=my_cut, step=0.1, key=f"My Cut_{month}")

            total_ing += ing_value
            total_cec += cec_value

        if st.button("Download"):
            st.markdown(get_table_download_link(dataframe), unsafe_allow_html=True)

        all_ing = 13529.00
        all_cec = 38660.00

        current_ing = 6042.86 + total_ing
        current_cec = 3448.43 + total_cec

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("## Current")
            st.number_input("ING Current", min_value=0.0, step=0.1, value=current_ing, key="ING - Current")
            st.number_input("CEC Current", min_value=0.0, step=0.1, value=current_cec, key="CEC - Current")
            st.markdown("---")

        remaining_ing = all_ing - current_ing
        remaining_cec = all_cec - current_cec

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

        st.markdown("## Max Funds")

        st.number_input("ING Funds", min_value=0.0, step=0.1, value=all_ing, key="ING - Total")
        st.number_input("CEC Funds", min_value=0.0, step=0.1, value=all_cec, key="CEC - Total")
        st.markdown("---")

        save_data(data)

        return dataframe

    except Exception as e:
        st.error(f"Error: {e}")
