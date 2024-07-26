import sys
import streamlit as st

import db

class DATA_FORM:

    # def __init__(self):

    def select_search(self):
        with st.form("Select search type"):
            st.header("Select search type")
            st.selectbox("How was your experience learning about Streamlit?", ["---", "Good", "Neutral", "Bad"])
            st.select_slider("How would you rate the article",
                             ["Very Poor", "Poor", "As Expected", "Easy to follow", "Excellent"], value="As Expected")
            st.text_area("Any other comments?")
            st.text("Thank you for your time!")
            st.form_submit_button("Submit")

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