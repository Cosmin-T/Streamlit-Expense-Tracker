# data_plug.py

import streamlit as st
from logic.currency import *
import plotly.graph_objects as go
from logic.database import *

def show_details(total_income: float, currency: str, total_expense: float, remaining_budget: float):
    """
    Displays the calculated income, expense, and remaining balance in the Streamlit app.

    Args:
        total_income (float): The total income.
        currency (str): The currency symbol.
        total_expense (float): The total expense.
        remaining_budget (float): The remaining balance.
    """
    # Display the calculated metrics in the Streamlit app.
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"{total_income} {currency}",
                help="The total income.")
    col2.metric("Total Expense", f"{total_expense} {currency}",
                help="The total expense.")
    col3.metric("Remaining Balance", f"{remaining_budget} {currency}",
                help="The remaining balance.")

def plug():
    """
    The main function to display the data visualization section.

    This function is called from the Streamlit app and displays the data visualization section.

    It fetches the data for the selected period from the database and displays the calculated metrics, including the total income, total expense, and remaining balance.

    It also displays a Sankey diagram to visualize the income and expense data.
    """
    # Get the current currency for display purposes.
    currency = curr()

    # Display a header indicating the section's purpose.
    st.header("Data Visualization")

    # Initialize session state for tracking data fetching
    if 'data_fetched' not in st.session_state:
        st.session_state['data_fetched'] = False

    with st.form("saved_periods"):
        # Dropdown to select a period for data visualization
        period = st.selectbox("Select Period:", get_all_periods())

        # Submit button for the form
        submitted = st.form_submit_button("Plug Data")

        # When the form is submitted, fetch data for the selected period
        if submitted:
            # Fetch the data for the selected period from the database
            period_data = get_period(period)

            # Store the fetched data in the session state
            st.session_state['period_data'] = period_data

            # Set the flag to indicate that data has been fetched
            st.session_state['data_fetched'] = True

    # Check if data has been fetched or is available in session state
    if st.session_state['data_fetched']:
        # Use the data stored in the session state
        period_data = st.session_state['period_data']

        # Ensure that there is data for the selected period
        if period_data:
            # Extract details from the period data
            comment = period_data.get("comment")
            expenses = period_data.get("expenses")
            incomes = period_data.get("incomes")

            # Calculate total income, expense, and remaining budget
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense

            # Display the calculated metrics
            show_details(total_income, currency, total_expense, remaining_budget)

            # Text area for editing the comment
            edited_comment = st.text_area("Edit Comment:", comment)

            # Button to save the edited comment
            save_btn = st.button("Save")

            # Check if the comment has been edited and save it
            if save_btn:
                if edited_comment.strip() != comment:
                    # Update the comment in the database
                    update_comment(period, edited_comment)
                    st.success("Comment updated successfully")

                    # Reset the data fetched flag
                    st.session_state['data_fetched'] = False

            # Display the edited or original comment
            st.text(f"Comment: {edited_comment}")

            # Set up the data for the Sankey diagram
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())

            # Structure the data and attributes for the Sankey diagram
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#6a2336")
            data = go.Sankey(link=link, node=node)

            # Render the Sankey diagram in Streamlit
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Display a warning if no data is found for the selected period
            st.warning("No data found for the selected period.")
