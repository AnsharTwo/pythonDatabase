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
        if "pwd_changed" not in st.session_state:
            st.session_state.pwd_changed = False
        if "pwd_current" not in st.session_state:
            st.session_state.pwd_current = ""
        if "pwd_new" not in st.session_state:
            st.session_state.pwd_new = ""
        if "pwd_new_confirm" not in st.session_state:
            st.session_state.pwd_new_confirm = ""
        authent = self.authenticator
        self.set_prof_flow()
        if st.session_state.form_prof_flow == "profile settings":
            prf_auth_obj = form_auth.LOGIN()
            st.header("Manage Profile")
            if st.session_state["authentication_status"]:
                if st.session_state.pwd_changed:
                    with st.form("Changed password"):
                        st.success("Password has been changed.")
                        st.session_state.pwd_changed = False
                        btn_pwd_changed = st.form_submit_button("Done")
                        if btn_pwd_changed:
                            st.rerun()
                else:
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
                        if btn_chng_pwd:
                            can_change = True
                            if not stauth.Hasher.check_pw(st.session_state.pwd_current, pwd_hashed_curr):
                                st.markdown(":red[Enter current password.]")
                                can_change = False
                            elif not authent.authentication_controller.validator.validate_password(st.session_state.pwd_new):
                                st.markdown(
                                    """:red[New password must be between 8 and 20 characters long, contain at least: one uppercase letter,
                                     one lowercase letter, one number, and one special chararcter from the set @$!%*?&.]""")
                                can_change = False
                            elif st.session_state.pwd_new != st.session_state.pwd_new_confirm:
                                st.markdown(":red[New and confirmed passwords don't match.]")
                                can_change = False
                            if can_change:
                                hashed_password = stauth.Hasher.hash(st.session_state.pwd_new)
                                auth_config["credentials"]["usernames"][st.session_state.username]["password"] = hashed_password
                                prf_auth_obj.write_auth_obj(auth_config)
                                st.session_state.pwd_changed = True
                                st.rerun()