import streamlit as st
import form_sr

class PROF_FORM (form_sr.FORM):

    def __init__(self, authenticator):
        super().__init__()
        self.authenticator = authenticator

    def set_prof_flow(self):
        st.session_state.form_prof_flow = "profile settings"

    def edt_prfl(self):
        self.set_prof_flow()
        if st.session_state.form_prof_flow == "profile settings":
            st.header("Manage Profile")
            if st.session_state["authentication_status"]:
                try:
                    if self.authenticator.reset_password(st.session_state.username, "main", clear_on_submit=True, key="lbrtt_chng_pwd"):
                        st.success('Password has been changed.')
                except Exception as e:
                    st.error(e)