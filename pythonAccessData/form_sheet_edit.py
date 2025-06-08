import streamlit as st#
import form_sr

class EDIT_SHEET_FORM(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_edit_sheet_do = {
        "header": "Select sheet search",
        "title": "Select sheet search type"
    }

    dict_book_sheets_edt = {
        "none": "none",
        "do_web_pages": "Create, edit or delete a webpage entry",
        "do_videos": "Create, edit or delete a video entry",
        "do_sites": "Create, edit or delete a website entry"
    }

    def webpages_do_new_entry(self):
        st.session_state.do_webpages_form_flow = "do_webpages"

    def videos_do_new_entry(self):
        st.session_state.do_videos_form_flow = "do_videos"

    def sites_do_new_entry(self):
        st.session_state.do_sites_form_flow = "do_sites"

    def select_edt_sht_webpages(self):
        if "do_webpages_form_flow" not in st.session_state:
            st.session_state.do_webpages_form_flow = "do_webpages"
        self.webpages_do_new_entry()
        if st.session_state.do_webpages_form_flow == "do_webpages":
            with st.form("Edit web pages"):
                try:
                    sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
                    sheet_videos = self.load_book_sheet(self.dict_book_sheets.get("videos"))
                    sheet_sites = self.load_book_sheet(self.dict_book_sheets.get("sites"))
                except Exception as ex:
                    st.write(":red[" + self.dict_err_msgs.get("cursor_exec") + "]")
                    st.write(str(ex))
                    st.form_submit_button(str(self.dict_err_msgs.get("form_no_display")), disabled=True)
                else:
                    sheet_web_pages[self.dict_book_sheets_spec.get("web_pages").get("page_no")] = range(1,
                                                                                                    len(sheet_web_pages) + 1)
                    edit_sheet_wbpgs = st.data_editor(sheet_web_pages, hide_index=True, num_rows="dynamic",
                                                      column_order=(self.dict_book_sheets_spec.get("web_pages").get("page_no"),
                                                                    self.dict_book_sheets_spec.get("web_pages").get("desc"),
                                                                    self.dict_book_sheets_spec.get("web_pages").get("read"),
                                                                    self.dict_book_sheets_spec.get("web_pages").get("url"),
                                                                    self.dict_book_sheets_spec.get("web_pages").get("note")),
                                                      column_config={
                                                        self.dict_book_sheets_spec.get("web_pages").get("url"): \
                                                            st.column_config.LinkColumn(self.dict_book_sheets_spec.get("web_pages").get("url")),
                                                        self.dict_book_sheets_spec.get("web_pages").get("page_no"): \
                                                            st.column_config.NumberColumn(disabled=True),
                                                        self.dict_book_sheets_spec.get("web_pages").get("read"): \
                                                            st.column_config.SelectboxColumn(
                                                                            default=self.dict_sheets_cll_clr.get("is_read").get("cll_unread"),
                                                                            options=[self.dict_sheets_cll_clr.get("is_read").get("cll_read"),
                                                                                     self.dict_sheets_cll_clr.get("is_read").get("cll_unread")],
                                                                            required=True),
                                                        self.dict_book_sheets_spec.get("web_pages").get("note"): \
                                                            st.column_config.TextColumn(max_chars=250)
                                                      })
                    btn_apply_webpages = st.form_submit_button("Apply web pages")
                    if btn_apply_webpages:
                        try:
                            self.load_book_sheet.clear()
                            self.write_book_sheet(edit_sheet_wbpgs, sheet_videos, sheet_sites)
                            st.rerun()
                        except Exception as ex:
                            st.write(":red[" + self.dict_err_msgs.get("cursor_exec") + "]")
                            st.write(str(ex))
                            st.form_submit_button(str(self.dict_err_msgs.get("form_no_display")), disabled=True)

    def select_edt_sht_videos(self):
        if "do_videos_form_flow" not in st.session_state:
            st.session_state.do_videos_form_flow = "do_videos"
        self.videos_do_new_entry()
        if st.session_state.do_videos_form_flow == "do_videos":
            with st.form("Edit videos"):
                try:
                    sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
                    sheet_videos = self.load_book_sheet(self.dict_book_sheets.get("videos"))
                    sheet_sites = self.load_book_sheet(self.dict_book_sheets.get("sites"))
                except Exception as ex:
                    st.write(":red[" + self.dict_err_msgs.get("cursor_exec") + "]")
                    st.write(str(ex))
                    st.form_submit_button(str(self.dict_err_msgs.get("form_no_display")), disabled=True)
                else:
                    sheet_videos[self.dict_book_sheets_spec.get("videos").get("video_no")] = range(1, len(sheet_videos) + 1)
                    edit_sheet_vds = st.data_editor(sheet_videos, hide_index=True, num_rows="dynamic",
                                                      column_order=(self.dict_book_sheets_spec.get("videos").get("video_no"),
                                                                    self.dict_book_sheets_spec.get("videos").get("desc"),
                                                                    self.dict_book_sheets_spec.get("videos").get("watched"),
                                                                    self.dict_book_sheets_spec.get("videos").get("url"),
                                                                    self.dict_book_sheets_spec.get("videos").get("note")),
                                                      column_config={
                                                        self.dict_book_sheets_spec.get("videos").get("video_no") : \
                                                            st.column_config.NumberColumn(disabled=True),
                                                        self.dict_book_sheets_spec.get("videos").get("url") \
                                                            : st.column_config.LinkColumn(self.dict_book_sheets_spec.get("videos").get("url")),
                                                        self.dict_book_sheets_spec.get("videos").get("watched"): \
                                                            st.column_config.SelectboxColumn(
                                                                            default=self.dict_sheets_cll_clr.get("is_read").get("cll_unread"),
                                                                            options=[self.dict_sheets_cll_clr.get("is_read").get("cll_read"),
                                                                                     self.dict_sheets_cll_clr.get("is_read").get("cll_unread")],
                                                                            required=True),
                                                        self.dict_book_sheets_spec.get("videos").get("note"): \
                                                            st.column_config.Column()
                                                      })
                    btn_apply_webpages = st.form_submit_button("Apply videos")
                    if btn_apply_webpages:
                        try:
                            self.load_book_sheet.clear()
                            self.write_book_sheet(sheet_web_pages, edit_sheet_vds, sheet_sites)
                            st.rerun()
                        except Exception as ex:
                            st.write(":red[" + self.dict_err_msgs.get("cursor_exec") + "]")
                            st.write(str(ex))
                            st.form_submit_button(str(self.dict_err_msgs.get("form_no_display")), disabled=True)

    def select_edt_sht_sites(self):
        if "do_sites_form_flow" not in st.session_state:
            st.session_state.do_sites_form_flow = "do_sites"
        self.sites_do_new_entry()
        if st.session_state.do_sites_form_flow == "do_sites":
            with st.form("Edit sites"):
                try:
                    sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
                    sheet_videos = self.load_book_sheet(self.dict_book_sheets.get("videos"))
                    sheet_sites = self.load_book_sheet(self.dict_book_sheets.get("sites"))
                except Exception as ex:
                    st.write(":red[" + self.dict_err_msgs.get("cursor_exec") + "]")
                    st.write(str(ex))
                    st.form_submit_button(str(self.dict_err_msgs.get("form_no_display")), disabled=True)
                else:
                    sheet_sites[self.dict_book_sheets_spec.get("sites").get("site_no")] = range(1, len(sheet_sites) + 1)
                    edit_sheet_sites = st.data_editor(sheet_sites, hide_index=True, num_rows="dynamic",
                                                      column_order=(self.dict_book_sheets_spec.get("sites").get("site_no"),
                                                                    self.dict_book_sheets_spec.get("sites").get("desc"),
                                                                    self.dict_book_sheets_spec.get("sites").get("url")),
                                                      column_config={
                                                        self.dict_book_sheets_spec.get("sites").get("site_no"): \
                                                            st.column_config.NumberColumn(disabled=True),
                                                        self.dict_book_sheets_spec.get("sites").get("url"): \
                                                            st.column_config.LinkColumn(self.dict_book_sheets_spec.get("sites").get("url")),
                                                         })
                    btn_apply_webpages = st.form_submit_button("Apply sites")
                    if btn_apply_webpages:
                        try:
                            self.load_book_sheet.clear()
                            self.write_book_sheet(sheet_web_pages, sheet_videos, edit_sheet_sites)
                            st.rerun()
                        except Exception as ex:
                            st.write(":red[" + self.dict_err_msgs.get("cursor_exec") + "]")
                            st.write(str(ex))
                            st.form_submit_button(str(self.dict_err_msgs.get("form_no_display")), disabled=True)