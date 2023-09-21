# period.py

import calendar
from datetime import datetime
import streamlit as st
from logic.currency import *

def per():

    # Get the current currency.
    currency = curr()

    # Set up the options for months and years for the dropdown.
    current_year = datetime.today().year
    years = [current_year + i for i in range(8)]
    months = list(calendar.month_name[1:])

    # Display the header for data entry and dropdowns for selecting the month and year.
    st.header(f"Data Entry in: {currency}")
    col1, col2 = st.columns(2)
    month = col1.selectbox("Select Month", months)
    year = col2.selectbox("Select Year", years)

    return month, year