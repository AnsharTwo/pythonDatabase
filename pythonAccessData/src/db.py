import pyodbc


class DATA_SOURCE:

    def __init__(self, connectString):
        self.connStr = connectString

    def __str__(self):
        return f"{self.connStr}"

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
        results = cursor.execute(self.dict_queries.get("books_all_count"))

        res = results.fetchone()
        return res[0]

    def selectBooksAll(self, cursor):
        books = cursor.execute(self.dict_queries.get("books_all"))
        return books

    def resAnnotsAll(self, cursor):
        results = cursor.execute(self.dict_queries.get("annots_all_count"))

        res = results.fetchone()
        return res[0]

    def selectAnnotsAll(self, cursor):
        annots = cursor.execute(self.dict_queries.get("annots_all"))
        return annots

    def resAnnotsbyBook(self, cursor, book_title):
        results = cursor.execute(self.dict_queries.get("annots_by_bk_count").format(book_title))

        res = results.fetchone()
        return res[0]


    def selectAnnotsbyBook(self, cursor, book_title):
        annots = cursor.execute(self.dict_queries.get("annots_by_bk").format(book_title))

        return annots

    def resAnnotsbyAuthor(self, cursor, author):
        results = cursor.execute(
            self.dict_queries.get("annots_by_auth_count").format(author))

        res = results.fetchone()
        return res[0]

    def selectAnnotsbyAuthor(self, cursor, author):
        annots = cursor.execute(self.dict_queries.get("annots_by_auth").format(author))

        return annots

    def resBooksByAuthor(self, cursor, author):
        results = cursor.execute(
            self.dict_queries.get("books_by_auth_count").format(author))

        res = results.fetchone()
        return res[0]

    def selectBooksByAuthor(self, cursor, author):
        annots = cursor.execute(self.dict_queries.get("books_by_auth").format(author))

        return annots

    def resAnnotsbySearchString(self, cursor, searchString):
        sqlStr = self.dict_queries.get("annots_by_sch_str_count")
        if len(searchString) == 1:
            results = cursor.execute(sqlStr.format(str(searchString[0])))
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])))
            for srchStrs in range(1, len(searchString)):
                sqlStr = sqlStr + self.dict_queries.get("append_srch_txt").format(str(searchString[srchStrs]))
            results = cursor.execute(sqlStr)
        res = results.fetchone()
        return res[0]

    def selectAnnotsbySearchString(self, cursor, searchString):
        sqlStr = self.dict_queries.get("annots_by_sch_str")
        if len(searchString) == 1:
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            annots = cursor.execute(sqlStr.format(str(searchString[0])))
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])))
            for srchStrs in range(1, len(searchString)):
                sqlStr = sqlStr + self.dict_queries.get("append_srch_txt").format(str(searchString[srchStrs]))
            sqlStr = sqlStr + self.dict_queries.get("append_srch_txt_order_by")
            annots = cursor.execute(sqlStr)
        return annots

    def resAnnotsbySrchStrAndBook(self, cursor, searchString, book):
        results = cursor.execute(self.dict_queries.get("annots_by_schstr_and_bk_count").format(searchString, book))

        res = results.fetchone()
        return res[0]

    def selectAnnotsbySrchStrAndBook(self, cursor, searchString, book):
        annots = cursor.execute(self.dict_queries.get("annots_by_schstr_and_bk").format(searchString, book))

        return annots
    def resAnnotsbySrchStrAndAuthor(self, cursor, author, searchString):
        sqlStr = self.dict_queries.get("annots_schstr_and_auth_count")
        print(str(searchString))
        if len(searchString) == 1:
            results = cursor.execute(sqlStr.format(author, str(searchString[0])))
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(author), 1)
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(str(searchString[0])), 1)
            for srchStrs in range(1, len(searchString)):
                sqlTemp = self.dict_queries.get("insert_srch_txt_auth")
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(author), 1)
                sqlTemp = sqlTemp.replace("('{}')", "('{}')".format(str(searchString[srchStrs])), 1)
                sqlStr = sqlStr + sqlTemp
            results = cursor.execute(sqlStr)
        res = results.fetchone()
        return res[0]

    def selectAnnotsbySrchStrAndAuthor(self, cursor, searchString, author):

        sqlStr = self.dict_queries.get("annots_schstr_and_auth")
        print("LEN IS " + str(len(searchString)))
        if len(searchString) == 1:
            annots = cursor.execute(sqlStr.format(author, str(searchString[0])))
        else:
            sqlStr = sqlStr.replace("('{}')", "('{}')".format(author, str(searchString[0])))
            for srchStrs in range(1, len(searchString)):
                sqlStr = sqlStr + self.dict_queries.get("append_srch_txt").format(str(searchString[srchStrs]))
            print("QQQQQQ " + sqlStr)
            annots = cursor.execute(sqlStr)

        return annots

