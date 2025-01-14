import streamlit as st
from spellchecker import SpellChecker
import form_sr
import form_bk

class EDIT_ANNOT(form_sr.FORM):

    book_worker = form_bk.EDIT_BOOK()
    book_remover = form_bk.DEL_BOOK()

    dict_edit_annot_nonmenu_flags = {
        "ants_edt_add_bk_srch": "Search for book for new annotation",
        "ants_edt_add_srch_ppg_no": "search for page number",
        "ants_edt_add_updte_annot": "add or update annotation",
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
                    elif st.session_state["date_published"] != "" and not super().isValidYearFormat(
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
                book_search.append(st.session_state["book_no"]) # not used but needed to set correct index
                book_search.append(super().format_sql_wrap(st.session_state["book_title"]))
                book_search.append(super().format_sql_wrap(st.session_state["author"]))
                # TODO - use function created for add update book below
                if st.session_state["publisher"] != "":
                    book_search.append(super().format_sql_wrap(st.session_state["publisher"]))
                else:
                    book_search.append("")
                if st.session_state["date_published"] != "":
                    book_search.append(super().format_sql_wrap(str(st.session_state["date_published"])))
                else:
                    book_search.append("")
                bkSum = self.db_records(self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_bk_srch"), book_search, True)
                bks = self.db_records(self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_bk_srch"), book_search, False)
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
                        st.session_state["publisher"] = super().conv_none_for_db(bk.Publisher)
                        st.session_state["date_published"] = super().conv_none_for_db(bk.Dat)
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
            # TODO - get below working (btn above is disabled while not
            #if add_nw_bk:
            #    self.book_worker.add_new_bk()
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
                    elif super().has_illegal_text(st.session_state["annot_txt_area"], illegal_txt):
                        st.markdown(":red[text cannot contain a bracket immediately enclosing a space chracter e.g. '( ', ' }'.]")
                    elif super().has_illegal_text(st.session_state["annot_txt_area"], stops_txt):
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
                                        super().formatSQLSpecialChars(st.session_state["annot_txt_area"]).strip()
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

    def db_records(self, searchSelection, record, getResultsCount):
        sourceData = super().get_data_source()
        conn = super().get_connection(sourceData)
        if searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_bk_srch"):
            return self.__srch_bks_for_new_annot(sourceData, conn, record, getResultsCount)
        elif searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_srch_ppg_no"):
            return self.__srch_ants_for_exists_annot(sourceData, conn, record)
        elif searchSelection == self.dict_edit_annot_nonmenu_flags.get("ants_edt_add_updte_annot"):
            self.__add_update_annot(sourceData, conn, record, getResultsCount)
        conn.close()

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

    def __format_page_no(self, pageNo):
        return pageNo.lstrip("0")

    def __format_book_no(self, bookNo):
        return bookNo.lstrip("0")

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

class DEL_ANNOT(form_sr.FORM):
    def dlt_annot(self):
        st.write("Page is under construction - delete annotation. Check back real soon.")