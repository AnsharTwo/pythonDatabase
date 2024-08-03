import sys
import streamlit as st
from tornado import auth

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
            st.form_submit_button("Go")
            if searchSelection == self.dict_searches.get("ants_srch_txt"):
                self.srch_searchtext()
            elif searchSelection == self.dict_searches.get("ants_srch_txt_auth"):
                self.srch_searchtext_auth()
            elif searchSelection == self.dict_searches.get("ants_srch_txt_bk"):
                self.srch_searchtext_bk()
            elif searchSelection == self.dict_searches.get("ants_bk"):
                self.srch_bk()

    def srch_searchtext(self):
        txt = st.text_area("Annotated text to search for (separate multiple with comma)")
        searched = st.form_submit_button("Search")
        if searched:
            if txt == "":
                st.markdown(":red[no search text given.]")
            else:
                self.db_records(self.dict_searches.get("ants_srch_txt"), txt, "", "")

    def srch_searchtext_auth(self):
        txt = st.text_area("Annotated text to search for (separate multiple with comma)")
        author = st.text_input("Author")
        searched = st.form_submit_button("Search")
        if searched:
            if txt == "":
                st.markdown(":red[no search text given.]")
            else:
                if author == "":
                    st.markdown(":red[no author given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_srch_txt_auth"), txt, author, "")

    def srch_searchtext_bk(self):
        txt = st.text_area("Annotated text to search for (separate multiple with comma)")
        book = st.text_input("Book")
        searched = st.form_submit_button("Search")
        if searched:
            if txt == "":
                st.markdown(":red[no search text given.]")
            else:
                if book == "":
                    st.markdown(":red[no book given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_srch_txt_bk"), txt, "", book)

    def srch_bk(self):
        book = st.text_input("Book")
        searched = st.form_submit_button("Search")
        if searched:
            if book == "":
                st.markdown(":red[no book given.]")
            else:
                self.db_records(self.dict_searches.get("ants_bk"), "", "", book)

    def select_url_search(self):
        st.write("Page is pending, under construction")

    def db_records(self, searchSelection, searchText, auth, bk):
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

        elif searchSelection == self.dict_searches.get("ants_srch_txt_bk"):
            resCountSrchStrAndBook = sourceData.resAnnotsbySrchStrAndBook(conn.cursor(), searchText, bk)
            annots = sourceData.selectAnnotsbySrchStrAndBook(conn.cursor(), searchText, bk)
            st.write("Found {} results.".format(resCountSrchStrAndBook))
            for ant in annots:
                st.write(f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

        elif searchSelection == self.dict_searches.get("ants_bk"):
            # use \'' if single quote is in e.g. hitler's
            resCountBooks = sourceData.resAnnotsbyBook(conn.cursor(), bk)
            annots = sourceData.selectAnnotsbyBook(conn.cursor(), bk)
            st.write("Found {} results.".format(resCountBooks))
            st.write(bk)
            for ant in annots:
                st.write(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

        conn.close()

    dict_searches = {
        "ants_srch_txt": "Annotations by search text",
        "ants_srch_txt_auth": "Annotations by search text and author",
        "ants_srch_txt_bk": "Annotations by search text and book",
        "ants_bk": "Annotations by book"
    }