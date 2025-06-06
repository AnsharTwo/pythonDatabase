import streamlit as st
import streamlit_authenticator as stauth
from tkinter import filedialog as fd
import tkinter as tk
import form_sr
import form_auth

class PROF_FORM (form_sr.FORM):

    def __init__(self, authenticator):
        super().__init__()
        self.authenticator = authenticator

    dict_data_locs = {
        "librotate_close_msg": "NOTE: Please quit the background popup window after your have selected your file.",
        "tkinter_close_msg": "PLEASE CLOSE THIS WINDOW AFTER YOU HAVE FINISHED SELECTING YOUR DATA SOURCE FILE."
    }

    dict_pwd_chng = {
        "length": 16
    }

    def set_prof_flow_data_locs(self):
        st.session_state.form_prof_flow = "profile settings - data locations"

    def set_prof_flow_chang_pwd(self):
        st.session_state.form_prof_flow = "profile settings - change password"

    def edt_prfl(self):
        if "form_prof_flow" not in st.session_state:
            st.session_state.form_prof_flow = ""

        #if "dt_lcs_run" not in st.session_state:
        #    st.session_state.dt_lcs_run = False

        if "pwd_changed" not in st.session_state:
            st.session_state.pwd_changed = False
        if "pwd_current" not in st.session_state:
            st.session_state.pwd_current = ""
        if "pwd_new" not in st.session_state:
            st.session_state.pwd_new = ""
        if "pwd_new_confirm" not in st.session_state:
            st.session_state.pwd_new_confirm = ""
        authent = self.authenticator
        prf_auth_obj = form_auth.LOGIN()
        st.header("Manage Profile")

        #################################
        self.set_prof_flow_data_locs()
        if st.session_state.form_prof_flow == "profile settings - data locations":
            with st.form("data locations"):
                #self.data_loc_msg()
                config_data = self.load_ini_config()
                st.markdown(f"**:blue[Data locations]**")
                st.write("Annotations database")
                st.markdown(":orange[(Current: ]" + str(
                    st.session_state.ss_dat_loc_annots).title() + ":orange[)]  ")
                if st.form_submit_button("Browse annotations files"):
                    root = tk.Tk()
                    tk.Button(root, text="Confirm data source file selection", font=("Arial", 12), command=root.destroy).pack()
                    tk.Label(root, text = self.dict_data_locs.get("tkinter_close_msg")).pack()
                    pth = self.ds_file_dialog("Access", ".mdb")
                    if pth != "":
                        config_data["data locations"]["annotations"] = pth
                        st.session_state.ss_dat_loc_annots = pth
                        self.write_ini_config(config_data)
                    root.after(1000)
                    root.mainloop()
                    st.rerun()
                st.divider()
                st.write("URL sheets")
                st.markdown(":orange[(Current: ]" + str(
                    st.session_state.ss_dat_loc_urls).title() + ":orange[)]  ")
                if st.form_submit_button("Browse URLs files"):
                    root = tk.Tk()
                    tk.Button(root, text="Confirm data source file selection", font=("Arial", 12), command=root.destroy).pack()
                    tk.Label(root, text = self.dict_data_locs.get("tkinter_close_msg")).pack()
                    pth = self.ds_file_dialog("Excel", ".xlsx")
                    if pth != "":
                        config_data["data locations"]["urls"] = pth
                        st.session_state.ss_dat_loc_urls = pth
                        self.write_ini_config(config_data)
                        self.load_book_sheet.clear() # clear cache or new data will not show
                    root.after(1000)
                    root.mainloop()
                    st.rerun()
        #################################

        self.set_prof_flow_chang_pwd()
        if st.session_state.form_prof_flow == "profile settings - change password":
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
                        st.markdown(f"**:blue[Change password]**")
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

    @st.dialog("Before selecting your data source file", width="small")
    def data_loc_msg(self):
        st.write(self.dict_data_locs.get("librotate_close_msg"))
        #st.checkbox(label="Okay", key="lbrtt_dt_lc_swe")
        #st.rerun()

    def ds_file_dialog(self, file_brand, file_type):
        input_path = fd.askopenfilename(title="Select a data location", filetypes=[(file_brand, file_type)])
        return str(input_path)