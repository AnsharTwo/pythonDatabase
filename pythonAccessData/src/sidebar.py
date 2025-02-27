import streamlit as st
import form_sr
import form_view
import form_sheet
import form_bk
import form_annt
import form_sheet_edit

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
        "Edit": "Do"
    }

    def init_sidebars(self):
        db_viewer = form_view.DATA_FORM()
        annt_worker_form = form_annt.EDIT_ANNOT()
        bk_worker_form = form_bk.EDIT_BOOK()
        sheetForm = form_sheet.SHEET_FORM()
        editSheetForm = form_sheet_edit.EDIT_SHEET_FORM()
        tabViewData, tabEditData = st.tabs([self.dict_tabh_drs.get("Read"), self.dict_tabh_drs.get("Edit")])
        st.sidebar.write(":green[Welcome, {}!]".format(self.user))
        dropSelectApp = st.sidebar.selectbox("Select to view", [self.dict_data_app.get("annotDb"),
                                                                self.dict_data_app.get("urlExcel"), "None"])
        if dropSelectApp == self.dict_data_app.get("annotDb"):
            with tabViewData:
                itm_slctd = self.select_edit_form(db_viewer.dict_List_view.get("header"),
                                                        db_viewer.dict_List_view.get("title"),
                                                        db_viewer.dict_searches)
                if itm_slctd == db_viewer.dict_searches.get("ants_srch_txt"):
                    db_viewer.srch_searchtext()
                elif itm_slctd == db_viewer.dict_searches.get("ants_srch_txt_auth"):
                    db_viewer.srch_searchtext_auth()
                elif itm_slctd == db_viewer.dict_searches.get("ants_srch_txt_bk"):
                    db_viewer.srch_searchtext_bk()
                elif itm_slctd == db_viewer.dict_searches.get("ants_bk"):
                    db_viewer.srch_bk()
                elif itm_slctd == db_viewer.dict_searches.get("ants_auth"):
                    db_viewer.srch_auth()
                elif itm_slctd == db_viewer.dict_searches.get("bks_auth"):
                    db_viewer.bks_auth()
                elif itm_slctd == db_viewer.dict_searches.get("bks_all"):
                    db_viewer.bks_all()
                elif itm_slctd == db_viewer.dict_searches.get("bks_yr_read"):
                    db_viewer.bks_yr_read()
                elif itm_slctd == db_viewer.dict_searches.get("ants_all"):
                    db_viewer.ants_all()
                elif itm_slctd == db_viewer.dict_searches.get("ants_yr_read"):
                    db_viewer.ants_yr_read()
        elif dropSelectApp == self.dict_data_app.get("urlExcel"):
            with tabViewData:
                sheetForm.select_url_search()
        dropSelectDataApp = st.sidebar.selectbox("Select to do", [self.dict_edit_data_app.get("annotDb"),
                                                                  self.dict_edit_data_app.get("urlExcel"),"None"])
        if dropSelectDataApp == self.dict_edit_data_app.get("annotDb"):
            with (tabEditData):
                itm_slctd = self.select_edit_form(self.dict_list_annt_wrkr.get("header"),
                                                        self.dict_list_annt_wrkr.get("title"),
                                                        self.dict_list_wrkr_items)
                if itm_slctd == self.dict_list_wrkr_items.get("ants_edt_add"):
                    annt_worker_form.edt_new_annot()
                elif itm_slctd == self.dict_list_wrkr_items.get("bk_add_update_bk"):
                    bk_worker_form.add_new_bk()
        elif dropSelectDataApp == self.dict_edit_data_app.get("urlExcel"):
            with tabEditData:
                editSheetForm.select_edit_form_sheet()
        st.sidebar.divider()
        cl = st.sidebar.columns(2,gap="small", vertical_alignment="center")
        cl[0].write("Settings")
        cl[1].link_button("", f"http://localhost:8501/Settings", icon=":material/settings:", type="secondary", use_container_width=True)
        st.sidebar.divider()