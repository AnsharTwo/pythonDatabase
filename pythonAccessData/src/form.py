import sys
from datetime import datetime, date

import pandas as pd
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
                "Annotations by author",
                "Books by author",
                "All books",
                "Books by year read",
                "All annotations",
                "Annotations by year read"
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
            elif searchSelection == self.dict_searches.get("ants_auth"):
                self.srch_auth()
            elif searchSelection == self.dict_searches.get("bks_auth"):
                self.bks_auth()
            elif searchSelection == self.dict_searches.get("bks_all"):
                self.bks_all()
            elif searchSelection == self.dict_searches.get("bks_yr_read"):
                self.bks_yr_read()
            elif searchSelection == self.dict_searches.get("ants_all"):
                self.ants_all()
            elif searchSelection == self.dict_searches.get("ants_yr_read"):
                self.ants_yr_read()

    def srch_searchtext(self):
        txt = st.text_area("Annotated text to search for (separate multiple with comma)")
        searched = st.form_submit_button("Search")
        if searched:
            if txt == "":
                st.markdown(":red[no search text given.]")
            else:
                self.db_records(self.dict_searches.get("ants_srch_txt"), txt, "", "", "", "")

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
                    self.db_records(self.dict_searches.get("ants_srch_txt_auth"), txt, author, "", "", "")

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
                    self.db_records(self.dict_searches.get("ants_srch_txt_bk"), txt, "", book, "", "")

    def srch_bk(self):
        book = st.text_input("Book")
        searched = st.form_submit_button("Search")
        if searched:
            if book == "":
                st.markdown(":red[no book given.]")
            else:
                self.db_records(self.dict_searches.get("ants_bk"), "", "", book, "", "")

    def srch_auth(self):
        author = st.text_input("Author")
        searched = st.form_submit_button("Search")
        if searched:
            if author == "":
                st.markdown(":red[no author given.]")
            else:
                self.db_records(self.dict_searches.get("ants_auth"), "", author, "", "", "")

    def bks_auth(self):
        author = st.text_input("Author")
        searched = st.form_submit_button("Search")
        if searched:
            if author == "":
                st.markdown(":red[no author given.]")
            else:
                self.db_records(self.dict_searches.get("bks_auth"), "", author, "", "", "")

    def bks_all(self):
        searched = st.form_submit_button("Search")
        if searched:
            self.db_records(self.dict_searches.get("bks_all"), "", "", "", "", "")

    def bks_yr_read(self):
        yearFrom = st.text_input("From year (yyyy)")
        yearTo = st.text_input("To year (yyyy)")
        searched = st.form_submit_button("Search")
        if searched:
            if yearFrom == "":
                st.markdown(":red[no start year given.]")
            else:
                if yearTo == "":
                    st.markdown(":red[no end year given.]")
                else:
                    if not self.__isValidYearFormat(yearFrom, "%Y"):
                        st.markdown(":red[From year is not in format yyyy.]")
                    else:
                        if not self.__isValidYearFormat(yearTo, "%Y"):
                            st.markdown(":red[To year is not in format yyyy.]")
                        else:
                            if date(int(yearFrom), 1, 1) > date(int(yearTo), 1, 1):
                                st.markdown(":red[From year cannot be greater than To year.]")
                            else:
                                self.db_records(self.dict_searches.get("bks_yr_read"), "", "", "", yearFrom, yearTo)

    def ants_all(self):
        st.write("NOTE: page may be slow to load searching on all annotations...")
        searched = st.form_submit_button("Search")
        if searched:
            self.db_records(self.dict_searches.get("ants_all"), "", "", "", "", "")

    def ants_yr_read(self):
        yearFrom = st.text_input("From year (yyyy)")
        yearTo = st.text_input("To year (yyyy)")
        searched = st.form_submit_button("Search")
        if searched:
            if yearFrom == "":
                st.markdown(":red[no start year given.]")
            else:
                if yearTo == "":
                    st.markdown(":red[no end year given.]")
                else:
                    if not self.__isValidYearFormat(yearFrom, "%Y"):
                        st.markdown(":red[From year is not in format yyyy.]")
                    else:
                        if not self.__isValidYearFormat(yearTo, "%Y"):
                            st.markdown(":red[To year is not in format yyyy.]")
                        else:
                            if date(int(yearFrom), 1, 1) > date(int(yearTo), 1, 1):
                                st.markdown(":red[From year cannot be greater than To year.]")
                            else:
                                self.db_records(self.dict_searches.get("ants_yr_read"), "", "", "", yearFrom, yearTo)

    def select_url_search(self):
        st.write("Page is pending, under construction")

    def db_records(self, searchSelection, searchText, auth, bk, yearFrom, yearTo):
        dbPath = sys.argv[1] + sys.argv[2]
        sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % dbPath)
        sourceData.is_ms_access_driver()
        conn = sourceData.db_connect()
        sourceData.report_tables(conn.cursor())

        st.header("Database Records")

        if searchSelection == self.dict_searches.get("ants_srch_txt"):
            self.__show_srch_ants_srch_txt(sourceData, conn, searchText)
        elif searchSelection == self.dict_searches.get("ants_srch_txt_auth"):
            self.__show_srch_ants_auth_srch_txt(sourceData, conn, auth, searchText)
        elif searchSelection == self.dict_searches.get("ants_srch_txt_bk"):
            self.__show_srch_ants_bk_srch_txt(sourceData, conn, bk, searchText)
        elif searchSelection == self.dict_searches.get("ants_bk"):
            self.__show_srch_ants_bk(sourceData, conn, bk)
        elif searchSelection == self.dict_searches.get("ants_auth"):
            self.__show_srch_ants_auth(sourceData, conn, auth)
        elif searchSelection == self.dict_searches.get("bks_auth"):
            self.__show_srch_bks_auth(sourceData, conn, auth)
        elif searchSelection == self.dict_searches.get("bks_all"):
            self.__show_srch_bk_all(sourceData, conn)
        elif searchSelection == self.dict_searches.get("bks_yr_read"):
            self.__show_srch_bks_yr_rd(sourceData, conn, yearFrom, yearTo)
        elif searchSelection == self.dict_searches.get("ants_all"):
            self.__show_srch_ants_all(sourceData, conn)
        elif searchSelection == self.dict_searches.get("ants_yr_read"):
            self.__show_srch_ants_yr_rd(sourceData, conn, yearFrom, yearTo)

        conn.close()

    def __show_srch_ants_srch_txt(self, sourceData, conn, searchText):
        searchTxtArr = self.__formatSearchText(searchText)
        resCountSearchString = sourceData.resAnnotsbySearchString(conn.cursor(), searchTxtArr)
        annots = sourceData.selectAnnotsbySearchString(conn.cursor(), searchTxtArr)

        st.write("Found {} results.".format(resCountSearchString))
        for ant in annots:
            self.__markdown_srch_res_temp(ant,searchTxtArr)

    def __show_srch_ants_auth_srch_txt(self, sourceData, conn, auth, searchText):
        searchTxtArr = self.__formatSearchText(searchText)
        resCountSrchStrAndAuthor = sourceData.resAnnotsbySrchStrAndAuthor(conn.cursor(),
                                                                          self.__format_sql_wrap(auth),
                                                                          searchTxtArr)
        annots = sourceData.selectAnnotsbySrchStrAndAuthor(conn.cursor(), self.__format_sql_wrap(auth),
                                                                          searchTxtArr)
        st.write("Found {} results.".format(resCountSrchStrAndAuthor))
        for ant in annots:
            self.__markdown_srch_res(ant)

    def __show_srch_ants_bk_srch_txt(self, sourceData, conn, bk, searchText):
        searchTxtArr = self.__formatSearchText(searchText)
        resCountSrchStrAndBook = sourceData.resAnnotsbySrchStrAndBook(conn.cursor(), self.__format_sql_wrap(bk),
                                                                                     searchTxtArr)
        annots = sourceData.selectAnnotsbySrchStrAndBook(conn.cursor(),  self.__format_sql_wrap(bk),
                                                                         searchTxtArr)
        st.write("Found {} results.".format(resCountSrchStrAndBook))
        for ant in annots:
            self.__markdown_srch_res(ant)

    def __show_srch_ants_bk(self, sourceData, conn, bk):
        resCountBooks = sourceData.resAnnotsbyBook(conn.cursor(), self.__format_sql_wrap(bk))
        annots = sourceData.selectAnnotsbyBook(conn.cursor(), self.__format_sql_wrap(bk))
        st.write("Found {} results.".format(resCountBooks))
        st.write(bk)
        for ant in annots:
            self.__markdown_srch_res(ant)

    def __show_srch_ants_auth(self, sourceData, conn, auth):
        resCountAuthor = sourceData.resAnnotsbyAuthor(conn.cursor(), self.__format_sql_wrap(auth))
        annots = sourceData.selectAnnotsbyAuthor(conn.cursor(), self.__format_sql_wrap(auth))
        st.write("Found {} results.".format(resCountAuthor))
        for ant in annots:
            self.__markdown_srch_res(ant)

    def __show_srch_bks_auth(self, sourceData, conn, auth):
        resCountBks = sourceData.resBooksByAuthor(conn.cursor(), self.__format_sql_wrap(auth))
        annots = sourceData.selectBooksByAuthor(conn.cursor(), self.__format_sql_wrap(auth))
        st.write("Found {} results.".format(resCountBks))
        for ant in annots:
            self.__markdown_bks_res(ant)

    def __show_srch_bk_all(self, sourceData, conn):
        resCountBooksAll = sourceData.resBooksAll(conn.cursor())
        books = sourceData.selectBooksAll(conn.cursor())
        st.write("Found {} results.".format(resCountBooksAll))
        if resCountBooksAll > 0:
            df = pd.DataFrame(([self.__format_book_no(bk.__getattribute__('Book No')),
                                bk.__getattribute__('Book Title'),
                                bk.Author,
                                bk.Date,
                                bk.__getattribute__('Year Read'),
                                bk.__getattribute__('Publication Locale'),
                                bk.Edition,
                                bk.__getattribute__('First Edition'),
                                bk.__getattribute__('First Edition Locale'),
                                bk.__getattribute__('First Edition Name'),
                                bk.__getattribute__('First Edition Publisher')
                                ] for bk in books),
                        None,
                              columns=['Book no.',
                                       'Title',
                                       'Author',
                                       'Date',
                                       'Year read',
                                       'Locale',
                                       'Edition',
                                       'First Edition',
                                       'First Edition Locale',
                                       'First Edition Name',
                                       'First Edition Publisher'
                                ]
                            )
            st.dataframe(df, None, height=625, hide_index=True)

    def __show_srch_bks_yr_rd(self, sourceData, conn, yearFrom, yearTo):
        resCountBooksYearRead = sourceData.resBooksbyYearRead(conn.cursor(), yearFrom, yearTo)
        books = sourceData.selectBooksbyYearRead(conn.cursor(), yearFrom, yearTo)
        st.write("Found {} results.".format(resCountBooksYearRead))
        if resCountBooksYearRead > 0:
            df = pd.DataFrame(([self.__format_book_no(bk.__getattribute__('Book No')),
                                bk.__getattribute__('Book Title'),
                                bk.Author,
                                bk.__getattribute__('Year Read'),
                                ] for bk in books),
                        None,
                                columns=['Book no.',
                                        'Title',
                                        'Author',
                                        'Year read'
                                ]
                            )
            st.dataframe(df, None, height=625, hide_index=True)

    def __show_srch_ants_all(self, sourceData, conn):
        resCountAnnotsAll = sourceData.resAnnotsAll(conn.cursor())
        annots = sourceData.selectAnnotsAll(conn.cursor())
        st.write("Found {} results.".format(resCountAnnotsAll))
        for ant in annots:
            self.__markdown_srch_res(ant)

    def __show_srch_ants_yr_rd(self, sourceData, conn, yearFrom, yearTo):
        resCountAnnotsYearRead = sourceData.resAnnotsbyYearRead(conn.cursor(), yearFrom, yearTo)
        annots = sourceData.selectAnnotsbyYearRead(conn.cursor(), yearFrom, yearTo)
        st.write("Found {} results.".format(resCountAnnotsYearRead))
        for ant in annots:
            st.markdown(":gray[year read:] :orange[{year_read}] ->...\r\r".format(year_read=ant.__getattribute__('Year Read')))
            self.__markdown_srch_res(ant)

    def __markdown_srch_res(self, ant):
        st.markdown(""":green[Title:] :red[{title}]
                    \r\r:blue[Author: {author}]
                    \r\r:violet[page] {pageno}
                    \r\r{sourcetext}"""
            .format(
                title=ant.__getattribute__('Book Title'),
                author=ant.Author,
                pageno=self.__format_page_no(ant.__getattribute__('Page No')),
                sourcetext=ant.__getattribute__('Source Text')
            )
        )

    def __markdown_srch_res_temp(self, ant, searchTxts):
        srcText = str(ant.__getattribute__('Source Text'))
        for txt in searchTxts:
            strForHghlghts = str(str(txt))
            strForHghlghts = strForHghlghts.lstrip("%").rstrip("%")
            srcText = srcText.replace(strForHghlghts, ":orange-background[{}]".format(strForHghlghts))
        st.markdown(""":green[Title:] :red[{title}]
                    \r\r:blue[Author: {author}]
                    \r\r:violet[page] {pageno}
                    \r\r{sourcetext}"""
            .format(
                title=ant.__getattribute__('Book Title'),
                author=ant.Author,
                pageno=self.__format_page_no(ant.__getattribute__('Page No')),
                sourcetext=srcText
            )
        )

    def __markdown_bks_res(self, ant):
        st.markdown(""":green[Title:] :red[{title}]
                    \r\r:blue[Author:] {author}
                    \r\r:violet[Publisher:] {publisher}
                    \r\r:orange[Date:] {date}"""
            .format(
                title=ant.__getattribute__('Book Title'),
                author=ant.Author,
                publisher=ant.Publisher,
                date=ant.Date
            )
        )

    def __format_page_no(self, pageNo):
        return pageNo.lstrip("0")

    def __format_book_no(self, bookNo):
        return bookNo.lstrip("0")

    def __formatSearchText(self, searchText):
        searchArr = []
        if searchText.find(",") == -1:
            searchArr.append(self.__format_sql_wrap(searchText))
        else:
            searchTxt = searchText.split(",")
            for txt in searchTxt:
                searchArr.append(self.__format_sql_wrap(txt))
        return searchArr

    def __format_sql_wrap(self, searchDatum):
        datum = searchDatum
        if not searchDatum.startswith("%"):
            datum = "%" + datum
        if not searchDatum.endswith("%"):
            datum = datum + "%"
        return datum

    def __isValidYearFormat(self,year, format):
        try:
            res = bool(datetime.strptime(year, format))
        except ValueError:
            res = False
        return res

    dict_searches = {
        "ants_srch_txt": "Annotations by search text",
        "ants_srch_txt_auth": "Annotations by search text and author",
        "ants_srch_txt_bk": "Annotations by search text and book",
        "ants_bk": "Annotations by book",
        "ants_auth": "Annotations by author",
        "bks_auth": "Books by author",
        "bks_all": "All books",
        "bks_yr_read": "Books by year read",
        "ants_all": "All annotations",
        "ants_yr_read": "Annotations by year read"
    }