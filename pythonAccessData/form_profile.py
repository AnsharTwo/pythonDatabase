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
        "librotate_close_msg": "NOTE: Please quit the background popup window after you have selected your file.",
        "tkinter_close_msg": "PLEASE CLOSE THIS WINDOW AFTER YOU HAVE FINISHED SELECTING YOUR DATA SOURCE FILE."
    }

    def set_prof_flow_data_locs(self):
        st.session_state.form_prof_flow = "profile settings - data locations"

    def set_prof_flow_chang_pwd(self):
        st.session_state.form_prof_flow = "profile settings - change password"

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
        if "loc_db_ant_chng" not in st.session_state:
            st.session_state.loc_db_ant_chng = False
        if "loc_db_bk_chng" not in st.session_state:
            st.session_state.loc_db_bk_chng = False
        if "val_shw_data_loc_msg" not in st.session_state:
            st.session_state.val_shw_data_loc_msg = False
        authent = self.authenticator
        prf_auth_obj = form_auth.LOGIN()
        st.header("Manage Profile")
        self.set_prof_flow_data_locs()
        if st.session_state.form_prof_flow == "profile settings - data locations":
            with st.form("data locations"):
                config_data = self.load_ini_config()
                st.markdown(f"**:blue[Data locations]**")
                st.write("Annotations database")
                if st.session_state.loc_db_ant_chng or st.session_state.loc_db_bk_chng:
                    st.write(self.dict_err_msgs.get("db_locked_in_changes"))
                    st.markdown(":red[ENSURE YOU CLOSE THE FILE SELECTION AND CONFIRM BOXES] if they are open.]")
                    st.form_submit_button("Locked", disabled=True)
                else:
                    st.markdown(":orange[(Current: ]" + str(
                        st.session_state.ss_dat_loc_annots).title() + ":orange[)]  ")
                    if st.form_submit_button("Browse annotations files"):
                        try:
                            config_data = self.load_ini_config()
                            if int(config_data.get('show_messages', 'profile_note')) == 1:
                                self.__data_loc_modal()
                            else:
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
                        except Exception as ex:
                            st.write(":red[" + self.dict_err_msgs.get("tkinter_dialog_err") + "]")
                            st.markdown(ex)
                            st.write(":green[" + self.dict_err_msgs.get("tkinter_dialog_err_act") + "]")
                st.divider()
                st.write("URL sheets")
                st.markdown(":orange[(Current: ]" + str(
                    st.session_state.ss_dat_loc_urls).title() + ":orange[)]  ")
                if st.form_submit_button("Browse URLs files"):
                    try:
                        config_data = self.load_ini_config()
                        if int(config_data.get('show_messages', 'profile_note')) == 1:
                            self.__data_loc_modal()
                        else:
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
                    except Exception as ex:
                        st.write(":red[" + self.dict_err_msgs.get("tkinter_dialog_err") + "]")
                        st.markdown(ex)
                        st.write(":green[" + self.dict_err_msgs.get("tkinter_dialog_err_act") + "]")
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
                                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_curr_pwd") + "]")
                                can_change = False
                            elif not authent.authentication_controller.validator.validate_password(st.session_state.pwd_new):
                                st.markdown(
                                    ":red[" + self.dict_chng_pwd_err_msgs.get("valid_new_pwd") + "]")
                                can_change = False
                            elif st.session_state.pwd_new == st.session_state.pwd_current:
                                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_uniq_new_pwd") + "]")
                                can_change = False
                            elif st.session_state.pwd_new != st.session_state.pwd_new_confirm:
                                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_conf_new_pwd") + "]")
                                can_change = False
                            if can_change:
                                hashed_password = stauth.Hasher.hash(st.session_state.pwd_new)
                                auth_config["credentials"]["usernames"][st.session_state.username]["password"] = hashed_password
                                prf_auth_obj.write_auth_obj(auth_config)
                                st.session_state.pwd_changed = True
                                st.rerun()

    @st.dialog("When selecting your data source file", width="small")
    def __data_loc_modal(self):
        st.write(self.dict_data_locs.get("librotate_close_msg"))
        cbx_data_loc_no_show = st.checkbox(label="OK, got it", key="lbrtt_dt_lc_swe")
        if cbx_data_loc_no_show:
            config_data = self.load_ini_config()
            config_data["show_messages"]["profile_note"] = "0"
            if st.session_state.val_shw_data_loc_msg:  # val of Settings > show messages > dredge web note
                st.session_state.val_shw_data_loc_msg = False
            self.write_ini_config(config_data)
            st.rerun()

    def ds_file_dialog(self, file_brand, file_type):
        input_path = fd.askopenfilename(title="Select a data location", filetypes=[(file_brand, file_type)])
        return str(input_path)