# return by year read
    def resAnnotsbyYearRead(self, cursor, fromYear, toYear):
        results = cursor.execute(self.dict_queries.get("annots_by_yr_read_count").format(fromYear, toYear))

        res = results.fetchone()
        return res[0]

    def selectAnnotsbyYearRead(self, cursor, fromYear, toYear):
        annots = cursor.execute(self.dict_queries.get("annots_by_yr_read").format(fromYear, toYear))

        return annots

    def resBooksbyYearRead(self, cursor, fromYear, toYear):
        results = cursor.execute(self.dict_queries.get("books_by_yr_read_count").format(fromYear, toYear))

        res = results.fetchone()
        return res[0]

    def selectBooksbyYearRead(self, cursor, fromYear, toYear):
        annots = cursor.execute(self.dict_queries.get("books_by_yr_read").format(fromYear, toYear))

        return annots

    dict_queries = {
        "books_all_count": """SELECT COUNT(*) 
                                  FROM Books""",
        "books_all": """SELECT * 
                            FROM Books 
                            ORDER BY [Book No]""",
        "annots_all_count": """SELECT COUNT(*) 
                                   FROM [Source Text]""",
        "annots_all": """SELECT Books.[Book Title], Books.Author, [Source Text].[Page No], [Source Text].[Source Text]  
                             FROM [Source Text]
                             INNER JOIN Books
                             ON [Source Text].[Book No] = Books.[Book No] 
                             ORDER BY [Source Text].[Book No], [Source Text].[Page No]""",
        "annots_by_bk_count": """SELECT COUNT(*) 
                                     FROM [Source Text] 
                                     INNER JOIN Books 
                                     ON [Source Text].[Book No] = Books.[Book No] 
                                     WHERE Books.[Book Title] LIKE ('{}')""",
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
                                    Books.Date 
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
                                                WHERE [Source Text].[Source Text] LIKE ('{}') 
                                                AND Books.[Book Title] LIKE ('{}') """,
        "annots_by_schstr_and_bk": """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No], 
                                            [Source Text].[Source Text] 
                                          FROM [Source Text] 
                                          INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
                                          WHERE [Source Text].[Source Text] LIKE ('{}') 
                                          AND Books.[Book Title] LIKE ('{}') 
                                          ORDER BY [Source Text].[Book No], [Source Text].[Page No]""",
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
                    WHERE [Source Text].[Source Text] LIKE ('{}') 
                    AND Books.[Author] LIKE ('{}')
                    ORDER BY [Source Text].[Book No], [Source Text].[Page No]""",
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
        "append_srch_txt": " OR [Source Text].[Source Text] Like ('{}')",
        "append_srch_txt_order_by": " ORDER BY [Source Text].[Book No], [Source Text].[Page No]",
        "insert_srch_txt_auth": " OR (Books.[Author] LIKE('{}') AND [Source Text].[Source Text] LIKE('{}'))"
    }