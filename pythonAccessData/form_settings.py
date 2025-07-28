import streamlit as st
import streamlit_authenticator as stauth
import os
import shutil
import form_sr
import form_auth

class CONFIG_FORM (form_sr.FORM):

    def __init__(self, authenticator):
        super().__init__()
        self.authenticator = authenticator

    form_config = {
        "wdgt_specs": {
            "inpt_ant_edt_hght": 3,
            "inpt_ant_edt_hght_minval": 68,
            "inpt_ant_edt_hght_maxval": 528,
            "inpt_spllchck_dstnc": 1,
            "inpt_spllchck_dstnc_minval": 1,
            "inpt_spllchck_dstnc_maxval": 2,
            "basic_clr_def_index": 0,
            "font_def_index": 0,
            "inpt_drdg_timeout": 3,
            "inpt_drdg_timeout_minval": 10,
            "inpt_drdg_timeout_maxval": 60,
            "inpt_drdg_distance": 3,
            "inpt_drdg_distance_minval": 21,
            "inpt_drdg_distance_maxval": 264,
            "inpt_drdg_max_pages": 5,
            "inpt_drdg_max_pages_minval": 1,
            "inpt_drdg_max_pages_maxval": 99999
        }
    }

    ddlist_itms = {
        "basic_clr": {
            "drk": "Dark",
            "lght": "Light"
        },
        "font": {
            "ss": "sans serif",
            "s": "serif",
            "msp": "monospace",
        }
    }

    def set_config_flow_theme(self):
        st.session_state.form_config_flow_theme = "config settings - theme"

    def set_config_flow_annt_hght(self):
        st.session_state.form_config_flow_annt_hght = "config settings - annot height"

    def set_config_flow_spell(self):
        st.session_state.form_config_flow_spell = "config settings - spell"

    def set_config_flow_dredge(self):
        st.session_state.form_config_flow_dredge = "config settings - dredge"

    def set_config_flow_shw_msgs(self):
        st.session_state.form_config_flow_shw_msgs = "config settings - show messages"

    def set_config_flow_bk_fct_defs(self):
        st.session_state.form_bk_fct_defs = "config settings - book source file factory defaults"

    def set_config_flow_url_fct_defs(self):
        st.session_state.form_url_fct_defs = "config settings - url source file factory defaults"

    def set_config_flow_url_del_accnt(self):
        st.session_state.form_del_accnt = "config settings - delete account"

    def edt_sttngs(self):
        if "form_config_flow_theme" not in st.session_state:
            st.session_state.form_config_flow_theme = ""
        if "form_config_flow_annt_hght" not in st.session_state:
            st.session_state.form_config_flow_annt_hght = ""
        if "form_config_flow_spell" not in st.session_state:
            st.session_state.form_config_flow_spell = ""
        if "form_config_flow_dredge" not in st.session_state:
            st.session_state.form_config_flow_dredge = ""
        if "form_config_flow_shw_msgs" not in st.session_state:
            st.session_state.form_config_flow_shw_msgs = ""
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
        if "inpt_annt_hght" not in st.session_state:
            st.session_state.inpt_annt_hght = ""
        if "val_inpt_annt_hght" not in st.session_state:
            st.session_state.val_inpt_annt_hght = ""
        if "inpt_spell_dstnc" not in st.session_state:
            st.session_state.inpt_spell_dstnc = ""
        if "val_inpt_spell_dstnc" not in st.session_state:
            st.session_state.val_inpt_spell_dstnc = ""
        if "inpt_drdg_timeout" not in st.session_state:
            st.session_state.inpt_drdg_timeout = ""
        if "inpt_drdg_max_wbpgs" not in st.session_state:
            st.session_state.inpt_drdg_max_wbpgs = ""
        if "val_inpt_drdg_max_wbpgs" not in st.session_state:
            st.session_state.val_inpt_drdg_max_wbpgs = ""
        if "val_inpt_drdg_timeout" not in st.session_state:
            st.session_state.val_inpt_drdg_timeout = ""
        if "inpt_drdge_dstnc" not in st.session_state:
            st.session_state.inpt_drdge_dstnc = ""
        if "val_inpt_drdge_dstnc" not in st.session_state:
            st.session_state.val_inpt_drdge_dstnc = ""
        if "val_inpt_shw_drdg_msg" not in st.session_state:
            st.session_state.val_inpt_shw_drdg_msg = ""
        if "inpt_shw_drdg_msg" not in st.session_state:
            st.session_state.inpt_shw_drdg_msg = ""
        if "form_bk_fct_defs" not in st.session_state:
            st.session_state.form_bk_fct_defs = ""
        if "form_url_fct_defs" not in st.session_state:
            st.session_state.form_url_fct_defs = ""

        if "form_del_accnt" not in st.session_state:
            st.session_state.form_del_accnt = ""

        if "fac_bk_def_sbmttd" not in st.session_state:
            st.session_state.fac_bk_def_sbmttd = False
        if "fac_url_def_sbmttd" not in st.session_state:
            st.session_state.fac_url_def_sbmttd = False

        if "del_accnt_sbmttd" not in st.session_state:
            st.session_state.del_accnt_sbmttd = False
        if "del_accnt_db_src" not in st.session_state:
            st.session_state.del_accnt_db_src = False
        if "del_accnt_urls_src" not in st.session_state:
            st.session_state.del_accnt_urls_src = False

        if "loc_db_ant_chng" not in st.session_state:
            st.session_state.loc_db_ant_chng = False
        if "loc_db_bk_chng" not in st.session_state:
            st.session_state.loc_db_bk_chng = False
        if "shw_data_loc_msg" not in st.session_state:
            st.session_state.shw_data_loc_msg = False
        if "val_shw_data_loc_msg" not in st.session_state:
            st.session_state.val_shw_data_loc_msg = ""
        self.set_config_flow_theme()
        if st.session_state.form_config_flow_theme == "config settings - theme":
            config_toml_data = self.load_toml_config()
            st.header("Manage Settings")
            with (st.form("config_settings")):
                st.markdown(f":blue[**Theme**]")
                cols_wrkspc_clr = st.columns(4, gap="small", vertical_alignment="center")
                sel_opt_bscol = 'selectbox_option_' + "base_colour_itms"
                if sel_opt_bscol not in st.session_state:
                    st.session_state[sel_opt_bscol] = 0
                values_list_bscol = list(self.ddlist_itms.get("basic_clr").values())
                st.session_state.sel_thm_bs_clr = cols_wrkspc_clr[0].selectbox("Base colour",
                                             [
                                                 value
                                                 for value in self.ddlist_itms.get("basic_clr").values()
                                             ],
                                             index=st.session_state[sel_opt_bscol]
                                             )
                if values_list_bscol.index(st.session_state.sel_thm_bs_clr) != st.session_state[sel_opt_bscol]:
                    st.session_state[sel_opt_bscol] = values_list_bscol.index(st.session_state.sel_thm_bs_clr)
                st.markdown(":orange[(Current: ]" + str(config_toml_data["theme"]["base"]).title() + ":orange[)]  ")
                st.divider()
                cols_wrkspc_fnt = st.columns(4, gap="small", vertical_alignment="center")
                sel_opt_fnt = 'selectbox_option_' + "font"
                if sel_opt_fnt not in st.session_state:
                    st.session_state[sel_opt_fnt] = 0
                values_list_fnt = list(self.ddlist_itms.get("font").values())
                st.session_state.sel_thm_fnt = cols_wrkspc_fnt[0].selectbox("Font",
                                             [
                                                 value
                                                 for value in self.ddlist_itms.get("font").values()
                                             ],
                                             index=st.session_state[sel_opt_fnt]
                                             )
                if values_list_fnt.index(st.session_state.sel_thm_fnt) != st.session_state[sel_opt_fnt]:
                    st.session_state[sel_opt_fnt] = values_list_fnt.index(st.session_state.sel_thm_fnt)
                st.markdown(":orange[(Current: ]" + str(config_toml_data["theme"]["font"]).title() + ":orange[)]  ")
                st.divider()
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    st.session_state[sel_opt_bscol] = values_list_bscol.index(st.session_state.sel_thm_bs_clr)
                    st.session_state[sel_opt_fnt] = values_list_fnt.index(st.session_state.sel_thm_fnt)
                    config_toml_data["theme"]["base"] = str('"' + st.session_state.sel_thm_bs_clr + '"').lower()
                    config_toml_data["theme"]["font"] = str('"' + st.session_state.sel_thm_fnt + '"')
                    self.write_toml_config(config_toml_data)
                    st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    os.remove(self.dict_config.get("toml_config"))
                    shutil.copy(self.dict_config.get("toml_config_def"), self.dict_config.get("toml_config"))
                    st.session_state[sel_opt_bscol] = self.form_config.get("wdgt_specs").get("basic_clr_def_index")
                    st.session_state[sel_opt_fnt] = self.form_config.get("wdgt_specs").get("font_def_index")
                    st.rerun()
        self.set_config_flow_annt_hght()
        if st.session_state.form_config_flow_annt_hght == "config settings - annot height":
            config_data = self.load_ini_config()
            if st.session_state.val_inpt_annt_hght == "":
                st.session_state.val_inpt_annt_hght = config_data['widget_dims']['textarea_annot_height']
            with (st.form("config_settings_wrkspc_szs")):
                st.markdown(f"**:blue[Workspace sizes]**")
                cols_wrkspc_wrkspc_szs = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_annt_hght = cols_wrkspc_wrkspc_szs[0].text_input("Annotations editor height (pixels)",
                                                                value=int(st.session_state.val_inpt_annt_hght),
                                                                max_chars=self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght"),
                                                                help="""Must be a number of pixels between """ +
                                                                str(self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_minval")) +
                                                                " and " +
                                                                str(self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_maxval")) + ".")
                st.markdown(":orange[(Current: ]" + str(config_data["widget_dims"]["textarea_annot_height"]).title() + ":orange[)]  ")
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    can_save = True
                    if st.session_state.inpt_annt_hght == "" or not st.session_state.inpt_annt_hght.isdigit() \
                                                               or int(st.session_state.inpt_annt_hght) < \
                                                                   self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_minval") \
                                                               or int(st.session_state.inpt_annt_hght) > \
                                                                   self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_maxval"):
                        st.markdown(":red[Annotations editor height must be entered as a number between " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_minval")) +
                                    " and " + str(self.form_config.get("wdgt_specs").get("inpt_ant_edt_hght_maxval")) + ".]")
                        can_save = False
                    if can_save:
                        config_data["widget_dims"]["textarea_annot_height"] = st.session_state.inpt_annt_hght
                        if st.session_state.val_inpt_annt_hght != st.session_state.inpt_annt_hght:
                            st.session_state.val_inpt_annt_hght = st.session_state.inpt_annt_hght
                        self.write_ini_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    config_def_data = self.load_ini_config_def()
                    config_data = self.load_ini_config()
                    config_data["widget_dims"]["textarea_annot_height"] = config_def_data["widget_dims"]["textarea_annot_height"]
                    st.session_state.val_inpt_annt_hght = config_def_data["widget_dims"]["textarea_annot_height"]
                    self.write_ini_config(config_data)
                    st.rerun()
        self.set_config_flow_spell()
        if st.session_state.form_config_flow_spell == "config settings - spell":
            config_data = self.load_ini_config()
            if st.session_state.val_inpt_spell_dstnc == "":
                st.session_state.val_inpt_spell_dstnc = config_data['spellcheck']['distance']
            with (st.form("config_settings_spell")):
                st.markdown(f"**:blue[Spell checker]**")
                cols_wrkspc_spll_dstnc = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_spell_dstnc = cols_wrkspc_spll_dstnc[0].text_input("Distance",
                                                                            value=int(st.session_state.val_inpt_spell_dstnc),
                                                                            max_chars=self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc"),
                                                                            help="""The number of words from the spell-checked word
                                                                            that will be used to compute the suggestions. Must be between """ +
                                                                            str(self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_minval")) +
                                                                            " and " +
                                                                            str(self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_maxval")) + ".")
                st.markdown(":orange[(Current: ]" + str(config_data["spellcheck"]["distance"]).title() + ":orange[)]  ")
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    can_save = True
                    if st.session_state.inpt_spell_dstnc == "" or not st.session_state.inpt_spell_dstnc.isdigit() \
                                                               or int(st.session_state.inpt_spell_dstnc) < \
                                                                   self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_minval") \
                                                               or int(st.session_state.inpt_spell_dstnc) > \
                                                                   self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_maxval"):
                        st.markdown(":red[Spell check distance must be entered as a number between " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_minval")) +
                                    " and " + str(self.form_config.get("wdgt_specs").get("inpt_spllchck_dstnc_maxval")) + ".]")
                        can_save = False
                    if can_save:
                        config_data["spellcheck"]["distance"] = st.session_state.inpt_spell_dstnc
                        if st.session_state.val_inpt_spell_dstnc != st.session_state.inpt_spell_dstnc:
                            st.session_state.val_inpt_spell_dstnc = st.session_state.inpt_spell_dstnc
                        self.write_ini_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    config_def_data = self.load_ini_config_def()
                    config_data = self.load_ini_config()
                    config_data["spellcheck"]["distance"] = config_def_data["spellcheck"]["distance"]
                    st.session_state.val_inpt_spell_dstnc = config_def_data["spellcheck"]["distance"]
                    self.write_ini_config(config_data)
                    st.rerun()
        self.set_config_flow_dredge()
        if st.session_state.form_config_flow_dredge == "config settings - dredge":
            config_data = self.load_ini_config()
            if st.session_state.val_inpt_drdg_timeout == "":
                st.session_state.val_inpt_drdg_timeout = config_data['dredge']['response_timeout']
            if st.session_state.val_inpt_drdge_dstnc == "":
                st.session_state.val_inpt_drdge_dstnc = config_data['dredge']['result_distance']
            if st.session_state.val_inpt_drdg_max_wbpgs == "":
                st.session_state.val_inpt_drdg_max_wbpgs = config_data['dredge']['max_web_pages']
            with (st.form("config_settings_dredge")):
                st.markdown(f"**:blue[Dredge web pages]**")
                cols_wrkspc_drdg_timeout = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_drdge_dstnc = cols_wrkspc_drdg_timeout[0].text_input("Returned text snippet size",
                                                                                  value=int(st.session_state.val_inpt_drdge_dstnc),
                                                                                  max_chars=self.form_config.get("wdgt_specs").get("inpt_drdg_distance"),
                                                                                  help="""must be a number of characters between """ +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_drdg_distance_minval")) +
                                                                                       " and " +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_drdg_distance_maxval")))
                st.markdown(":orange[(Current: ]" + str(config_data["dredge"]["result_distance"]).title() + ":orange[)]  ")
                st.divider()
                cols_wrkspc_drdg_max_wbpgs = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_drdg_max_wbpgs = cols_wrkspc_drdg_max_wbpgs[0].text_input("Max. number of web pages to dredge.",
                                                                                  value=int(st.session_state.val_inpt_drdg_max_wbpgs),
                                                                                  max_chars=self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages"),
                                                                                  help="""must be a number between """ +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages_minval")) +
                                                                                       " and " +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages_maxval")) +
                                                                                        " (WARNING - very high number NOT recommended).")
                st.markdown(":orange[(Current: ]" + str(config_data["dredge"]["max_web_pages"]).title() + ":orange[)]  ")
                st.divider()
                cols_wrkspc_drdg_timeout = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_drdg_timeout = cols_wrkspc_drdg_timeout[0].text_input("Web page server response timeout",
                                                                                  value=int(st.session_state.val_inpt_drdg_timeout),
                                                                                  max_chars=self.form_config.get("wdgt_specs").get("inpt_drdg_timeout"),
                                                                                  help="""must be a number in seconds between """ +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_drdg_timeout_minval")) +
                                                                                       " and " +
                                                                                       str(self.form_config.get("wdgt_specs").get("inpt_drdg_timeout_maxval")))
                st.markdown(":orange[(Current: ]" + str(config_data["dredge"]["response_timeout"]).title() + ":orange[)]  ")
                st.divider()
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    can_save = True
                    if st.session_state.inpt_drdge_dstnc == "" or not st.session_state.inpt_drdge_dstnc.isdigit() \
                                                               or int(st.session_state.inpt_drdge_dstnc) < \
                                                                   self.form_config.get("wdgt_specs").get("inpt_drdg_distance_minval") \
                                                               or int(st.session_state.inpt_drdge_dstnc) > \
                                                                   self.form_config.get("wdgt_specs").get("inpt_drdg_distance_maxval"):
                        st.markdown(":red[Text snippet size must be entered as a number up to " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_drdg_distance_maxval")) +
                                    " digits, and not lesser than " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_drdg_distance_minval")) + ".]")
                        can_save = False
                    elif st.session_state.inpt_drdg_timeout == "" or not st.session_state.inpt_drdg_timeout.isdigit() \
                                                                or int(st.session_state.inpt_drdg_timeout) < \
                                                                    self.form_config.get("wdgt_specs").get("inpt_drdg_timeout_minval") \
                                                                or int(st.session_state.inpt_drdg_timeout) > \
                                                                    self.form_config.get("wdgt_specs").get("inpt_drdg_timeout_maxval"):
                        st.markdown(":red[Web page server response timeout must be entered as a number up to " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_drdg_timeout_maxval")) +
                                    " digits, and not lesser than " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_drdg_timeout_minval")) + ".]")
                        can_save = False
                    elif st.session_state.inpt_drdg_max_wbpgs == "" or not st.session_state.inpt_drdg_max_wbpgs.isdigit() \
                                                                or int(st.session_state.inpt_drdg_max_wbpgs) < \
                                                                    self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages_minval") \
                                                                or int(st.session_state.inpt_drdg_max_wbpgs) > \
                                                                    self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages_maxval"):
                        st.markdown(":red[Number of web pages to search must be entered as a number up to " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages_maxval")) +
                                    " digits, and not lesser than " +
                                    str(self.form_config.get("wdgt_specs").get("inpt_drdg_max_pages_minval")) + ".]")
                        can_save = False
                    if can_save:
                        config_data["dredge"]["result_distance"] = st.session_state.inpt_drdge_dstnc
                        config_data["dredge"]["response_timeout"] = st.session_state.inpt_drdg_timeout
                        config_data["dredge"]["max_web_pages"] = st.session_state.inpt_drdg_max_wbpgs
                        if st.session_state.val_inpt_drdge_dstnc != st.session_state.inpt_drdge_dstnc:
                            st.session_state.val_inpt_drdge_dstnc = st.session_state.inpt_drdge_dstnc
                        if st.session_state.val_inpt_drdg_timeout != st.session_state.inpt_drdg_timeout:
                            st.session_state.val_inpt_drdg_timeout = st.session_state.inpt_drdg_timeout
                        if st.session_state.val_inpt_drdg_max_wbpgs != st.session_state.inpt_drdg_max_wbpgs:
                            st.session_state.val_inpt_drdg_max_wbpgs = st.session_state.inpt_drdg_max_wbpgs
                        self.write_ini_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    config_def_data = self.load_ini_config_def()
                    config_data = self.load_ini_config()
                    config_data["dredge"]["result_distance"] = config_def_data["dredge"]["result_distance"]
                    config_data["dredge"]["response_timeout"] = config_def_data["dredge"]["response_timeout"]
                    config_data["dredge"]["max_web_pages"] = config_def_data["dredge"]["max_web_pages"]
                    st.session_state.val_inpt_drdge_dstnc = config_def_data["dredge"]["result_distance"]
                    st.session_state.val_inpt_drdg_timeout = config_def_data["dredge"]["response_timeout"]
                    st.session_state.val_inpt_drdg_max_wbpgs = config_def_data["dredge"]["max_web_pages"]
                    self.write_ini_config(config_data)
                    st.rerun()
        self.set_config_flow_shw_msgs() # now inited in if.. at top
        if st.session_state.form_config_flow_shw_msgs == "config settings - show messages":
            config_data = self.load_ini_config()
            if st.session_state.val_inpt_shw_drdg_msg == "":
                if config_data['show_messages']['dredge_note'] == "1":
                    st.session_state.val_inpt_shw_drdg_msg = True
                else:
                    st.session_state.val_inpt_shw_drdg_msg = False
            if st.session_state.val_shw_data_loc_msg == "":
                if config_data['show_messages']['profile_note'] == "1":
                    st.session_state.val_shw_data_loc_msg = True
                else:
                    st.session_state.val_shw_data_loc_msg = False
            with (st.form("config_settings_shw_msgs")):
                st.markdown(f"**:blue[Show/hide user messages]**")
                cols_shw_msgs_drdge = st.columns(2, gap="small", vertical_alignment="center")
                st.session_state.inpt_shw_drdg_msg = cols_shw_msgs_drdge[0].checkbox("Internet web pages search notification",
                                                                value=int(st.session_state.val_inpt_shw_drdg_msg),
                                                                key="shw_drdg_msg_wfs543")
                if st.session_state.val_inpt_shw_drdg_msg:
                    st.markdown(":orange[(Current: ]" + "Showing" + ":orange[)]  ")
                else:
                    st.markdown(":orange[(Current: ]" + "Not showing" + ":orange[)]  ")
                st.divider()
                cols_shw_msgs_dt_lc = st.columns(2, gap="small", vertical_alignment="center")
                st.session_state.shw_data_loc_msg = cols_shw_msgs_dt_lc[0].checkbox("Data locations selection notification",
                                                                value=int(st.session_state.val_shw_data_loc_msg),
                                                                key="shw_drdg_msg_tky982")
                if st.session_state.val_shw_data_loc_msg:
                    st.markdown(":orange[(Current: ]" + "Showing" + ":orange[)]  ")
                else:
                    st.markdown(":orange[(Current: ]" + "Not showing" + ":orange[)]  ")
                st.divider()
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    if st.session_state.inpt_shw_drdg_msg:
                        if config_data["show_messages"]["dredge_note"] == "0":
                            config_data["show_messages"]["dredge_note"] = "1"
                    else:
                        if config_data["show_messages"]["dredge_note"] == "1":
                            config_data["show_messages"]["dredge_note"] = "0"
                    if st.session_state.val_inpt_shw_drdg_msg != st.session_state.inpt_shw_drdg_msg:
                        st.session_state.val_inpt_shw_drdg_msg = st.session_state.inpt_shw_drdg_msg
                    if st.session_state.shw_data_loc_msg:
                        if config_data["show_messages"]["profile_note"] == "0":
                            config_data["show_messages"]["profile_note"] = "1"
                    else:
                        if config_data["show_messages"]["profile_note"] == "1":
                            config_data["show_messages"]["profile_note"] = "0"
                    if st.session_state.val_shw_data_loc_msg != st.session_state.shw_data_loc_msg:
                        st.session_state.val_shw_data_loc_msg = st.session_state.shw_data_loc_msg
                    self.write_ini_config(config_data)
                    st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    config_def_data = self.load_ini_config_def()
                    config_data = self.load_ini_config()
                    config_data["show_messages"]["dredge_note"] = config_def_data["show_messages"]["dredge_note"]
                    config_data["show_messages"]["profile_note"] = config_def_data["show_messages"]["profile_note"]
                    st.session_state.val_inpt_shw_drdg_msg = config_def_data["show_messages"]["dredge_note"]
                    st.session_state.val_shw_data_loc_msg = config_def_data["show_messages"]["profile_note"]
                    self.write_ini_config(config_data)
                    st.rerun()
        self.set_config_flow_bk_fct_defs()
        if st.session_state.form_bk_fct_defs == "config settings - book source file factory defaults":
            if st.session_state.fac_bk_def_sbmttd:
                sttngs_auth_obj = form_auth.LOGIN()
                auth_config = sttngs_auth_obj.create_auth_ojb()
                pwd_hashed_curr = auth_config["credentials"]["usernames"][st.session_state.username]["password"]
                with st.form("Enter book password"):
                    if st.session_state.loc_db_ant_chng or st.session_state.loc_db_bk_chng:
                        st.write(self.dict_err_msgs.get("db_locked_in_changes"))
                        st.form_submit_button("Locked", disabled=True)
                        st.session_state.fac_bk_def_sbmttd = False
                    else:
                        st.markdown(f"**:blue[Restore book data source to factory default]**")
                        st.write("Enter your password to restore your book data source file to factory default.")
                        pwd_sttngs = st.text_input("Password", type="password",
                                                                     max_chars=self.dict_pwd_chng.get("length")) # max chars in profile too - add to Super
                        cols_config_pwd = st.columns(2, gap="small", vertical_alignment="center")
                        if cols_config_pwd[0].form_submit_button("Submit password"):
                            can_change = True
                            if not stauth.Hasher.check_pw(pwd_sttngs, pwd_hashed_curr):
                                st.markdown(":red[Enter current password.]")
                                can_change = False
                            if can_change:
                                try:
                                    dstn = st.session_state.ss_dat_loc_annots.rsplit("/", 1)
                                    fact_def_file = str(self.dict_fac_defs.get("bk")).rsplit("/", 1)
                                    if not os.path.exists(str(dstn[0]) + "/" + str(fact_def_file[1])):
                                        self.__fac_def_bk_switch(str(dstn[0]),str(fact_def_file[1]))
                                        st.rerun()
                                    else:
                                        st.write("The file " + ":red[" + str(dstn[0]) + "/" + str(fact_def_file[1]) + "] already exists.")
                                        btn_fac_def_bk_overwrite = st.checkbox("Overwrite book file")
                                        if btn_fac_def_bk_overwrite:
                                            self.__fac_def_bk_switch(str(dstn[0]), str(fact_def_file[1]))
                                            st.rerun()
                                except Exception as ex:
                                    st.markdown(":red[The operation could not be performed.]")
                                    st.write(str(ex))
                        if cols_config_pwd[1].form_submit_button("Cancel"):
                            st.session_state.fac_bk_def_sbmttd = False
                            self.set_config_flow_bk_fct_defs()
                            st.rerun()
            else:
                with (st.form("config_settings_bk_fac_defs")):
                    st.markdown(f"**:blue[Restore book data source to factory default]**")
                    st.markdown(":orange[Current book database location:] " + str(st.session_state.ss_dat_loc_annots))
                    st.markdown(""":red[WARNING. Restoring your data source files to empty default source data files will 
                                                            delete all of your existing saved data.]""")
                    cols_config_bk = st.columns(2, gap="small", vertical_alignment="center")
                    if cols_config_bk[0].form_submit_button("Restore book source"):
                        st.session_state.fac_bk_def_sbmttd = True
                        st.rerun()
        self.set_config_flow_url_fct_defs()
        if st.session_state.form_url_fct_defs == "config settings - url source file factory defaults":
            if st.session_state.fac_url_def_sbmttd:
                sttngs_auth_obj = form_auth.LOGIN()
                auth_config = sttngs_auth_obj.create_auth_ojb()
                pwd_hashed_curr = auth_config["credentials"]["usernames"][st.session_state.username]["password"]
                with st.form("Enter url password"):
                    st.markdown(f"**:blue[Restore online url data source to factory default]**")
                    st.write("Enter your password to restore your online url data source file to factory default.")
                    pwd_sttngs = st.text_input("Password", type="password",
                                                                 max_chars=self.dict_pwd_chng.get("length")) # max chars in profile too - add to Super
                    cols_config_pwd = st.columns(2, gap="small", vertical_alignment="center")
                    if cols_config_pwd[0].form_submit_button("Submit password"):
                        can_change = True
                        if not stauth.Hasher.check_pw(pwd_sttngs, pwd_hashed_curr):
                            st.markdown(":red[Enter current password.]")
                            can_change = False
                        if can_change:
                            try:
                                dstn = st.session_state.ss_dat_loc_urls.rsplit("/", 1)
                                fact_def_file = str(self.dict_fac_defs.get("url")).rsplit("/", 1)
                                if not os.path.exists(str(dstn[0]) + "/" + str(fact_def_file[1])):
                                    self.__fac_def_url_switch(str(dstn[0]),str(fact_def_file[1]))
                                    st.rerun()
                                else:
                                    st.write("The file " + ":red[" + str(dstn[0]) + "/" + str(fact_def_file[1]) + "] already exists.")
                                    btn_fac_def_url_overwrite = st.checkbox("Overwrite URLs file")
                                    if btn_fac_def_url_overwrite:
                                        self.__fac_def_url_switch(str(dstn[0]), str(fact_def_file[1]))
                                        st.rerun()
                            except Exception as ex:
                                st.markdown(":red[The operation could not be performed.]")
                                st.write(str(ex))
                    if cols_config_pwd[1].form_submit_button("Cancel"):
                        st.session_state.fac_url_def_sbmttd = False
                        self.set_config_flow_url_fct_defs()
                        st.rerun()
            else:
                with (st.form("config_settings_url_fac_defs")):
                    st.markdown(f"**:blue[Restore online url data source to factory default]**")
                    st.markdown(":orange[Current url data location:] " + str(st.session_state.ss_dat_loc_urls))
                    st.markdown(""":red[WARNING. Restoring your data source files to empty default source data files will 
                                                            delete all of your existing saved data.]""")
                    cols_config_url = st.columns(2, gap="small", vertical_alignment="center")
                    if cols_config_url[0].form_submit_button("Restore online url source"):
                        st.session_state.fac_url_def_sbmttd = True
                        st.rerun()

        self.set_config_flow_url_del_accnt()
        if st.session_state.form_del_accnt == "config settings - delete account":
            if st.session_state.del_accnt_sbmttd:
                sttngs_auth_obj = form_auth.LOGIN()
                auth_config = sttngs_auth_obj.create_auth_ojb()
                pwd_hashed_curr = auth_config["credentials"]["usernames"][st.session_state.username]["password"]
                with st.form("Delete account"):
                    st.markdown(f"**:blue[Cancel your account]**")
                    st.write("Enter your password to cancel your Librotate account.")
                    pwd_sttngs = st.text_input("Password", type="password",
                                                                 max_chars=self.dict_pwd_chng.get("length")) # max chars in profile too - add to Super
                    cols_config_pwd = st.columns(2, gap="small", vertical_alignment="center")
                    if cols_config_pwd[0].form_submit_button("Submit password"):
                        can_change = True
                        if not stauth.Hasher.check_pw(pwd_sttngs, pwd_hashed_curr):
                            st.markdown(":red[Enter current password.]")
                            can_change = False
                        if can_change:
                            try:
                                # TODO - delete user's ini and toml files, set a ss flag (or check if those files exist when logging out.
                                # TODO - at logout, need to handle deleted account (do not overwrite user's ini and toml files with the root dir toml and ini)
                                # TODO - delete (at logout) data sources files depending on checkbox logic

                                print("x")

                            except Exception as ex:
                                st.markdown(":red[The operation could not be performed.]")
                                st.write(str(ex))
                    if cols_config_pwd[1].form_submit_button("Cancel"):
                        st.session_state.del_accnt_sbmttd = False
                        self.set_config_flow_url_del_accnt()
                        st.rerun()
            else:
                with (st.form("config_settings_del_accnt")):
                    st.markdown(f"**:blue[Cancel your Librotate account]**")
                    st.markdown(""":orange[If you cancel your Librotate account, you will not be able to restore it.
                                You could however create a new account, which will be set up for you with default settings.]""")
                    st.write("""If you cancel your account, your data location sources will not be deleted, unless you tick the 
                             delete data files checkboxes.""")
                    st.divider()
                    st.session_state.del_accnt_db_src = st.checkbox("Delete database data source")
                    st.session_state.del_accnt_urls_src = st.checkbox("Delete URLs data source")
                    cols_config_url = st.columns(2, gap="small", vertical_alignment="center")
                    if cols_config_url[0].form_submit_button("Cancel account"):
                        st.session_state.del_accnt_sbmttd = True
                        st.rerun()

    def __fac_def_bk_switch(self, dest_path, dest_file):
        os.remove(st.session_state.ss_dat_loc_annots)
        st.session_state.ss_dat_loc_annots = dest_path + "/" + dest_file
        shutil.copy(self.dict_fac_defs.get("bk"), dest_path)
        config_data = self.load_ini_config()
        config_data["data locations"]["annotations"] = st.session_state.ss_dat_loc_annots
        self.write_ini_config(config_data)
        st.session_state.fac_bk_def_sbmttd = False

    def __fac_def_url_switch(self, dest_path, dest_file):
        os.remove(st.session_state.ss_dat_loc_urls)
        st.session_state.ss_dat_loc_urls = dest_path + "/" + dest_file
        shutil.copy(self.dict_fac_defs.get("url"), dest_path)
        config_data = self.load_ini_config()
        config_data["data locations"]["urls"] = st.session_state.ss_dat_loc_urls
        self.write_ini_config(config_data)
        st.session_state.fac_url_def_sbmttd = False