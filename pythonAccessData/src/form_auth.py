import streamlit as st
#import streamlit_authenticator as stauth
import form_sr
import sidebar

class LOGIN(form_sr.FORM):

    def __init__(self):
        super().__init__()

    def login_to_app(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        with st.form("Enter your credentials to continue"):
            submit_login = st.form_submit_button("Log in")
            if submit_login:
                st.session_state.logged_in = True
                st.rerun()
            else:
                if st.session_state.logged_in:
                    sbar = sidebar.SIDEBAR()
                    sbar.init_sidebars()