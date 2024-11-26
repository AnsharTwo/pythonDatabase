import sys
from datetime import datetime, date
import streamlit as st
from spellchecker import SpellChecker
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
        "ants_edt_add_srch_ppg_no": "search for page number",
        "ants_edt_add_updte_annot": "add or update annotation"
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

    def annot_srch_bk(self):
        st.session_state["form_flow"] = "search_for_book_to_annotate"

    def annot_srch_bk_res(self):
        st.session_state["form_flow"] = "search_results_for_book_to_annotate"

    def annot_new_annot(self):
        st.session_state["form_flow"] = "create_the_new_annotation"

    def annot_do_new_annot(self):
        st.session_state["form_flow"] = "action_the_new_annotation"

    def spell_chk(self):
        st.session_state["form_flow"] = "spell_check_Annotation"

    def annot_success_new_annot(self):
        st.session_state["form_flow"] = "post_add_new_annotation"

    def updte_bk(self):
        st.session_state["form_flow_bk"] = "add_update_book"

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
        spell = SpellChecker("en", None, 4, None, False)
        spell_no_suggest = "no suggestions"
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
        if "book_no" not in st.session_state:
            st.session_state["book_no"] = ""
        if "book_title" not in st.session_state:
            st.session_state["book_title"] = ""
        if "author" not in st.session_state:
            st.session_state["author"] = ""
        if "publisher" not in st.session_state:
            st.session_state["publisher"] = ""
        if "date_published" not in st.session_state:
            st.session_state["date_published"] = ""
        if "page_no" not in st.session_state:
            st.session_state["page_no"] = ""
        if "annot_txt_area" not in st.session_state:
            st.session_state["annot_txt_area"] = ""
        if "annot_text" not in st.session_state:
            st.session_state["annot_text"] = ""
        if "annot_sql_done" not in st.session_state:
            st.session_state["annot_sql_done"] = False
        if "spell_txt_area" not in st.session_state:
            st.session_state["spell_txt_area"] = ""
        if "commit_spell_txt_area" not in st.session_state:
            st.session_state["commit_spell_txt_area"] = ""
        if "mis_spelled" not in st.session_state:
            st.session_state["mis_spelled"] = []
        if "has_annot" not in st.session_state:
            st.session_state["has_annot"] = None
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
                    book_search.append(self.__format_sql_wrap(str(st.session_state["date_published"])))
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
                    for bk in bks:
                        st.session_state["book_no"] = bk.__getattribute__('Book No')
                        st.session_state["book_title"] = bk.__getattribute__('Book Title')
                        st.session_state["author"] = bk.Author
                        st.session_state["publisher"] = self.conv_none_for_db(bk.Publisher)
                        st.session_state["date_published"] = self.conv_none_for_db(bk.Dat)
                    self.__show_bk_srch_res()
                    btn_annot_go = st.form_submit_button(label="Create or edit annotation")
                    btn_annot_back = st.form_submit_button(label="Back")
                    if btn_annot_go:
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
            with st.form("New annotation"):
                self.__show_bk_srch_res()
                annot_page_no = st.text_input("Page number:red[*]", max_chars=4)
                btn_show_annot_textarea = st.form_submit_button(label="Go")
                btn_annots_back = st.form_submit_button(label="Back to search results")
                if btn_annots_back:
                    self.annot_srch_bk_res()
                    st.rerun()
                if btn_show_annot_textarea:
                    if annot_page_no == "" or not annot_page_no.isdigit():
                        st.markdown(":red[Page number must entered as a number up to 4 digits.]")
                    else:
                        st.session_state["page_no"] = annot_page_no
                        self.annot_do_new_annot()
                        st.rerun()
        elif st.session_state["form_flow"] == "action_the_new_annotation":
            with st.form("New annotation"):
                st.markdown(":green[{}]".format(st.session_state["book_title"]))
                st.markdown(":rainbow[{}]\r\r".format(st.session_state["author"]))
                st.markdown(":blue[Page {}]".format(st.session_state["page_no"]))
                page_no_record = [st.session_state["book_no"], # is already len formatted
                                  st.session_state["page_no"].zfill(self.dict_db_fld_validations.get("annots_pg_no_len"))]
                annot = self.db_records(self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_srch_ppg_no"), page_no_record,
                                                                 False)
                if not st.session_state["annot_sql_done"]:
                    st.session_state["has_annot"] = False
                    for ants in annot:
                        st.session_state["annot_text"] = ants.__getattribute__('Source Text')
                    st.session_state["annot_sql_done"] = True
                if st.session_state["annot_text"] != "":
                    st.session_state["has_annot"] = True
                    st.markdown(":orange[(Page already has an annotation entered.)]")
                st.session_state["annot_txt_area"] = st.text_area("Enter the annotation", value=st.session_state["annot_text"], height=250)
                btn_spell_check = st.form_submit_button("Check spelling")
                if btn_spell_check:
                    illegal_txt = ["( ", " )", "[ ", " ]", "{ ", " }", "< ",
                                   " >"]  # these not compatible with :<markdown colour>[]
                    stops_txt = ["..."]
                    if st.session_state["annot_txt_area"] == "":
                        st.markdown(":red[No annotation to spell check.]")
                    elif self.__has_illegal_text(st.session_state["annot_txt_area"], illegal_txt):
                        st.markdown(":red[text cannot contain a bracket immediately enclosing a space chracter e.g. '( ', ' }'.]")
                    elif self.__has_illegal_text(st.session_state["annot_txt_area"], stops_txt):
                        st.markdown(":red[text cannot contain 3 consecutive full-stops (2 are allowed).]")
                    else:
                        self.spell_chk()
                        st.rerun()
                add_update_annot = st.form_submit_button("Add or update annotation")
                discard_doing_new_annot = st.form_submit_button("Discard annotation changes \ go back")
                if discard_doing_new_annot:
                    st.session_state["annot_sql_done"] = False
                    st.session_state["page_no"] = ""
                    st.session_state["annot_text"] = ""
                    self.annot_new_annot()
                    st.rerun()
                if add_update_annot:
                    if st.session_state["annot_txt_area"] == "":
                        st.markdown(":red[Annotation cannot be left empty]")
                    else:
                        annot_record = [st.session_state["book_no"],
                                        st.session_state["page_no"].zfill(self.dict_db_fld_validations.get("annots_pg_no_len")),
                                        self.__formatSQLSpecialChars(st.session_state["annot_txt_area"]).strip()
                                        ]
                        self.db_records(self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_updte_annot"),
                                        annot_record, st.session_state["has_annot"]) # NOTE this is NOT using wraps of % with __format_sql_wrap(), works.
                        st.session_state["annot_sql_done"] = False
                        st.session_state["annot_text"] = ""
                        self.annot_success_new_annot()
                        st.rerun()
        elif st.session_state["form_flow"] == "spell_check_Annotation":
            with st.form("Spell check annotation"):
                if st.session_state["spell_txt_area"] == "":
                    st.session_state["spell_txt_area"] =  st.session_state["annot_txt_area"]
                    spell_check_list = st.session_state["spell_txt_area"].split(" ")
                    for ctr in range(0, len(spell_check_list)):
                        splt_ln_list = str(spell_check_list[ctr]).splitlines()
                        if len(splt_ln_list) > 1:
                            spell_check_list.pop(ctr)
                            spell_check_list.insert(ctr, splt_ln_list[0])
                            splt_ln_list.pop(0)
                            while len(splt_ln_list) > 0:
                                spell_check_list.append(splt_ln_list[0])
                                splt_ln_list.pop(0)
                        splt_ln_list.clear()
                    spell_check_list = self.__format_spell_List_words(spell_check_list)
                    temp_wrds_unknwn = spell.unknown(spell_check_list)
                    temp_spell_list = []
                    ctr = 0
                    for wrd in spell_check_list:
                        for misp in temp_wrds_unknwn:
                            if str(wrd).lower() == str(misp).lower(): # misp will be lower case but in case :)...
                                temp_spell_list.insert(ctr, wrd)
                                ctr += 1
                    st.session_state["mis_spelled"] = temp_spell_list
                    hghlght_lst = st.session_state["spell_txt_area"].split(" ")
                    temp_spell_txt_wrds = st.session_state["spell_txt_area"].split(" ")
                    for mis in st.session_state["mis_spelled"]:
                        for h_wrd_indx in range(0, len(hghlght_lst)):
                            if str(hghlght_lst[h_wrd_indx]).find(":orange") == -1: # passover word that has been acted on already
                                if str(hghlght_lst[h_wrd_indx]).find(mis) != -1:
                                    wd = str(hghlght_lst[h_wrd_indx]).splitlines() # handle \n in split text area (not here in spell list)
                                    hghlght_lst.pop(h_wrd_indx)
                                    hghlght_lst.insert(h_wrd_indx, wd[0])
                                    tmp_wrd_frmt_lst = [str(hghlght_lst[h_wrd_indx])]
                                    tmp_wrd_frmt = self.__format_spell_List_words(tmp_wrd_frmt_lst)
                                    if len(tmp_wrd_frmt) > 0:
                                        if len(str(tmp_wrd_frmt[0])) == len(str(mis)):
                                            hghlght_lst.pop(h_wrd_indx)
                                            hghlght_lst.insert(h_wrd_indx, str(temp_spell_txt_wrds[h_wrd_indx]).replace(str(mis),
                                                                                                                ":orange[{}]".format(
                                                                                                                    str(mis)), 1))
                    st.session_state["spell_txt_area"] = ""
                    for h_wrd_indx in range(0, len(hghlght_lst)):
                        st.session_state["spell_txt_area"] = st.session_state["spell_txt_area"] + str(hghlght_lst[h_wrd_indx])
                        if h_wrd_indx < len(hghlght_lst):
                            st.session_state["spell_txt_area"] = st.session_state["spell_txt_area"] + " "
                st.markdown(st.session_state["spell_txt_area"])
                st.session_state["commit_spell_txt_area"] = st.session_state["annot_txt_area"]
                spell_data = []
                for mis in st.session_state["mis_spelled"]:
                    crrct = spell.correction(str(mis))
                    if str(crrct) == "None":
                        if spell_data.count(str(mis) + " -> " + spell_no_suggest) == 0:
                            spell_data.append(str(mis) + " -> " + spell_no_suggest)
                    else:
                        if spell_data.count(str(mis) + " -> " + str(crrct)) == 0:
                            spell_data.append(str(mis) + " -> " + str(crrct))
                    crrct = ""
                self.__checkbox_container(spell_data)
                spell_corrects_true = self.__get_selected_checkboxes()
                not_set_grn = []
                not_set_err = []
                for corrects in spell_corrects_true:
                    set_wrd_no_sggst = False
                    flagged = corrects.split(" -> ")
                    if flagged[1] != spell_no_suggest:
                        st.session_state["spell_txt_area"] = st.session_state["spell_txt_area"].replace(":orange[{}]".format(str(flagged[0])),
                                                                                                ":green[{}]".format(
                                                                                                    str(flagged[1])))
                    else:
                        not_set_grn.insert(len(not_set_grn), str(flagged[0]))
                        set_wrd_no_sggst = True
                    if not set_wrd_no_sggst and st.session_state["spell_txt_area"].find(":green[{}]".format(str(flagged[1]))) == -1:
                        not_set_err.insert(len(not_set_err), str(flagged[0]))
                if len(not_set_grn) > 0:
                    st.warning("the following words have no suggestions and will not be changed: :orange[" + str(not_set_grn) + "]")
                if len(not_set_err) > 0:
                    st.warning("""Word format error: the following words can be corrected, 
                    but an error has occured in highlighting this word.: :orange[""" + str(not_set_err) + """]""")
                vw_cng = st.form_submit_button("View changes")
                if vw_cng:
                    corrects_unseld = self.__get_unselected_checkboxes()
                    for corrects_revert in corrects_unseld:
                        unflagged = corrects_revert.split(" -> ")
                        if unflagged[1] != spell_no_suggest:
                            st.session_state["spell_txt_area"] = st.session_state["spell_txt_area"].replace(
                                ":green[{}]".format(str(unflagged[1])),
                                ":orange[{}]".format(
                                    str(unflagged[0])))
                    self.spell_chk()
                    st.rerun()
                cmt_cng = st.form_submit_button("Commit spelling")
                if cmt_cng:
                    spell_corrects_true = self.__get_selected_checkboxes()
                    for corrects in spell_corrects_true:
                        flagged = corrects.split(" -> ")
                        if flagged[1] != spell_no_suggest:
                            st.session_state["commit_spell_txt_area"] = st.session_state["commit_spell_txt_area"].replace(
                                flagged[0], flagged[1])
                    st.session_state["annot_text"] = st.session_state["commit_spell_txt_area"]
                    st.session_state["commit_spell_txt_area"] = ""
                    if st.session_state["spell_txt_area"] != "":
                        st.session_state["spell_txt_area"] = ""
                    st.session_state["mis_spelled"] = []
                    self.__rem_checkbox_ss_keys()
                    self.annot_do_new_annot()
                    st.rerun()
        elif st.session_state["form_flow"] == "post_add_new_annotation":
            with st.form("Annotation done."):
                st.success("Annotation added.")
                btn_add_anoth_annot = st.form_submit_button("Add or edit a new annotation")
                btn_not_add_annot = st.form_submit_button("Done")
                if btn_add_anoth_annot:
                    self.annot_new_annot()
                    st.rerun()
                if btn_not_add_annot:
                    st.session_state["res_multi_books_for_new_annot"] = False # was-multi-srch-result originally (for Back processing)
                    st.session_state["book_no"] = ""
                    st.session_state["book_title"] = ""
                    st.session_state["author"] = ""
                    st.session_state["publisher"] = ""
                    st.session_state["date_published"] = ""
                    self.annot_srch_bk()
                    st.rerun()

    def add_new_bk(self):

        # TODO = separate flow for add book
        if "form_flow_bk" not in st.session_state:
            st.session_state["form_flow_bk"] = "add_update_book"
        placeholder = st.empty()
        placeholder.title("Add new book")
        sbmt_bk = False
        with placeholder.form("Add new book"):
            st.write(":green[Add new book]")
            book_title = st.text_input("Book title:red[*]", max_chars=self.dict_db_fld_validations.get("books_bk_ttl_len"))
            author = st.text_input("Author:red[*]", max_chars=self.dict_db_fld_validations.get("books_auth_len"))
            publisher = st.text_input("Publisher", max_chars=self.dict_db_fld_validations.get("books_pub_len"))
            date_pub = st.text_input("Date", max_chars=self.dict_db_fld_validations.get("books_dat_pub_len"))
            year_read = st.text_input("Year read", max_chars=self.dict_db_fld_validations.get("books_yr_rd"))
            pub_location = st.text_input("Publication location", max_chars=self.dict_db_fld_validations.get("books_pub_locale"))
            edition = st.text_input("Edition", max_chars=self.dict_db_fld_validations.get("books_edition"))
            first_edition = st.text_input("First edition", max_chars=self.dict_db_fld_validations.get("books_frst_edition"))
            first_edition_locale = st.text_input("First edition location", max_chars=self.dict_db_fld_validations.get("first_edition_locale"))
            first_edition_name = st.text_input("First edition name", max_chars=self.dict_db_fld_validations.get("first_edition_name"))
            first_edition_publisher = st.text_input("First edition publisher", max_chars=self.dict_db_fld_validations.get("first_edition_publisher"))
            add = st.form_submit_button("Add")
            if add:
                if not sbmt_bk:
                    sbmt_bk = True
                if book_title == "":
                    st.markdown(":red[No book title given]")
                    sbmt_bk = False
                elif author == "":
                    st.markdown(":red[No author given]")
                    sbmt_bk = False
                elif date_pub != "" and not self.__isValidYearFormat(date_pub, "%Y"):
                    st.write("DATE: " + date_pub)
                    st.markdown(":red[Date of publication must be in YYYY format]")
                    sbmt_bk = False
                elif year_read != "" and not self.__isValidYearFormat(year_read, "%Y"):
                    st.markdown(":red[Year read must be in YYYY format]")
                    sbmt_bk = False
                elif first_edition != "" and not self.__isValidYearFormat(first_edition, "%Y"):
                    st.markdown(":red[First edition must be in YYYY format]")
                    sbmt_bk = False
                if sbmt_bk:
                    book = []
                    book.append(book_title)
                    book.append(author)
                    book.append(self.conv_none_for_db(publisher))
                    book.append(self.conv_none_for_db(date_pub))
                    book.append(self.conv_none_for_db(year_read))
                    book.append(self.conv_none_for_db(pub_location))
                    book.append(self.conv_none_for_db(edition))
                    book.append(self.conv_none_for_db(first_edition))
                    book.append(self.conv_none_for_db(first_edition_locale))
                    book.append(self.conv_none_for_db(first_edition_name))
                    book.append(self.conv_none_for_db(first_edition_publisher))
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

    def edt_edt_annot(self):
        st.write("Page is under construction - edit annotation. Check back real soon.")

    def edt_dlt_annot(self):
        st.write("Page is under construction - delete annotation. Check back real soon.")

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
        elif searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_updte_annot"):
            self.__add_update_annot(sourceData, conn, record, getResultsCount)
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

    def __add_update_annot(self, sourceData, conn, ant, annotExists):
        sourceData.addUpdateAnnot(conn.cursor(), ant, annotExists)

    def __show_bk_srch_res(self):
        st.markdown(":blue[Title:] :orange[{}]\r\r".format(
            st.session_state["book_title"]))
        st.markdown(":gray[Author:] :orange[{}]\r\r".format(
            st.session_state["author"]))
        st.markdown(":gray[Publisher:] :orange[{}]\r\r".format(
            st.session_state["publisher"]))
        st.markdown(":gray[Date:] :orange[{}]\r\r".format(
            st.session_state["date_published"]))

    def __checkbox_container(self, data):
            cols = st.columns(5, gap="small")
            if cols[1].form_submit_button('Select All'):
                for datum in data:
                    st.session_state['dynamic_checkbox_' + datum] = True
            if cols[2].form_submit_button('UnSelect All'):
                for datum in data:
                    st.session_state['dynamic_checkbox_' + datum] = False
            if cols[3].form_submit_button('Back/Discard'):
                st.session_state["annot_text"] = st.session_state["annot_txt_area"] # revoke to text in text area
                st.session_state["spell_txt_area"] = ""
                st.session_state["commit_spell_txt_area"] = ""
                st.session_state["mis_spelled"] = []
                self.__rem_checkbox_ss_keys()
                self.annot_do_new_annot()
                st.rerun()
            with st.popover("Suggested spellings"):
                for datum in data:
                    st.checkbox(datum, key='dynamic_checkbox_' + datum)

    def __get_selected_checkboxes(self):
        return [ky.replace('dynamic_checkbox_', '') for ky in st.session_state.keys() if
                ky.startswith('dynamic_checkbox_') and st.session_state[ky]]

    def __get_unselected_checkboxes(self):
        return [ky.replace('dynamic_checkbox_', '') for ky in st.session_state.keys() if
                ky.startswith('dynamic_checkbox_') and not st.session_state[ky]]

    def __rem_checkbox_ss_keys(self):
        for ky in st.session_state.keys():
            if ky.startswith('dynamic_checkbox_'):
                del ky

    def __format_spell_List_words(self, spell_check_list):
        temp_spell_check_list = spell_check_list
        split_wrds = False
        pref_postf_remd = False
        tmp_wrds = []
        for ctr in range(0, len(temp_spell_check_list)):
            if split_wrds:
                split_wrds = False
            if pref_postf_remd:
                pref_postf_remd = False
            if str(temp_spell_check_list[ctr]).find("..") != -1: # special case to handle all pos. instances of ..
                tmp_wrd = str(temp_spell_check_list[ctr])
                if tmp_wrd.startswith(".."):
                    tmp_wrd = tmp_wrd.lstrip("..")
                    pref_postf_remd = True
                if tmp_wrd.endswith(".."):
                    tmp_wrd = tmp_wrd.rstrip("..")
                    if not pref_postf_remd:
                        pref_postf_remd = True
                if tmp_wrd.count("..") > 0:
                    splt_wrds_indx = 0
                    wrds_to_add_spll_lst = []
                    while tmp_wrd.count("..") > 0:
                        split_wrds = True
                        tmp_wrds = tmp_wrd.split("..")
                        wrds_to_add_spll_lst.insert(splt_wrds_indx, tmp_wrds[0])
                        tmp_wrd = tmp_wrd.lstrip(str(tmp_wrds[0]) + "..")
                        splt_wrds_indx += 1
                    wrds_to_add_spll_lst.insert(splt_wrds_indx, tmp_wrds[1])
                    if split_wrds:
                        temp_spell_check_list.pop(ctr)
                        temp_spell_check_list.insert(ctr, str(wrds_to_add_spll_lst[0]))
                        w = 1
                        for w in range(1, len(wrds_to_add_spll_lst)):
                            temp_spell_check_list.append(str(wrds_to_add_spll_lst[w]))
                        wrds_to_add_spll_lst.clear()
                    tmp_wrds.clear()
                else:
                    if pref_postf_remd:
                        temp_spell_check_list.pop(ctr)
                        temp_spell_check_list.insert(ctr, tmp_wrd)
        trim_chars_list = ["\"'", "'\"", "'.", ".'"] # works - add more multi-char if not caught by single char list below
        for chr in trim_chars_list:
            for sp_ctr in range(0, len(temp_spell_check_list)):
                if str(temp_spell_check_list[sp_ctr]).find(str(chr)) != -1:
                    temp_char = str(temp_spell_check_list[sp_ctr])
                    temp_spell_check_list.pop(sp_ctr)
                    temp_spell_check_list.insert(sp_ctr, temp_char.replace(str(chr), ""))
        trim_char_list = ['"', """'""", "", ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "<", ">", "?", "!", "£", "$"]
        for chr in trim_char_list:
            for sp_ctr in range(0, len(temp_spell_check_list)):
                if str(temp_spell_check_list[sp_ctr]).find(str(chr)) == 0:
                    temp_char = str(temp_spell_check_list[sp_ctr])
                    temp_spell_check_list.pop(sp_ctr)
                    temp_spell_check_list.insert(sp_ctr, temp_char.replace(str(chr), "", 1))
                if str(temp_spell_check_list[sp_ctr]).rfind(str(chr), 1) != -1:
                    temp_char = str(temp_spell_check_list[sp_ctr])
                    temp_spell_check_list.pop(sp_ctr)
                    temp_spell_check_list.insert(sp_ctr, temp_char.replace(str(chr), "", 1))
        return temp_spell_check_list

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
        return formattedDatum

    def __format_page_no(self, pageNo):
        return pageNo.lstrip("0")

    def __format_book_no(self, bookNo):
        return bookNo.lstrip("0")

    def __has_illegal_text(self, txt_area, illegal_txt):
        is_illegal_txt = False
        for il_txt in illegal_txt:
            if txt_area.find(il_txt) != -1:
                is_illegal_txt = True
        return is_illegal_txt

    def conv_none_for_db(self, fld_val):
        if fld_val == None:
            return ""
        else:
            return fld_val