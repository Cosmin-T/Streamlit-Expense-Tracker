# income.py

import streamlit as st

def inc():

    # Define the types of income sources.
    incomes = [
        "Salary",
        "Bonuses",
        "Interest and Dividends",
        "Business Income",
        "Rental Income",
        "Investment Income",
        "Freelance Income",
        "Government Benefits",
        "Other"
    ]

    # Display an expandable section for users to input values for each income source.
    with st.expander("Income"):
        # Create a dropdown list for expense types.
        selected_income = st.selectbox("Select an expense:", options=incomes)

        # Retrieve the current value for the selected expense from session state (or default to 0).
        default_value = st.session_state.get(f"expense_{selected_income}", 0)

        # Allow users to input a value for the selected expense.
        income_value = st.number_input(f"{selected_income} amount:", min_value=0, format="%i", step=5, value=default_value)

        # Update the session state with the new input value.
        st.session_state[f"income_{selected_income}"] = income_value
    return incomes