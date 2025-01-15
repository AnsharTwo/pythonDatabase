import streamlit as st
import form_sr
import form
import form_sheet
import form_bk
import form_annt
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

    dict_list_annt_wrkr = {
        "header": "Edit annotations data",
        "title": "Select data activity"
    }

    dict_List_view = {
        "header": "Select annotations search",
        "title": "Select search type"
    }

    dict_list_wrkr_items = {
        "None": "none",
        "ants_edt_add": "Create or update annotation",
        "ants_edt_dlt": "Delete an annotation",
        "bk_add_update_bk": "Add or update a book",
        "bk_dlt": "Delete a book",
    }

    dict_list_view_items = {
        "None": "none",
        "ants_srch_txt": "Annotations by search text",
        "ants_srch_txt_auth": "Annotations by search text and author",
        "ants_srch_txt_bk": "Annotations by search text and book",
        "ants_bk": "Annotations by book",
        "ants_auth": "Annotations by author",
        "bks_auth": "Books by author",
        "bks_all": "All books",
        "bks_yr_read": "Books by year read",
        "ants_all": "All annotations",
        "ants_yr_read": "Annotations by year read"
    }


    def init_sidebars(self):
        super_form = form_sr.FORM()
        db_viewer = form.DATA_FORM()
        annt_worker_form = form_annt.EDIT_ANNOT()
        annt_worker_del_form = form_annt.DEL_ANNOT()
        bk_worker_form = form_bk.EDIT_BOOK()
        bk_worker_del_form = form_bk.DEL_BOOK()
        sheetForm = form_sheet.SHEET_FORM()
        editSheetForm = form_sheet_edit.EDIT_SHEET_FORM()
        tabViewData, tabEditData = st.tabs([self.dict_tabh_drs.get("Read"), self.dict_tabh_drs.get("Edit")])
        dropSelectApp = st.sidebar.selectbox("Select to view", [self.dict_data_app.get("annotDb"),
                                                                self.dict_data_app.get("urlExcel"), "None"]
                                            )
        if dropSelectApp == self.dict_data_app.get("annotDb"):
            with tabViewData:

                itm_slctd = super_form.select_edit_form(self.dict_List_view.get("header"),
                                                        self.dict_List_view.get("title"),
                                                        self.dict_list_view_items)
                if itm_slctd == self.dict_list_view_items.get("ants_srch_txt"):
                    db_viewer.srch_searchtext()


        elif dropSelectApp == self.dict_data_app.get("urlExcel"):
            with tabViewData:
                sheetForm.select_url_search()
        dropSelectDataApp = st.sidebar.selectbox("Select to do", [self.dict_edit_data_app.get("annotDb"),
                                                                  self.dict_edit_data_app.get("urlExcel"),"None"],
                                                )
        if dropSelectDataApp == self.dict_edit_data_app.get("annotDb"):
            with (tabEditData):
                itm_slctd = super_form.select_edit_form(self.dict_list_annt_wrkr.get("header"),
                                                        self.dict_list_annt_wrkr.get("title"),
                                                        self.dict_list_wrkr_items)
                if itm_slctd == self.dict_list_wrkr_items.get("ants_edt_add"):
                    annt_worker_form.edt_new_annot()
                elif itm_slctd == self.dict_list_wrkr_items.get("bk_add_update_bk"):
                    bk_worker_form.add_new_bk()
                elif itm_slctd == self.dict_list_wrkr_items.get("ants_edt_dlt"):
                    annt_worker_del_form.dlt_annot()
                elif itm_slctd == self.dict_list_wrkr_items.get("bk_dlt"):
                    bk_worker_del_form.dlt_bk()
        elif dropSelectDataApp == self.dict_edit_data_app.get("urlExcel"):
            with tabEditData:
                editSheetForm.select_edit_form_sheet()