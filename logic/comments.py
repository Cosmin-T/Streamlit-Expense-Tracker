# comments.py

import streamlit as st

def com(key: str) -> str:
    """
    Create an expandable section for users to enter a comment.

    Parameters
    ----------
    key : str
        The key to use when storing the comment.

    Returns
    -------
    str
        The comment entered by the user.
    """
    # Create an expandable section for users to enter a comment.
    with st.expander("Comment"):
        # Create a text area for the user to enter their comment.
        comment = st.text_area(f"{key}", placeholder="Provide comments on specifics like: Income particulars, Expense particulars, etc...")
    return comment
