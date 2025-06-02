import pyodbc
import streamlit as st

class DATA_SOURCE():

    def __init__(self, connectString):
        self.connStr = connectString

    dict_err_gener_msgs = {
        "cursor_exec": "Error executing data query (Is your data source file a valid one?)"
    }

    def is_ms_access_driver(self):
        found = False
        for i in pyodbc.drivers():
            if i.startswith('Microsoft Access Driver'):
                found = True
                print(f'..found Microsoft Access Driver (*.mdb, *.accdb)')
                break
        if not found:
            print(f'ERROR - Microsoft Access Driver not found.')

    def db_connect(self):
        return pyodbc.connect(self.connStr)

    def report_tables(self, cursor):
        print(f'listing tables in database found...')
        for i in cursor.tables(tableType='TABLE'):
            print(i.table_name)

    def resBooksAll(self, cursor):
        try:
            results = cursor.execute(self.dict_queries.get("books_all_count"))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def resBookLatest(self, cursor):
        try:
            result = cursor.execute(self.dict_queries.get("books_max_key"))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = result.fetchone()
            return res[0]

    def selectBooksAll(self, cursor):
        try:
            books = cursor.execute(self.dict_queries.get("books_all"))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return books

    def resAnnotsbyBook(self, cursor, book_title):
        try:
            results = cursor.execute(self.dict_queries.get("annots_by_bk_count").format(book_title))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def resExactAnnotsbyBook(self, cursor, book):
        try:
            results = cursor.execute(self.dict_queries.get("annots_by_bk_exact_count").format(book[self.dict_books_indx.get("no")]))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def selectAnnotsbyBook(self, cursor, book_title):
        try:
            annots = cursor.execute(self.dict_queries.get("annots_by_bk").format(book_title))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return annots

    def resAnnotsbyAuthor(self, cursor, author):
        try:
            results = cursor.execute(
                self.dict_queries.get("annots_by_auth_count").format(author))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def selectAnnotsbyAuthor(self, cursor, author):
        try:
            annots = cursor.execute(self.dict_queries.get("annots_by_auth").format(author))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return annots

    def resBooksByAuthor(self, cursor, author):
        try:
            results = cursor.execute(
                self.dict_queries.get("books_by_auth_count").format(author))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def selectBooksByAuthor(self, cursor, author):
        try:
            annots = cursor.execute(self.dict_queries.get("books_by_auth").format(author))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return annots

    def resAnnotsbySearchString(self, cursor, searchString):
        sqlStr = self.dict_queries.get("annots_by_sch_str_count")
        if len(searchString) == 1:
            try:
                results = cursor.execute(sqlStr.format(str(searchString[0])))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                res = results.fetchone()
                return res[0]
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])))
            for srchStrs in range(1, len(searchString)):
                sqlStr = sqlStr + self.dict_queries.get("append_srch_txt").format(str(searchString[srchStrs]))
            try:
                results = cursor.execute(sqlStr)
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                res = results.fetchone()
                return res[0]

    def selectAnnotsbySearchString(self, cursor, searchString):
        sqlStr = self.dict_queries.get("annots_by_sch_str")
        if len(searchString) == 1:
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            try:
                annots = cursor.execute(sqlStr.format(str(searchString[0])))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec")+ "] " + str(ex))
            else:
                return annots
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])))
            for srchStrs in range(1, len(searchString)):
                sqlStr = sqlStr + self.dict_queries.get("append_srch_txt").format(str(searchString[srchStrs]))
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            try:
                annots = cursor.execute(sqlStr)
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                return annots

    def resAnnotsbySrchStrAndBook(self, cursor, book, searchString):
        sqlStr = self.dict_queries.get("annots_by_schstr_and_bk_count")
        if len(searchString) == 1:
            try:
                results = cursor.execute(sqlStr.format(book, str(searchString[0])))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                res = results.fetchone()
                return res[0]
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(book), 1)
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])), 1)
            for srchStrs in range(1, len(searchString)):
                sqlTemp = self.dict_queries.get("insert_srch_txt_bk")
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(book), 1)
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(str(searchString[srchStrs])), 1)
                sqlStr = sqlStr + sqlTemp
            try:
                results = cursor.execute(sqlStr)
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                res = results.fetchone()
                return res[0]

    def selectAnnotsbySrchStrAndBook(self, cursor, book, searchString):
        sqlStr = self.dict_queries.get("annots_by_schstr_and_bk")
        if len(searchString) == 1:
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            try:
                annots = cursor.execute(sqlStr.format(book, str(searchString[0])))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                return annots
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(book), 1)
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])), 1)
            for srchStrs in range(1, len(searchString)):
                sqlTemp = self.dict_queries.get("insert_srch_txt_bk")
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(book), 1)
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(str(searchString[srchStrs])), 1)
                sqlStr = sqlStr + sqlTemp
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            try:
                annots = cursor.execute(sqlStr)
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                return annots

    def resAnnotsbySrchStrAndAuthor(self, cursor, author, searchString):
        sqlStr = self.dict_queries.get("annots_schstr_and_auth_count")
        if len(searchString) == 1:
            try:
                results = cursor.execute(sqlStr.format(author, str(searchString[0])))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                res = results.fetchone()
                return res[0]
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(author), 1)
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])), 1)
            for srchStrs in range(1, len(searchString)):
                sqlTemp = self.dict_queries.get("insert_srch_txt_auth")
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(author), 1)
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(str(searchString[srchStrs])), 1)
                sqlStr = sqlStr + sqlTemp
            try:
                results = cursor.execute(sqlStr)
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                res = results.fetchone()
                return res[0]

    def selectAnnotsbySrchStrAndAuthor(self, cursor, author, searchString):
        sqlStr = self.dict_queries.get("annots_schstr_and_auth")
        if len(searchString) == 1:
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            try:
                annots = cursor.execute(sqlStr.format(author, str(searchString[0])))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                return annots
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(author), 1)
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])), 1)
            for srchStrs in range(1, len(searchString)):
                sqlTemp = self.dict_queries.get("insert_srch_txt_auth")
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(author), 1)
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(str(searchString[srchStrs])), 1)
                sqlStr = sqlStr + sqlTemp
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            try:
                annots = cursor.execute(sqlStr)
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
            else:
                return annots

    def resAnnotsbyYearRead(self, cursor, fromYear, toYear):
        try:
            results = cursor.execute(self.dict_queries.get("annots_by_yr_read_count").format(fromYear, toYear))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def selectAnnotsbyYearRead(self, cursor, fromYear, toYear):
        try:
            annots = cursor.execute(self.dict_queries.get("annots_by_yr_read").format(fromYear, toYear))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return annots

    def resBooksbyYearRead(self, cursor, fromYear, toYear):
        try:
            results = cursor.execute(self.dict_queries.get("books_by_yr_read_count").format(fromYear, toYear))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def selectBooksbyYearRead(self, cursor, fromYear, toYear):
        try:
            annots = cursor.execute(self.dict_queries.get("books_by_yr_read").format(fromYear, toYear))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return annots

    def resAddUpdateExactBk(self, cursor, book):
        try:
            results = cursor.execute(self.dict_queries.get("bk_add_edit_exact_count").format(str(book[0])))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def AddUpdateExactBk(self, cursor, book):
        try:
            bk = cursor.execute(self.dict_queries.get("bk_add_edit_exact").format(str(book[0])))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return bk

    def resAddUpdateNewBk(self, cursor, book):
        sqlStr = self.__sql_bk_srch(True, book)
        try:
            results = cursor.execute(sqlStr)
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def addUpdateNewBk(self, cursor, book):
        sqlStr = self.__sql_bk_srch(False, book)
        try:
            bk = cursor.execute(sqlStr)
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return bk

    def addUpdateNewBook(self, cursor, bk_sum, book, bk_exists):
        if not bk_exists:
            sql_str = self.dict_inserts.get("books_new_add")
            try:
                cursor.execute(sql_str.format(
                         bk_sum, # book no.
                               str(book[self.dict_books_indx.get("title")]),
                               str(book[self.dict_books_indx.get("author")]),
                               str(book[self.dict_books_indx.get("publisher")]),
                               str(book[self.dict_books_indx.get("dat")]),
                               str(book[self.dict_books_indx.get("year_read")]),
                               str(book[self.dict_books_indx.get("publication_locale")]),
                               str(book[self.dict_books_indx.get("edition")]), # edition
                               str(book[self.dict_books_indx.get("first_edition")]),
                               str(book[self.dict_books_indx.get("first_edition_locale")]),
                               str(book[self.dict_books_indx.get("first_edition_name")]),
                               str(book[self.dict_books_indx.get("first_edition_publisher")])
                ))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            sql_str = self.dict_updates.get("books_update_add")
            try:
                cursor.execute(sql_str.format(
                          str(book[self.dict_books_indx.get("author")]),
                                str(book[self.dict_books_indx.get("publisher")]),
                                str(book[self.dict_books_indx.get("dat")]),
                                str(book[self.dict_books_indx.get("year_read")]),
                                str(book[self.dict_books_indx.get("publication_locale")]),
                                str(book[self.dict_books_indx.get("edition")]),  # edition
                                str(book[self.dict_books_indx.get("first_edition")]),
                                str(book[self.dict_books_indx.get("first_edition_locale")]),
                                str(book[self.dict_books_indx.get("first_edition_name")]),
                                str(book[self.dict_books_indx.get("first_edition_publisher")]),
                                str(book[self.dict_books_indx.get("no")])
                ))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))

                # HERE ############################################################
                raise self.dict_err_gener_msgs.get("cursor_exec") + str(ex) from RuntimeError
        try:
            cursor.commit()
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))

    def resAddNewAnnot_srch_bk(self, cursor, book):
        sqlStr = self.__sql_nw_annt_bk_srch("count", book)
        try:
            results = cursor.execute(sqlStr)
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            res = results.fetchone()
            return res[0]

    def addNewAnnot_srch_bk(self, cursor, book):
        sqlStr = self.__sql_nw_annt_bk_srch("records", book)
        try:
            annots = cursor.execute(sqlStr)
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return annots

    def delExactAnnotsbyBook(self, cursor, book):
        try:
            cursor.execute(self.dict_deletes.get("annots_by_bk_exact_del").format(book[self.dict_books_indx.get("no")]))
            cursor.commit()
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))

    def addNewAnnot_srch_page_no(self, cursor, record):
        try:
            annot = cursor.execute(self.dict_queries.get("new_annot_page_no_exists").format(
                                                         str(record[self.dict_annots_indx.get("book_no")]),
                                                               str(record[self.dict_annots_indx.get("page_no")]) # book no, page no
                                                        ))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            return(annot)

    def addUpdateAnnot(self, cursor, ant, annotExists):
        if not annotExists:
            try:
                cursor.execute(self.dict_inserts.get("annots_new_add").format(
                                                             str(ant[self.dict_annots_indx.get("book_no")]),
                                                                   str(ant[self.dict_annots_indx.get("page_no")]),
                                                                   str(ant[self.dict_annots_indx.get("source_text")])
                                                        ))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        else:
            try:
                cursor.execute(self.dict_updates.get("annots_update_add").format(
                                                             str(ant[self.dict_annots_indx.get("source_text")]),
                                                                   str(ant[self.dict_annots_indx.get("book_no")]),
                                                                   str(ant[self.dict_annots_indx.get("page_no")])
                                                            ))
            except pyodbc.Error as ex:
                st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        try:
            cursor.commit()
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))

    def deleteAnnot(self, cursor, ant):
        try:
            cursor.execute(self.dict_deletes.get("annots_del").format(str(ant[self.dict_annots_indx.get("book_no")]),
                                                                            str(ant[self.dict_annots_indx.get("page_no")])))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        try:
            cursor.commit()
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))

    def delete_bk(self, cursor, bk):
        try:
            cursor.execute(self.dict_deletes.get("bk_del").format(str(bk[self.dict_books_indx.get("no")])))
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))
        try:
            cursor.commit()
        except pyodbc.Error as ex:
            st.markdown(":red[" + self.dict_err_gener_msgs.get("cursor_exec") + "] " + str(ex))

    def __sql_bk_srch(self, isCountQuery, book):
        if isCountQuery:
            prefix_sqlStr = self.dict_queries.get("bk_add_edit_count")
        else:
            prefix_sqlStr = self.dict_queries.get("bk_add_edit")
        sqlStr = prefix_sqlStr.format(str(book[self.dict_books_indx.get("title")]))
        if not isCountQuery:
            sqlStr = sqlStr + self.dict_queries.get("bk_add_edit_order")
        return sqlStr

    def __sql_nw_annt_bk_srch(self, queryType, book):
        sqlStr = ""
        prefix_sqlStr = ""
        srchOnPub = True
        srchOnDate = True
        if queryType == "count":
            prefix_sqlStr = self.dict_queries.get("bk_fr_annot_add_count")
        elif queryType == "records":
            prefix_sqlStr = self.dict_queries.get("bk_fr_annot_add")
        # TODO - implement easier code here for publisher and dat and remove below after
        # if str(book[int(self.dict_books_indx.get("publisher"))]) != "":
        #     sqlStr = (sqlStr + self.dict_queries.get("bk_add_edit_pub")).format(str(book[int(self.dict_books_indx.get("publisher"))]))
        # if str(book[int(self.dict_books_indx.get("dat"))]) != "":
        if str(book[int(self.dict_books_indx.get("publisher"))]) == "":
            srchOnPub = False
        if str(book[int(self.dict_books_indx.get("dat"))]) == "":
            srchOnDate = False
        if not srchOnPub and not srchOnDate:
            sqlStr = prefix_sqlStr.format(str(book[int(self.dict_books_indx.get("title"))]),
                                          str(book[int(self.dict_books_indx.get("author"))]))
            if queryType == "records":
                sqlStr = sqlStr + self.dict_queries.get("append_bk_fr_annot_add")
        elif srchOnPub and srchOnDate:
            sqlStr = (prefix_sqlStr +
                     self.dict_queries.get("insert_bk_fr_annot_add_pub") +
                     self.dict_queries.get("insert_bk_fr_annot_add_date")).format(str(book[int(self.dict_books_indx.get("title"))]),
                                                                                  str(book[int(self.dict_books_indx.get("author"))]),
                                                                                  str(book[int(self.dict_books_indx.get("publisher"))]),
                                                                                  str(book[int(self.dict_books_indx.get("dat"))]))
            if queryType == "records":
                sqlStr = sqlStr + self.dict_queries.get("append_bk_fr_annot_add")
        elif srchOnPub and not srchOnDate:
            sqlStr = (prefix_sqlStr +
                      self.dict_queries.get("insert_bk_fr_annot_add_pub")).format(str(book[int(self.dict_books_indx.get("title"))]),
                                                                                  str(book[int(self.dict_books_indx.get("author"))]),
                                                                                  str(book[int(self.dict_books_indx.get("publisher"))]))
            if queryType == "records":
                sqlStr = sqlStr + self.dict_queries.get("append_bk_fr_annot_add")
        elif not srchOnPub and srchOnDate:
            sqlStr = (prefix_sqlStr +
                      self.dict_queries.get("insert_bk_fr_annot_add_date")).format(str(book[int(self.dict_books_indx.get("title"))]),
                                                                                   str(book[int(self.dict_books_indx.get("author"))]),
                                                                                   str(book[int(self.dict_books_indx.get("dat"))]))
            if queryType == "records":
                sqlStr = sqlStr + self.dict_queries.get("append_bk_fr_annot_add")
        return sqlStr

    dict_books_indx = {
        "no":                       0,
        "title":                    1,
        "author":                   2,
        "publisher":                3,
        "dat":                      4,
        "year_read":                5,
        "publication_locale":       6,
        "edition":                  7,
        "first_edition":            8,
        "first_edition_locale":     9,
        "first_edition_name":       10,
        "first_edition_publisher":  11
    }

    dict_annots_indx = {
        "book_no":                  0,
        "page_no":                  1,
        "source_text":              2,
    }

    dict_queries = {
        "books_all_count": """SELECT COUNT(*) 
                                  FROM Books""",
        "books_all": """SELECT * 
                            FROM Books 
                            ORDER BY [Book No]""",
        "books_max_key": "SELECT MAX([Book No]) FROM Books As Result",
        "annots_by_bk_count": """SELECT COUNT(*) 
                                     FROM [Source Text] 
                                     INNER JOIN Books 
                                     ON [Source Text].[Book No] = Books.[Book No] 
                                     WHERE Books.[Book Title] LIKE ('{}')""",
        "annots_by_bk_exact_count": """SELECT COUNT(*) 
                                 FROM [Source Text] WHERE [Source Text].[Book No] = ('{}')""",
        "annots_by_bk": """SELECT [Source Text].[Book No], [Source Text].[Page No], Books.[Book Title], Books.Author,
                                  [Source Text].[Source Text] 
                               FROM [Source Text] 
                               INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
                               WHERE Books.[Book Title] LIKE ('{}') 
                               ORDER BY Books.[Book Title], [Source Text].[Page No]""",
        "annots_by_auth_count": """SELECT COUNT(*) 
                                       FROM [Source Text] 
                                       INNER JOIN Books 
                                       ON [Source Text].[Book No] = Books.[Book No] 
                                       WHERE Books.Author LIKE ('{}')""",
        "annots_by_auth": """SELECT Books.Author, [Source Text].[Book No], [Source Text].[Page No], Books.[Book Title], 
                                    [Source Text].[Source Text] 
                                 FROM [Source Text] 
                                 INNER JOIN Books 
                                 ON [Source Text].[Book No] = Books.[Book No] 
                                 WHERE Books.Author LIKE ('{}') 
                                 ORDER BY [Source Text].[Book No], [Source Text].[Page No]""",
        "books_by_auth_count": """SELECT COUNT(*) 
                                    FROM [Books] 
                                    WHERE Books.Author LIKE ('{}')""",
        "books_by_auth": """SELECT [Books].[Book No], Books.[Book Title], [Books].[Author], Books.Publisher,
                                    Books.Dat 
                                FROM [Books] 
                                WHERE Books.Author LIKE ('{}') 
                                ORDER BY [Books].[Book No]""",
        "annots_by_sch_str_count": """SELECT COUNT(*) 
                                          FROM [Source Text] 
                                          INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
                                          WHERE [Source Text].[Source Text] Like ('{}')""",
        "annots_by_sch_str": """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No], 
                                        [Source Text].[Source Text] 
                                    FROM [Source Text] 
                                    INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
                                    WHERE [Source Text].[Source Text] LIKE ('{}')""",
        "annots_by_schstr_and_bk_count": """SELECT COUNT(*) 
                                                FROM [Source Text] 
                                                INNER JOIN Books 
                                                ON [Source Text].[Book No] = Books.[Book No] 
                                                WHERE (Books.[Book Title] LIKE ('{}')
                                                AND [Source Text].[Source Text] LIKE ('{}'))""",
        "annots_by_schstr_and_bk": """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No], 
                                            [Source Text].[Source Text] 
                                          FROM [Source Text] 
                                          INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
                                          WHERE (Books.[Book Title] LIKE ('{}') AND [Source Text].[Source Text] LIKE ('{}'))""",
        "annots_schstr_and_auth_count": """SELECT COUNT(*) 
                                               FROM [Source Text] 
                                               INNER JOIN Books 
                                               ON [Source Text].[Book No] = Books.[Book No]
                                               WHERE (Books.[Author] LIKE('{}') 
                                               AND [Source Text].[Source Text] LIKE('{}'))""",
        "annots_schstr_and_auth": """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No],
                            [Source Text].[Source Text]
                    FROM [Source Text] 
                    INNER JOIN Books 
                    ON [Source Text].[Book No] = Books.[Book No]
                    WHERE (Books.[Author] LIKE('{}') 
                    AND [Source Text].[Source Text] LIKE('{}'))""",
        "annots_by_yr_read_count": """SELECT COUNT(*)
                                          FROM [Source Text] 
                                          INNER JOIN Books 
                                          ON [Source Text].[Book No] = Books.[Book No]
                                          WHERE Books.[Year Read] BETWEEN ('{}') 
                                          AND ('{}')""",
        "annots_by_yr_read": """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No],
                        [Source Text].[Source Text], Books.[Year Read]
                    FROM [Source Text] 
                    INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No]
                    WHERE Books.[Year Read] BETWEEN ('{}') 
                    AND ('{}')
                    ORDER BY [Source Text].[Book No], [Source Text].[Page No]""",
        "books_by_yr_read_count": """SELECT COUNT(*) 
                    FROM Books 
                    WHERE Books.[Year Read] BETWEEN ('{}') AND ('{}')""",
        "books_by_yr_read": """SELECT * FROM Books 
                WHERE Books.[Year Read] BETWEEN ('{}') AND ('{}') 
                ORDER BY Books.[Book No]""",
        "bk_fr_annot_add": """SELECT Books.[Book No], [Book Title], Author, Publisher, Dat
                              FROM Books 
                              WHERE [Book Title] LIKE ('{}') AND Author LIKE ('{}')""",
        "bk_fr_annot_add_count": """SELECT COUNT(*) 
                          FROM Books
                          WHERE [Book Title] LIKE ('{}') AND Author LIKE ('{}')""",
        "new_annot_page_no_exists": """SELECT [Source Text].[Page No], [Source Text].[Source Text] 
                    FROM [Source Text]
                    WHERE [Source Text].[Book No] Like ('{}') 
                    AND [Source Text].[Page No] LIKE ('{}')""",
        "append_srch_txt": " OR [Source Text].[Source Text] Like ('{}')",
        "append_srch_txt_order_by": " ORDER BY [Source Text].[Book No], [Source Text].[Page No]",
        "insert_srch_txt_auth": " OR (Books.[Author] LIKE('{}') AND [Source Text].[Source Text] LIKE('{}'))",
        "insert_srch_txt_bk": " OR (Books.[Book Title] LIKE ('{}') AND [Source Text].[Source Text] LIKE ('{}'))",
        "insert_bk_fr_annot_add_pub": " AND Publisher LIKE ('{}')",
        "insert_bk_fr_annot_add_date": " AND Dat LIKE ('{}')",
        "append_bk_fr_annot_add": " ORDER BY [Book No]",
        "bk_add_edit_exact_count": """SELECT COUNT(*) 
                  FROM Books
                  WHERE [Book Title] = ('{}')""",
        "bk_add_edit_exact": """SELECT Books.[Book No], [Book Title], Author, Publisher, Dat, [Year Read], [Publication Locale], Edition,
                                 [First Edition], [First Edition Locale], [First Edition Name], [First Edition Publisher] 
                                FROM Books
                                WHERE [Book Title] = ('{}')""",
        "bk_add_edit_count": """SELECT COUNT(*) 
                                FROM Books
                                WHERE [Book Title] LIKE ('{}')""",
        "bk_add_edit": """SELECT Books.[Book No], [Book Title], Author, Publisher, Dat, [Year Read], [Publication Locale], Edition,
                                 [First Edition], [First Edition Locale], [First Edition Name], [First Edition Publisher]
                          FROM Books 
                          WHERE [Book Title] LIKE ('{}')""",
        "bk_add_edit_pub": " AND Publisher LIKE ('{}')",
        "bk_add_edit_date": " AND Dat LIKE ('{}')",
        "bk_add_edit_yr_rd": " AND [Year Read] LIKE ('{}')",
        "bk_add_edit_pb_lcl": " AND [Publication Locale] LIKE ('{}')",
        "bk_add_edit_edtn": " AND Edition LIKE ('{}')",
        "bk_add_edit_frst_edtn": " AND [First Edition] LIKE ('{}')",
        "bk_add_edit_frst_edtn_lcl": " AND [First Edition Locale] LIKE ('{}')",
        "bk_add_edit_date_frst_edtn_nm": " AND [First Edition Name] LIKE ('{}')",
        "bk_add_edit_date_frst_edtn_pb": " AND [First Edition Publisher] LIKE ('{}')",
        "bk_add_edit_order": " ORDER BY [Book No]"
    }

    dict_inserts = {
        "books_new_add": """INSERT INTO Books ([Book No], [Book Title], Author, Publisher, Dat, [Year Read], [Publication Locale],
                                               Edition, [First Edition], [First Edition Locale], [First Edition Name],
                                               [First Edition Publisher]) 
                            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""",
        "annots_new_add" : """INSERT INTO [Source Text] ([Book No], [Page No], [Source Text]) 
                              VALUES ('{}', '{}', '{}')"""
    }

    dict_updates = {
        "annots_update_add": """UPDATE [Source Text] SET [Source Text].[Source Text] = ('{}')
                                WHERE [Source Text].[Book No] = ('{}') AND [Source Text].[Page No] = ('{}')""",
        "books_update_add": """UPDATE Books SET Books.Author = ('{}'), Books.Publisher = ('{}'), 
                                      Books.Dat = ('{}'),
                                      Books.[Year Read] = ('{}'), Books.[Publication Locale] = ('{}'),
                                      Books.Edition = ('{}'), Books.[First Edition] = ('{}'),
                                      Books.[First Edition Locale] = ('{}'), Books.[First Edition Name] = ('{}'),
                                      Books.[First Edition Publisher] = ('{}')
                               WHERE Books.[Book No] = ('{}')"""
    }

    dict_deletes = {
        "annots_del": "DELETE FROM [Source Text] WHERE [Source Text].[Book No] = ('{}') AND [Source Text].[Page No] = ('{}')",
        "bk_del": "DELETE FROM Books WHERE Books.[Book No] = ('{}')",
        "annots_by_bk_exact_del": "DELETE FROM [Source Text] WHERE [Source Text].[Book No] = ('{}')"
    }