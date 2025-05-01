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
            "inpt_drdg_distance_maxval": 264
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

    def edt_sttngs(self):
        if "form_config_flow_theme" not in st.session_state:
            st.session_state.form_config_flow_theme = ""
        if "form_config_flow_annt_hght" not in st.session_state:
            st.session_state.form_config_flow_annt_hght = ""
        if "form_config_flow_spell" not in st.session_state:
            st.session_state.form_config_flow_spell = ""
        if "form_config_flow_dredge" not in st.session_state:
            st.session_state.form_config_flow_dredge = ""
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
        if "val_inpt_drdg_timeout" not in st.session_state:
            st.session_state.val_inpt_drdg_timeout = ""
        if "inpt_drdge_dstnc" not in st.session_state:
            st.session_state.inpt_drdge_dstnc = ""
        if "val_inpt_drdge_dstnc" not in st.session_state:
            st.session_state.val_inpt_drdge_dstnc = ""
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
                    os.remove(self.dict_config.get("ini_config"))
                    shutil.copy(self.dict_config.get("ini_config_def"), self.dict_config.get("ini_config"))
                    config_def_data = self.load_ini_config()
                    st.session_state.val_inpt_annt_hght = config_def_data["widget_dims"]["textarea_annot_height"]
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
                    os.remove(self.dict_config.get("ini_config"))
                    shutil.copy(self.dict_config.get("ini_config_def"), self.dict_config.get("ini_config"))
                    config_def_data = self.load_ini_config()
                    st.session_state.val_inpt_spell_dstnc = config_def_data["spellcheck"]["distance"]
                    st.rerun()
        self.set_config_flow_dredge()
        if st.session_state.form_config_flow_dredge == "config settings - dredge":
            config_data = self.load_ini_config()
            if st.session_state.val_inpt_drdg_timeout == "":
                st.session_state.val_inpt_drdg_timeout = config_data['dredge']['response_timeout']
            if st.session_state.val_inpt_drdge_dstnc == "":
                st.session_state.val_inpt_drdge_dstnc = config_data['dredge']['result_distance']
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
                    if can_save:
                        config_data["dredge"]["result_distance"] = st.session_state.inpt_drdge_dstnc
                        config_data["dredge"]["response_timeout"] = st.session_state.inpt_drdg_timeout
                        if st.session_state.val_inpt_drdge_dstnc != st.session_state.inpt_drdge_dstnc:
                            st.session_state.val_inpt_drdge_dstnc = st.session_state.inpt_drdge_dstnc
                        if st.session_state.val_inpt_drdg_timeout != st.session_state.inpt_drdg_timeout:
                            st.session_state.val_inpt_drdg_timeout = st.session_state.inpt_drdg_timeout
                        self.write_ini_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset"):
                    os.remove(self.dict_config.get("ini_config"))
                    shutil.copy(self.dict_config.get("ini_config_def"), self.dict_config.get("ini_config"))
                    config_def_data = self.load_ini_config()
                    st.session_state.val_inpt_drdge_dstnc = config_def_data["dredge"]["result_distance"]
                    st.session_state.val_inpt_drdg_timeout = config_def_data["dredge"]["response_timeout"]
                    st.rerun()