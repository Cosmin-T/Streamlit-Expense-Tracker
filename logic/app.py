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
    if 'snow_initialized' not in st.session_state:
        current_month = datetime.datetime.now().month
        if current_month in [11, 12, 1, 2]:
            # Generate 50 unique snowflake animations
            snowflake_animations = [
                f"""
                @keyframes fall-{i} {{
                    from {{
                        transform: translate({(i % 5) * 20 - 50}vw, -10px) rotate(0deg);
                    }}
                    to {{
                        transform: translate({((i % 7) - 3) * 15}vw, 110vh) rotate({i * 360}deg);
                    }}
                }}""" for i in range(50)
            ]

            custom_css = f"""
                <style>
                    {' '.join(snowflake_animations)}

                    {''.join([f'''
                    .snowflake:nth-child({i}) {{
                        opacity: {0.4 + (i % 6) * 0.1};
                        width: {1 + (i % 4)}px;
                        height: {1 + (i % 4)}px;
                        left: {(i * 2) % 100}vw;
                        animation: fall-{i % 50} {5 + (i % 7)}s linear infinite;
                        animation-delay: -{i * 0.2}s;
                        pointer-events: none;
                    }}''' for i in range(150)])}

                    .snowflake {{
                        position: fixed;
                        background: white;
                        border-radius: 50%;
                        pointer-events: none;
                    }}

                    .snowfall {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        z-index: 9999;
                        pointer-events: none;
                    }}
                </style>
                <div class="snowfall">
                    {''.join(['<div class="snowflake"></div>' for _ in range(150)])}
                </div>
            """
            st.session_state.snow_css = custom_css
            st.session_state.snow_initialized = True

    # Render the snow if it's initialized
    if 'snow_css' in st.session_state:
        st.markdown(st.session_state.snow_css, unsafe_allow_html=True)

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
