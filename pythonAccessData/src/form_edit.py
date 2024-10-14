import sys
from datetime import datetime, date

import streamlit as st

import db

class EDIT_FORM:

    # def __init__(self):

    dict_edit_annot_sel = {
        "ants_edt_add": "Create new annotation",
        "ants_edt_add_bk_srch": "Search for book for new annotation",
        "ants_edt_edt": "Edit existing annotation",
        "ants_edt_dlt": "Delete an annotation",
        "ants_add_bk": "Add a new book"
    }

    dict_edit_annot_nonmenu_flags = {
        "ants_edt_add_srch_ppg_no": "search for page number"
    }
    dict_db_fld_validations = {
        "books_bk_no_len": 5,
        "books_bk_ttl_len": 250,
        "books_auth_len": 50,
        "books_pub_len": 50,
        "books_pub_locale": 50,
        "books_edition": 3,
        "first_edition_locale": 50,
        "first_edition_name": 50,
        "first_edition_publisher": 50,
        "annots_pg_no_len": 4
    }

    def annot_srch_bk(self):
        st.session_state["form_flow"] = "search_for_book_to_annotate"

    def annot_srch_bk_res(self):
        st.session_state["form_flow"] = "search_results_for_book_to_annotate"

    def annot_new_annot(self):
        st.session_state["form_flow"] = "create_the_new_annotation"

    def select_edit_form(self):
        st.header("Edit annotations data")
        editSelection = st.selectbox("Select data activity", [
            "---",
            self.dict_edit_annot_sel.get("ants_edt_add"),
            self.dict_edit_annot_sel.get("ants_edt_edt"),
            self.dict_edit_annot_sel.get("ants_edt_dlt"),
            self.dict_edit_annot_sel.get("ants_add_bk")
        ])
        if editSelection == self.dict_edit_annot_sel.get("ants_edt_add"):
            self.edt_new_annot()
        if editSelection == self.dict_edit_annot_sel.get("ants_edt_edt"):
            self.edt_edt_annot()
        if editSelection == self.dict_edit_annot_sel.get("ants_edt_dlt"):
            self.edt_dlt_annot()
        elif editSelection == self.dict_edit_annot_sel.get("ants_add_bk"):
            self.add_new_bk()

    def edt_new_annot(self):
        bkSum = -1
        bk_no = ""
        annot_page_no = ""
        if "form_flow" not in st.session_state:
            st.session_state["form_flow"] = "search_for_book_to_annotate"
        if "res_multi_books_for_new_annot" not in st.session_state:
            st.session_state["res_multi_books_for_new_annot"] = False # for clicking Back having selected book from multi-search dd
        if "orig_book_title" not in st.session_state:
            st.session_state["orig_book_title"] = "" # for clicking Back having selected book from multi-search dd
        if "orig_author" not in st.session_state:
            st.session_state["orig_author"] = "" # for clicking Back having selected book from multi-search dd
        if "orig_publisher" not in st.session_state:
            st.session_state["orig_publisher"] = "" # for clicking Back having selected book from multi-search dd
        if "orig_date_published" not in st.session_state:
            st.session_state["orig_date_published"] = "" # for clicking Back having selected book from multi-search dd
        if "book_title" not in st.session_state:
            st.session_state["book_title"] = ""
        if "author" not in st.session_state:
            st.session_state["author"] = ""
        if "author" not in st.session_state:
            st.session_state["publisher"] = ""
        if "author" not in st.session_state:
            st.session_state["date_published"] = ""
        if st.session_state["form_flow"] == "search_for_book_to_annotate":
            with st.form("Create a new annotation"):
                st.write(":green[Add new annotation]")
                st.session_state["book_title"] = st.text_input("Book title:red[*]",
                                                               max_chars=self.dict_db_fld_validations.get("books_bk_ttl_len"))
                st.session_state["author"] = st.text_input("Author:red[*]",
                                                           max_chars=self.dict_db_fld_validations.get("books_auth_len"))
                st.session_state["publisher"] = st.text_input("Publisher",
                                                              max_chars=self.dict_db_fld_validations.get("books_pub_len"))
                st.session_state["date_published"] = st.text_input("Date")
                search_books = st.form_submit_button(label="Search for book")
                if search_books:
                    if st.session_state["book_title"] == "":
                        st.markdown(":red[Book title must be given.]")
                    elif st.session_state["author"] == "":
                        st.markdown(":red[No author given]")
                    elif st.session_state["date_published"] != "" and not self.__isValidYearFormat(
                                                                                                   st.session_state["date_published"],
                                                                                            "%Y"
                                                                                                  ):
                        st.markdown(":red[Date of publication must be in YYYY format]")
                    else:
                        self.annot_srch_bk_res()
                        st.rerun()
        elif st.session_state["form_flow"] == "search_results_for_book_to_annotate":
            with st.form("Search book results"):
                book_search = []
                book_search.append(self.__format_sql_wrap(st.session_state["book_title"]))
                book_search.append(self.__format_sql_wrap(st.session_state["author"]))
                if st.session_state["publisher"] != "":
                    book_search.append(self.__format_sql_wrap(st.session_state["publisher"]))
                else:
                    book_search.append("")
                if st.session_state["date_published"] != "":
                    book_search.append(self.__format_sql_wrap(st.session_state["date_published"]))
                else:
                    book_search.append("")
                bkSum = self.db_records(self.dict_edit_annot_sel.get("ants_edt_add_bk_srch"), book_search, True)
                bks = self.db_records(self.dict_edit_annot_sel.get("ants_edt_add_bk_srch"), book_search, False)
                if bkSum > 1:
                    st.write("Found {} results.".format(str(bkSum)))
                add_nw_bk = False
                if bkSum == 0:
                    st.markdown(":red[Book was not found.]")
                    search_books_again = st.form_submit_button(label="Search for book again")
                    if search_books_again:
                        self.annot_srch_bk()
                        st.rerun()
                    add_new_book = st.form_submit_button(label="Add as new book")
                    if add_new_book:
                        add_nw_bk = True
                elif bkSum == 1:
                    st.markdown(":green[Book was found.]")
                    self.__show_bk_srch_res(bks)

                    # HERE ################################
                    #for b in bks:
                        #    bk_no = bks.__getattribute__('Book No')
                        #    st.write(b.__getattribute__('Book No'))
                    #print("bk no is " + str(bk_no))

                    btn_annot_go = st.form_submit_button(label="Create")
                    btn_annot_back = st.form_submit_button(label="Back")
                    if btn_annot_go:
                        if st.session_state["res_multi_books_for_new_annot"]:
                            st.session_state["res_multi_books_for_new_annot"] = False
                        self.annot_new_annot()
                        st.rerun()
                    elif btn_annot_back:
                       if st.session_state["res_multi_books_for_new_annot"]: # go back to multi-search result page with that data
                           st.session_state["book_title"] = st.session_state["orig_book_title"]
                           st.session_state["author"] = st.session_state["orig_author"]
                           st.session_state["publisher"] = st.session_state["orig_publisher"]
                           st.session_state["date_published"] = st.session_state["orig_date_published"]
                           st.session_state["res_multi_books_for_new_annot"] = False
                           self.annot_srch_bk_res()
                       else:
                            self.annot_srch_bk()
                       st.rerun()
                elif bkSum > 1:
                    editSelection = st.selectbox("Select book to annotate", [
                        "{title}>>{author}>>{publisher}>>{date}".format(
                            title = bk.__getattribute__('Book Title'),
                            author = bk.Author,
                            publisher = bk.Publisher,
                            date = bk.Dat
                            )
                        for bk in bks
                    ])
                    btn_book_select = st.form_submit_button(label="Select and annotate")
                    st.markdown(":orange[OR...]")
                    btn_book_again = st.form_submit_button(label="Refine the book search")
                    if btn_book_select:
                        book_selected = editSelection.split(">>")
                        for ctr in range(2, len(book_selected)): # i.e. non-mandatory fields pub, date pubed
                            if str(book_selected[ctr]) == "None":
                                book_selected.pop(ctr)
                                book_selected.insert(ctr, "")
                        st.session_state["orig_book_title"] = st.session_state["book_title"] # save srch to go back to multi-search result page
                        st.session_state["orig_author"] = st.session_state["author"]
                        st.session_state["orig_publisher"] = st.session_state["publisher"]
                        st.session_state["orig_date_published"] = st.session_state["date_published"]
                        st.session_state["res_multi_books_for_new_annot"] = True
                        st.session_state["book_title"] = str(book_selected[0])
                        st.session_state["author"] = str(book_selected[1])
                        st.session_state["publisher"] = str(book_selected[2])
                        st.session_state["date_published"] = str(book_selected[3])
                        self.annot_srch_bk_res()
                        st.rerun()
                    elif btn_book_again:
                        self.annot_srch_bk()
                        st.rerun()
            if add_nw_bk:
                self.add_new_bk()
        elif st.session_state["form_flow"] == "create_the_new_annotation":
            # TODO must set to FALSE when done (if was selected from multi-search result) -
            #  st.session_state["res_multi_books_for_new_annot"]
            with st.form("New annotation"):
                annot_page_no = st.text_input("Page number:red[*]", max_chars=4)
                btn_show_annot_textarea = st.form_submit_button(label="Go")
                if btn_show_annot_textarea:
                    if annot_page_no == "" or not annot_page_no.isdigit():
                        st.markdown(":red[Page number must entered as a number up to 4 digits.]")
                    else:
                        page_no_record = [bk_no.zfill(self.dict_db_fld_validations.get("books_bk_no_len")),
                                          annot_page_no.zfill(self.dict_db_fld_validations.get("annots_pg_no_len"))]

                        print("book no for sql is: " + str(page_no_record[0]))
                        print("page no for sql is: " + str(page_no_record[1]))

                        annot = self.db_records(self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_srch_ppg_no"), page_no_record,
                                                                         False)
                        i = 0
                        for ants in annot:
                            i = i + 1
                            print(str(i) + " " + ants.__getattribute__('Page No'))

                        annot_txt_area = st.text_area("Enter the annotation")

    def edt_edt_annot(self):
        st.write("Page is under construction - edit annotation. Check back real soon.")

    def edt_dlt_annot(self):
        st.write("Page is under construction - delete annotation. Check back real soon.")

    def add_new_bk(self):
        placeholder = st.empty()
        placeholder.title("Add new book")
        sbmt_bk = False
        with placeholder.form("Add new book"):
            st.write(":green[Add new book]")
            book_title = st.text_input("Book title:red[*]")
            author = st.text_input("Author:red[*]")
            publisher = st.text_input("Publisher")
            date_pub = st.text_input("Date")
            year_read = st.text_input("Year read")
            pub_location = st.text_input("Publication location")
            edition = st.text_input("Edition")
            first_edition = st.text_input("First edition")
            first_edition_locale = st.text_input("First edition location")
            first_edition_name = st.text_input("First edition name")
            first_edition_publisher = st.text_input("First edition publisher")
            add = st.form_submit_button("Add")
            if add:
                if not sbmt_bk:
                    sbmt_bk = True
                if book_title == "":
                    st.markdown(":red[No book title given]")
                    sbmt_bk = False
                elif len(book_title) > self.dict_db_fld_validations.get("books_bk_ttl_len"):
                    st.markdown(":red[Book title cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("books_bk_ttl_len"))))
                    sbmt_bk = False
                elif author == "":
                    st.markdown(":red[No author given]")
                    sbmt_bk = False
                elif len(author) > self.dict_db_fld_validations.get("books_auth_len"):
                    st.markdown(":red[Author cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("books_auth_len"))))
                    sbmt_bk = False
                elif len(publisher) > self.dict_db_fld_validations.get("books_pub_len"):
                    st.markdown(":red[Publisher cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("books_pub_len"))))
                    sbmt_bk = False
                elif date_pub != "" and not self.__isValidYearFormat(date_pub, "%Y"):
                    st.markdown(":red[Date of publication must be in YYYY format]")
                    sbmt_bk = False
                elif year_read != "" and not self.__isValidYearFormat(year_read, "%Y"):
                    st.markdown(":red[Year read must be in YYYY format]")
                    sbmt_bk = False
                elif len(pub_location) > self.dict_db_fld_validations.get("books_pub_locale"):
                    st.markdown(":red[Publication location cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("books_pub_locale"))))
                    sbmt_bk = False
                elif ((edition != "" and not edition.isdigit()) or
                      len(edition) > self.dict_db_fld_validations.get("books_edition")):
                    st.markdown(":red[Edition must be a number of not more than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("books_edition"))))
                    sbmt_bk = False
                elif first_edition != "" and not self.__isValidYearFormat(first_edition, "%Y"):
                    st.markdown(":red[First edition must be in YYYY format]")
                    sbmt_bk = False
                elif len(first_edition_locale) > self.dict_db_fld_validations.get("first_edition_locale"):
                    st.markdown(":red[First edition location cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("first_edition_locale"))))
                    sbmt_bk = False
                elif len(first_edition_name) > self.dict_db_fld_validations.get("first_edition_name"):
                    st.markdown(":red[First edition name cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("first_edition_name"))))
                    sbmt_bk = False
                elif len(first_edition_publisher) > self.dict_db_fld_validations.get("first_edition_publisher"):
                    st.markdown(":red[First edition publisher cannot be longer than {} characters]"
                                .format(str(self.dict_db_fld_validations.get("first_edition_publisher"))))
                    sbmt_bk = False
                if sbmt_bk:
                    book = []
                    book.append(book_title)
                    book.append(author)
                    book.append(publisher)
                    book.append(date_pub)
                    book.append(year_read)
                    book.append(pub_location)
                    book.append(edition)
                    book.append(first_edition)
                    book.append(first_edition_locale)
                    book.append(first_edition_name)
                    book.append(first_edition_publisher)
                    placeholder.empty()
                    self.db_records(self.dict_edit_annot_sel.get("ants_add_bk"), book, False)
        if sbmt_bk:
            st.success("New book added.")
            st.markdown(":blue[Title:] {}".format(book_title))
            st.markdown(":blue[Author:] {}".format(author))
            st.markdown(":blue[Publisher:] {}".format(publisher))
            st.markdown(":blue[Publication date:] {}".format(date_pub))
            st.markdown(":blue[Year read:] {}".format(year_read))
            st.markdown(":blue[Publication location:] {}".format(pub_location))
            st.markdown(":blue[Edition:] {}".format(edition))
            st.markdown(":blue[First edition:] {}".format(first_edition))
            st.markdown(":blue[First edition location:] {}".format(first_edition_locale))
            st.markdown(":blue[First edition name:] {}".format(first_edition_name))
            st.markdown(":blue[First edition publisher:] {}".format(first_edition_publisher))

    def db_records(self, searchSelection, record, getResultsCount):
        dbPath = sys.argv[1] + sys.argv[2]
        sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % dbPath)
        sourceData.is_ms_access_driver()
        conn = sourceData.db_connect()
        sourceData.report_tables(conn.cursor())
        if searchSelection == self.dict_edit_annot_sel.get("ants_add_bk"):
            self.__add_book(sourceData, conn, record)
        elif searchSelection == self.dict_edit_annot_sel.get("ants_edt_add_bk_srch"):
            return self.__srch_bks_for_new_annot(sourceData, conn, record, getResultsCount)
        elif searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_srch_ppg_no"):
            return self.__srch_ants_for_exists_annot(sourceData, conn, record)


        conn.close()

    def __add_book(self, sourceData, conn, book):
        bk_sum = str(sourceData.resBooksAll(conn.cursor()) + 1).zfill(self.dict_db_fld_validations.get("books_bk_no_len"))
        sourceData.addNewBook(conn.cursor(), bk_sum, book)

    def __srch_bks_for_new_annot(self, sourceData, conn, book, getResultsCount):
        if getResultsCount:
            bkSum = sourceData.resAddNewAnnot_srch_bk(conn.cursor(), book)
            return bkSum
        else:
            annots = sourceData.addNewAnnot_srch_bk(conn.cursor(), book)
            return annots

    def __srch_ants_for_exists_annot(self, sourceData, conn, record):
        return sourceData.addNewAnnot_srch_page_no(conn.cursor(), record)

    def __show_bk_srch_res(self, bks):
        for bk in bks:
            st.markdown(":blue[Title:] :orange[{}]\r\r".format(
                bk.__getattribute__('Book Title')))
            st.markdown(":gray[Author:] :orange[{}]\r\r".format(
                bk.Author))
            st.markdown(":gray[Publisher:] :orange[{}]\r\r".format(
                bk.Publisher))
            st.markdown(":gray[Date:] :orange[{}]\r\r".format(
                bk.Dat))


    def __isValidYearFormat(self,year, format):
        try:
            res = bool(datetime.strptime(year, format))
        except ValueError:
            res = False
        return res

    def __format_sql_wrap(self, searchDatum):
        datum = searchDatum
        if not searchDatum.startswith("%"):
            datum = "%" + datum
        if not searchDatum.endswith("%"):
            datum = datum + "%"
        datum = self.__formatSQLSpecialChars(datum)
        return datum

    def __formatSQLSpecialChars(self, searchDatum):
        formattedDatum = searchDatum.replace("'", "\''")
        formattedDatum = formattedDatum.replace("[", "[[]")
        return formattedDatum