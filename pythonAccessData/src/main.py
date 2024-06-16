
from src import db

if __name__ == '__main__':

    # verify MS Access driver is available
    db.is_ms_access_driver()

    conn = db.db_connect()

    db.report_tables(conn.cursor())

    # books = db.selectBooksAll(conn.cursor())

    # for bk in books:
    #   print(f"{bk.__getattribute__('Book No')}\t{bk.__getattribute__('Book Title')}\t{bk.Author}")

    # annots = db.selectAnnotsAll(conn.cursor())

    # for ant in annots:
    #   print(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # use \'' if single quote is in e.g. hitler's
    annots = db.selectAnnotsbyBook(conn.cursor(), "The Hundred-Year Marathon: China\''s Secret Strategy to Replace America as the Global Superpower")
    for ant in annots:
        print(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    conn.close()