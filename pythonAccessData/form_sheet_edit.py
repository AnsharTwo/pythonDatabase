import streamlit as st
import pandas as pd
import form_sr

class EDIT_SHEET_FORM(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_edit_sheet_do = {
        "header": "Select sheet search",
        "title": "Select search type"
    }

    dict_book_sheets_edt = {
        "none": "none",
        "do_web_pages": "Create, edit or delete a webpage entry",
        "do_videos": "Create, edit or delete a video entry",
        "do_sites": "Create, edit or delete a website entry"
    }

    def webpages_do_new_entry(self):
        st.session_state.do_webpages_form_flow = "do_webpages"

    def select_edt_sht_webpages(self):
        if "do_webpages" not in st.session_state:
            st.session_state.do_webpages_form_flow = "do_webpages"
        self.webpages_do_new_entry()
        if st.session_state.do_webpages_form_flow == "do_webpages":
            sheet_web_pages = self.load_book_sheet(self.dict_book_sheets.get("web_pages"))
            st.write("Contents of 'pages':\n", sheet_web_pages)

    def select_edt_sht_videos(self):
        sheet_videos = self.load_book_sheet(self.dict_book_sheets.get("videos"))
        st.write("Contents of 'pages':\n", sheet_videos)

    def select_edt_sht_sites(self):
        sheet_sites = self.load_book_sheet(self.dict_book_sheets.get("sites"))
        st.write("Contents of 'pages':\n", sheet_sites)