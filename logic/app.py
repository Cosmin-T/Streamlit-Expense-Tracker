# app.py

import streamlit as st
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from logic.navigation import nav
from logic.currency import curr
from logic.period import per
from logic.comments import com
from logic.income import inc
from logic.expense import exp
from logic.data_plug import *
from logic.database import *
from logic.tracker import *
from logic.authenticator import *
import datetime

def og_app():
    """
    The main entry point for the expense tracker app.

    Handles the user's choice between the Data Entry, Data Visualization, and Data Tracker sections.
    """
    # Check the current month and display snow effect if it's Nov, Dec, or Jan
    current_month = datetime.datetime.now().month
    if current_month in [11, 12, 1]:
        st.snow()

    # Use nav to determine user's choice
    selected_choice = nav()

    # Handle Data Entry section logic.
    if selected_choice == "Data-Entry":
        with st.form(key="main_form"):
            # Period (Month & Year) Entry
            month, year = per()
            period = f"{month} {year}"

            # Income
            incomes_list = inc()

            # Expenses
            expenses_list = exp()

            # Comment Section for Expenses
            expense_comment = com("Expense")

            # Submission logic
            submitted = st.form_submit_button("Save Data")

            if submitted:
                # Retrieve values from session_state
                incomes = {income: st.session_state.get(f"income_{income}", 0) for income in incomes_list}
                expenses = {expense: st.session_state.get(f"expense_{expense}", 0) for expense in expenses_list}

                # Fetch the current data for the selected period
                current_period_data = get_period(period)

                # Check if there is an existing comment and append the new one
                if current_period_data and "comment" in current_period_data:
                    expense_comment = current_period_data["comment"] + "\n\n" + expense_comment
                else:
                    expense_comment = expense_comment

                # Insert data for both Incomes and Expenses with the appended expense_comment
                insert_period(period, incomes, expenses, expense_comment)

                # Display the saved data
                st.success("Data Saved")

    # Handle Data Visualization section logic.
    elif selected_choice == "Data-Visualization":
        """
        Handles the Data Visualization section logic.
        """
        if st.button("Clear All Data"):
            """
            Clears all data from the database.
            """
            clear_data()
        plug()

    # Handle Tracker section logic.
    elif selected_choice == "Data-Tracker":
        """
        Handles the Data Tracker section logic.
        """
        username = st.session_state.get('username', None)
        if username == "cosmint":
            """
            If the user is authorized, display the tracker page.
            """
            f_instalments()

        else:
            """
            If the user is not authorized, display a warning message.
            """
            st.warning("You are not authorized to access this page.")
