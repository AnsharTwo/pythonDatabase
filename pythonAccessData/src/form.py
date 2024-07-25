import streamlit as st

class DATA_FORM:

    # def __init__(self):

    def test_form(self):
        st.header("Enter your credentials")
        name = st.text_input("What is your name?")
        password = st.text_input("What is your password?",type="password")

        st.button("Login")