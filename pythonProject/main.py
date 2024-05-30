import pyodbc

def dbConnect():
    conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=~C:\Users\rober\databaseForPythonApp\SourceNew.mdb;')

    # conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; rDBQ=~C:\Users\rober\databaseForPythonApp\SourceNew.accdb;'

    conn = pyodbc.connect(conn_str)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for i in pyodbc.drivers():
        if i.startswith('Microsoft Access Driver'):
            print(f'Microsoft Access Driver (*.mdb, *.accdb)')

    dbConnect()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
