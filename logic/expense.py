# expense.py

import streamlit as st

def exp():

    # Define the types of expenses.
    expenses = [
        "Housing and Utilities",
        "Transportation",
        "Food and Health",
        "Education and Entertainment",
        "Financial and Insurance"
    ]

    # Display an expandable section for users to input values for each expense type.
    with st.expander("Expense"):
        for expense in expenses:
            default_value = st.session_state.get(f"expense_{expense}", 0)
            st.number_input(f"{expense}:", min_value=0, format="%i", step=5, value=default_value, key=f"expense_{expense}")
    return expenses