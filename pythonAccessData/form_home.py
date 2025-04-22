import form_sr
import form_view
import form_sheet
import form_bk
import form_annt
import form_sheet_edit
import form_settings
import form_profile

class HOME_FORM (form_sr.FORM):

    def __init__(self, authenticator):
        super().__init__()
        self.auth = authenticator

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
    def select_view_st(self):
        sheetForm = form_sheet.SHEET_FORM()
        itm_slctd = self.select_edit_form(sheetForm.dict_view_sheet.get("header"),
                                          sheetForm.dict_view_sheet.get("title"),
                                          sheetForm.dict_book_sheets_view)
        if itm_slctd == sheetForm.dict_book_sheets_view.get("view_web_pages"):
            sheetForm.select_vw_sht_webpages()
        elif itm_slctd == sheetForm.dict_book_sheets_view.get("view_videos"):
            sheetForm.select_vw_sht_videos()
        elif itm_slctd == sheetForm.dict_book_sheets_view.get("view_sites"):
            sheetForm.select_vw_sht_sites()
        elif itm_slctd == sheetForm.dict_book_sheets_view.get("view_srch_pages"):
            sheetForm.select_srch_webpages()
        elif itm_slctd == sheetForm.dict_book_sheets_view.get("view_srch_videos"):
            sheetForm.select_srch_videos()
        elif itm_slctd == sheetForm.dict_book_sheets_view.get("view_srch_sites"):
            sheetForm.select_srch_sites(),
        elif itm_slctd == sheetForm.dict_book_sheets_view.get("view_dredge_pages"):
            sheetForm.select_drdg_webpages(),

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
        itm_slctd = self.select_edit_form(editSheetForm.dict_edit_sheet_do.get("header"),
                                          editSheetForm.dict_edit_sheet_do.get("title"),
                                          editSheetForm.dict_book_sheets_edt)
        if itm_slctd == editSheetForm.dict_book_sheets_edt.get("do_web_pages"):
            editSheetForm.select_edt_sht_webpages()
        elif itm_slctd == editSheetForm.dict_book_sheets_edt.get("do_videos"):
            editSheetForm.select_edt_sht_videos()
        elif itm_slctd == editSheetForm.dict_book_sheets_edt.get("do_sites"):
            editSheetForm.select_edt_sht_sites()

    def select_sttngs(self):
        configForm = form_settings.CONFIG_FORM()
        configForm.edt_sttngs()

    def select_prfl(self):
        profForm = form_profile.PROF_FORM(self.auth)
        profForm.edt_prfl()