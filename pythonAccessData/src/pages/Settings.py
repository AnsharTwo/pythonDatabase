import streamlit as st

class SETTINGS():

    def __init__(self):
        super().__init__()

    def form_settings(self):
        with st.form("settings"):
            st.header("Settings")
            st.form_submit_button("Submit")

setts = SETTINGS()
setts.form_settings()