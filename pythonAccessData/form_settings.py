import streamlit as st
import form_sr
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
            "inpt_spllchck_dstnc_minval": 1,
            "basic_clr_def_index": 0,
            "font_def_index": 0
        }
    }

    ddlist_itms = {
        "basic_clr": {
            "lght": "Light",
            "drk": "Dark"
        },
        "font": {
            "msp": "monospace",
            "ss": "sans serif",
            "s": "serif"
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
        if "sel_thm_bs_clr" not in st.session_state:
            st.session_state.sel_thm_bs_clr = ""
        if "sel_thm_fnt" not in st.session_state:
            st.session_state.sel_thm_fnt = ""
        self.set_config_flow()
        if st.session_state.form_config_flow == "config settings":
            config_data = self.load_ini_config()
            config_toml_data = self.load_toml_config()
            if st.session_state.val_ant_edt_hght == "":
                st.session_state.val_ant_edt_hght = config_data.get('widget_dims', 'textarea_annot_height')
            if st.session_state.val_spllchck_dstnc == "":
                st.session_state.val_spllchck_dstnc = config_data.get('spellcheck', 'distance')
            st.header("Manage Settings")
            with (st.form("config_settings")):
                st.markdown(f"**Theme**")
                st.markdown(":orange[(Current: ]" + str(config_toml_data["theme"]["base"]).title() + ":orange[)]  ")
                cols_wrkspc_sz = st.columns(4, gap="small", vertical_alignment="center")
                sel_opt_bscol = 'selectbox_option_' + "base_colour_itms"
                if sel_opt_bscol not in st.session_state:
                    st.session_state[sel_opt_bscol] = 0
                values_list_bscol = list(self.ddlist_itms.get("basic_clr").values())
                st.session_state.sel_thm_bs_clr = cols_wrkspc_sz[0].selectbox("Base colour",
                                             [
                                                 value
                                                 for value in self.ddlist_itms.get("basic_clr").values()
                                             ],
                                             index=st.session_state[sel_opt_bscol]
                                             )
                if values_list_bscol.index(st.session_state.sel_thm_bs_clr) != st.session_state[sel_opt_bscol]:
                    st.session_state[sel_opt_bscol] = values_list_bscol.index(st.session_state.sel_thm_bs_clr)
                st.divider()
                st.markdown(f"**Font**")
                st.markdown(":orange[(Current: ]" + str(config_toml_data["theme"]["font"]).title() + ":orange[)]  ")
                cols_wrkspc_sz = st.columns(4, gap="small", vertical_alignment="center")
                sel_opt_fnt = 'selectbox_option_' + "font"
                if sel_opt_fnt not in st.session_state:
                    st.session_state[sel_opt_fnt] = 0
                values_list_fnt = list(self.ddlist_itms.get("font").values())
                st.session_state.sel_thm_fnt = cols_wrkspc_sz[0].selectbox("Font",
                                             [
                                                 value
                                                 for value in self.ddlist_itms.get("font").values()
                                             ],
                                             index=st.session_state[sel_opt_fnt]
                                             )
                if values_list_fnt.index(st.session_state.sel_thm_fnt) != st.session_state[sel_opt_fnt]:
                    st.session_state[sel_opt_fnt] = values_list_fnt.index(st.session_state.sel_thm_fnt)
                st.divider()


                st.markdown(f"**Workspace sizes**")
                st.markdown(":orange[(Current: ]" + str(config_data["widget_dims"]["textarea_annot_height"]).title() + ":orange[)]  ")
                cols_wrkspc_sz = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_ant_edt_hght = cols_wrkspc_sz[0].text_input("Annotations editor height (pixels)",
                                                                                  value=int(st.session_state.val_ant_edt_hght),
                                                                                  max_chars=self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght"),
                                                                                  help="""must be at least """ +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_minval")) +
                                                                                       """ pixels""")
                st.divider()
                st.markdown(f"**Spell checker**")
                st.markdown(":orange[(Current: ]" + str(
                config_data["spellcheck"]["distance"]).title() + ":orange[)]  ")
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
                        st.session_state[sel_opt_bscol] = values_list_bscol.index(st.session_state.sel_thm_bs_clr)
                        st.session_state[sel_opt_fnt] = values_list_fnt.index(st.session_state.sel_thm_fnt)
                        config_toml_data["theme"]["base"] = str('"' + st.session_state.sel_thm_bs_clr + '"').lower()
                        config_toml_data["theme"]["font"] = str('"' + st.session_state.sel_thm_fnt + '"')
                        config_data["widget_dims"]["textarea_annot_height"] = st.session_state.inpt_ant_edt_hght
                        config_data["spellcheck"]["distance"] = st.session_state.inpt_spllchck_dstnc
                        if st.session_state.val_ant_edt_hght != st.session_state.inpt_ant_edt_hght:
                            st.session_state.val_ant_edt_hght = st.session_state.inpt_ant_edt_hght
                        if st.session_state.val_spllchck_dstnc != st.session_state.inpt_spllchck_dstnc:
                            st.session_state.val_spllchck_dstnc = st.session_state.inpt_spllchck_dstnc
                        self.write_toml_config(config_toml_data)
                        self.write_ini_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    os.remove(self.dict_config.get("toml_config"))
                    os.remove(self.dict_config.get("ini_config"))
                    shutil.copy(self.dict_config.get("toml_config_def"), self.dict_config.get("toml_config"))
                    shutil.copy(self.dict_config.get("ini_config_def"), self.dict_config.get("ini_config"))
                    st.session_state[sel_opt_bscol] = self.form_config.get("wdgt_specs").get("basic_clr_def_index")
                    st.session_state[sel_opt_fnt] = self.form_config.get("wdgt_specs").get("font_def_index")
                    config_def_data = self.load_ini_config()
                    st.session_state.val_ant_edt_hght = config_def_data["widget_dims"]["textarea_annot_height"]
                    st.session_state.val_spllchck_dstnc = config_def_data["spellcheck"]["distance"]
                    st.rerun()