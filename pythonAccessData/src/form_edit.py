import sys

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
        "books_bk_ttl_len": "250",
        "books_auth_len": "50"
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
        date = st.text_input("Date")
        year_read = st.text_input("Year read")
        pub_location = st.text_input("Publication location")
        edition = st.text_input("Edition")
        first_edition = st.text_input("First edition")
        first_edition_locale = st.text_input("First edition location")
        first_edition_name = st.text_input("First edition name")
        first_edition_publisher = st.text_input("First edition publisher")
        add = st.form_submit_button("Add")
        if add:
            if book_title == "":
                st.markdown(":red[No book title given]")
            else:
                if  len(book_title) > int(self.dict_db_fld_validations.get("books_bk_ttl_len")):
                    st.markdown(":red[Book title cannot be longer than {} characters]"
                                .format(self.dict_db_fld_validations.get("books_bk_ttl_len")))
                else:
                    if author == "":
                        st.markdown(":red[No author given]")
                    else:
                        if len(author) > int(self.dict_db_fld_validations.get("books_auth_len")):
                            st.markdown(":red[Author cannot be longer than {} characters]"
                                        .format(self.dict_db_fld_validations.get("books_auth_len")))
                        else:
                            # TODO add field len valid for all other fields here
                            book = []
                            book.append(book_title)
                            book.append(author)
                            book.append(publisher)
                            book.append(date)
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
        sourceData.resBooksAll(conn.cursor())
        bk_sum = str(sourceData.resBooksAll(conn.cursor()) + 1)
        sourceData.addNewBook(conn.cursor(), bk_sum, book)