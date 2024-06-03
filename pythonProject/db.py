import pyodbc
def isMSAccessDriver():
    found = False
    for i in pyodbc.drivers():
        if i.startswith('Microsoft Access Driver'):
            found = True
            print(f'..found Microsoft Access Driver (*.mdb, *.accdb)')
    if not found:
        print(f'ERROR - Microsoft Access Driver not found.')

def dbConnect():
    conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'r'DBQ=C:\Users\rober\databaseForPythonApp\SourceNew.mdb')
    return pyodbc.connect(conn_str)

def reportTables(cursor):
    print(f'listing tables in database found...')
    for i in cursor.tables(tableType='TABLE'):
        print(i.table_name)
