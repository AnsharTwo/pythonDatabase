import streamlit as st
#import streamlit_authenticator as stauth
import form_sr
import sidebar
import yaml
from yaml.loader import SafeLoader

class LOGIN(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_login = {
        "eml_len": 32,
        "pwd_len": 16
    }

    def create_auth_ojb(self):
        with open('auth/auths.YAML') as file:
            ath_cnfg = yaml.load(file, Loader=SafeLoader)
            return ath_cnfg

    def login_to_app(self):
        if "logged_in" not in st.session_state:
           st.session_state.logged_in = False
        if "sssn_usr_eml" not in st.session_state:
           st.session_state.sssn_usr_eml = ""
        if "sssn_usr_pwd" not in st.session_state:
           st.session_state.sssn_usr_pwd = ""
        auth_config = self.create_auth_ojb()
        placeholder = st.empty()
        if not st.session_state.logged_in:
            with placeholder.container():
                with st.form("Enter your details"):
                    st.header("Librotater")
                    st.session_state.sssn_usr_eml = st.text_input("Email address:red[*]",
                                                               max_chars=self.dict_login.get("eml_len"))
                    st.session_state.sssn_usr_pwd = st.text_input("Password:red[*]",
                                                               max_chars=self.dict_login.get("pwd_len"), type="password")
                    submit_login = st.form_submit_button("Log in")
                    if submit_login:
                        can_login = True
                        if st.session_state.sssn_usr_eml == "":
                            st.markdown(":red[Enter your email address.]")
                            can_login = False
                        #elif
                        #   #unknown email address
                        #   st.markdown(":red[Email address is not recognised.")
                        #   can_login = False
                        elif st.session_state.sssn_usr_pwd == "":
                            st.markdown(":red[Enter your password.]")
                            can_login = False
                        #elif
                        #   #unknown password
                        #   st.markdown(":red[Password is not recognised.")
                        #   can_login = False
                        if can_login:
                            st.session_state.logged_in = True
                            st.rerun()
        else:
            placeholder.empty()
            sbar = sidebar.SIDEBAR()
            sbar.init_sidebars()