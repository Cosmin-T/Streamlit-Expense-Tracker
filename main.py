# main.py

import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from logic.settings import settings
from logic.navigation import nav
from logic.currency import curr
from logic.period import per
from logic.comments import com
from logic.income import inc
from logic.expense import exp
from logic.data_plug import *
from logic.database import *

def main():

    # Configure the page with title and icon
    settings()
    # Use nav to determine user's choice
    selected_choice = nav()
    # show_details(total_income, currency, total_expense, remaining_budget)

    # Handle Data Entry section logic.
    if selected_choice == "Data Entry":
        with st.form(key="main_form"):
            # Period (Month & Year) Entry
            month, year = per()
            period = f"{month} {year}"

            # Income
            incomes_list = inc()

            # Expenses
            expenses_list = exp()

            # Comment Section for Expenses
            expense_comment = com("Details")

            # Submission logic
            submitted = st.form_submit_button("Save Data")

            if submitted:
                # Retrieve values from session_state
                incomes = {income: st.session_state.get(f"income_{income}", 0) for income in incomes_list}
                expenses = {expense: st.session_state.get(f"expense_{expense}", 0) for expense in expenses_list}

                # Insert data for Incomes with the income_comment
                insert_period(period, incomes, {})

                # Insert data for Expenses with the expense_comment
                insert_period(period, {}, expenses, expense_comment)

                # Display the saved data
                st.success("Data Saved")


    # Handle Data Visualization section logic.
    elif selected_choice == "Data-Visualization":
        if st.button("Clear All Data"):
            clear_data()
        plug()

# Start
if __name__ == "__main__":
    main()