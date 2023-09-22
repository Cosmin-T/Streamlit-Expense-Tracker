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

    # Display an expandable section for users to input values for each expense type.
    with st.expander("Expense"):
        for expense in expenses:
            default_value = st.session_state.get(f"expense_{expense}", 0)
            st.number_input(f"{expense}:", min_value=0, format="%i", step=5, value=default_value, key=f"expense_{expense}")
    return expenses