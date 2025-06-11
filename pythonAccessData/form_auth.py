import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import form_sr
import sidebar

class LOGIN(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_auth = {
        "auth_path": "auth/auths.YAML"
    }

    def create_auth_ojb(self):
        with open(self.dict_auth.get("auth_path")) as file:
            ath_cnfg = yaml.load(file, Loader=SafeLoader)
            return ath_cnfg

    def write_auth_obj(self, ath_config):
        with open(self.dict_auth.get("auth_path"), 'w') as file:
            yaml.dump(ath_config, file, default_flow_style=False, indent=4)

    def create_authenticator(self, auth_config):
        authent = stauth.Authenticate(
            auth_config['credentials'],
            auth_config['cookie']['name'],
            auth_config['cookie']['key'],
            auth_config['cookie']['expiry_days'],
        )
        return authent

    def login_to_app(self):
        auth_config = self.create_auth_ojb()
        authenticator = self.create_authenticator(auth_config)
        st.header(":blue[Librotate]")
        authenticator.login(location='main', max_concurrent_users=100, captcha=False, single_session=False, clear_on_submit=False,
                            key="lbrtt_auth_01")
        if st.session_state["authentication_status"]:
            config_data = self.load_ini_config()
            if "ss_dat_loc_annots" not in st.session_state:
                st.session_state.ss_dat_loc_annots = str(config_data["data locations"]["annotations"])
            if "ss_dat_loc_urls" not in st.session_state:
                st.session_state.ss_dat_loc_urls = str(config_data["data locations"]["urls"])
            sbar = sidebar.SIDEBAR(st.session_state.name, authenticator)
            sbar.init_sidebars()
            authenticator.logout(location="sidebar")
            if st.session_state["authentication_status"] is None:
                st.session_state.clear()
                st.rerun()
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
        elif not st.session_state["authentication_status"]:
            st.error('Username/password is incorrect')