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
    books = cursor.execute('select * from Books order by [Book No]')
    return books

def selectAnnotsAll(cursor):
    annots = cursor.execute('select * from [Source Text] order by [Book No]')
    return annots

# return by book/s
def selectAnnotsbyBook(cursor, book_title):
    annots = cursor.execute(
        """select [Source Text].[Book No], [Source Text].[Page No], [Source Text].[Source Text] 
        from [Source Text] inner join Books on [Source Text].[Book No] = Books.[Book No] 
        where Books.[Book Title] like ('{}') order by [Source Text].[Page No]""".format(book_title))
    return annots

# return by author/s
def selectAnnotsbyAuthor(cursor, author):
    annots = cursor.execute(
        """select Books.Author, [Source Text].[Book No], [Source Text].[Page No], [Source Text].[Source Text] 
        from [Source Text] inner join Books on [Source Text].[Book No] = Books.[Book No] 
        where Books.Author like ('{}') order by [Source Text].[Book No], [Source Text].[Page No]""".format(author))
    return annots

# return by keyword/s

# return by year read

# return year range