# expense.py

import streamlit as st

def exp():

    # Define the types of expenses.
    expenses = [
        "Housing",
        "Utilities",
        "Rent/Mortgage",
        "Property Taxes",
        "Vices",
        "Home Insurance",
        "Home Maintenance/Repairs",
        "Transportation",
        "Vehicle Payments",
        "Fuel",
        "Vehicle Maintenance/Repairs",
        "Public Transportation",
        "Food",
        "Groceries",
        "Dining Out",
        "Food Delivery",
        "Healthcare",
        "Health Insurance",
        "Doctor Visits",
        "Medications",
        "Medical Supplies",
        "Education",
        "Tuition Fees",
        "School Supplies",
        "Educational Services",
        "Entertainment",
        "Movies/Concerts",
        "Streaming Services",
        "Recreational Activities",
        "Debt Payments",
        "Loan Payments",
        "Credit Card Payments",
        "Savings",
        "Emergency Fund",
        "Retirement Fund",
        "Other Savings",
        "Insurance",
        "Auto Insurance",
        "Home/Renters Insurance"
    ]

    # Display an expandable section for users to input values for the selected expense type from the dropdown.
    with st.expander("Expense"):
        # Create a dropdown list for expense types.
        selected_expense = st.selectbox("Select an expense:", options=expenses)

        # Retrieve the current value for the selected expense from session state (or default to 0).
        default_value = st.session_state.get(f"expense_{selected_expense}", 0)

        # Allow users to input a value for the selected expense.
        expense_value = st.number_input(f"{selected_expense} amount:", min_value=0, format="%i", step=5, value=default_value)

        # Update the session state with the new input value.
        st.session_state[f"expense_{selected_expense}"] = expense_value
    return expenses