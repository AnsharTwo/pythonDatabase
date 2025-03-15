import streamlit as st
from streamlit.components.v1 import html
import form_sr
import form_home

class SIDEBAR (form_sr.FORM):

    def __init__(self, name_of_user):
        super().__init__()
        self.user = name_of_user

    dict_data_app = {
        "annotDb": "Annotations database",
        "urlExcel": "Excel URLs sheets"
    }

    dict_edit_data_app = {
        "annotDb": "Annotations database",
        "urlExcel": "Excel URLs sheets"
    }

    dict_tabh_drs = {
        "Read": "View",
        "Edit": "Do",
        "Config": "Settings"
    }

    def init_sidebars(self):
        home = form_home.HOME_FORM()
        tabViewData, tabEditData, tabSettingsData = st.tabs([self.dict_tabh_drs.get("Read"),
                                                             self.dict_tabh_drs.get("Edit"),
                                                             self.dict_tabh_drs.get("Config")])
        st.sidebar.write(":green[Welcome, {}!]".format(self.user))
        dropSelectApp = st.sidebar.selectbox("Select what to view", [self.dict_data_app.get("annotDb"),
                                                                self.dict_data_app.get("urlExcel"), "None"])
        if dropSelectApp == self.dict_data_app.get("annotDb"):
            with tabViewData:
                home.select_view_ant()
        elif dropSelectApp == self.dict_data_app.get("urlExcel"):
            with tabViewData:
                home.select_view_st()
        dropSelectDataApp = st.sidebar.selectbox("Select what to do", [self.dict_edit_data_app.get("annotDb"),
                                                                  self.dict_edit_data_app.get("urlExcel"),"None"])
        if dropSelectDataApp == self.dict_edit_data_app.get("annotDb"):
            with (tabEditData):
                home.select_do_ant()
        elif dropSelectDataApp == self.dict_edit_data_app.get("urlExcel"):
            with tabEditData:
                home.select_do_st()
        with tabSettingsData:
            home.select_sttngs()
        st.sidebar.divider()
        btn_view = st.sidebar.button("View", use_container_width=True)
        btn_do = st.sidebar.button("Do", use_container_width=True)
        st.sidebar.divider()
        btn_sttngs = st.sidebar.button("Settings", icon=":material/settings:")
        if btn_view:
            self.button_tab_switch("View", "View")
        if btn_do:
            self.button_tab_switch("Do", "Do")
        if btn_sttngs:
            self.button_tab_switch("Settings", "Settings")
        st.sidebar.divider()

    def button_tab_switch(self, button_text, tab_text):
        html(f"""<script>
        (() => {{
            let button = [...window.parent.document.querySelectorAll("button")].filter(button => {{
                console.log(">>>", button.innerText)
                return button.innerText.includes("{button_text}")
            }})[0];
            if(button) {{
                button.onclick = () => {{
                    var tabGroup = window.parent.document.getElementsByClassName("stTabs")[0]
                    const tabButton = [...tabGroup.querySelectorAll("button")].filter(button => {{
                        return button.innerText.includes("{tab_text}")
                    }})[0];
                    if(tabButton) {{
                        tabButton.click();
                    }} else {{
                        console.log("tab button {tab_text} not found")
                    }}
                }}
            }} else {{
                console.log("button not found: {button_text}")
            }}
        }})();
        </script>""", height=0)