# comments.py

import streamlit as st

def com():

    # Create an expandable section for users to enter a comment.
    with st.expander("Comment"):
        comment = st.text_area("", placeholder="Eneter a comment here...")
    return comment