import streamlit as st
import form
import form_sheet
import form_edit
import form_sheet_edit

class SIDEBAR:

    # def __init__(self):

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
        "Edit": "Do"
    }

    def init_sidebars(self):

        tabViewData, tabEditData = st.tabs([self.dict_tabh_drs.get("Read"), self.dict_tabh_drs.get("Edit")])

        dataForm = form.DATA_FORM()
        sheetForm = form_sheet.SHEET_FORM()
        editForm = form_edit.EDIT_FORM()
        editSheetForm = form_sheet_edit.EDIT_SHEET_FORM()

        st.sidebar.title("Annotations and URL manager")

        dropSelectApp = st.sidebar.selectbox("Select to view", [self.dict_data_app.get("annotDb"),
                                                                self.dict_data_app.get("urlExcel"), "None"]
                                            )
        if dropSelectApp == self.dict_data_app.get("annotDb"):
            with tabViewData:
                dataForm.select_search()
        elif dropSelectApp == self.dict_data_app.get("urlExcel"):
            with tabViewData:
                sheetForm.select_url_search()

        dropSelectDataApp = st.sidebar.selectbox("Select to do", [self.dict_edit_data_app.get("annotDb"),
                                                                  self.dict_edit_data_app.get("urlExcel"),"None"],
                                                )
        if dropSelectDataApp == self.dict_edit_data_app.get("annotDb"):
            with tabEditData:
                editForm.select_edit_form()
        elif dropSelectDataApp == self.dict_edit_data_app.get("urlExcel"):
            with tabEditData:
                editSheetForm.select_edit_form_sheet()