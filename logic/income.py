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
        for income in incomes:
            default_value = st.session_state.get(f"income_{income}", 0)
            st.number_input(f"{income}:", min_value=0, format="%i", step=5, value=default_value, key=f"income_{income}")
    return incomes