# expense.py

import streamlit as st

def exp():
    """
    A function to generate an expandable section for users to input their expense values.

    The function generates a list of expense types and displays an expandable section with a number input for each type.
    The default value for each input is set to 0 and the step is set to 5. The function stores the input values in the session state.
    """
    # Define the types of expenses.
    expenses = [
        "Housing and Utilities",
        "Transportation",
        "Food and Health",
        "Education and Entertainment",
        "Financial and Insurance",
        "Other"
    ]

    # Display an expandable section for users to input values for each expense type.
    with st.expander("Expense"):
        # Iterate over the expense types
        for expense in expenses:
            # Set the default value to 0, and the step to 5
            default_value = st.session_state.get(f"expense_{expense}", 0)
            # Generate a number input and store the value in the session state
            st.number_input(
                f"{expense}:",
                min_value=0,
                format="%i",
                step=5,
                value=default_value,
                key=f"expense_{expense}"
            )
    return expenses
