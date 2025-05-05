import time
import streamlit as st
from pandasql import sqldf
from bs4 import BeautifulSoup
import requests
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
        "view_srch_sites": "Search sites",
        "view_dredge_pages": "Dredge webpages"
    }

    def webpages_vw_new_entry(self):
        st.session_state.vw_webpages_form_flow = "vw_webpages"

    def videos_vw_new_entry(self):
        st.session_state.vw_videos_form_flow = "vw_videos"

    def sites_vw_new_entry(self):
        st.session_state.vw_sites_form_flow = "vw_sites"

    def webpages_sheet_srch(self):
        st.session_state.webpages_st_srch = "vw_sch_webpages"

    def videos_sheet_srch(self):
        st.session_state.videos_st_srch = "vw_sch_videos"

    def sites_sheet_srch(self):
        st.session_state.sites_st_srch = "vw_sch_sites"

    def webpages_web_dredge(self):
        st.session_state.webpages_web_drdg = "vw_drdg_webpages"

    def webpages_web_dredge_sel_pages(self):
        st.session_state.webpages_web_drdg = "webpages_web_drdg_sel_pages"

    def webpages_web_dredge_sel_results(self):
        st.session_state.webpages_web_drdg = "webpages_web_drdg_sel_results"

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
                            df_srch = sqldf(self.sql_web_pages(st.session_state.webpages_st_srch_str,
                                            self.dict_sql_df.get("web_pages_sheet").get("web_pages")), env=None)
                            row_sum = sqldf(self.sql_web_pages(st.session_state.webpages_st_srch_str,
                                            self.dict_sql_df.get("web_pages_sheet").get("web_pages_count")), env=None)
                        else:
                            df_srch = sqldf(self.sql_web_pages_url(st.session_state.webpages_st_srch_str,
                                            self.dict_sql_df.get("web_pages_sheet").get("web_pages_and_url")), env=None)
                            row_sum = sqldf(self.sql_web_pages_url(st.session_state.webpages_st_srch_str,
                                            self.dict_sql_df.get("web_pages_sheet").get("web_pages_and_url_count")), env=None)
                        if self.write_srch_row_sum(row_sum) != "0":
                            st.header("Sheet rows")
                            st.dataframe(df_srch, hide_index=True,
                                         column_order=(self.dict_book_sheets_spec.get("web_pages").get("desc"),
                                                       self.dict_book_sheets_spec.get("web_pages").get("read"),
                                                       self.dict_book_sheets_spec.get("web_pages").get("url"),
                                                       self.dict_book_sheets_spec.get("web_pages").get("note")),
                                         column_config={
                                             "URL": st.column_config.LinkColumn(
                                                 self.dict_book_sheets_spec.get("web_pages").get("url")),
                                         })

    def select_srch_videos(self):
        if "videos_st_srch" not in st.session_state:
            st.session_state.videos_st_srch = "vw_sch_videos"
        if "go_srch_st_videos" not in st.session_state:
            st.session_state.go_srch_st_videos = False
        if "videos_st_srch_str" not in st.session_state:
            st.session_state.videos_st_srch_str = ""
        if "videos_st_srch_inc_url" not in st.session_state:
            st.session_state.videos_st_srch_inc_url = False
        self.videos_sheet_srch()
        if st.session_state.videos_st_srch == "vw_sch_videos":
            with st.form("Search videos sheet"):
                st.session_state.videos_st_srch_str = st.text_area("Text to search for (separate multiple with comma)",
                                                                     value=st.session_state.videos_st_srch_str)
                st.session_state.videos_st_srch_inc_url = st.checkbox("Search in URLs as well", key="xcel_vw_srch+vds",
                                                                        value=st.session_state.videos_st_srch_inc_url)
                btn_videos_srch_submit = st.form_submit_button("Submit")
                if btn_videos_srch_submit:
                    st.session_state.go_srch_st_videos = True
                    st.rerun()
                elif st.session_state.go_srch_st_videos:
                    if st.session_state.videos_st_srch_str == "":
                        st.markdown(":red[no search text given.]")
                    else:
                        sheet_videos = self.load_book_sheet(self.dict_book_sheets.get("videos"))
                        if not st.session_state.videos_st_srch_inc_url:
                            df_srch = sqldf(self.sql_videos(st.session_state.videos_st_srch_str,
                                            self.dict_sql_df.get("videos_sheet").get("videos")), env=None)
                            row_sum = sqldf(self.sql_videos(st.session_state.videos_st_srch_str,
                                            self.dict_sql_df.get("videos_sheet").get("videos_count")), env=None)
                        else:
                            df_srch = sqldf(self.sql_videos_url(st.session_state.videos_st_srch_str,
                                            self.dict_sql_df.get("videos_sheet").get("videos_and_url")), env=None)
                            row_sum = sqldf(self.sql_videos_url(st.session_state.videos_st_srch_str,
                                            self.dict_sql_df.get("videos_sheet").get("videos_and_url_count")), env=None)
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

    def select_srch_sites(self):
        if "sites_st_srch" not in st.session_state:
            st.session_state.sites_st_srch = "vw_sch_sites"
        if "go_srch_st_sites" not in st.session_state:
            st.session_state.go_srch_st_sites = False
        if "sites_st_srch_str" not in st.session_state:
            st.session_state.sites_st_srch_str = ""
        if "sites_st_srch_inc_url" not in st.session_state:
            st.session_state.sites_st_srch_inc_url = False
        self.sites_sheet_srch()
        if st.session_state.sites_st_srch == "vw_sch_sites":
            with st.form("Search sites sheet"):
                st.session_state.sites_st_srch_str = st.text_area("Text to search for (separate multiple with comma)",
                                                                     value=st.session_state.sites_st_srch_str)
                st.session_state.sites_st_srch_inc_url = st.checkbox("Search in URLs as well", key="xcel_vw_srch+sts",
                                                                        value=st.session_state.sites_st_srch_inc_url)
                btn_sites_srch_submit = st.form_submit_button("Submit")
                if btn_sites_srch_submit:
                    st.session_state.go_srch_st_sites = True
                    st.rerun()
                elif st.session_state.go_srch_st_sites:
                    if st.session_state.sites_st_srch_str == "":
                        st.markdown(":red[no search text given.]")
                    else:
                        sheet_sites = self.load_book_sheet(self.dict_book_sheets.get("sites"))
                        if not st.session_state.sites_st_srch_inc_url:
                            df_srch = sqldf(self.sql_sites(st.session_state.sites_st_srch_str,
                                            self.dict_sql_df.get("sites_sheet").get("sites")), env=None)
                            row_sum = sqldf(self.sql_sites(st.session_state.sites_st_srch_str,
                                            self.dict_sql_df.get("sites_sheet").get("sites_count")), env=None)
                        else:
                            df_srch = sqldf(self.sql_sites_url(st.session_state.sites_st_srch_str,
                                            self.dict_sql_df.get("sites_sheet").get("sites_and_url")), env=None)
                            row_sum = sqldf(self.sql_sites_url(st.session_state.sites_st_srch_str,
                                            self.dict_sql_df.get("sites_sheet").get("sites_and_url_count")), env=None)
                        if self.write_srch_row_sum(row_sum) != "0":
                            st.header("Sheet rows")
                            st.dataframe(df_srch, hide_index=True,
                                         column_order=(self.dict_book_sheets_spec.get("sites").get("desc"),
                                                       self.dict_book_sheets_spec.get("sites").get("url"),),
                                         column_config={
                                             "URL": st.column_config.LinkColumn(
                                                 self.dict_book_sheets_spec.get("sites").get("url")),
                                         })

    def select_drdg_webpages(self):
        if "webpages_web_drdg" not in st.session_state:
            st.session_state.webpages_web_drdg = "vw_drdg_webpages"
        if "web_drdg_srch_str" not in st.session_state:
            st.session_state.web_drdg_srch_str = ""
        if "web_drdg_srch_str_value" not in st.session_state:
            st.session_state.web_drdg_srch_str_value = ""
        if "web_drdg_srch_exclsv_in_row" not in st.session_state:
            st.session_state.web_drdg_srch_exclsv_in_row = False
        if "web_drdg_srch_exclsv_in_row_value" not in st.session_state:
            st.session_state.web_drdg_srch_exclsv_in_row_value = False
        if "rows_selected_dredge" not in st.session_state:
            st.session_state.rows_selected_dredge = None
        if "drdg_sheet_web_pages" not in st.session_state:
            st.session_state.drdg_sheet_web_pages = None
        if "ant_drdg_timeout" not in st.session_state:
            st.session_state.ant_drdg_timeout = None
        if "ant_drdg_distance" not in st.session_state:
            st.session_state.ant_drdg_distance = None
        if st.session_state.webpages_web_drdg == "vw_drdg_webpages":
            with st.form("Dredge internet pages saved"):
                st.session_state.web_drdg_srch_str = st.text_area("Text to search for (separate multiple with comma)",
                                                                  value=st.session_state.web_drdg_srch_str_value)
                btn_drdg_next_1 = st.form_submit_button("Next")
                if btn_drdg_next_1:
                    if st.session_state.web_drdg_srch_str == "":
                        st.markdown(":red[no search text given.]")
                    else:
                        self.webpages_web_dredge_sel_pages()
                        st.session_state.web_drdg_srch_str_value = st.session_state.web_drdg_srch_str
                        st.rerun()
        elif st.session_state.webpages_web_drdg == "webpages_web_drdg_sel_pages":
            with st.form("Dredge internet pages saved - select pages"):
                st.session_state.web_drdg_srch_exclsv_in_row = st.checkbox("""Only search in URLs with a row description containing
                                                                              the search text""",
                                                                           key="xcel_vw_drdg+pgs",
                                                                           value=st.session_state.web_drdg_srch_exclsv_in_row_value)
                st.write("Select web pages to search for :blue[ " + st.session_state.web_drdg_srch_str + "]")
                st.session_state.drdg_sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
                st.session_state.rows_selected_dredge = st.dataframe(st.session_state.drdg_sheet_web_pages,
                                                                     on_select="rerun", selection_mode="multi-row")
                cols_pages_btns = st.columns(2, gap="small", vertical_alignment="center")
                if cols_pages_btns[0].form_submit_button("Start dredge search"):
                    st.session_state.web_drdg_srch_exclsv_in_row_value = st.session_state.web_drdg_srch_exclsv_in_row
                    if len(st.session_state.rows_selected_dredge.selection.rows) == 0:
                        st.markdown(":red[Select at least one row to continue.]")
                    else:
                        self.webpages_web_dredge_sel_results()
                        st.rerun()
                if cols_pages_btns[1].form_submit_button("Back to add search text"):
                    st.session_state.web_drdg_srch_exclsv_in_row = False
                    st.session_state.web_drdg_srch_exclsv_in_row_value = False
                    self.webpages_web_dredge()
                    st.rerun()
        elif st.session_state.webpages_web_drdg == "webpages_web_drdg_sel_results":
            with (st.form("Dredge internet pages saved - result")):
                config_data = self.load_ini_config()
                st.session_state.ant_drdg_timeout = int(config_data.get('dredge', 'response_timeout'))
                st.session_state.ant_drdg_distance = int(config_data.get('dredge', 'result_distance'))
                cols_pages_btns = st.columns(2, gap="small", vertical_alignment="center")
                st.write("Search results for :green[ " + st.session_state.web_drdg_srch_str + "]")
                srch_txts = []
                prog_bar = st.progress(0)
                for r in range(0, len(st.session_state.rows_selected_dredge.selection.rows)):
                    time.sleep(0.1)
                    prog_bar.progress(r / len(st.session_state.rows_selected_dredge.selection.rows),
                                      text="Dredging web pages for search text in progress, " + str(r) +
                                           " of " + str(len(st.session_state.rows_selected_dredge.selection.rows)) +". Please wait...")
                    st.divider()
                    st.write(":orange[" + st.session_state.drdg_sheet_web_pages.iloc[r,
                                                                self.dict_book_sheets_spec.get("web_pages").get("index").get("desc")] + "]")
                    st.write(st.session_state.drdg_sheet_web_pages.iloc[r,
                                                                self.dict_book_sheets_spec.get("web_pages").get("index").get("read")])
                    if str(st.session_state.drdg_sheet_web_pages.iloc[r,
                                                             self.dict_book_sheets_spec.get("web_pages").get("index").get("url")]) \
                                                                == "nan":
                        st.markdown(":red[No URL had been given for this web page (row " + str(r) + ".)]")
                    else:
                        st.write(st.session_state.drdg_sheet_web_pages.iloc[r,
                                                                self.dict_book_sheets_spec.get("web_pages").get("index").get("url")])
                        run_dredge = True
                        srch_txt_lst = self.formatSheetSearchText(st.session_state.web_drdg_srch_str)
                        if st.session_state.web_drdg_srch_exclsv_in_row:
                            for s_tmp in srch_txt_lst:
                                if str(st.session_state.drdg_sheet_web_pages.iloc[r,
                                        self.dict_book_sheets_spec.get("web_pages").get("index").get("desc")]).find(s_tmp) == -1:
                                    st.write(":violet[The search text '" + str(s_tmp) +
                                             "' was not found in the webpage description (You selected to only search for '"
                                             + str(s_tmp) + "' in URLs with a row description containing your search text.)]")
                                else:
                                    srch_txts.append(str(s_tmp))
                            if len(srch_txts) == 0:
                                run_dredge = False
                        if run_dredge:
                            try:
                                html_page = requests.get(st.session_state.drdg_sheet_web_pages.iloc[r,
                                                         self.dict_book_sheets_spec.get("web_pages").get("index").get("url")],
                                                         timeout=st.session_state.ant_drdg_timeout)
                                if str(html_page).find("<Response [404") != -1:
                                    st.markdown(":red[The web page was not found. " + str(html_page) + ".]")
                                elif str(html_page).find("<Response [5") != -1:
                                    st.markdown(":red[Server error (the web page server could not connect. " + str(html_page) + ".]")
                                else:
                                    if str(html_page).find("403") != -1:
                                        st.markdown(""":violet[NOTE the web page requires authorisation (response code 403). ] 
                                                    :red[(The search may not not find matches as an 'access denied' or similar 
                                                    message may be returned instead. A manual visit to the web page amy enable a search.)]""")
                                    text = BeautifulSoup(html_page.text, 'lxml').get_text()
                                    if st.session_state.web_drdg_srch_exclsv_in_row:
                                        srch_txt_lst.clear()
                                        srch_txt_lst = srch_txts
                                    for s_txt in srch_txt_lst:
                                        found_all = 0
                                        txt_bkmrk = 0
                                        drdg_txt = ""
                                        while found_all != -1:
                                            s = str(s_txt)
                                            srch_indx = text.find(s, txt_bkmrk)
                                            if srch_indx != -1:
                                                if srch_indx < st.session_state.ant_drdg_distance:
                                                    start = 0
                                                else:
                                                    start = srch_indx - st.session_state.ant_drdg_distance
                                                drdg_txt = text[start:srch_indx + len(s) + st.session_state.ant_drdg_distance] # no excptn if over end
                                                if (srch_indx + len(s)) <= (len(text) - 1):
                                                    txt_bkmrk  = srch_indx + len(s)
                                                else:
                                                    found_all = srch_indx
                                            else:
                                                found_all = srch_indx
                                            if drdg_txt == "":
                                                st.write(":red[Search text '" + s + "' was not found at this URL.]")
                                            else:
                                                drdg_txt = self.hghlght_txt(drdg_txt, srch_txt_lst)
                                                st.write(":green[Search result.]")
                                                st.write("..." + drdg_txt + "...")
                            except requests.RequestException as e:
                                st.markdown(":rainbow[Error getting web page:] :red[" + str(e) + "]")
                        srch_txt_lst.clear()
                time.sleep(1)
                prog_bar.empty()
                if cols_pages_btns[0].form_submit_button("Done"):
                    st.session_state.web_drdg_srch_str_value = ""
                    st.session_state.web_drdg_srch_str = ""
                    st.session_state.web_drdg_srch_exclsv_in_row = False
                    st.session_state.web_drdg_srch_exclsv_in_row_value = False
                    st.session_state.rows_selected_dredge = None
                    st.session_state.drdg_rows = None
                    self.webpages_web_dredge()
                    st.rerun()
                if cols_pages_btns[1].form_submit_button("Back to select web pages"):
                    self.webpages_web_dredge_sel_pages()
                    st.rerun()

    def write_srch_row_sum(self, row_sum):
        rsum = str(row_sum).split(" ")
        rsum.reverse()  # 2-digit sum will be at different rsum[idx] than 1 digit
        if rsum[0] > "0":
            st.write(":green[Found " + rsum[0] + " rows.]")
        else:
            st.write(":red[Found " + rsum[0] + " rows.]")
        return rsum[0]

    def sql_web_pages(self, search_string, sql_web_pages):
        srch_txt_lst = self.formatSearchText(search_string)
        sql = sql_web_pages
        sql = sql.replace("('{}')", "('{}')".format(str(srch_txt_lst[0])))
        if len(srch_txt_lst) > 1:
            for srchStrs in range(1, len(srch_txt_lst)):
                sql = sql + self.dict_sql_df.get("web_pages_sheet").get(
                    "append_web_pages").format(str(srch_txt_lst[srchStrs]))
        return sql

    def sql_web_pages_url(self, search_string, sql_web_pages):
        srch_txt_lst = self.formatSearchText(search_string)
        sql = sql_web_pages
        sql = sql.replace("('{}')", "('{}')".format(str(srch_txt_lst[0]), str(srch_txt_lst[0])))
        if len(srch_txt_lst) > 1:
            for srchStrs in range(1, len(srch_txt_lst)):
                sql = sql + self.dict_sql_df.get("web_pages_sheet").get(
                    "append_web_pages_and_url").format(str(srch_txt_lst[srchStrs]), str(srch_txt_lst[srchStrs]))
        return sql

    def sql_videos(self, search_string, sql_videos):
        srch_txt_lst = self.formatSearchText(search_string)
        sql = sql_videos
        sql = sql.replace("('{}')", "('{}')".format(str(srch_txt_lst[0])))
        if len(srch_txt_lst) > 1:
            for srchStrs in range(1, len(srch_txt_lst)):
                sql = sql + self.dict_sql_df.get("videos_sheet").get(
                    "append_videos").format(str(srch_txt_lst[srchStrs]))
        return sql

    def sql_videos_url(self, search_string, sql_videos):
        srch_txt_lst = self.formatSearchText(search_string)
        sql = sql_videos
        sql = sql.replace("('{}')", "('{}')".format(str(srch_txt_lst[0]), str(srch_txt_lst[0])))
        if len(srch_txt_lst) > 1:
            for srchStrs in range(1, len(srch_txt_lst)):
                sql = sql + self.dict_sql_df.get("videos_sheet").get(
                    "append_videos_and_url").format(str(srch_txt_lst[srchStrs]), str(srch_txt_lst[srchStrs]))
        return sql

    def sql_sites(self, search_string, sql_sites):
        srch_txt_lst = self.formatSearchText(search_string)
        sql = sql_sites
        sql = sql.replace("('{}')", "('{}')".format(str(srch_txt_lst[0])))
        if len(srch_txt_lst) > 1:
            for srchStrs in range(1, len(srch_txt_lst)):
                sql = sql + self.dict_sql_df.get("sites_sheet").get(
                    "append_sites").format(str(srch_txt_lst[srchStrs]))
        return sql

    def sql_sites_url(self, search_string, sql_sites):
        srch_txt_lst = self.formatSearchText(search_string)
        sql = sql_sites
        sql = sql.replace("('{}')", "('{}')".format(str(srch_txt_lst[0]), str(srch_txt_lst[0])))
        if len(srch_txt_lst) > 1:
            for srchStrs in range(1, len(srch_txt_lst)):
                sql = sql + self.dict_sql_df.get("sites_sheet").get(
                    "append_sites_and_url").format(str(srch_txt_lst[srchStrs]), str(srch_txt_lst[srchStrs]))
        return sql

    dict_sql_df = {
        "web_pages_sheet": {
            "web_pages": '''SELECT * FROM sheet_web_pages WHERE Description LIKE ('{}')''',
            "web_pages_count": '''SELECT COUNT(*) FROM sheet_web_pages WHERE Description LIKE ('{}')''',
            "web_pages_and_url": '''SELECT * FROM sheet_web_pages WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
            "web_pages_and_url_count": '''SELECT COUNT(*) FROM sheet_web_pages WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
            "append_web_pages": ''' OR Description LIKE ('{}')''',
            "append_web_pages_and_url": ''' OR Description LIKE ('{}') OR URL LIKE ('{}')'''
        },
        "videos_sheet": {
            "videos": '''SELECT * FROM sheet_videos WHERE Description LIKE ('{}')''',
            "videos_count": '''SELECT COUNT(*) FROM sheet_videos WHERE Description LIKE ('{}')''',
            "videos_and_url": '''SELECT * FROM sheet_videos WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
            "videos_and_url_count": '''SELECT COUNT(*) FROM sheet_videos WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
            "append_videos": ''' OR Description LIKE ('{}')''',
            "append_videos_and_url": ''' OR Description LIKE ('{}') OR URL LIKE ('{}')'''
        },
        "sites_sheet": {
            "sites": '''SELECT * FROM sheet_sites WHERE Description LIKE ('{}')''',
            "sites_count": '''SELECT COUNT(*) FROM sheet_sites WHERE Description LIKE ('{}')''',
            "sites_and_url": '''SELECT * FROM sheet_sites WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
            "sites_and_url_count": '''SELECT COUNT(*) FROM sheet_sites WHERE Description LIKE ('{}') OR URL LIKE ('{}')''',
            "append_sites": ''' OR Description LIKE ('{}')''',
            "append_sites_and_url": ''' OR Description LIKE ('{}') OR URL LIKE ('{}')'''
        }
    }