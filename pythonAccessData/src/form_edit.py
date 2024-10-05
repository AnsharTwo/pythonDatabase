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
    }

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
        placeholder = st.empty()
        can_search = False
        bkSum = -1
        placeholder.title("Add new annotation")
        with (placeholder.form("Create a new annotation")):
            st.write(":green[Add new annotation]")
            book_title = st.text_input("Book title:red[*]")
            author = st.text_input("Author:red[*]")
            publisher = st.text_input("Publisher")
            date_pub = st.text_input("Date")
            search_books = st.form_submit_button(label="Search for book")
            if not search_books and not st.session_state.get("submit_srch_bks"):
                st.stop()
            st.session_state["submit_srch_bks"] = True
            if not can_search:
                can_search = True
            if book_title == "":
                st.markdown(":red[Book title must be given.]")
                can_search = False
            elif len(book_title) > self.dict_db_fld_validations.get("books_bk_ttl_len"):
                st.markdown(":red[Book title cannot be longer than {} characters]"
                            .format(str(self.dict_db_fld_validations.get("books_bk_ttl_len"))))
                can_search = False
            elif author == "":
                st.markdown(":red[No author given]")
                can_search = False
            elif len(author) > self.dict_db_fld_validations.get("books_auth_len"):
                st.markdown(":red[Author cannot be longer than {} characters]"
                            .format(str(self.dict_db_fld_validations.get("books_auth_len"))))
                can_search = False
            elif len(publisher) > self.dict_db_fld_validations.get("books_pub_len"):
                st.markdown(":red[Publisher cannot be longer than {} characters]"
                            .format(str(self.dict_db_fld_validations.get("books_pub_len"))))
                can_search = False
            elif date_pub != "" and not self.__isValidYearFormat(date_pub, "%Y"):
                st.markdown(":red[Date of publication must be in YYYY format]")
                can_search = False
            if can_search:
                book_search = []
                book_search.append(self.__format_sql_wrap(book_title))
                book_search.append(self.__format_sql_wrap(author))
                if publisher != "":
                    book_search.append(self.__format_sql_wrap(publisher))
                else:
                    book_search.append("")
                if date_pub != "":
                    book_search.append(self.__format_sql_wrap(date_pub))
                else:
                    book_search.append("")
                bkSum = self.db_records(self.dict_edit_annot_sel.get("ants_edt_add_bk_srch"), book_search)
        placeholder = st.empty()
        placeholder.title("Book search")
        with placeholder.form("Search book results"):
            add_nw_bk = False
            if bkSum > 0:
                st.write("Found {} results.".format(str(bkSum)))
            if bkSum == 0:
                st.markdown(":red[Book was not found.]")
                search_books_again = st.form_submit_button(label="Search for book again")
                add_new_book = st.form_submit_button(label="Add as new book")
                if not  search_books_again and not add_new_book:
                    st.stop()
                st.session_state["submit_srch_bks"] = False
                if add_new_book:
                    add_nw_bk = True
                if search_books_again:
                    placeholder.empty()
            elif bkSum == 1:
                btn_annot_go = st.form_submit_button(label="Create")
                btn_annot_cancel = st.form_submit_button(label="Discard")
                if not btn_annot_go and not btn_annot_cancel:
                    st.stop()
                st.session_state["submit_srch_bks"] = False
                if btn_annot_go:
                    annot_page_no = st.text_input("Page number", max_chars=4)
                    annot_txt_area = st.text_area("Enter the annotation")
                if btn_annot_cancel:
                    placeholder.empty()
            elif bkSum > 1:
                btn_book_again = st.form_submit_button(label="More than 1 book found. Refine the book search")
                if not btn_book_again:
                    st.stop()
                st.session_state["submit_srch_bks"] = False
                if btn_book_again:
                    placeholder.empty()
        if add_nw_bk:
            self.add_new_bk()

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
                    self.db_records(self.dict_edit_annot_sel.get("ants_add_bk"), book)
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

    def db_records(self, searchSelection, record):
        dbPath = sys.argv[1] + sys.argv[2]
        sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % dbPath)
        sourceData.is_ms_access_driver()
        conn = sourceData.db_connect()
        sourceData.report_tables(conn.cursor())
        if searchSelection == self.dict_edit_annot_sel.get("ants_add_bk"):
            self.__add_book(sourceData, conn, record)
        elif searchSelection == self.dict_edit_annot_sel.get("ants_edt_add_bk_srch"):
            return self.__srch_bks_for_new_annot(sourceData, conn, record)
        conn.close()

    def __add_book(self, sourceData, conn, book):
        bk_sum = str(sourceData.resBooksAll(conn.cursor()) + 1).zfill(self.dict_db_fld_validations.get("books_bk_no_len"))
        sourceData.addNewBook(conn.cursor(), bk_sum, book)

    def __srch_bks_for_new_annot(self, sourceData, conn, book):
        bkSum = sourceData.resAddNewAnnot_srch_bk(conn.cursor(), book)
        return bkSum

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
