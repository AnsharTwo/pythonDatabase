import streamlit as st
import streamlit_authenticator as stauth
import form_sr
import form_auth

class PROF_FORM (form_sr.FORM):

    def __init__(self, authenticator):
        super().__init__()
        self.authenticator = authenticator

    dict_pwd_chng = {
        "length": 16
    }

    def set_prof_flow(self):
        st.session_state.form_prof_flow = "profile settings"

    def edt_prfl(self):
        if "form_prof_flow" not in st.session_state:
            st.session_state.form_prof_flow = ""
        if "pwd_current" not in st.session_state:
            st.session_state.pwd_current = ""
        if "pwd_new" not in st.session_state:
            st.session_state.pwd_new = ""
        if "pwd_new_confirm" not in st.session_state:
            st.session_state.pwd_new_confirm = ""
        self.set_prof_flow()
        if st.session_state.form_prof_flow == "profile settings":
            prf_auth_obj = form_auth.LOGIN()
            st.header("Manage Profile")
            if st.session_state["authentication_status"]:
                auth_config = prf_auth_obj.create_auth_ojb()
                pwd_hashed_curr = auth_config["credentials"]["usernames"][st.session_state.username]["password"]
                with st.form("Reset password"):
                    st.markdown(f"**Change password**")
                    st.session_state.pwd_current = st.text_input("Current password", type="password",
                                                                 max_chars=self.dict_pwd_chng.get("length"))
                    st.session_state.pwd_new = st.text_input("New password", type="password",
                                                                 max_chars=self.dict_pwd_chng.get("length"))
                    st.session_state.pwd_new_confirm = st.text_input("Confirm new password", type="password",
                                                                 max_chars=self.dict_pwd_chng.get("length"))
                    btn_chng_pwd = st.form_submit_button("Change")
                    can_change = True
                    if btn_chng_pwd:
                        if not stauth.Hasher.check_pw(st.session_state.pwd_current, pwd_hashed_curr):
                            st.markdown(
                                ":red[Enter current password.]")
                        # TODO - complete validation from here
                        else:
                            hashed_password = stauth.Hasher.hash(st.session_state.pwd_new)
                            auth_config["credentials"]["usernames"][st.session_state.username]["password"] = hashed_password
                            prf_auth_obj.write_auth_obj(auth_config)