from datetime import date
import pandas as pd
import streamlit as st
import form_sr

class DATA_FORM(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_List_view = {
        "header": "Select annotations search",
        "title": "Select search type"
    }

    dict_searches = {
        "None": "none",
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

    def srch_searchtext(self):
        if "go_srch_searchtext" not in st.session_state:
            st.session_state["go_srch_searchtext"] = False
        if "txt_srch_searchtext" not in st.session_state:
            st.session_state["txt_srch_searchtext"] = ""
        with st.form("Search by annotation only"):
            st.session_state["txt_srch_searchtext"] = st.text_area("Annotated text to search for (separate multiple with comma)",
                                                   value=st.session_state["txt_srch_searchtext"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_srch_searchtext"] = True
                st.rerun()
            elif st.session_state["go_srch_searchtext"]:
                if st.session_state["txt_srch_searchtext"] == "":
                    st.markdown(":red[no search text given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_srch_txt"), st.session_state["txt_srch_searchtext"],
                                    "", "", "", "")

    def srch_searchtext_auth(self):
        if "go_srch_searchtext_auth" not in st.session_state:
            st.session_state["go_srch_searchtext_auth"] = False
        if "txt_srch_searchtext_auth" not in st.session_state:
            st.session_state["txt_srch_searchtext_auth"] = ""
        if "auth_srch_searchtext_auth" not in st.session_state:
            st.session_state["auth_srch_searchtext_auth"] = ""
        with st.form("Search by annotation and author"):
            st.session_state["txt_srch_searchtext_auth"] = st.text_area("Annotated text to search for (separate multiple with comma)",
                                                                        value=st.session_state["txt_srch_searchtext_auth"])
            st.session_state["auth_srch_searchtext_auth"] = st.text_input("Author",
                                                                          value=st.session_state["auth_srch_searchtext_auth"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_srch_searchtext_auth"] = True
                st.rerun()
            elif st.session_state["go_srch_searchtext_auth"]:
                if st.session_state["txt_srch_searchtext_auth"] == "":
                    st.markdown(":red[no search text given.]")
                else:
                    if st.session_state["auth_srch_searchtext_auth"] == "":
                        st.markdown(":red[no author given.]")
                    else:
                        self.db_records(self.dict_searches.get("ants_srch_txt_auth"),
                                        st.session_state["txt_srch_searchtext_auth"],
                                        st.session_state["auth_srch_searchtext_auth"], "", "", "")

    def srch_searchtext_bk(self):
        if "go_srch_searchtext_bk" not in st.session_state:
            st.session_state["go_srch_searchtext_bk"] = False
        if "txt_srch_searchtext_bk" not in st.session_state:
            st.session_state["txt_srch_searchtext_bk"] = ""
        if "bk_srch_searchtext_bk" not in st.session_state:
            st.session_state["bk_srch_searchtext_bk"] = ""
        with st.form("Search by annotation and book title"):
            st.session_state["txt_srch_searchtext_bk"] = st.text_area("Annotated text to search for (separate multiple with comma)",
                                                                      value=st.session_state["txt_srch_searchtext_bk"])
            st.session_state["bk_srch_searchtext_bk"] = st.text_input("Book", value=st.session_state["bk_srch_searchtext_bk"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_srch_searchtext_bk"] = True
                st.rerun()
            elif st.session_state["go_srch_searchtext_bk"]:
                if st.session_state["txt_srch_searchtext_bk"] == "":
                    st.markdown(":red[no search text given.]")
                else:
                    if st.session_state["bk_srch_searchtext_bk"] == "":
                        st.markdown(":red[no book given.]")
                    else:
                        self.db_records(self.dict_searches.get("ants_srch_txt_bk"), st.session_state["txt_srch_searchtext_bk"],
                                        "", st.session_state["bk_srch_searchtext_bk"], "", "")

    def srch_bk(self):
        if "go_srch_bk" not in st.session_state:
            st.session_state["go_srch_bk"] = False
        if "bk_srch_bk" not in st.session_state:
            st.session_state["bk_srch_bk"] = ""
        with st.form("Search for annotations by book title"):
            st.session_state["bk_srch_bk"] = st.text_input("Book", value=st.session_state["bk_srch_bk"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_srch_bk"] = True
                st.rerun()
            elif st.session_state["go_srch_bk"]:
                if st.session_state["bk_srch_bk"] == "":
                    st.markdown(":red[no book given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_bk"), "", "", st.session_state["bk_srch_bk"],
                                    "", "")

    def srch_auth(self):
        if "go_srch_auth" not in st.session_state:
            st.session_state["go_srch_auth"] = False
        if "auth_srch_auth" not in st.session_state:
            st.session_state["auth_srch_auth"] = ""
        with st.form("Search for annotations by author"):
            st.session_state["auth_srch_auth"] = st.text_input("Author", value=st.session_state["auth_srch_auth"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_srch_auth"] = True
                st.rerun()
            elif st.session_state["go_srch_auth"]:
                if st.session_state["auth_srch_auth"] == "":
                    st.markdown(":red[no author given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_auth"), "", st.session_state["auth_srch_auth"],
                                "", "", "")

    def bks_auth(self):
        if "go_srch_bks_auth" not in st.session_state:
            st.session_state["go_srch_bks_auth"] = False
        if "auth_srch_bks_auth" not in st.session_state:
            st.session_state["auth_srch_bks_auth"] = ""
        with st.form("Search for book titles by author"):
            st.session_state["auth_srch_bks_auth"] = st.text_input("Author", value=st.session_state["auth_srch_bks_auth"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_srch_bks_auth"] = True
                st.rerun()
            elif st.session_state["go_srch_bks_auth"]:
                if st.session_state["auth_srch_bks_auth"] == "":
                    st.markdown(":red[no author given.]")
                else:
                    self.db_records(self.dict_searches.get("bks_auth"), "", st.session_state["auth_srch_bks_auth"],
                                    "", "", "")

    def bks_all(self):
        if "go_bks_all" not in st.session_state:
            st.session_state["go_bks_all"] = False
        with st.form("Search for all book titles"):
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_bks_all"] = True
                st.rerun()
            elif st.session_state["go_bks_all"]:
                self.db_records(self.dict_searches.get("bks_all"), "", "", "", "", "")

    def bks_yr_read(self):
        if "go_bks_yr" not in st.session_state:
            st.session_state["go_bks_yr"] = False
        if "yr_bks_from" not in st.session_state:
            st.session_state["yr_bks_from"] = ""
        if "yr_bks_to" not in st.session_state:
            st.session_state["yr_bks_to"] = ""
        with st.form("Search for book titles by year read"):
            st.session_state["yr_bks_from"] = st.text_input("From year (yyyy)", value=st.session_state["yr_bks_from"])
            st.session_state["yr_bks_to"] = st.text_input("To year (yyyy)", value=st.session_state["yr_bks_to"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_bks_yr"] = True
                st.rerun()
            elif st.session_state["go_bks_yr"]:
                if st.session_state["yr_bks_from"] == "":
                    st.markdown(":red[no start year given.]")
                else:
                    if st.session_state["yr_bks_to"] == "":
                        st.markdown(":red[no end year given.]")
                    else:
                        if not self.isValidYearFormat(st.session_state["yr_bks_from"], "%Y"):
                            st.markdown(":red[From year is not in format yyyy.]")
                        else:
                            if not self.isValidYearFormat(st.session_state["yr_bks_to"], "%Y"):
                                st.markdown(":red[To year is not in format yyyy.]")
                            else:
                                if date(int(st.session_state["yr_bks_from"]), 1,
                                        1) > date(int(st.session_state["yr_bks_to"]), 1, 1):
                                    st.markdown(":red[From year cannot be greater than To year.]")
                                else:
                                    self.db_records(self.dict_searches.get("bks_yr_read"), "", "", "", st.session_state["yr_bks_from"],
                                                    st.session_state["yr_bks_to"])

    def ants_all(self):
        if "go_ants_all" not in st.session_state:
            st.session_state["go_ants_all"] = False
        with st.form("Search for all annotations"):
            st.markdown(":red-background[NOTE: page may be slow to load searching on all annotations...]")
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_ants_all"] = True
                st.rerun()
            elif st.session_state["go_ants_all"]:
                self.db_records(self.dict_searches.get("ants_all"), "", "", "", "", "")

    def ants_yr_read(self):
        with st.form("Search for annotations by year book titles read"):
            if "go_ants_yr" not in st.session_state:
                st.session_state["go_ants_yr"] = False
            if "yr_ants_from" not in st.session_state:
                st.session_state["yr_ants_from"] = ""
            if "yr_ants_to" not in st.session_state:
                st.session_state["yr_ants_to"] = ""
            st.session_state["yr_ants_from"] = st.text_input("From year (yyyy)", value=st.session_state["yr_ants_from"])
            st.session_state["yr_ants_to"] = st.text_input("To year (yyyy)", value=st.session_state["yr_ants_to"])
            searched = st.form_submit_button("Search")
            if searched:
                st.session_state["go_ants_yr"] = True
                st.rerun()
            elif st.session_state["go_ants_yr"]:
                if st.session_state["yr_ants_from"] == "":
                    st.markdown(":red[no start year given.]")
                else:
                    if st.session_state["yr_ants_to"] == "":
                        st.markdown(":red[no end year given.]")
                    else:
                        if not self.isValidYearFormat(st.session_state["yr_ants_from"], "%Y"):
                            st.markdown(":red[From year is not in format yyyy.]")
                        else:
                            if not self.isValidYearFormat(st.session_state["yr_ants_to"], "%Y"):
                                st.markdown(":red[To year is not in format yyyy.]")
                            else:
                                if date(int(st.session_state["yr_ants_from"]), 1, 1) > date(int(st.session_state["yr_ants_to"]),
                                                                                                1, 1):
                                    st.markdown(":red[From year cannot be greater than To year.]")
                                else:
                                    self.db_records(self.dict_searches.get("ants_yr_read"), "", "", "", st.session_state["yr_ants_from"],
                                                    st.session_state["yr_ants_to"])

    def db_records(self, searchSelection, searchText, auth, bk, yearFrom, yearTo):
        sourceData = self.get_data_source()
        conn = self.get_connection(sourceData)
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
        searchTxtArr = self.formatSearchText(searchText)
        resCountSearchString = sourceData.resAnnotsbySearchString(conn.cursor(), searchTxtArr)
        annots = sourceData.selectAnnotsbySearchString(conn.cursor(), searchTxtArr)
        st.write("Found {} results.".format(resCountSearchString))
        for ant in annots:
            self.__markdown_srch_res(ant,searchTxtArr)

    def __show_srch_ants_auth_srch_txt(self, sourceData, conn, auth, searchText):
        searchTxtArr = self.formatSearchText(searchText)
        resCountSrchStrAndAuthor = sourceData.resAnnotsbySrchStrAndAuthor(conn.cursor(),
                                                                          self.format_sql_wrap(auth),
                                                                          searchTxtArr)
        annots = sourceData.selectAnnotsbySrchStrAndAuthor(conn.cursor(), self.format_sql_wrap(auth),
                                                                          searchTxtArr)
        st.write("Found {} results.".format(resCountSrchStrAndAuthor))
        for ant in annots:
            self.__markdown_srch_res(ant,searchTxtArr)

    def __show_srch_ants_bk_srch_txt(self, sourceData, conn, bk, searchText):
        searchTxtArr = self.formatSearchText(searchText)
        resCountSrchStrAndBook = sourceData.resAnnotsbySrchStrAndBook(conn.cursor(), self.format_sql_wrap(bk),
                                                                                     searchTxtArr)
        annots = sourceData.selectAnnotsbySrchStrAndBook(conn.cursor(),  self.format_sql_wrap(bk),
                                                                         searchTxtArr)
        st.write("Found {} results.".format(resCountSrchStrAndBook))
        for ant in annots:
            self.__markdown_srch_res(ant, searchTxtArr)

    def __show_srch_ants_bk(self, sourceData, conn, bk):
        resCountBooks = sourceData.resAnnotsbyBook(conn.cursor(), self.format_sql_wrap(bk))
        annots = sourceData.selectAnnotsbyBook(conn.cursor(), self.format_sql_wrap(bk))
        st.write("Found {} results.".format(resCountBooks))
        for ant in annots:
            self.__markdown_srch_res(ant, "")

    def __show_srch_ants_auth(self, sourceData, conn, auth):
        resCountAuthor = sourceData.resAnnotsbyAuthor(conn.cursor(), self.format_sql_wrap(auth))
        annots = sourceData.selectAnnotsbyAuthor(conn.cursor(), self.format_sql_wrap(auth))
        st.write("Found {} results.".format(resCountAuthor))
        for ant in annots:
            self.__markdown_srch_res(ant, "")

    def __show_srch_bks_auth(self, sourceData, conn, auth):
        resCountBks = sourceData.resBooksByAuthor(conn.cursor(), self.format_sql_wrap(auth))
        annots = sourceData.selectBooksByAuthor(conn.cursor(), self.format_sql_wrap(auth))
        st.write("Found {} results.".format(resCountBks))
        for ant in annots:
            self.__markdown_bks_res(ant)

    def __show_srch_bk_all(self, sourceData, conn):
        resCountBooksAll = sourceData.resBooksAll(conn.cursor())
        books = sourceData.selectBooksAll(conn.cursor())
        st.write("Found {} results.".format(resCountBooksAll))
        if resCountBooksAll > 0:
            df = pd.DataFrame(([self.format_book_no(bk.__getattribute__('Book No')), # note self.format_book_no() not working
                                bk.__getattribute__('Book Title'),
                                bk.Author,
                                bk.Publisher,
                                bk.Dat,
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
                                       'Publisher',
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
            df = pd.DataFrame(([self.format_book_no(bk.__getattribute__('Book No')),  # note self.format_book_no() not working
                                bk.__getattribute__('Book Title'),
                                bk.Author,
                                bk.Publisher,
                                bk.__getattribute__('Year Read'),
                                ] for bk in books),
                        None,
                                columns=['Book no.',
                                        'Title',
                                        'Author',
                                        'Publisher',
                                        'Year read'
                                ]
                            )
            st.dataframe(df, None, height=625, hide_index=True)

    def __show_srch_ants_all(self, sourceData, conn):
        resCountAnnotsAll = sourceData.resAnnotsAll(conn.cursor())
        annots = sourceData.selectAnnotsAll(conn.cursor())
        st.write("Found {} results.".format(resCountAnnotsAll))
        for ant in annots:
            self.__markdown_srch_res(ant, "")

    def __show_srch_ants_yr_rd(self, sourceData, conn, yearFrom, yearTo):
        resCountAnnotsYearRead = sourceData.resAnnotsbyYearRead(conn.cursor(), yearFrom, yearTo)
        annots = sourceData.selectAnnotsbyYearRead(conn.cursor(), yearFrom, yearTo)
        st.write("Found {} results.".format(resCountAnnotsYearRead))
        for ant in annots:
            st.markdown(":gray[year read:] :orange[{year_read}] ->...\r\r".format(year_read=ant.__getattribute__('Year Read')))
            self.__markdown_srch_res(ant, "")


    def __markdown_srch_res(self, ant, searchTxts):
        srcText = self.hghlght_txt(str(ant.__getattribute__('Source Text')), searchTxts)
        if srcText.find(":orange-background[") == -1 and searchTxts != "":
            st.write(":green-background[The text you searched for was found but cannot be highlighted ¬]")
        st.markdown(""":green[Title:] :red[{title}]
                    \r\r:blue[Author: {author}]
                    \r\r:violet[page] {pageno}
                    \r\r{sourcetext}"""
            .format(
                title=ant.__getattribute__('Book Title'),
                author=ant.Author,
                pageno=self.format_page_no(ant.__getattribute__('Page No')),
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
                date=ant.Dat
            )
        )