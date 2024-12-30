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
        "bk_add_update_bk": "Add or update a book"
    }

    dict_edit_annot_nonmenu_flags = {
        "ants_edt_add_srch_ppg_no": "search for page number",
        "ants_edt_add_updte_annot": "add or update annotation",
        "bk_add_edit_bk_res_0": "Add a new book"
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

    dict_separators = {
        "spell_chkbx_indx_prfix": "{^pos.",
        "spell_chk_grn_prefix_len": 6,
        "spell_chk_orng_prefix_len": 7
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

    def add_updt_bk_srch(self):
        st.session_state["form_flow_bk"] = "add_update_book_search"

    def add_updt_bk(self):
        st.session_state["form_flow_bk"] = "add_update_book"

    def add_updt_bk_sbmttd(self):
        st.session_state["form_flow_bk"] = "add_update_book_sbmttd"

    def add_updt_bk_added(self):
        st.session_state["form_flow_bk"] = "add_update_book_added"

    def select_edit_form(self):
        st.header("Edit annotations data")
        editSelection = st.selectbox("Select data activity", [
            "---",
            self.dict_edit_annot_sel.get("ants_edt_add"),
            self.dict_edit_annot_sel.get("ants_edt_edt"),
            self.dict_edit_annot_sel.get("ants_edt_dlt"),
            self.dict_edit_annot_sel.get("bk_add_update_bk")
        ])
        if editSelection == self.dict_edit_annot_sel.get("ants_edt_add"):
            self.edt_new_annot()
        if editSelection == self.dict_edit_annot_sel.get("ants_edt_edt"):
            self.edt_edt_annot()
        if editSelection == self.dict_edit_annot_sel.get("ants_edt_dlt"):
            self.edt_dlt_annot()
        elif editSelection == self.dict_edit_annot_sel.get("bk_add_update_bk"):
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
        if "visited_spell_check" not in st.session_state:
            st.session_state["visited_spell_check"] = False
        if "spell_txt_area" not in st.session_state:
            st.session_state["spell_txt_area"] = ""
        if "has_annot" not in st.session_state:
            st.session_state["has_annot"] = False
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
                # TODO - use function created for add update book below
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
                    if not st.session_state["visited_spell_check"]:
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
                    st.session_state["has_annot"] = False
                    st.session_state["visited_spell_check"] = False
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
                        st.session_state["has_annot"] = False
                        st.session_state["visited_spell_check"] = False
                        st.session_state["annot_text"] = ""
                        self.annot_success_new_annot()
                        st.rerun()
        elif st.session_state["form_flow"] == "spell_check_Annotation":
            if not st.session_state["visited_spell_check"]:
                st.session_state["visited_spell_check"] = True
            with st.form("Spell check annotation"):
                # TODO - can this be moved to top of func
                if "mis_spelled" not in st.session_state:
                    st.session_state["mis_spelled"] = []
                if st.session_state["spell_txt_area"] == "":
                    st.session_state["spell_txt_area"] = st.session_state["annot_txt_area"]
                    spell_check_list = st.session_state["spell_txt_area"].split(" ")
                    has_newlines = False
                    where_newlines = []
                    for ctr in range(0, len(spell_check_list)): # rem newline chars
                        tmp_trimmed = str(spell_check_list[ctr]).strip()
                        spell_check_list.pop(ctr)
                        spell_check_list.insert(ctr, tmp_trimmed)
                        splt_ln_list = str(spell_check_list[ctr]).splitlines()
                        if len(splt_ln_list) > 1:
                            has_newlines = True
                            for i in range(0, len(splt_ln_list)):
                                where_newlines.append(str(splt_ln_list[i]))
                            spell_check_list.pop(ctr)
                            spell_check_list.insert(ctr, str(splt_ln_list[0]))
                            splt_ln_list.pop(0)
                            splt_ctr = 0
                            while len(splt_ln_list) > 0:
                                splt_ctr += 1
                                spell_check_list.insert(ctr + splt_ctr, str(splt_ln_list[0]))
                                splt_ln_list.pop(0)
                        splt_ln_list.clear()
                    if has_newlines:
                        st.warning("""(new lines have been removed: {} 
                                       If you commit, please reformat the text with new lines as desired).""".format(str(where_newlines)))
                    # TODO TASK - here V, implement removal of .. and nline chars, with a map list to reassemble them into spell markdown text
                    # and can remove warning above for nl removed. See code in drinks xls. (note index of 2 words btaiend form one i.e.
                    # word1..word2 or word1nlword2 will have to be catered for in temp_spell_list (to make popover checkboxes) variable below.
                    # code to remove .. was worngly in __format_spell_List_words() (too late, as afte rebuild spell text area) and needed
                    # rewrite as used strip() incorrectly as now fixed elsewhere.
                    st.session_state["spell_txt_area"] = self.__rebuild_txt_area(spell_check_list) # This updates with any extra words from dealing with splitline newline porcess above
                    spell_check_list = self.__format_spell_List_words(spell_check_list)
                    temp_wrds_unknwn = spell.unknown(spell_check_list)
                    temp_spell_list = []
                    ctr = 0
                    for wrd in range(0, len(spell_check_list)):
                        for misp in temp_wrds_unknwn:
                            if str(spell_check_list[wrd]).lower() == str(misp).lower(): # misp will be lower case but in case :)...
                                temp_spell_list.insert(ctr, str(spell_check_list[wrd]) + "||" + str(wrd))
                                ctr += 1
                    st.session_state["mis_spelled"] = temp_spell_list
                    temp_wrds_unknwn.clear()
                    hghlght_lst = st.session_state["spell_txt_area"].split(" ")
                    for mis in range(0, len(st.session_state["mis_spelled"])):
                        spll_map_indx = self.__get_spell_map_index_split(str(st.session_state["mis_spelled"][mis]))
                        temp_hghlght_wrd = str(hghlght_lst[spll_map_indx])
                        hghlght_lst.pop(spll_map_indx)
                        hghlght_lst.insert(spll_map_indx, ":orange[{}]".format(temp_hghlght_wrd))
                    st.session_state["spell_txt_area"] = self.__rebuild_txt_area(hghlght_lst)
                st.markdown(st.session_state["spell_txt_area"])
                spell_data = []
                for mis in range(0, len(st.session_state["mis_spelled"])):
                    spll_wrd = self.__get_spell_word_split(str(st.session_state["mis_spelled"][mis]))
                    spll_map_indx = self.__get_spell_map_index_split(str(st.session_state["mis_spelled"][mis]))
                    crrct = spell.correction(spll_wrd)
                    if str(crrct) == "None":
                        spell_data.append(spll_wrd + " -> " + spell_no_suggest + " {^pos. " + str(spll_map_indx) + "}")
                    else:
                            spell_data.append(spll_wrd + " -> " + str(crrct) +  " {^pos. " + str(spll_map_indx) + "}")
                self.__checkbox_container(spell_data)
                spell_corrects_true = self.__get_selected_checkboxes()
                hghlght_lst = st.session_state["spell_txt_area"].split(" ") # already formatted split lines and spelling format
                st.session_state["spell_txt_area"] = ""
                for corrects in range(0, len(spell_corrects_true)):
                    flagged = spell_corrects_true[corrects].split(" -> ")
                    spll_map_indx = self.__get_spell_chkbox_indx(str(flagged[1]))
                    spll_wrd = self.__get_spell_chkbx_split(str(flagged[0]))
                    sggstn = self.__get_spell_chkbox_sggstn(str(str(flagged[1])))
                    temp_hghlght_wrd = str(hghlght_lst[spll_map_indx])
                    if temp_hghlght_wrd.find(":orange[") != -1:
                        temp_hghlght_wrd = self.__rem_markdown_colour(temp_hghlght_wrd,
                                                                      self.dict_separators.get(
                                                                          "spell_chk_orng_prefix_len"))
                    if flagged[1].find(spell_no_suggest) != -1:
                        hghlght_lst.pop(spll_map_indx)
                        hghlght_lst.insert(spll_map_indx, ":orange[{}]".format(temp_hghlght_wrd))
                    else:
                        temp_hghlght_wrd = temp_hghlght_wrd.replace(spll_wrd, sggstn)
                        hghlght_lst.pop(spll_map_indx)
                        if temp_hghlght_wrd.find(":green[") == -1:
                            hghlght_lst.insert(spll_map_indx, ":green[{}]".format(temp_hghlght_wrd))
                        else:
                            hghlght_lst.insert(spll_map_indx, temp_hghlght_wrd)
                st.session_state["spell_txt_area"] = self.__rebuild_txt_area(hghlght_lst)
                vw_cng = st.form_submit_button("View changes")
                if vw_cng:
                    hghlght_lst = st.session_state["spell_txt_area"].split(" ")
                    st.session_state["spell_txt_area"] = ""
                    corrects_unseld = self.__get_unselected_checkboxes()
                    for corrects_revert in range(0, len(corrects_unseld)):
                        unflagged = str(corrects_unseld[corrects_revert]).split(" -> ")
                        if unflagged[1].find(spell_no_suggest) == -1:
                            spll_map_indx = self.__get_spell_chkbox_indx(str(unflagged[1]))
                            spll_wrd = self.__get_spell_chkbx_split(str(unflagged[0]))
                            sggstn = self.__get_spell_chkbox_sggstn(str(unflagged[1]))
                            temp_hghlght_wrd = str(hghlght_lst[spll_map_indx])
                            if temp_hghlght_wrd.find(":green[") != -1:
                                temp_hghlght_wrd = self.__rem_markdown_colour(temp_hghlght_wrd,
                                                                              self.dict_separators.get("spell_chk_grn_prefix_len"))
                                temp_hghlght_wrd = temp_hghlght_wrd.replace(sggstn, spll_wrd)
                            hghlght_lst.pop(spll_map_indx)
                            if temp_hghlght_wrd.find(":orange[") == -1:
                                hghlght_lst.insert(spll_map_indx, ":orange[{}]".format(temp_hghlght_wrd))
                            else:
                                hghlght_lst.insert(spll_map_indx, temp_hghlght_wrd)
                    st.session_state["spell_txt_area"] = self.__rebuild_txt_area(hghlght_lst)
                    self.spell_chk()
                    st.rerun()
                cmt_cng = st.form_submit_button("Commit spelling")
                if cmt_cng:
                    hghlght_lst = st.session_state["spell_txt_area"].split(" ")
                    st.session_state["spell_txt_area"] = ""
                    for rems in range(0, len(hghlght_lst)): # remove ALL words' green and orange markdown formatting
                        tmp_rem = str(hghlght_lst[rems])
                        if tmp_rem.find(":orange[") != -1:
                            tmp_rem = self.__rem_markdown_colour(tmp_rem,
                                                                          self.dict_separators.get(
                                                                          "spell_chk_orng_prefix_len"))
                            hghlght_lst.pop(rems)
                            hghlght_lst.insert(rems, tmp_rem)
                        elif tmp_rem.find(":green[") != -1:
                            tmp_rem = self.__rem_markdown_colour(tmp_rem,
                                                                          self.dict_separators.get(
                                                                          "spell_chk_grn_prefix_len"))
                            hghlght_lst.pop(rems)
                            hghlght_lst.insert(rems, tmp_rem)
                    st.session_state["spell_txt_area"] = self.__rebuild_txt_area(hghlght_lst)
                    st.session_state["annot_text"] = st.session_state["spell_txt_area"]
                    st.session_state["spell_txt_area"] = ""
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
        if "form_flow_bk" not in st.session_state:
            st.session_state["form_flow_bk"] = "add_update_book_search"
        if "bk_srch_sum" not in st.session_state:
            st.session_state["bk_srch_sum"] = 0
        if "bk_is_editing" not in st.session_state:
            st.session_state["bk_is_editing"] = False
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

        #########################
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
            #########################

        if st.session_state["form_flow_bk"] == "add_update_book":

            #########################
            bk_title = []
            bk_title.append(self.__format_sql_wrap(st.session_state["srch_book_title"]))
            # TODO - first needs to do exact match query as in flow chart
            st.session_state["bk_srch_sum"] = self.db_records(self.dict_edit_annot_sel.get("bk_add_update_bk"),
                                                              bk_title,
                                                              True)
            with st.form("Search results for book title"):

                st.write("title " + st.session_state["srch_book_title"])
                st.write("Sum " + str(st.session_state["bk_srch_sum"]))

                if st.session_state["bk_srch_sum"] == 1:
                    st.info("The following book has been found that matches your search text.")
                    btn_edt_bk = st.form_submit_button("Edit book")
                    btn_return_bk = st.form_submit_button("Search again")
                #########################



            with st.form("Add or update book"):
                sbmt_bk = False
                st.write(":green[Add new book]")
                st.session_state["bk_book_title"] = st.text_input("Book title:red[*]",
                                                                  max_chars=self.dict_db_fld_validations.get("books_bk_ttl_len"),
                                                                  value=st.session_state["res1_bk_book_title"])
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
                add = st.form_submit_button("Add")
                if add:
                    if not sbmt_bk:
                        sbmt_bk = True
                    if st.session_state["bk_book_title"] == "":
                        st.markdown(":red[No book title given]")
                        sbmt_bk = False
                    elif st.session_state["bk_author"] == "":
                        st.markdown(":red[No author given]")
                        sbmt_bk = False
                    elif st.session_state["bk_date_pub"] != "" and not self.__isValidYearFormat(st.session_state["bk_date_pub"],
                                                                                                "%Y"):
                        st.markdown(":red[Date of publication must be in YYYY format]")
                        sbmt_bk = False
                    elif st.session_state["bk_year_read"] != "" and not self.__isValidYearFormat(st.session_state["bk_year_read"],
                                                                                                 "%Y"):
                        st.markdown(":red[Year read must be in YYYY format]")
                        sbmt_bk = False
                    elif st.session_state["bk_first_edition"] != "" and not self.__isValidYearFormat(st.session_state["bk_first_edition"],
                                                                                                     "%Y"):
                        st.markdown(":red[First edition must be in YYYY format]")
                        sbmt_bk = False
                    if sbmt_bk:
                        self.add_updt_bk_sbmttd()
                        st.rerun()
        if st.session_state["form_flow_bk"] == "add_update_book_sbmttd":
            book = []
            book.append(self.__format_sql_wrap(st.session_state["bk_book_title"]))
            book.append(self.__format_sql_wrap(st.session_state["bk_author"]))
            book.append(self.__append_for_db_write(st.session_state["bk_publisher"]))
            book.append(self.__append_for_db_write(st.session_state["bk_date_pub"]))
            book.append(self.__append_for_db_write(st.session_state["bk_year_read"]))
            book.append(self.__append_for_db_write(st.session_state["bk_pub_location"]))
            book.append(self.__append_for_db_write(st.session_state["bk_edition"]))
            book.append(self.__append_for_db_write(st.session_state["bk_first_edition"]))
            book.append(self.__append_for_db_write(st.session_state["bk_first_edition_locale"]))
            book.append(self.__append_for_db_write(st.session_state["bk_first_edition_name"]))
            book.append(self.__append_for_db_write(st.session_state["bk_first_edition_publisher"]))
            if not st.session_state["bk_is_editing"]:
                st.session_state["bk_srch_sum"] = self.db_records(self.dict_edit_annot_sel.get("bk_add_update_bk"), book, True)
            if st.session_state["bk_srch_sum"] == 0:
                if st.session_state["bk_is_editing"]:
                    self.db_records(self.dict_edit_annot_sel.get("bk_add_edit_bk_res_0"), book, True) # get res count bool not ideal name for this
                else:
                    self.db_records(self.dict_edit_annot_sel.get("bk_add_edit_bk_res_0"), book, False)
            elif st.session_state["bk_srch_sum"] == 1:
                bk_rec = self.db_records(self.dict_edit_annot_sel.get("bk_add_update_bk"), book, False)
                for bk in bk_rec:
                    st.session_state["res1_bk_book_title"] = bk.__getattribute__('Book Title')
                    st.session_state["res1_bk_author"] = bk.Author
                    st.session_state["res1_bk_publisher"] = bk.Publisher
                    st.session_state["res1_bk_date_pub"] = self.conv_none_for_db(bk.Dat)
                    st.session_state["res1_bk_year_read"] = self.conv_none_for_db(bk.__getattribute__('Year Read'))
                    st.session_state["res1_bk_pub_location"] = self.conv_none_for_db(bk.__getattribute__("Publication Locale"))
                    st.session_state["res1_bk_edition"] = self.conv_none_for_db(bk.Edition)
                    st.session_state["res1_bk_first_edition"] = self.conv_none_for_db(bk.__getattribute__("First Edition"))
                    st.session_state["res1_bk_first_edition_locale"] = self.conv_none_for_db(bk.__getattribute__("First Edition Locale"))
                    st.session_state["res1_bk_first_edition_name"] = self.conv_none_for_db(bk.__getattribute__("First Edition Name"))
                    st.session_state["res1_bk_first_edition_publisher"] = self.conv_none_for_db(bk.__getattribute__("First Edition Publisher"))
            self.add_updt_bk_added()
            st.rerun()
        if st.session_state["form_flow_bk"] == "add_update_book_added":
            with st.form("Book added"):
                if st.session_state["bk_srch_sum"] == 0: # must be 0 (set to) for all add ops
                    st.success("New book added.")
                    self.__show_book_entered("blue", st.session_state["bk_book_title"], st.session_state["bk_author"],
                                             st.session_state["bk_publisher"], st.session_state["bk_date_pub"],
                                             st.session_state["bk_year_read"], st.session_state["bk_pub_location"],
                                             st.session_state["bk_edition"], st.session_state["bk_first_edition"],
                                             st.session_state["bk_first_edition_locale"], st.session_state["bk_first_edition_name"],
                                             st.session_state["bk_first_edition_publisher"])
                    if st.session_state["bk_is_editing"]:
                        st.session_state["bk_is_editing"] = False
                    btn_cntn = st.form_submit_button("Continue")
                    if btn_cntn:
                        st.session_state["bk_is_editing"] = False
                        self.__clear_ss_bk_flds()
                        self.__clear_ss_res1_bk_flds()
                        self.add_updt_bk()
                        st.rerun()
                elif st.session_state["bk_srch_sum"] == 1:
                    st.info("One book entry matches the data of the book you have entered into the Add/Edit book form.")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(":orange[Existing book]")
                        self.__show_book_entered("blue", st.session_state["res1_bk_book_title"], st.session_state["res1_bk_author"],
                                                 st.session_state["res1_bk_publisher"], st.session_state["res1_bk_date_pub"],
                                                 st.session_state["res1_bk_year_read"], st.session_state["res1_bk_pub_location"],
                                                 st.session_state["res1_bk_edition"], st.session_state["res1_bk_first_edition"],
                                                 st.session_state["res1_bk_first_edition_locale"], st.session_state["res1_bk_first_edition_name"],
                                                 st.session_state["res1_bk_first_edition_publisher"])
                    with col2:
                        st.write(":orange[Your updates to this book]")
                        self.__show_book_entered("green", st.session_state["bk_book_title"], st.session_state["bk_author"],
                                                 st.session_state["bk_publisher"], st.session_state["bk_date_pub"],
                                                 st.session_state["bk_year_read"], st.session_state["bk_pub_location"],
                                                 st.session_state["bk_edition"], st.session_state["bk_first_edition"],
                                                 st.session_state["bk_first_edition_locale"], st.session_state["bk_first_edition_name"],
                                                 st.session_state["bk_first_edition_publisher"])

                    btn_exit_bk = st.form_submit_button("Discard new book")
                    btn_edt_bk = st.form_submit_button("Edit this book's details")
                    btn_add_bk_anyway = st.form_submit_button("Add this book anyway")
                    if btn_exit_bk:
                        st.session_state["bk_srch_sum"] = 0
                        st.session_state["bk_is_editing"] = False
                        self.__clear_ss_bk_flds()
                        self.__clear_ss_res1_bk_flds()
                        self.add_updt_bk_srch()
                        st.rerun()
                    if btn_edt_bk:
                        st.session_state["bk_srch_sum"] = 0 # i.e. will treat on rerun as working with update of record
                        st.session_state["bk_is_editing"] = True
                        self.add_updt_bk()
                        st.rerun()
                    if btn_add_bk_anyway:
                        # TODO - only allow this if book title is NOT 100% match
                        # TODO - if want to update book title (YES), add res1 SS title (original title to the book list
                        #  "if SS is updating book" is True (and down call stack), try it. Else, make book title disable field on edit
                        st.session_state["bk_srch_sum"] = 0
                        st.session_state["bk_is_editing"] = False
                        self.add_updt_bk_sbmttd()
                        st.rerun()

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
        if searchSelection == self.dict_edit_annot_sel.get("bk_add_update_bk"):
            if getResultsCount:
                return self.__add_update_book_count(sourceData, conn, record)
            else:
                return self.__add_update_book(sourceData, conn, record)
        elif searchSelection == self.dict_edit_annot_sel.get("bk_add_edit_bk_res_0"):
            self.__add_update_book_new(sourceData, conn, record, getResultsCount)
        elif searchSelection == self.dict_edit_annot_sel.get("ants_edt_add_bk_srch"):
            return self.__srch_bks_for_new_annot(sourceData, conn, record, getResultsCount)
        elif searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_srch_ppg_no"):
            return self.__srch_ants_for_exists_annot(sourceData, conn, record)
        elif searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_updte_annot"):
            self.__add_update_annot(sourceData, conn, record, getResultsCount)
        conn.close()

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
            book.insert(ctr, self.__rem_sql_wrap_chars(tmp_fld))
        if not bk_exists:
            bk_sum = str(sourceData.resBooksAll(conn.cursor()) + 1).zfill(self.dict_db_fld_validations.get("books_bk_no_len"))
        sourceData.addUpdateNewBook(conn.cursor(), bk_sum, book, bk_exists)

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

    def __show_book_entered(self, colour, bk_title, bk_author, bk_publisher, bk_date_pub, bk_year_read, bk_pub_location, bk_edition,
                            bk_first_edition, bk_first_edition_locale, bk_first_edition_name, bk_first_edition_publisher):
        st.markdown(":{}[Title:] {}".format(colour, bk_title))
        st.markdown(":{}[Author:] {}".format(colour, bk_author))
        st.markdown(":{}[Publisher:] {}".format(colour, bk_publisher))
        st.markdown(":{}[Publication date:] {}".format(colour, bk_date_pub))
        st.markdown(":{}[Year read:] {}".format(colour, bk_year_read))
        st.markdown(":{}[Publication location:] {}".format(colour, bk_pub_location))
        st.markdown(":{}[Edition:] {}".format(colour, bk_edition))
        st.markdown(":{}[First edition:] {}".format(colour, bk_first_edition))
        st.markdown(":{}[First edition location:] {}".format(colour, bk_first_edition_locale))
        st.markdown(":{}[First edition name:] {}".format(colour, bk_first_edition_name))
        st.markdown(":{}[First edition publisher:] {}".format(colour, bk_first_edition_publisher))

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
        # code for rem of .. was here
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
                if chr == """'""":
                    elem = str(temp_spell_check_list[sp_ctr])
                    if elem.find(chr) != -1:
                        if elem.index(chr) < (len(elem) - 1): # handle case for words like couldn't, wouldn't, can't
                            post_apost = elem[elem.index("""'""") + 1:]
                            if not post_apost[0:1].isalpha():
                                temp_char = str(temp_spell_check_list[sp_ctr])
                                temp_spell_check_list.pop(sp_ctr)
                                temp_spell_check_list.insert(sp_ctr, temp_char.replace(str(chr), "", 1))
                        else:
                            if str(temp_spell_check_list[sp_ctr]).rfind(str(chr), 1) != -1:
                                temp_char = str(temp_spell_check_list[sp_ctr])
                                temp_spell_check_list.pop(sp_ctr)
                                temp_spell_check_list.insert(sp_ctr, temp_char.replace(str(chr), "", 1))
                else:
                    if str(temp_spell_check_list[sp_ctr]).rfind(str(chr), 1) != -1:
                        temp_char = str(temp_spell_check_list[sp_ctr])
                        temp_spell_check_list.pop(sp_ctr)
                        temp_spell_check_list.insert(sp_ctr, temp_char.replace(str(chr), "", 1))
        return temp_spell_check_list

    def __rebuild_txt_area(self, wrd_lst):
        tmp_txt_area = ""
        st.session_state["spell_txt_area"] = ""
        for h_wrd_indx in range(0, len(wrd_lst)):
            tmp_txt_area = tmp_txt_area + str(wrd_lst[h_wrd_indx])
            if h_wrd_indx < (len(wrd_lst) - 1):
                tmp_txt_area = tmp_txt_area + " "
        return tmp_txt_area

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

    def __rem_sql_wrap_chars(self, datum):
        return datum.strip("%")

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

    def __get_spell_word_split(self, w_Line):
        temp_wl = w_Line.split("||")
        return str(temp_wl[0])

    def __get_spell_map_index_split(self, w_Line):
        temp_wl = w_Line.split("||")
        return int(temp_wl[1])

    def __get_spell_chkbox_sggstn(self, chkbx_itm):
        tmp_sggst = chkbx_itm.split(self.dict_separators.get("spell_chkbx_indx_prfix"))
        sggst = str(tmp_sggst[0].strip())
        return sggst

    def __get_spell_chkbox_indx(self, chkbx_itm):
        tmp_sggst = chkbx_itm.split(self.dict_separators.get("spell_chkbx_indx_prfix"))
        indx = str(tmp_sggst[1].lstrip())
        return int(indx.rstrip("}"))

    def __get_spell_chkbx_split(self, chkbx_itm):
        temp_itm = chkbx_itm.split(self.dict_separators.get("spell_chkbx_indx_prfix"))
        return str(temp_itm[0]).rstrip()

    def __rem_markdown_colour(self, wrd, colour_prefix):
        temp__wrd = wrd[colour_prefix + 1:]
        temp__wrd = temp__wrd[0:len(temp__wrd) - 1] # rem ] (markdown closure bracket)
        return(temp__wrd)

    def __append_for_db_write(self, fld):
        if fld != "":
            return self.__format_sql_wrap(fld)
        else:
            return ""

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