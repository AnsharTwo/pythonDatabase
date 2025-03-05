import streamlit as st
import form_sr
import json

class CONFIG_FORM (form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_config = {
        "json_config": "config.json"
    }

    def edt_sttngs(self):
        st.header("Manage Settings")
        config_data = self.__load_json_config()
        ant_edt_hght = config_data['librotate_config']['widget_dims']['textarea_annot_height']
        with st.form("config_settings"):
            st.markdown(f"**Workspace sizes**")
            cols_wrkspc_sz = st.columns(4, gap="small", vertical_alignment="center")
            cols_wrkspc_sz[0].text_input("Annotations editor height (pixels)", value=ant_edt_hght, max_chars=4,
                                         help="must be at least 68 pixels")
            st.divider()
            cols_config = st.columns(2, gap="small", vertical_alignment="center")
            if cols_config[0].form_submit_button("Save"):
                st.write("placeholder save")
            elif cols_config[1].form_submit_button("Reset to defaults"):
                st.write("placeholder reset")

    def __load_json_config(self):
        with open(self.dict_config.get("json_config"), 'r') as file:
            config_data = json.load(file)
            return config_data