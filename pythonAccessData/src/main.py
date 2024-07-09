
# from src import db
import db

if __name__ == '__main__':

    # sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'r'DBQ=C:\Users\rober\databaseForPythonApp\SourceNew.mdb')
    sourceData = db.DATA_SOURCE(
        r'DRIVER={Microsoft Access Driver (*.mdb)};'r'DBQ=C:\Users\rober\databaseForPythonApp\SourceNew.mdb')

    # verify MS Access driver is available
    sourceData.is_ms_access_driver()

    conn = sourceData.db_connect()

    sourceData.report_tables(conn.cursor())

    # resCountBooksAll = sourceData.resBooksAll(conn.cursor())

    # books = sourceData.selectBooksAll(conn.cursor())

    # for bk in books:
    #   print(f"{bk.__getattribute__('Book No')}\t{bk.__getattribute__('Book Title')}\t{bk.Author}")
    #print("Found {} results.".format(resCountBooksAll))

    # resCountAnnotsAll = sourceData.resAnnotsAll(conn.cursor())

    # annots = sourceData.selectAnnotsAll(conn.cursor())

    # for ant in annots:
    #   print(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")
    #   print("Found {} results.".format(resCountAnnotsAll))

    # use \'' if single quote is in e.g. hitler's
    # resCountBooks = sourceData.resAnnotsbyBook(conn.cursor(), "%The Hundred-Year Marathon: China\''s%")

    # annots = sourceData.selectAnnotsbyBook(conn.cursor(), "%The Hundred-Year Marathon: China\''s%")

    # print("Found {} results.".format(resCountBooks))
    # for ant in annots:
    #     print(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountAuthor = sourceData.resAnnotsbyAuthor(conn.cursor(),
    #                                '%Tompk%')

    # annots = sourceData.selectAnnotsbyAuthor(conn.cursor(),
    #                               '%Tompk%')

    # print("Found {} results.".format(resCountAuthor))
    #for ant in annots:
    #    print(
    #        f"{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountSearchString = sourceData.resAnnotsbySearchString(conn.cursor(),
    #                               '%Hitler%')

    # annots = sourceData.selectAnnotsbySearchString(conn.cursor(),
    #                               '%Hitler%')

    #print("Found {} results.".format(resCountSearchString))
    # for ant in annots:
    #    print(
    #        f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountSrchStrAndBook = sourceData.resAnnotsbySrchStrAndBook(conn.cursor(),
    #                               '%Tesla%', '%Secrets of Anti%')

    # annots = sourceData.selectAnnotsbySrchStrAndBook(conn.cursor(),
    #                               '%Tesla%', '%Secrets of Anti%')

    # print("Found {} results.".format(resCountSrchStrAndBook))

    # for ant in annots:
    #    print(f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountSrchStrAndAuthor = sourceData.resAnnotsbySrchStrAndAuthor(conn.cursor(),
    #                                '%Marckus%', '%Cook%')
    # annots = sourceData.selectAnnotsbySrchStrAndAuthor(conn.cursor(),
    #                                '%Marckus%', '%Cook%')
    #print("Found {} results.".format(resCountSrchStrAndAuthor))
    # for ant in annots:
    #    print(
    #        f"{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountAnnotsYearRead = sourceData.resAnnotsbyYearRead(conn.cursor(),
    #                                           '2016', '2017')

    # annots = sourceData.selectAnnotsbyYearRead(conn.cursor(),
    #                                           '2016', '2017')

    # for ant in annots:
    #    print(
    #        f"{ant.__getattribute__('Year Read')}\t{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")
    # print("Found {} results.".format(resCountAnnotsYearRead))

    resCountBooksYearRead = sourceData.resBooksbyYearRead(conn.cursor(),
                                               '2010', '2015')

    annots = sourceData.selectBooksbyYearRead(conn.cursor(),
                                               '2010', '2015')

    print("Found {} results.".format(resCountBooksYearRead))
    for ant in annots:
        print(
            f"{ant.__getattribute__('Year Read')}\t{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}")

    conn.close()