import pyodbc

connStr = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'r'DBQ=C:\Users\rober\databaseForPythonApp\SourceNew.mdb')

def is_ms_access_driver():
    found = False
    for i in pyodbc.drivers():
        if i.startswith('Microsoft Access Driver'):
            found = True
            print(f'..found Microsoft Access Driver (*.mdb, *.accdb)')
    if not found:
        print(f'ERROR - Microsoft Access Driver not found.')

def db_connect():
    return pyodbc.connect(connStr)

def report_tables(cursor):
    print(f'listing tables in database found...')
    for i in cursor.tables(tableType='TABLE'):
        print(i.table_name)

def selectBooksAll(cursor):
    books = cursor.execute('SELECT * FROM Books ORDER BY [Book No]')
    return books

def selectAnnotsAll(cursor):
    annots = cursor.execute('SELECT * FROM [Source Text] ORDER BY [Book No]')
    return annots

# return by book/s
def selectAnnotsbyBook(cursor, book_title):
    annots = cursor.execute(
        """SELECT [Source Text].[Book No], [Source Text].[Page No], [Source Text].[Source Text] 
        FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
        WHERE Books.[Book Title] LIKE ('{}') ORDER BY [Source Text].[Page No]""".format(book_title))
    return annots

# return by author/s
def selectAnnotsbyAuthor(cursor, author):
    annots = cursor.execute(
        """SELECT Books.Author, [Source Text].[Book No], [Source Text].[Page No], [Source Text].[Source Text] 
        FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
        WHERE Books.Author LIKE ('{}') ORDER BY [Source Text].[Book No], [Source Text].[Page No]""".format(author))
    return annots

def resAnnotsbySearchString(cursor, searchString):

    results = cursor.execute(
        """SELECT COUNT(*) 
        FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
        WHERE [Source Text].[Source Text] LIKE ('{}') """.format(searchString))

    res = results.fetchone()
    return res[0]

def selectAnnotsbySearchString(cursor, searchString):
    annots = cursor.execute(
        """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No], 
        [Source Text].[Source Text] 
        FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
        WHERE [Source Text].[Source Text] LIKE ('{}') 
        ORDER BY [Source Text].[Book No], [Source Text].[Page No]""".format(searchString))

    return annots

def resAnnotsbySrchStrAndBook(cursor, searchString, book):
    results = cursor.execute("""SELECT COUNT(*) FROM [Source Text] INNER JOIN Books 
    ON [Source Text].[Book No] = Books.[Book No] 
    WHERE [Source Text].[Source Text] LIKE ('{}') 
    AND Books.[Book Title] LIKE ('{}') """.format(searchString, book))

    res = results.fetchone()
    return res[0]

def selectAnnotsbySrchStrAndBook(cursor, searchString, book):
    annots = cursor.execute(
        """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No], 
        [Source Text].[Source Text] 
        FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No] 
        WHERE [Source Text].[Source Text] LIKE ('{}') AND Books.[Book Title] LIKE ('{}') 
        ORDER BY [Source Text].[Book No], [Source Text].[Page No]""".format(searchString, book))

    return annots
def resAnnotsbySrchStrAndAuthor(cursor, searchString, author):
    results = cursor.execute(
        """SELECT COUNT(*) FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No]
        WHERE[Source Text].[Source Text] LIKE('{}') AND Books.[Author] LIKE('{}') """.format(searchString, author))

    res = results.fetchone()
    return res[0]

def selectAnnotsbySrchStrAndAuthor(cursor, searchString, author):
    annots = cursor.execute(
        """SELECT Books.[Book Title], Books.Author, [Source Text].[Book No], [Source Text].[Page No],
        [Source Text].[Source Text]
        FROM [Source Text] INNER JOIN Books ON [Source Text].[Book No] = Books.[Book No]
        WHERE [Source Text].[Source Text] LIKE ('{}') AND Books.[Author] LIKE ('{}')
        ORDER BY [Source Text].[Book No], [Source Text].[Page No]""".format(searchString, author))
    return annots

# return by year read

# return year range