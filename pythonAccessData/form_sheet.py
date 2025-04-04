import streamlit as st
import form_sr

class SHEET_FORM(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_view_sheet = {
        "header": "Select view sheet search",
        "title": "Select view sheet search type"
    }

    dict_book_sheets_view = {
        "none": "none",
        "view_web_pages": "View webpages",
        "view_videos": "View videos",
        "view_sites": "View websites"
    }

    def webpages_vw_new_entry(self):
        st.session_state.vw_webpages_form_flow = "vw_webpages"

    def videos_vw_new_entry(self):
        st.session_state.vw_videos_form_flow = "vw_videos"

    def sites_vw_new_entry(self):
        st.session_state.vw_sites_form_flow = "vw_sites"

    def select_vw_sht_webpages(self):
        if "vw_webpages_form_flow" not in st.session_state:
            st.session_state.vw_webpages_form_flow = "vw_webpages"
        self.webpages_vw_new_entry()
        if st.session_state.vw_webpages_form_flow == "vw_webpages":
            sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
            st.dataframe(sheet_web_pages, hide_index=True,
                                            column_order=(
                                                          self.dict_book_sheets_spec.get("web_pages").get("desc"),
                                                          self.dict_book_sheets_spec.get("web_pages").get("read"),
                                                          self.dict_book_sheets_spec.get("web_pages").get("url"),
                                                          self.dict_book_sheets_spec.get("web_pages").get("note")),
                                            column_config={
                                                  "_index": st.column_config.NumberColumn("Index",
                                                                                          required=True,
                                                                                          disabled=False),
                                                  "URL": st.column_config.LinkColumn(
                                                      self.dict_book_sheets_spec.get("web_pages").get("url")),
                                                  "Read": st.column_config.SelectboxColumn(
                                                      default=self.dict_sheets_cll_clr.get("is_read").get(
                                                          "cll_unread"),
                                                      options=[self.dict_sheets_cll_clr.get("is_read").get(
                                                          "cll_read"),
                                                               self.dict_sheets_cll_clr.get("is_read").get(
                                                                   "cll_unread")],
                                                      required=True),
                                                  "Note": st.column_config.TextColumn(max_chars=25)
                                              })

    def select_vw_sht_videos(self):
        if "vw_videos_form_flow" not in st.session_state:
            st.session_state.vw_videos_form_flow = "vw_videos"
        self.videos_vw_new_entry()
        if st.session_state.vw_videos_form_flow == "vw_videos":
            sheet_videos = self.load_book_sheet(self.dict_book_sheets.get("videos"))
            st.dataframe(sheet_videos, hide_index=False,
                                          column_order=(self.dict_book_sheets_spec.get("videos").get("desc"),
                                                        self.dict_book_sheets_spec.get("videos").get("read"),
                                                        self.dict_book_sheets_spec.get("videos").get("url"),
                                                        self.dict_book_sheets_spec.get("videos").get("note")),
                                          column_config={
                                                "_index": st.column_config.NumberColumn("Index", required=True,
                                                                                        disabled=False),
                                                "URL": st.column_config.LinkColumn(
                                                    self.dict_book_sheets_spec.get("videos").get("url")),
                                                "Read": st.column_config.SelectboxColumn(
                                                    default=self.dict_sheets_cll_clr.get("is_read").get(
                                                        "cll_unread"),
                                                    options=[
                                                        self.dict_sheets_cll_clr.get("is_read").get("cll_read"),
                                                        self.dict_sheets_cll_clr.get("is_read").get(
                                                            "cll_unread")],
                                                    required=True),
                                                "Note": st.column_config.TextColumn(max_chars=25)
                                            })

    def select_vw_sht_sites(self):
        if "vw_sites_form_flow" not in st.session_state:
            st.session_state.vw_sites_form_flow = "vw_sites"
        self.sites_vw_new_entry()
        if st.session_state.vw_sites_form_flow == "vw_sites":
            sheet_sites = self.load_book_sheet(self.dict_book_sheets.get("sites"))
            st.dataframe(sheet_sites, hide_index=True,
                                            column_order=(self.dict_book_sheets_spec.get("sites").get("desc"),
                                                            self.dict_book_sheets_spec.get("sites").get("url")),
                                            column_config={
                                                  "_index": st.column_config.NumberColumn("Index",
                                                                                          required=True,
                                                                                          disabled=False),
                                                  "URL": st.column_config.LinkColumn(
                                                      self.dict_book_sheets_spec.get("sites").get("url")),
                                              })