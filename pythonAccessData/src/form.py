from datetime import datetime, date
import pandas as pd
import streamlit as st
import form_sr

class DATA_FORM(form_sr.FORM):

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

    dict_hlght_cases = {
        "cap": "capitalise",
        "cap_all": "capitaliseAll",
        "lwr": "lower",
        "upr": "upper"
    }

    def srch_searchtext(self):
        with st.form("Search by annotation only"):
            txt = st.text_area("Annotated text to search for (separate multiple with comma)")
            searched = st.form_submit_button("Search")
            if searched:
                if txt == "":
                    st.markdown(":red[no search text given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_srch_txt"), txt, "", "", "", "")

    def srch_searchtext_auth(self):
        with st.form("Search by annotation and author"):
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
        with st.form("Search by annotation and book title"):
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
        with st.form("Search for annotations by book title"):
            book = st.text_input("Book")
            searched = st.form_submit_button("Search")
            if searched:
                if book == "":
                    st.markdown(":red[no book given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_bk"), "", "", book, "", "")

    def srch_auth(self):
        with st.form("Search for annotations by author"):
            author = st.text_input("Author")
            searched = st.form_submit_button("Search")
            if searched:
                if author == "":
                    st.markdown(":red[no author given.]")
                else:
                    self.db_records(self.dict_searches.get("ants_auth"), "", author, "", "", "")

    def bks_auth(self):
        with st.form("Search for book titles by author"):
            author = st.text_input("Author")
            searched = st.form_submit_button("Search")
            if searched:
                if author == "":
                    st.markdown(":red[no author given.]")
                else:
                    self.db_records(self.dict_searches.get("bks_auth"), "", author, "", "", "")

    def bks_all(self):
        with st.form("Search for all book titles"):
            searched = st.form_submit_button("Search")
            if searched:
                self.db_records(self.dict_searches.get("bks_all"), "", "", "", "", "")

    def bks_yr_read(self):
        with st.form("Search for book titles by year read"):
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
                        if not super().isValidYearFormat(yearFrom, "%Y"):
                            st.markdown(":red[From year is not in format yyyy.]")
                        else:
                            if not super().isValidYearFormat(yearTo, "%Y"):
                                st.markdown(":red[To year is not in format yyyy.]")
                            else:
                                if date(int(yearFrom), 1, 1) > date(int(yearTo), 1, 1):
                                    st.markdown(":red[From year cannot be greater than To year.]")
                                else:
                                    self.db_records(self.dict_searches.get("bks_yr_read"), "", "", "", yearFrom, yearTo)

    def ants_all(self):
        with st.form("Search for all annotations"):
            st.markdown(":red-background[NOTE: page may be slow to load searching on all annotations...]")
            searched = st.form_submit_button("Search")
            if searched:
                self.db_records(self.dict_searches.get("ants_all"), "", "", "", "", "")

    def ants_yr_read(self):
        with st.form("Search for annotations by year book titles read"):
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
                        if not super().isValidYearFormat(yearFrom, "%Y"):
                            st.markdown(":red[From year is not in format yyyy.]")
                        else:
                            if not super().isValidYearFormat(yearTo, "%Y"):
                                st.markdown(":red[To year is not in format yyyy.]")
                            else:
                                if date(int(yearFrom), 1, 1) > date(int(yearTo), 1, 1):
                                    st.markdown(":red[From year cannot be greater than To year.]")
                                else:
                                    self.db_records(self.dict_searches.get("ants_yr_read"), "", "", "", yearFrom, yearTo)

    def db_records(self, searchSelection, searchText, auth, bk, yearFrom, yearTo):
        sourceData = super().get_data_source()
        conn = super().get_connection(sourceData)
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
            self.__markdown_srch_res(ant,searchTxtArr)

    def __show_srch_ants_auth_srch_txt(self, sourceData, conn, auth, searchText):
        searchTxtArr = self.__formatSearchText(searchText)
        resCountSrchStrAndAuthor = sourceData.resAnnotsbySrchStrAndAuthor(conn.cursor(),
                                                                          super().format_sql_wrap(auth),
                                                                          searchTxtArr)
        annots = sourceData.selectAnnotsbySrchStrAndAuthor(conn.cursor(), super().format_sql_wrap(auth),
                                                                          searchTxtArr)
        st.write("Found {} results.".format(resCountSrchStrAndAuthor))
        for ant in annots:
            self.__markdown_srch_res(ant,searchTxtArr)

    def __show_srch_ants_bk_srch_txt(self, sourceData, conn, bk, searchText):
        searchTxtArr = self.__formatSearchText(searchText)
        resCountSrchStrAndBook = sourceData.resAnnotsbySrchStrAndBook(conn.cursor(), super().format_sql_wrap(bk),
                                                                                     searchTxtArr)
        annots = sourceData.selectAnnotsbySrchStrAndBook(conn.cursor(),  super().format_sql_wrap(bk),
                                                                         searchTxtArr)
        st.write("Found {} results.".format(resCountSrchStrAndBook))
        for ant in annots:
            self.__markdown_srch_res(ant, searchTxtArr)

    def __show_srch_ants_bk(self, sourceData, conn, bk):
        resCountBooks = sourceData.resAnnotsbyBook(conn.cursor(), super().format_sql_wrap(bk))
        annots = sourceData.selectAnnotsbyBook(conn.cursor(), super().format_sql_wrap(bk))
        st.write("Found {} results.".format(resCountBooks))
        for ant in annots:
            self.__markdown_srch_res(ant, "")

    def __show_srch_ants_auth(self, sourceData, conn, auth):
        resCountAuthor = sourceData.resAnnotsbyAuthor(conn.cursor(), super().format_sql_wrap(auth))
        annots = sourceData.selectAnnotsbyAuthor(conn.cursor(), super().format_sql_wrap(auth))
        st.write("Found {} results.".format(resCountAuthor))
        for ant in annots:
            self.__markdown_srch_res(ant, "")

    def __show_srch_bks_auth(self, sourceData, conn, auth):
        resCountBks = sourceData.resBooksByAuthor(conn.cursor(), super().format_sql_wrap(auth))
        annots = sourceData.selectBooksByAuthor(conn.cursor(), super().format_sql_wrap(auth))
        st.write("Found {} results.".format(resCountBks))
        for ant in annots:
            self.__markdown_bks_res(ant)

    def __show_srch_bk_all(self, sourceData, conn):
        resCountBooksAll = sourceData.resBooksAll(conn.cursor())
        books = sourceData.selectBooksAll(conn.cursor())
        st.write("Found {} results.".format(resCountBooksAll))
        if resCountBooksAll > 0:
            df = pd.DataFrame(([super().format_book_no(bk.__getattribute__('Book No')),
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
            df = pd.DataFrame(([super().format_book_no(bk.__getattribute__('Book No')),
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
        srcText = str(ant.__getattribute__('Source Text'))
        if searchTxts != "":
            for txt in searchTxts:
                txt = str(txt).lstrip("%").rstrip("%")
                txt = txt.replace("''", "'")
                txt = txt.replace("[[]", "[")
                srcText = srcText.replace(txt, ":orange-background[{}]".format(txt))
                srcText = srcText.replace(txt.capitalize(),
                                          ":orange-background[{}]".format(txt.capitalize()))
                srcText = srcText.replace(txt.lower(),
                                          ":orange-background[{}]".format(txt.lower()))
                srcText = srcText.replace(txt.upper(),
                                          ":orange-background[{}]".format(txt.upper()))
                strForHghlghts = txt.split(" ")
                if len(strForHghlghts) > 1:
                    srcText = self.__srcTxtCaseHghlghtsByWrd(srcText, txt, self.dict_hlght_cases.get("cap_all"))
                    srcText = self.__srcTxtCaseHghlghtsByWrd(srcText, txt, self.dict_hlght_cases.get("lwr"))
                    srcText = self.__srcTxtCaseHghlghtsByWrd(srcText, txt, self.dict_hlght_cases.get("upr"))
                    capAllStr = ""
                    for wrd in range(0, len(strForHghlghts)):
                        capAllStr = capAllStr + str(strForHghlghts[wrd]).capitalize() + " "
                    capAllStr = capAllStr.strip()
                    srcText = self.__srcTxtCaseHghlghtsByWrd(srcText, capAllStr, self.dict_hlght_cases.get("lwr"))
                    srcText = self.__srcTxtCaseHghlghtsByWrd(srcText, capAllStr, self.dict_hlght_cases.get("upr"))
            if srcText.find(":orange-background[") == -1:
                st.write(":green-background[The text you searched for was found but cannot be highlighted ¬]")
        st.markdown(""":green[Title:] :red[{title}]
                    \r\r:blue[Author: {author}]
                    \r\r:violet[page] {pageno}
                    \r\r{sourcetext}"""
            .format(
                title=ant.__getattribute__('Book Title'),
                author=ant.Author,
                pageno=super().format_page_no(ant.__getattribute__('Page No')),
                sourcetext=srcText
            )
        )

    def __srcTxtCaseHghlghtsByWrd(self,srcText, txt, case):
        sText = srcText
        strForHghlghts = txt.split(" ")
        capAllStr = ""
        if case == self.dict_hlght_cases.get("cap_all"):
            for wrd in range(0, len(strForHghlghts)):
                capAllStr = capAllStr + str(strForHghlghts[wrd]).capitalize() + " "
            capAllStr = capAllStr.strip()
            sText = sText.replace(capAllStr,
                                  ":orange-background[{}]".format(capAllStr))
        else:
            for wrd in range(0, len(strForHghlghts)):
                tempStr = ""
                tempwrd = ""
                if case == self.dict_hlght_cases.get("cap"):
                    tempwrd = strForHghlghts[wrd].capitalize()
                elif case == self.dict_hlght_cases.get("lwr"):
                    tempwrd = strForHghlghts[wrd].lower()
                elif case == self.dict_hlght_cases.get("upr"):
                    tempwrd = strForHghlghts[wrd].upper()
                for wrdIndx in range(0, len(strForHghlghts)):
                    if wrd == wrdIndx:
                        tempStr = tempStr + " " + tempwrd
                    else:
                        tempStr = tempStr + " " + str(strForHghlghts[wrdIndx])
                tempStr = tempStr.strip()
                sText = sText.replace(tempStr,
                                      ":orange-background[{}]".format(tempStr))
        return sText

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

    def __formatSearchText(self, searchText):
        searchArr = []
        if searchText.find(",") == -1:
            searchArr.append(super().format_sql_wrap(searchText))
        else:
            searchTxt = searchText.split(",")
            for txt in searchTxt:
                searchArr.append(super().format_sql_wrap(txt))
        return searchArr