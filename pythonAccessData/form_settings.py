import streamlit as st
import form_sr
import json

class CONFIG_FORM (form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_config = {
        "json_config": "config.json",
        "wdgt_specs": {
            "inpt_ant_edt_hght": 3
        }
    }

    def set_config_flow(self):
        st.session_state.form_config_flow = "config settings"

    def edt_sttngs(self):
        if "form_config_flow" not in st.session_state:
            st.session_state.form_config_flow = ""
        if "ant_edt_hght" not in st.session_state:
            st.session_state.ant_edt_hght = ""
        if "inpt_ant_edt_hght" not in st.session_state:
            st.session_state.inpt_ant_edt_hght = ""
        self.set_config_flow()
        if st.session_state.form_config_flow == "config settings":
            st.header("Manage Settings")
            config_data = self.__load_json_config()
            inpt_ant_edt_hght = config_data['librotate_config']['widget_dims']['textarea_annot_height']
            with st.form("config_settings"):
                st.markdown(f"**Workspace sizes**")
                cols_wrkspc_sz = st.columns(4, gap="small", vertical_alignment="center")
                st.session_state.inpt_ant_edt_hght = cols_wrkspc_sz[0].text_input("Annotations editor height (pixels)",
                                                                                  value=inpt_ant_edt_hght,
                                                                                  max_chars=self.dict_config.get("wdgt_specs").get("inpt_ant_edt_hght"),
                                                                                  help="must be at least 68 pixels")
                st.divider()
                cols_config = st.columns(2, gap="small", vertical_alignment="center")
                if cols_config[0].form_submit_button("Save"):
                    can_save = True
                    if st.session_state.inpt_ant_edt_hght == "" or not st.session_state.inpt_ant_edt_hght.isdigit():
                        st.markdown(":red[Annotations editor height must entered as a number up to 3 digits.]")
                        can_save = False
                    if can_save:
                        config_data['librotate_config']['widget_dims']['textarea_annot_height'] = st.session_state.inpt_ant_edt_hght
                        self.__write_json_config(config_data)
                        st.rerun()
                if cols_config[1].form_submit_button("Reset to defaults"):
                    st.write("placeholder reset")

    # TODO - move these to SR form
    def __load_json_config(self):
        with open(self.dict_config.get("json_config"), 'r') as file:
            config_data = json.load(file)
            return config_data

    def __write_json_config(self, config_data):
        with open(self.dict_config.get("json_config"), "w") as file:
            json.dump(config_data, file)