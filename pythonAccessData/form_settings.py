import streamlit as st
import form_sr
import json
import os
import shutil

class CONFIG_FORM (form_sr.FORM):

    def __init__(self):
        super().__init__()

    form_config = {
        "wdgt_specs": {
            "inpt_ant_edt_hght": 3,
            "inpt_ant_edt_hght_minval": 68,
            "inpt_spllchck_dstnc": 1,
            "inpt_spllchck_dstnc_minval": 1
        }
    }

    def set_config_flow(self):
        st.session_state.form_config_flow = "config settings"

    def edt_sttngs(self):
        if "form_config_flow" not in st.session_state:
            st.session_state.form_config_flow = ""
        if "inpt_ant_edt_hght" not in st.session_state:
            st.session_state.inpt_ant_edt_hght = ""
        if "val_ant_edt_hght" not in st.session_state:
            st.session_state.val_ant_edt_hght = ""
        if "inpt_spllchck_dstnc" not in st.session_state:
            st.session_state.inpt_spllchck_dstnc = ""
        if "val_spllchck_dstnc" not in st.session_state:
            st.session_state.val_spllchck_dstnc = ""
        self.set_config_flow()
        if st.session_state.form_config_flow == "config settings":
            config_data = self.load_ini_config()
            if st.session_state.val_ant_edt_hght == "":
                st.session_state.val_ant_edt_hght = config_data.get('widget_dims', 'textarea_annot_height')
            if st.session_state.val_spllchck_dstnc == "":
                st.session_state.val_spllchck_dstnc = config_data.get('spellcheck', 'distance')
            st.header("Manage Settings")
            with st.form("config_settings"):
                st.markdown(f"**Workspace sizes**")
                cols_wrkspc_sz = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_ant_edt_hght = cols_wrkspc_sz[0].text_input("Annotations editor height (pixels)",
                                                                                  value=int(st.session_state.val_ant_edt_hght),
                                                                                  max_chars=self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght"),
                                                                                  help="""must be at least """ +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_minval")) +
                                                                                       """ pixels""")
                st.divider()
                st.markdown(f"**Spell checker**")
                cols_spll_chck_sz = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_spllchck_dstnc = cols_spll_chck_sz[0].text_input("Distance",
                                                                                  value=int(st.session_state.val_spllchck_dstnc),
                                                                                  max_chars=self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc"),
                                                                                  help="""The number of words from the spell-checked word
                                                                                  that will be used to compute the suggestions (click
                                                                                  'Check Spelling' button to update)""")
                st.divider()
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    can_save = True
                    if st.session_state.inpt_ant_edt_hght == "" or not st.session_state.inpt_ant_edt_hght.isdigit() \
                                                                or int (st.session_state.inpt_ant_edt_hght) < \
                                                                    self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_minval"):
                        st.markdown(":red[Annotations editor height must be entered as a number up to 3 digits, and not lesser than 68.]")
                        can_save = False
                    elif st.session_state.inpt_spllchck_dstnc == "" or not st.session_state.inpt_spllchck_dstnc.isdigit() \
                                                                or int (st.session_state.inpt_spllchck_dstnc) < \
                                                                    self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_minval"):
                        st.markdown(":red[Spellcheck distance must be entered as a number up to 1 digit, and greater than 0.]")
                        can_save = False
                    if can_save:
                        st.session_state.val_ant_edt_hght = st.session_state.inpt_ant_edt_hght
                        st.session_state.val_spllchck_dstnc = st.session_state.inpt_spllchck_dstnc
                        config_data["widget_dims"]["textarea_annot_height"] = st.session_state.inpt_ant_edt_hght
                        config_data["spellcheck"]["distance"] = st.session_state.inpt_spllchck_dstnc
                        if st.session_state.val_ant_edt_hght != st.session_state.inpt_ant_edt_hght:
                            st.session_state.val_ant_edt_hght = st.session_state.inpt_ant_edt_hght
                        if st.session_state.val_spllchck_dstnc != st.session_state.inpt_spllchck_dstnc:
                            st.session_state.val_spllchck_dstnc = st.session_state.inpt_spllchck_dstnc
                        self.write_ini_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    os.remove(self.dict_config.get("ini_config"))
                    shutil.copy(self.dict_config.get("ini_config_def"), self.dict_config.get("ini_config"))
                    config_def_data = self.load_ini_config()
                    st.session_state.val_ant_edt_hght = config_def_data["widget_dims"]["textarea_annot_height"]
                    st.session_state.val_spllchck_dstnc = config_def_data["spellcheck"]["distance"]
                    st.rerun()