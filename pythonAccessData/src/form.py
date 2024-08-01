import sys
import streamlit as st

import db

class DATA_FORM:

    # def __init__(self):


    def init_sidebar(self):
        annotDb = "Annotations database"
        urlExcel = "Excel URLs sheets"

        st.sidebar.title("Annotations and URL manager")
        form = st.sidebar.selectbox("Select to do", [annotDb, urlExcel])
        if form == annotDb:
            self.select_search()
        elif form == urlExcel:
            self.select_url_search()

    def select_search(self):
        with st.form("Search"):
            st.header("Select search")
            searchSelection = st.selectbox("Select search type",[
                "---",
                "Annotations by search text",
                "Annotations by search text and author",
                "Annotations by search text and book",
                "Annotations by book",
                "Annotations by Author",
                "All books",
                "Books by year read",
                "All annotations",
                "Annotations by year/s read"
            ])
            gone = st.form_submit_button("Go")
            if gone:
                if searchSelection == self.dict_searches.get("ants_srch_txt"):
                    self.srch_searchtext()

    def srch_searchtext(self):
        txt = st.text_area("Annotated text to search for (separate multiple with comma)")
        searched = st.form_submit_button("Search")
        if searched:
            st.write("I sent it")
            self.db_records(self.dict_Searches.get("ants_srch_txt"), txt, "")

    def select_url_search(self):
        st.write("Page is pending, under construction")

    def db_records(self, searchSelection, searchText, auth):
        dbPath = sys.argv[1] + sys.argv[2]

        sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % dbPath)
        sourceData.is_ms_access_driver()
        conn = sourceData.db_connect()
        sourceData.report_tables(conn.cursor())

        st.header("Database Records")

        if searchSelection == self.dict_searches.get("ants_srch_txt"):
            resCountSearchString = sourceData.resAnnotsbySearchString(conn.cursor(), searchText)
            annots = sourceData.selectAnnotsbySearchString(conn.cursor(), searchText)
            st.write("Found {} results.".format(resCountSearchString))
            for ant in annots:
                st.write(
                    f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")
        elif searchSelection == self.dict_searches.get("ants_srch_txt_auth"):
            resCountSrchStrAndAuthor = sourceData.resAnnotsbySrchStrAndAuthor(conn.cursor(), searchText, auth)
            annots = sourceData.selectAnnotsbySrchStrAndAuthor(conn.cursor(),  searchText, auth)

            st.write("Found {} results.".format(resCountSrchStrAndAuthor))
            for ant in annots:
                st.write(
                    f"{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

        conn.close()

    dict_searches = {
        "ants_srch_txt": "Annotations by search text",
        "ants_srch_txt_auth": "Annotations by search text and author"
    }