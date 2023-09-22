# comments.py

import streamlit as st

def com(key):

    # Create an expandable section for users to enter a comment.
    with st.expander("Comment"):
        comment = st.text_area(f"{key}", placeholder="Provide comments on specifics like: Income particulars, Expense particulars, etc...")
    return comment