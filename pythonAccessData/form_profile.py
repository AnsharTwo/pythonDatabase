import streamlit as st
import form_sr

class PROF_FORM (form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_pwd_spec = {
        "lngth": 15
    }

    def set_prof_flow(self):
        st.session_state.form_prof_flow = "profile settings"

    def edt_prfl(self):
        if "pwd_temp" not in st.session_state:
            st.session_state.pwd_temp = ""
        if "pwd_conf_temp" not in st.session_state:
            st.session_state.pwd_conf_temp = ""
        if "pwd_new_temp" not in st.session_state:
            st.session_state.pwd_new_temp = ""
        self.set_prof_flow()
        if st.session_state.form_prof_flow == "profile settings":
            st.header("Manage Profile")
            with st.form("Edit Profile"):
                profile_auth = self.create_auth_ojb()
                # TODO - st.session_state.username needs to search usenames in YAML as keyerr comes up as ss username is lower case
                # TODO ...and YAML is robAsc01. username, name and email are in ss (not password)
                #w = profile_auth["credentials"]["usernames"]["robAsc01"]#[str(st.session_state.username)]
                st.markdown(f"**Change password**")
                st.session_state.pwd_temp = st.text_input("Current password",
                                                                                  max_chars=self.dict_pwd_spec.get("lngth"),
                                                                                  help="""TBC""", type="password")
                st.session_state.pwd_conf_temp = st.text_input("Confirm password",
                                                                                  max_chars=self.dict_pwd_spec.get("lngth"),
                                                                                  help="""TBC""", type="password")
                st.session_state.pwd_new_temp = st.text_input("New password",
                                                                                  max_chars=self.dict_pwd_spec.get("lngth"),
                                                                                  help="""TBC""", type="password")
                st.divider()
                btn_save_profile = st.form_submit_button("Save profile")