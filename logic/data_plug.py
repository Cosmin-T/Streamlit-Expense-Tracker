# data_plug.py

import streamlit as st
from logic.currency import *
import plotly.graph_objects as go
from logic.database import *

def show_details(total_income, currency, total_expense, remaining_budget):

    # Display the calculated metrics in the Streamlit app.
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"{total_income} {currency}")
    col2.metric("Total Expense", f"{total_expense} {currency}")
    col3.metric("Remaining Balance", f"{remaining_budget} {currency}")

def plug():

    # Get the current currency for display purposes.
    currency = curr()

    # Display a header indicating the section's purpose.
    st.header("Data Visualization")

    # Create a form that allows users to select a period from the available list to visualize its data.
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plug Data")

        if submitted:
            # Fetch the data for the selected period from the database.
            period_data = get_period(period)

            # Ensure period_data is not None before proceeding.
            if period_data:
                # Extract the comment, incomes, and expenses from the retrieved data.
                comment = period_data.get("comment")
                expenses = period_data.get("expenses")
                incomes = period_data.get("incomes")

                # Calculate totals and remaining budget for the selected period.
                total_income = sum(incomes.values())
                total_expense = sum(expenses.values())
                remaining_budget = total_income - total_expense

                # Display the calculated metrics in the Streamlit app.
                show_details(total_income, currency, total_expense, remaining_budget)

                # Display the comment associated with the data.
                st.text(f"Comment: {comment}")

                # Create a sankey chart to visually represent the flow of incomes and expenses.
                # Setup the source, target, and values for the sankey diagram.
                label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
                source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
                target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
                value = list(incomes.values()) + list(expenses.values())

                # Structure the data and attributes for the sankey diagram.
                link = dict(source=source, target=target, value=value)
                node = dict(label=label, pad=20, thickness=30, color="#6a2336")
                data = go.Sankey(link=link, node=node)

                # Render the sankey diagram in Streamlit.
                fig = go.Figure(data)
                fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                st.plotly_chart(fig, use_container_width=True)

            else:
                # Display a warning to the user if no data is found for the selected period.
                st.warning("No data found for the selected period.")