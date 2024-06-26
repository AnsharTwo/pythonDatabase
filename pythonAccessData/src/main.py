
from src import db

if __name__ == '__main__':

    # verify MS Access driver is available
    db.is_ms_access_driver()

    conn = db.db_connect()

    db.report_tables(conn.cursor())

    # resCountBooksAll = db.resBooksAll(conn.cursor())

    # books = db.selectBooksAll(conn.cursor())

    # for bk in books:
    #   print(f"{bk.__getattribute__('Book No')}\t{bk.__getattribute__('Book Title')}\t{bk.Author}")
    # print("Found {} results.".format(resCountBooksAll))

    # resCountAnnotsAll = db.resAnnotsAll(conn.cursor())

    # annots = db.selectAnnotsAll(conn.cursor())

    # for ant in annots:
    #   print(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")
    # print("Found {} results.".format(resCountAnnotsAll))

    # use \'' if single quote is in e.g. hitler's
    # resCountBooks = db.resAnnotsbyBook(conn.cursor(), "%The Hundred-Year Marathon: China\''s%")

    # annots = db.selectAnnotsbyBook(conn.cursor(), "%The Hundred-Year Marathon: China\''s%")

    # print("Found {} results.".format(resCountBooks))
    # for ant in annots:
    #     print(f"{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountAuthor = db.resAnnotsbyAuthor(conn.cursor(),
    #                                '%Tompk%')

    # annots = db.selectAnnotsbyAuthor(conn.cursor(),
    #                               '%Tompk%')

    # print("Found {} results.".format(resCountAuthor))
    # for ant in annots:
    #    print(
    #        f"{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountSearchString = annots = db.resAnnotsbySearchString(conn.cursor(),
    #                               '%Hitler%')

    # annots = db.selectAnnotsbySearchString(conn.cursor(),
    #                               '%Hitler%')

    # print("Found {} results.".format(resCountSearchString))
    # for ant in annots:
    #    print(
    #        f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountSrchStrAndBook = db.resAnnotsbySrchStrAndBook(conn.cursor(),
    #                               '%Tesla%', '%Secrets of Anti%')

    # annots = db.selectAnnotsbySrchStrAndBook(conn.cursor(),
    #                               '%Tesla%', '%Secrets of Anti%')

    # print("Found {} results.".format(resCountSrchStrAndBook))

    # for ant in annots:
    #    print(f"{ant.__getattribute__('Book Title')}\t{ant.Author}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountSrchStrAndAuthor = db.resAnnotsbySrchStrAndAuthor(conn.cursor(),
    #                               '%Bell%', '%Cook%')
    # annots = db.selectAnnotsbySrchStrAndAuthor(conn.cursor(),
   #                                            '%Bell%', '%Cook%')
    # print("Found {} results.".format(resCountSrchStrAndAuthor))
    # for ant in annots:
    #    print(
    #        f"{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")

    # resCountAnnotsYearRead = db.resAnnotsbyYearRead(conn.cursor(),
    #                                           '2016', '2017')

    #annots = db.selectAnnotsbyYearRead(conn.cursor(),
    #                                           '2016', '2017')

    #for ant in annots:
    #    print(
    #        f"{ant.__getattribute__('Year Read')}\t{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}\t{ant.__getattribute__('Page No')}\t{ant.__getattribute__('Source Text')}")
    #print("Found {} results.".format(resCountAnnotsYearRead))

    resCountBooksYearRead = db.resBooksbyYearRead(conn.cursor(),
                                               '2005', '2007')

    annots = db.selectBooksbyYearRead(conn.cursor(),
                                               '2005', '2007')

    print("Found {} results.".format(resCountBooksYearRead))
    for ant in annots:
        print(
            f"{ant.__getattribute__('Year Read')}\t{ant.Author}\t{ant.__getattribute__('Book Title')}\t{ant.__getattribute__('Book No')}")

    conn.close()