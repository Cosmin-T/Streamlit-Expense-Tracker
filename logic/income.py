# income.py

import streamlit as st

def inc():
    """
    A function to generate an expandable section for users to input their income values.

    The function generates a list of income sources and displays an expandable section with a number input for each source.
    The default value for each input is set to 0 and the step is set to 5. The function stores the input values in the session state.
    """
    # Define the types of income sources.
    incomes = [
        "Salary",
        "Bonuses",
        "Other"
    ]

    # Display an expandable section for users to input values for each income source.
    with st.expander("Income"):
        # Iterate over the income sources
        for income in incomes:
            # Set the default value to 0, and the step to 5
            default_value = st.session_state.get(f"income_{income}", 0)
            # Generate a number input and store the value in the session state
            st.number_input(
                f"{income}:",
                min_value=0,
                format="%i",
                step=5,
                value=default_value,
                key=f"income_{income}"
            )
    return incomes
