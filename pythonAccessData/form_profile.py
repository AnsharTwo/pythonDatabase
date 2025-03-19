import streamlit as st
import form_sr
import form_auth

class PROF_FORM (form_sr.FORM):

    def __init__(self, authenticator):
        super().__init__()
        self.authenticator = authenticator

    def set_prof_flow(self):
        st.session_state.form_prof_flow = "profile settings"

    def edt_prfl(self):
        if "form_prof_flow" not in st.session_state:
            st.session_state.form_prof_flow = ""
        if "prf_auth_obj" not in st.session_state:
            st.session_state.prf_auth_obj = None
        self.set_prof_flow()
        if st.session_state.form_prof_flow == "profile settings":
            st.session_state.prf_auth_obj = form_auth.LOGIN()
            auth_config = st.session_state.prf_auth_obj.create_auth_ojb()
            st.header("Manage Profile")
            if st.session_state["authentication_status"]:
                try:
                    if self.authenticator.reset_password(st.session_state.username, "main", clear_on_submit=False, key="lbrtt_chg_pwd"):
                        st.success('Password has been changed.')
                except Exception as e:
                    st.error(e)
                st.session_state.prf_auth_obj.write_auth_obj(auth_config)