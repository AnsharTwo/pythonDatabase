import streamlit as st
from pandasql import sqldf
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
        "view_sites": "View websites",
        "view_srch_pages": "Search webpages",
        "view_srch_videos": "Search videos",
        "view_srch_sites": "Search sites"
    }

    def webpages_vw_new_entry(self):
        st.session_state.vw_webpages_form_flow = "vw_webpages"

    def videos_vw_new_entry(self):
        st.session_state.vw_videos_form_flow = "vw_videos"

    def sites_vw_new_entry(self):
        st.session_state.vw_sites_form_flow = "vw_sites"

    def webpages_sheet_srch(self):
        st.session_state.webpages_st_srch = "vw_sch_webpages"

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
                                                  "URL": st.column_config.LinkColumn(
                                                      self.dict_book_sheets_spec.get("web_pages").get("url")),
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
                                                "URL": st.column_config.LinkColumn(
                                                    self.dict_book_sheets_spec.get("videos").get("url")),
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
                                                  "URL": st.column_config.LinkColumn(
                                                      self.dict_book_sheets_spec.get("sites").get("url")),
                                              })

    def select_srch_webpages(self):
        if "webpages_st_srch" not in st.session_state:
            st.session_state.webpages_st_srch = "vw_sch_webpages"
        if "go_srch_st_webpages" not in st.session_state:
            st.session_state.go_srch_st_webpages = False
        if "webpages_st_srch_str" not in st.session_state:
            st.session_state.webpages_st_srch_str = ""
        if "webpages_st_srch_inc_url" not in st.session_state:
            st.session_state.webpages_st_srch_inc_url = False
        self.webpages_sheet_srch()
        if st.session_state.webpages_st_srch == "vw_sch_webpages":
            with st.form("Search webpages sheet"):
                st.session_state.webpages_st_srch_str = st.text_area("Text to search for (separate multiple with comma)",
                                                                     value=st.session_state.webpages_st_srch_str)
                st.session_state.webpages_st_srch_inc_url = st.checkbox("Search in URLs as well", key="xcel_vw_srch+wbpgs",
                                                                        value=st.session_state.webpages_st_srch_inc_url)
                btn_webpages_srch_submit = st.form_submit_button("Submit")
                if btn_webpages_srch_submit:
                    st.session_state.go_srch_st_webpages = True
                    st.rerun()
                elif st.session_state.go_srch_st_webpages:
                    if st.session_state.webpages_st_srch_str == "":
                        st.markdown(":red[no search text given.]")
                    else:
                        sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
                        if not st.session_state.webpages_st_srch_inc_url:
                            df_srch = sqldf(self.dict_sql_df.get("web_pages").format(
                                                                self.format_sql_wrap(st.session_state.webpages_st_srch_str)),
                                            env=None)
                            row_sum = sqldf(self.dict_sql_df.get("web_pages_count").format(
                                                                self.format_sql_wrap(st.session_state.webpages_st_srch_str)),
                                            env=None)
                        else:
                            df_srch = sqldf(
                                self.dict_sql_df.get("web_pages_and_url").format(self.format_sql_wrap(
                                                                            st.session_state.webpages_st_srch_str),
                                                                                       self.format_sql_wrap(
                                                                            st.session_state.webpages_st_srch_str)),
                                env=None)
                            row_sum = sqldf(self.dict_sql_df.get("web_pages_and_url_count").format(self.format_sql_wrap(
                                                                            st.session_state.webpages_st_srch_str),
                                                                                       self.format_sql_wrap(
                                                                            st.session_state.webpages_st_srch_str)),
                                env=None)
                        if self.write_srch_row_sum(row_sum) != "0":
                            st.header("Sheet rows")
                            st.dataframe(df_srch, hide_index=True,
                                         column_order=(self.dict_book_sheets_spec.get("videos").get("desc"),
                                                       self.dict_book_sheets_spec.get("videos").get("read"),
                                                       self.dict_book_sheets_spec.get("videos").get("url"),
                                                       self.dict_book_sheets_spec.get("videos").get("note")),
                                         column_config={
                                             "URL": st.column_config.LinkColumn(
                                                 self.dict_book_sheets_spec.get("videos").get("url")),
                                         })

    def select_srch_videos(self):
        st.write("Under construction - videos")

    def select_srch_sites(self):
        st.write("Under construction - sites")

    def write_srch_row_sum(self, row_sum):
        rsum = str(row_sum).split(" ")
        rsum.reverse()  # 2-digit sum will be at different rsum[idx] than 1 digit
        if rsum[0] > "0":
            st.write(":green[Found " + rsum[0] + " rows.]")
        else:
            st.write(":red[Found " + rsum[0] + " rows.]")
        return rsum[0]

    dict_sql_df = {
        "web_pages": '''SELECT * FROM sheet_web_pages WHERE Description LIKE ('{}')''',
        "web_pages_count": '''SELECT COUNT(*) FROM sheet_web_pages WHERE Description LIKE ('{}')''',
        "web_pages_and_url": '''SELECT * FROM sheet_web_pages WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
        "web_pages_and_url_count": '''SELECT COUNT(*) FROM sheet_web_pages WHERE Description LIKE ('{}') OR URL LIKE ('{}')'''
    }