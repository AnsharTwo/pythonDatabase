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
        with st.form("Select search type"):
            st.header("Select search type")
            st.selectbox("Select search type", ["---",
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
            st.text_area("Annotated text to search for (separate multiple with comma)")
            st.form_submit_button("Submit")

    def select_url_search(self):
        st.write("Page is pending, under construction")

    def db_records(self):
        dbPath = sys.argv[1] + sys.argv[2]

        sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % dbPath)
        sourceData.is_ms_access_driver()
        conn = sourceData.db_connect()
        sourceData.report_tables(conn.cursor())

        st.header("Database Records")

        # resCountBooksAll = sourceData.resBooksAll(conn.cursor())
        # books = sourceData.selectBooksAll(conn.cursor())
        # st.write("Found {} results.".format(resCountBooksAll))
        # for bk in books:
        #    st.write(f"{bk.__getattribute__('Book No')}\t{bk.__getattribute__('Book Title')}\t{bk.Author}")

        resCountSearchString = sourceData.resAnnotsbySearchString(conn.cursor(),
                                       '%Ayn Rand%')
        annots = sourceData.selectAnnotsbySearchString(conn.cursor(),
                                       '%Ayn Rand%')
        st.write("Found {} results.".format(resCountSearchString))
        for ant in annots:
            st.write(
                f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

        conn.close()