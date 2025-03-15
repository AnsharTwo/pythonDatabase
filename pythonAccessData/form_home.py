import form_sr
import form_view
import form_sheet
import form_bk
import form_annt
import form_sheet_edit
import form_settings

class HOME_FORM (form_sr.FORM):

    def __init__(self):
        super().__init__()

    def select_view_ant(self):
        db_viewer = form_view.DATA_FORM()
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
    def select_view_st(selfself):
        sheetForm = form_sheet.SHEET_FORM()
        sheetForm.select_url_search()

    def select_do_ant(self):
        annt_worker_form = form_annt.EDIT_ANNOT()
        bk_worker_form = form_bk.EDIT_BOOK()
        itm_slctd = self.select_edit_form(self.dict_list_annt_wrkr.get("header"),
                                          self.dict_list_annt_wrkr.get("title"),
                                          self.dict_list_wrkr_items)
        if itm_slctd == self.dict_list_wrkr_items.get("ants_edt_add"):
            annt_worker_form.edt_new_annot()
        elif itm_slctd == self.dict_list_wrkr_items.get("bk_add_update_bk"):
            bk_worker_form.add_new_bk()

    def select_do_st(self):
        editSheetForm = form_sheet_edit.EDIT_SHEET_FORM()
        editSheetForm.select_edit_form_sheet()

    def select_sttngs(self):
        configForm = form_settings.CONFIG_FORM()
        configForm.edt_sttngs()