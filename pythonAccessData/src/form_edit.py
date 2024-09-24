import sys
from datetime import datetime, date

import streamlit as st

import db

class EDIT_FORM:

    # def __init__(self):

    dict_edit_annot_sel = {
        "ants_edt_add": "Create new annotation",
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
        with st.form("Edit"):
            st.header("Edit annotations data")
            editSelection = st.selectbox("Select data activity", [
                "---",
                self.dict_edit_annot_sel.get("ants_edt_add"),
                self.dict_edit_annot_sel.get("ants_edt_edt"),
                self.dict_edit_annot_sel.get("ants_edt_dlt"),
                self.dict_edit_annot_sel.get("ants_add_bk")
            ])
            st.form_submit_button("Go")
            if editSelection == self.dict_edit_annot_sel.get("ants_edt_add"):
                self.edt_new_annot()
            if editSelection == self.dict_edit_annot_sel.get("ants_edt_edt"):
                self.edt_edt_annot()
            if editSelection == self.dict_edit_annot_sel.get("ants_edt_dlt"):
                self.edt_dlt_annot()
            elif editSelection == self.dict_edit_annot_sel.get("ants_add_bk"):
                self.add_new_bk()

    def edt_new_annot(self):
        st.write(":green[Add new annotation]")
        book_title = st.text_input("Book title:red[*]")
        author = st.text_input("Author:red[*]")
        publisher = st.text_input("Publisher")
        date = st.text_input("Date")
        txt = st.text_area("Enter new annotation")
        create = st.form_submit_button("Create")
        if create:
            if txt == "":
                st.markdown(":red[no text entered.]")

    def edt_edt_annot(self):
        st.write("Page is under construction - edit annotation. Check back real soon.")

    def edt_dlt_annot(self):
        st.write("Page is under construction - delete annotation. Check back real soon.")

    def add_new_bk(self):
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
                self.db_records(self.dict_edit_annot_sel.get("ants_add_bk"), book)

    def db_records(self, searchSelection, record):
        dbPath = sys.argv[1] + sys.argv[2]
        sourceData = db.DATA_SOURCE(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;' % dbPath)
        sourceData.is_ms_access_driver()
        conn = sourceData.db_connect()
        sourceData.report_tables(conn.cursor())

        if searchSelection == self.dict_edit_annot_sel.get("ants_add_bk"):
            self.__add_book(sourceData, conn, record)

        conn.close()

    def __add_book(self, sourceData, conn, book):
        bk_sum = str(sourceData.resBooksAll(conn.cursor()) + 1).zfill(self.dict_db_fld_validations.get("books_bk_no_len"))
        sourceData.addNewBook(conn.cursor(), bk_sum, book)

    def __isValidYearFormat(self,year, format):
        try:
            res = bool(datetime.strptime(year, format))
        except ValueError:
            res = False
        return res