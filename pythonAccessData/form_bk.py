import streamlit as st
import form_sr

class EDIT_BOOK(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_flow_flags = {
        "bk_add_update_bk": "Add or update a book",
        "bk_add_edit_is_full_match": "Book search for exact title match",
        "bk_add_edit_bk_write": "Book to database",
        "bk_del": "delete book",
        "bk_del_Annots_count": "deleted book annot count",
        "bk_del_Annots": "delete book assoc annotations"
    }

    dict_bk_rec_indx = {
        "bk_no": 0
    }

    dict_db_fld_validations = {
        "books_bk_no_len": 5,
        "books_bk_ttl_len": 250,
        "books_auth_len": 50,
        "books_pub_len": 50,
        "books_dat_pub_len": 4,
        "books_yr_rd": 4,
        "books_pub_locale": 50,
        "books_edition": 3,
        "books_frst_edition": 4,
        "first_edition_locale": 50,
        "first_edition_name": 50,
        "first_edition_publisher": 50,
        "annots_pg_no_len": 4
    }

    def add_updt_bk_srch(self):
        st.session_state["form_flow_bk"] = "add_update_book_search"

    def add_updt_bk(self):
        st.session_state["form_flow_bk"] = "add_update_book"

    def add_updt_bk_edit(self):
        st.session_state["form_flow_bk"] = "add_update_book_edit"

    def add_updt_bk_sbmttd(self):
        st.session_state["form_flow_bk"] = "add_update_book_sbmttd"

    def add_updt_bk_added(self):
        st.session_state["form_flow_bk"] = "add_update_book_added"

    def add_new_bk(self):
        if "form_flow_bk" not in st.session_state:
            st.session_state["form_flow_bk"] = "add_update_book_search"
        if "bk_srch_sum" not in st.session_state:
            st.session_state["bk_srch_sum"] = 0
        if "bk_is_editing" not in st.session_state:
            st.session_state["bk_is_editing"] = False
        if "bk_add_from_part_match" not in st.session_state:
            st.session_state["bk_add_from_part_match"] = False
        if "bk_res_multi_books_part_mtch_srch" not in st.session_state:
            st.session_state["bk_res_multi_books_part_mtch_srch"] = False
        if "del_bk" not in st.session_state:
            st.session_state["del_bk"] = False
        if "del_bk_yes" not in st.session_state:
            st.session_state["del_bk_yes"] = False
        if "del_bk_no" not in st.session_state:
            st.session_state["del_bk_no"] = False
        if "del_bk_has_annots" not in st.session_state:
            st.session_state["del_bk_has_annots"] = 0
        if "srch_book_title" not in st.session_state:
            st.session_state["srch_book_title"] = ""
        if "bk_book_title" not in st.session_state:
            st.session_state["bk_book_title"] = ""
        if "bk_author" not in st.session_state:
            st.session_state["bk_author"] = ""
        if "bk_publisher" not in st.session_state:
            st.session_state["bk_publisher"] = ""
        if "bk_date_pub" not in st.session_state:
            st.session_state["bk_date_pub"] = ""
        if "bk_year_read" not in st.session_state:
            st.session_state["bk_year_read"] = ""
        if "bk_pub_location" not in st.session_state:
            st.session_state["bk_pub_location"] = ""
        if "bk_edition" not in st.session_state:
            st.session_state["bk_edition"] = ""
        if "bk_first_edition" not in st.session_state:
            st.session_state["bk_first_edition"] = ""
        if "bk_first_edition_locale" not in st.session_state:
            st.session_state["bk_first_edition_locale"] = ""
        if "bk_first_edition_name" not in st.session_state:
            st.session_state["bk_first_edition_name"] = ""
        if "bk_first_edition_publisher" not in st.session_state:
            st.session_state["bk_first_edition_publisher"] = ""
        if "res1_bk_book_no" not in st.session_state:
            st.session_state["res1_bk_book_no"] = ""
        if "res1_bk_book_title" not in st.session_state:
            st.session_state["res1_bk_book_title"] = ""
        if "res1_bk_author" not in st.session_state:
            st.session_state["res1_bk_author"] = ""
        if "res1_bk_publisher" not in st.session_state:
            st.session_state["res1_bk_publisher"] = ""
        if "res1_bk_date_pub" not in st.session_state:
            st.session_state["res1_bk_date_pub"] = ""
        if "res1_bk_year_read" not in st.session_state:
            st.session_state["res1_bk_year_read"] = ""
        if "res1_bk_pub_location" not in st.session_state:
            st.session_state["res1_bk_pub_location"] = ""
        if "res1_bk_edition" not in st.session_state:
            st.session_state["res1_bk_edition"] = ""
        if "res1_bk_first_edition" not in st.session_state:
            st.session_state["res1_bk_first_edition"] = ""
        if "res1_bk_first_edition_locale" not in st.session_state:
            st.session_state["res1_bk_first_edition_locale"] = ""
        if "res1_bk_first_edition_name" not in st.session_state:
            st.session_state["res1_bk_first_edition_name"] = ""
        if "res1_bk_first_edition_publisher" not in st.session_state:
            st.session_state["res1_bk_first_edition_publisher"] = ""
        if "res1_bk_first_edition_publisher" not in st.session_state:
            st.session_state["res1_bk_first_edition_publisher"] = ""
        if "bk_orig_title" not in st.session_state:
            st.session_state["bk_orig_title"] = ""
        if st.session_state["form_flow_bk"] == "add_update_book_search":
            with st.form("Add or search for book to update"):
                bk_lookup = False
                st.write(":green[Add or update book]")
                st.session_state["srch_book_title"] = st.text_input("Book title:red[*]",
                                                                  max_chars=self.dict_db_fld_validations.get("books_bk_ttl_len"),
                                                                  value=st.session_state["res1_bk_book_title"])
                bk_go = st.form_submit_button("Go")
                if bk_go:
                    if not bk_lookup:
                        bk_lookup = True
                    if st.session_state["srch_book_title"] == "":
                        st.markdown(":red[No book title given]")
                        bk_lookup = False
                    if bk_lookup:
                        self.add_updt_bk()
                        st.rerun()
        if st.session_state["form_flow_bk"] == "add_update_book":
            bk_title = []
            bk_title.append(self.formatSQLSpecialChars(st.session_state["srch_book_title"])) # i.e. without padding with % (need exact mtch)
            st.session_state["bk_srch_sum"] = self.db_records(self.dict_flow_flags.get("bk_add_edit_is_full_match"),
                                                              bk_title,True)

            if st.session_state["bk_srch_sum"] != None:

                with st.form("Search results for book title"):
                    if st.session_state["bk_srch_sum"] == 1:
                        bk_rec = self.db_records(self.dict_flow_flags.get("bk_add_edit_is_full_match"), bk_title, False)
                        st.info("The following book has been found that matches your search text.")
                        for bk in bk_rec:
                            self.show_book_entered("blue", bk.__getattribute__('Book Title'), bk.Author, bk.Publisher, bk.Dat,
                                                     bk.__getattribute__('Year Read'), bk.__getattribute__('Publication Locale'),
                                                     bk.Edition, bk.__getattribute__('First Edition'),
                                                     bk.__getattribute__("First Edition Locale"), bk.__getattribute__("First Edition Name"),
                                                     bk.__getattribute__("First Edition Publisher"),
                                                     )
                            self.__add_bk_to_s_state(bk)
                        bk_title.pop(
                            0)  # rem as bk title is formatted for special chars and this will be done in sql wrap function below
                        bk_title.append(self.format_sql_wrap(st.session_state["srch_book_title"]))
                        btn_edt_bk = st.form_submit_button("Edit book")
                        btn_return_bk = st.form_submit_button("Search again")
                        if btn_return_bk:
                            if st.session_state["bk_res_multi_books_part_mtch_srch"]:
                                st.session_state["bk_res_multi_books_part_mtch_srch"] = False
                            self.__clear_ss_bk_flds()
                            self.__clear_ss_res1_bk_flds()
                            self.add_updt_bk_srch()
                            st.rerun()
                        if st.session_state["bk_res_multi_books_part_mtch_srch"]:
                            btn_bk_back = st.form_submit_button("Back to book selection")
                            btn_add_prt_mtch_multi_sel_bk = st.form_submit_button("Add as a new book")
                            if btn_bk_back:
                                st.session_state["srch_book_title"] = st.session_state["bk_orig_title"]
                                self.add_updt_bk()
                                st.rerun()
                            if btn_add_prt_mtch_multi_sel_bk:
                                st.session_state["bk_add_from_part_match"] = True
                                st.session_state["res1_bk_book_title"] = st.session_state["bk_orig_title"]
                                self.add_updt_bk_edit()
                                st.rerun()
                        if btn_edt_bk:
                            st.session_state["bk_is_editing"] = True
                            self.add_updt_bk_edit()
                            st.rerun()
                    else:
                        bk_title.insert(0, "0") # dummy val to set correct index for bk title
                        temp_bk_title = str(bk_title[1])
                        temp_bk_title = self.format_sql_wrap(temp_bk_title)
                        bk_title.pop(1)
                        bk_title.insert(1, temp_bk_title) # now search for partial match of book title
                        bk_sum = self.db_records(self.dict_flow_flags.get("bk_add_update_bk"), bk_title, True)
                        if bk_sum == 0: # so no partial match as well as no exact match
                            st.session_state["res1_bk_book_title"] = st.session_state["srch_book_title"] # to show for Add book form
                            self.add_updt_bk_edit()
                            st.rerun()
                        else:
                            if bk_sum == 1:
                                bk_rec = self.db_records(self.dict_flow_flags.get("bk_add_update_bk"), bk_title,
                                                     False)
                                st.info("One book partially matches your search.")
                                for bk in bk_rec:
                                    self.show_book_entered("blue", bk.__getattribute__('Book Title'), bk.Author,
                                                             bk.Publisher, bk.Dat,
                                                             bk.__getattribute__('Year Read'),
                                                             bk.__getattribute__('Publication Locale'),
                                                             bk.Edition, bk.__getattribute__('First Edition'),
                                                             bk.__getattribute__("First Edition Locale"),
                                                             bk.__getattribute__("First Edition Name"),
                                                             bk.__getattribute__("First Edition Publisher"),
                                                             )
                                btn_edt_prt_mtch_bk = st.form_submit_button("Edit book found")
                                btn_rtrn_prt_mtch_bk = st.form_submit_button("Return to book search/add")
                                btn_add_prt_mtch_bk = st.form_submit_button("Add title as new book")
                                if btn_rtrn_prt_mtch_bk:
                                    self.add_updt_bk_srch()
                                    st.rerun()
                                if btn_edt_prt_mtch_bk:
                                    st.session_state["bk_is_editing"] = True
                                    self.__add_bk_to_s_state(bk)
                                    self.add_updt_bk_edit()
                                    st.rerun()
                                if btn_add_prt_mtch_bk:
                                    st.session_state["bk_add_from_part_match"] = True
                                    st.session_state["res1_bk_book_title"] = st.session_state["srch_book_title"]
                                    self.add_updt_bk_edit()
                                    st.rerun()
                            elif bk_sum > 1:
                                bk_rec = self.db_records(self.dict_flow_flags.get("bk_add_update_bk"), bk_title,
                                                     False)
                                st.info(str(bk_sum) + " books partially match your search.")
                                editSelection = st.selectbox("Select book to work with", [
                                    "{title}>>{author}>>{publisher}>>{date}".format(
                                        title=bk.__getattribute__('Book Title'),
                                        author=bk.Author,
                                        publisher=bk.Publisher,
                                        date=bk.Dat
                                    )
                                    for bk in bk_rec
                                ])
                                btn_bk_sel = st.form_submit_button(label="Select this book")
                                st.markdown(":orange[OR...]")
                                btn_book_again = st.form_submit_button(label="Refine the book search")
                                if btn_bk_sel:
                                    st.session_state["bk_res_multi_books_part_mtch_srch"] = True
                                    book_selected = editSelection.split(">>")
                                    st.session_state["bk_orig_title"] = st.session_state["srch_book_title"]
                                    st.session_state["srch_book_title"] = str(book_selected[0])
                                    self.add_updt_bk()
                                    st.rerun()
                                elif btn_book_again:
                                    if st.session_state["bk_is_editing"]:
                                        st.session_state["bk_is_editing"] = False
                                    if st.session_state["bk_add_from_part_match"]:
                                        st.session_state["bk_add_from_part_match"] = False
                                    self.__clear_ss_bk_flds()
                                    self.__clear_ss_res1_bk_flds()
                                    self.add_updt_bk_srch()
                                    st.rerun()
        if st.session_state["form_flow_bk"] == "add_update_book_edit":
            with st.form("Add or update book"):
                sbmt_bk = False
                if st.session_state["bk_is_editing"]:
                    st.write(":green[Edit new book]")
                else:
                    st.write(":green[Add new book]")
                st.session_state["bk_book_title"] = st.text_input("Book title:red[*]",
                                                                  max_chars=self.dict_db_fld_validations.get("books_bk_ttl_len"),
                                                                  value=st.session_state["res1_bk_book_title"],
                                                                  disabled=st.session_state["bk_is_editing"])
                st.session_state["bk_author"] = st.text_input("Author:red[*]", max_chars=self.dict_db_fld_validations.get("books_auth_len"),
                                                               value=st.session_state["res1_bk_author"])
                st.session_state["bk_publisher"] = st.text_input("Publisher", max_chars=self.dict_db_fld_validations.get("books_pub_len"),
                                                                 value=st.session_state["res1_bk_publisher"])
                st.session_state["bk_date_pub"] = st.text_input("Date", max_chars=self.dict_db_fld_validations.get("books_dat_pub_len"),
                                                                value=st.session_state["res1_bk_date_pub"])
                st.session_state["bk_year_read"] = st.text_input("Year read", max_chars=self.dict_db_fld_validations.get("books_yr_rd"),
                                                                 value=st.session_state["res1_bk_year_read"])
                st.session_state["bk_pub_location"] = st.text_input("Publication location",
                                                                    max_chars=self.dict_db_fld_validations.get("books_pub_locale"),
                                                                    value=st.session_state["res1_bk_pub_location"])
                st.session_state["bk_edition"] = st.text_input("Edition", max_chars=self.dict_db_fld_validations.get("books_edition"),
                                                               value=st.session_state["res1_bk_edition"])
                st.session_state["bk_first_edition"] = st.text_input("First edition",
                                                                     max_chars=self.dict_db_fld_validations.get("books_frst_edition"),
                                                                     value=st.session_state["res1_bk_first_edition"])
                st.session_state["bk_first_edition_locale"] = st.text_input("First edition location",
                                                                            max_chars=self.dict_db_fld_validations.get("first_edition_locale"),
                                                                            value=st.session_state["res1_bk_first_edition_locale"])
                st.session_state["bk_first_edition_name"] = st.text_input("First edition name",
                                                                          max_chars=self.dict_db_fld_validations.get("first_edition_name"),
                                                                          value=st.session_state["res1_bk_first_edition_name"])
                st.session_state["bk_first_edition_publisher"] = st.text_input("First edition publisher",
                                                                               max_chars=self.dict_db_fld_validations.get("first_edition_publisher"),
                                                                               value=st.session_state["res1_bk_first_edition_publisher"])
                btn_discard_add_edit_bk = st.form_submit_button("Discard")
                if btn_discard_add_edit_bk:
                    if st.session_state["bk_is_editing"]:
                        st.session_state["bk_is_editing"] = False
                    if st.session_state["bk_add_from_part_match"]:
                        st.session_state["bk_add_from_part_match"] = False
                    if st.session_state["bk_res_multi_books_part_mtch_srch"]:
                        st.session_state["bk_res_multi_books_part_mtch_srch"] = False
                    self.__clear_ss_bk_flds()
                    self.__clear_ss_res1_bk_flds()
                    self.add_updt_bk_srch()
                    st.rerun()
                btn_add_edit = st.form_submit_button("Submit book")
                if btn_add_edit:
                    if not sbmt_bk:
                        sbmt_bk = True
                    if st.session_state["bk_book_title"] == "":
                        if not st.session_state["bk_is_editing"]:
                            st.markdown(":red[No book title given]")
                            sbmt_bk = False
                    elif st.session_state["bk_author"] == "":
                        st.markdown(":red[No author given]")
                        sbmt_bk = False
                    elif st.session_state["bk_date_pub"] != "" and not self.isValidYearFormat(st.session_state["bk_date_pub"],
                                                                                                "%Y"):
                        st.markdown(":red[Date of publication must be in YYYY format]")
                        sbmt_bk = False
                    elif st.session_state["bk_year_read"] != "" and not self.isValidYearFormat(st.session_state["bk_year_read"],
                                                                                                 "%Y"):
                        st.markdown(":red[Year read must be in YYYY format]")
                        sbmt_bk = False
                    elif st.session_state["bk_first_edition"] != "" and not self.isValidYearFormat(st.session_state["bk_first_edition"],
                                                                                                     "%Y"):
                        st.markdown(":red[First edition must be in YYYY format]")
                        sbmt_bk = False
                    if sbmt_bk:
                        self.add_updt_bk_sbmttd()
                        st.rerun()
                if st.session_state["bk_is_editing"]:
                    btn_del_bk = st.form_submit_button("Delete book")
                    if btn_del_bk:
                        st.session_state["del_bk"] = True
                        self.add_updt_bk_sbmttd()
                        st.rerun()
        if st.session_state["form_flow_bk"] == "add_update_book_sbmttd":
            with st.form("Book submission"):
                if not st.session_state["del_bk"]:
                    book = []
                    if st.session_state["bk_is_editing"]:
                        book.append(self.format_sql_wrap(st.session_state["res1_bk_book_no"]))
                    else:
                        book.append("")
                    book.append(self.format_sql_wrap(st.session_state["bk_book_title"]))
                    book.append(self.format_sql_wrap(st.session_state["bk_author"]))
                    book.append(self.append_for_db_write(st.session_state["bk_publisher"]))
                    book.append(self.append_for_db_write(st.session_state["bk_date_pub"]))
                    book.append(self.append_for_db_write(st.session_state["bk_year_read"]))
                    book.append(self.append_for_db_write(st.session_state["bk_pub_location"]))
                    book.append(self.append_for_db_write(st.session_state["bk_edition"]))
                    book.append(self.append_for_db_write(st.session_state["bk_first_edition"]))
                    book.append(self.append_for_db_write(st.session_state["bk_first_edition_locale"]))
                    book.append(self.append_for_db_write(st.session_state["bk_first_edition_name"]))
                    book.append(self.append_for_db_write(st.session_state["bk_first_edition_publisher"]))
                    if not st.session_state["bk_is_editing"]:
                        if st.session_state["bk_add_from_part_match"]:
                            bk_title = []
                            bk_title.append(self.formatSQLSpecialChars(
                                st.session_state["bk_book_title"]))  # i.e. without padding with % (need exact mtch)
                            temp_bk_sum = self.db_records(
                                self.dict_flow_flags.get("bk_add_edit_is_full_match"),
                                bk_title, True)

                            if temp_bk_sum != None:
                                print("Temp book sum is not None:" + str(temp_bk_sum))
                            else:
                                print("Temp book sum IS None:" + str(temp_bk_sum))

                            if temp_bk_sum != None:

                                if temp_bk_sum == 0:
                                    self.db_records(self.dict_flow_flags.get("bk_add_edit_bk_write"), book, False)
                                    self.add_updt_bk_added()
                                    st.rerun()
                                else:
                                    st.warning("Book title already exists.")
                                    btn_again_bk_add = st.form_submit_button("Return to book form")
                                    btn_abndn_bk_add = st.form_submit_button("Leave adding book")
                                    if btn_abndn_bk_add:
                                        if st.session_state["bk_is_editing"]:
                                            st.session_state["bk_is_editing"] = False
                                        if st.session_state["bk_add_from_part_match"]:
                                            st.session_state["bk_add_from_part_match"] = False
                                        self.__clear_ss_bk_flds()
                                        self.__clear_ss_res1_bk_flds()
                                        self.add_updt_bk_srch()
                                        st.rerun()
                                    if btn_again_bk_add:
                                        st.session_state["res1_bk_book_title"] = self.conv_none_for_db(st.session_state["srch_book_title"])
                                        st.session_state["res1_bk_author"] = self.conv_none_for_db(st.session_state["bk_author"])
                                        st.session_state["res1_bk_publisher"] = self.conv_none_for_db(st.session_state["bk_publisher"])
                                        st.session_state["res1_bk_date_pub"] = self.conv_none_for_db(st.session_state["bk_date_pub"])
                                        st.session_state["res1_bk_year_read"] = self.conv_none_for_db(st.session_state["bk_year_read"])
                                        st.session_state["res1_bk_pub_location"] = self.conv_none_for_db(st.session_state["bk_pub_location"])
                                        st.session_state["res1_bk_edition"] = self.conv_none_for_db(st.session_state["bk_edition"])
                                        st.session_state["res1_bk_first_edition"] = self.conv_none_for_db(st.session_state["bk_first_edition"])
                                        st.session_state["res1_bk_first_edition_locale"] = self.conv_none_for_db(st.session_state["bk_first_edition_locale"])
                                        st.session_state["res1_bk_first_edition_name"] = self.conv_none_for_db(st.session_state["bk_first_edition_name"])
                                        st.session_state["res1_bk_first_edition_publisher"] = self.conv_none_for_db(st.session_state["bk_first_edition_publisher"])
                                        self.__clear_ss_bk_flds()
                                        self.add_updt_bk_edit()
                                        st.rerun()

                            else:  # add form button if exception raised
                                st.form_submit_button("Form can't be displayed.", disabled=True)

                        else:
                            self.db_records(self.dict_flow_flags.get("bk_add_edit_bk_write"), book, False)
                            self.add_updt_bk_added()
                            st.rerun()
                    else:
                        self.db_records(self.dict_flow_flags.get("bk_add_edit_bk_write"), book, True)
                        self.add_updt_bk_added()
                        st.rerun()
                else:
                    del_book = []
                    del_book.append(st.session_state["res1_bk_book_no"].zfill(
                        self.dict_bk_rec_indx.get("bk_no")))
                    if not st.session_state["del_bk_yes"] and not st.session_state["del_bk_no"]:
                        bk_annots_warn = self.db_records(self.dict_flow_flags.get("bk_del_Annots_count"),
                                                        del_book, False)

                        if bk_annots_warn != None:

                            if bk_annots_warn > 0:
                                st.warning("WARNING: Book has " + str(bk_annots_warn) +  " annotations added. Confirm deletion of this book AND its annotations?")
                            else:
                                st.warning("Confirm deletion of this book?")
                            cols_del_bk = st.columns(2, gap="small", vertical_alignment="center")
                            if cols_del_bk[0].form_submit_button("Yes, delete"):
                                st.session_state["del_bk_yes"] = True
                                self.add_updt_bk_sbmttd()
                                st.rerun()
                            if cols_del_bk[1].form_submit_button("No, don't delete"):
                                st.session_state["del_bk_no"] = True
                                self.add_updt_bk_sbmttd()
                                st.rerun()
                        else:  # add form button if exception raised
                            st.form_submit_button("Form can't be displayed.", disabled=True)

                    if st.session_state["del_bk_yes"]:
                        self.db_records(self.dict_flow_flags.get("bk_del"),
                                        del_book, False)
                        bk_annots_cnt = self.db_records(self.dict_flow_flags.get("bk_del_Annots_count"),
                                        del_book, False)

                        if bk_annots_cnt != None:

                            if bk_annots_cnt > 0:
                                st.session_state["del_bk_has_annots"] = bk_annots_cnt
                                self.db_records(self.dict_flow_flags.get("bk_del_Annots"), del_book, False)
                            self.add_updt_bk_added()
                            st.rerun()

                        else:  # add form button if exception raised
                            st.form_submit_button("Form can't be displayed.", disabled=True)

                    elif st.session_state["del_bk_no"]:
                        st.session_state["del_bk"] = False
                        st.session_state["del_bk_no"] = False
                        self.add_updt_bk_edit()
                        st.rerun()
        if st.session_state["form_flow_bk"] == "add_update_book_added":
            with st.form("Book added"):
                if not st.session_state["bk_is_editing"]:
                    st.success("New book added.")
                else:
                    if st.session_state["del_bk"]:
                        if st.session_state["del_bk_has_annots"] == 0:
                            st.info("Book deleted.")
                        else:
                            st.info("""Book deleted (""" + str(st.session_state["del_bk_has_annots"]) + """ annotations 
                                    associated with this book were also deleted)""")
                    else:
                        st.success("Book updated.")
                        self.show_book_entered("blue", st.session_state["bk_book_title"], st.session_state["bk_author"],
                                                 st.session_state["bk_publisher"], st.session_state["bk_date_pub"],
                                                 st.session_state["bk_year_read"], st.session_state["bk_pub_location"],
                                                 st.session_state["bk_edition"], st.session_state["bk_first_edition"],
                                                 st.session_state["bk_first_edition_locale"], st.session_state["bk_first_edition_name"],
                                                 st.session_state["bk_first_edition_publisher"])
                btn_book_done = st.form_submit_button("Leave book add/edits")
                if btn_book_done:
                    if st.session_state["bk_is_editing"]:
                        st.session_state["bk_is_editing"] = False
                    if st.session_state["bk_add_from_part_match"]:
                        st.session_state["bk_add_from_part_match"] = False
                    if st.session_state["bk_res_multi_books_part_mtch_srch"]:
                        st.session_state["bk_res_multi_books_part_mtch_srch"] = False
                    if st.session_state["del_bk"]:
                        st.session_state["del_bk"] = False
                    if st.session_state["del_bk_yes"]:
                        st.session_state["del_bk_yes"] = False
                    if st.session_state["del_bk_no"]:
                        st.session_state["del_bk_no"] = False
                    st.session_state["del_bk_has_annots"] = 0
                    self.__clear_ss_bk_flds()
                    self.__clear_ss_res1_bk_flds()
                    self.add_updt_bk_srch()
                    st.rerun()

    def db_records(self, searchSelection, record, getResultsCount):
        sourceData = self.get_data_source()
        conn = self.get_connection(sourceData)
        if searchSelection == self.dict_flow_flags.get("bk_add_edit_is_full_match"):
            if getResultsCount:
                return self.__add_update_book_exact_count(sourceData, conn, record)
            else:
                return self.__add_update_book_exact(sourceData, conn, record)
        elif searchSelection == self.dict_flow_flags.get("bk_add_update_bk"):
            if getResultsCount:
                return self.__add_update_book_count(sourceData, conn, record)
            else:
                return self.__add_update_book(sourceData, conn, record)
        elif searchSelection == self.dict_flow_flags.get("bk_add_edit_bk_write"):
            self.__add_update_book_new(sourceData, conn, record, getResultsCount)
        elif searchSelection == self.dict_flow_flags.get("bk_del"):
            self.__delete_book(sourceData, conn, record)
        elif searchSelection == self.dict_flow_flags.get("bk_del_Annots_count"):
            return self.__bk_has_annots_count(sourceData, conn, record)
        elif searchSelection == self.dict_flow_flags.get("bk_del_Annots"):
            return self.__bk_has_annots_delete(sourceData, conn, record)
        conn.close()

    def __add_update_book_exact_count(self, sourceData, conn, book):
        bk_sum = sourceData.resAddUpdateExactBk(conn.cursor(), book)
        return(bk_sum)

    def __add_update_book_exact(self, sourceData, conn, book):
        bk = sourceData.AddUpdateExactBk(conn.cursor(), book)
        return bk

    def __add_update_book_count(self, sourceData, conn, book):
        bk_sum = sourceData.resAddUpdateNewBk(conn.cursor(), book)
        return(bk_sum)

    def __add_update_book(self, sourceData, conn, book):
        bk = sourceData.addUpdateNewBk(conn.cursor(), book)
        return bk

    def __add_update_book_new(self, sourceData, conn, book, bk_exists):
        bk_sum = 0
        for ctr in range(0, len(book)):
            tmp_fld = str(book[ctr])
            book.pop(ctr)
            book.insert(ctr, self.rem_sql_wrap_chars(tmp_fld))
        if not bk_exists:
            bk_sum = str(int(sourceData.resBookLatest(conn.cursor())) + 1).zfill(self.dict_db_fld_validations.get("books_bk_no_len"))
        sourceData.addUpdateNewBook(conn.cursor(), bk_sum, book, bk_exists)

    def __delete_book(self, sourceData, conn, book):
        sourceData.delete_bk(conn.cursor(), book)

    def __bk_has_annots_count(self, sourceData, conn, book):
        return sourceData.resExactAnnotsbyBook(conn.cursor(), book)

    def __bk_has_annots_delete(self, sourceData, conn, book):
        sourceData.delExactAnnotsbyBook(conn.cursor(), book)

    def __add_bk_to_s_state(self, bk):
        st.session_state["res1_bk_book_no"] = bk.__getattribute__('Book No')
        st.session_state["res1_bk_book_title"] = bk.__getattribute__('Book Title')
        st.session_state["res1_bk_author"] = bk.Author
        st.session_state["res1_bk_publisher"] = self.conv_none_for_db(bk.Publisher)
        st.session_state["res1_bk_date_pub"] = self.conv_none_for_db(bk.Dat)
        st.session_state["res1_bk_year_read"] = self.conv_none_for_db(bk.__getattribute__('Year Read'))
        st.session_state["res1_bk_pub_location"] = self.conv_none_for_db(
            bk.__getattribute__("Publication Locale"))
        st.session_state["res1_bk_edition"] = self.conv_none_for_db(bk.Edition)
        st.session_state["res1_bk_first_edition"] = self.conv_none_for_db(
            bk.__getattribute__("First Edition"))
        st.session_state["res1_bk_first_edition_locale"] = self.conv_none_for_db(
            bk.__getattribute__("First Edition Locale"))
        st.session_state["res1_bk_first_edition_name"] = self.conv_none_for_db(
            bk.__getattribute__("First Edition Name"))
        st.session_state["res1_bk_first_edition_publisher"] = self.conv_none_for_db(
            bk.__getattribute__("First Edition Publisher"))

    def __clear_ss_bk_flds(self):
        st.session_state["bk_book_title"] = ""
        st.session_state["bk_author"] = ""
        st.session_state["bk_publisher"] = ""
        st.session_state["bk_date_pub"] = ""
        st.session_state["bk_year_read"] = ""
        st.session_state["bk_pub_location"] = ""
        st.session_state["bk_edition"] = ""
        st.session_state["bk_first_edition"] = ""
        st.session_state["bk_first_edition_locale"] = ""
        st.session_state["bk_first_edition_name"] = ""
        st.session_state["bk_first_edition_publisher"] = ""

    def __clear_ss_res1_bk_flds(self):
        st.session_state["res1_bk_book_title"] = ""
        st.session_state["res1_bk_author"] = ""
        st.session_state["res1_bk_publisher"] = ""
        st.session_state["res1_bk_date_pub"] = ""
        st.session_state["res1_bk_year_read"] = ""
        st.session_state["res1_bk_pub_location"] = ""
        st.session_state["res1_bk_edition"] = ""
        st.session_state["res1_bk_first_edition"] = ""
        st.session_state["res1_bk_first_edition_locale"] = ""
        st.session_state["res1_bk_first_edition_name"] = ""
        st.session_state["res1_bk_first_edition_publisher"] = ""