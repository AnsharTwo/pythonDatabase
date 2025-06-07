from datetime import datetime
import streamlit as st
import configparser
import pandas as pd
import db

class FORM:

    def __init__(self):
        self.connStr = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;'

    dict_config = {
        "ini_config": "config.ini",
        "ini_config_def": "config_def.ini",
        "toml_config": ".streamlit/config.toml",
        "toml_config_def": "config_toml.ini"
    }

    dict_list_annt_wrkr = {
        "header": "Edit annotations data",
        "title": "Select data activity"
    }

    dict_list_wrkr_items = {
        "None": "none",
        "ants_edt_add": "Create update or delete annotation",
        "bk_add_update_bk": "Create update or delete book",
    }

    dict_book_sheets = {
        "web_pages": "Pages",
        "videos": "Videos",
        "sites": "Sites"
    }

    dict_book_sheets_spec = {
        "web_pages":
            {
                "page_no": "Page no.",
                "desc": "Description",
                "read":  "Read",
                "url": "URL",
                "note": "Note",
                "index":
                    {
                        "desc": 0,
                        "read": 1,
                        "url": 2,
                    }
            },
        "videos":
            {
                "video_no": "Video no.",
                "desc": "Description",
                "watched": "Watched",
                "url": "URL",
                "note": "Note"
            },
        "sites":
            {
                "site_no": "Site no.",
                "desc": "Description",
                "url": "URL"
            }
    }

    dict_sheets_cll_clr = {
        "is_read": {
            "cll_unread": "\U0001F7E5",
            "cll_read": "\U0001F7E9"
        }
    }

    dict_hlght_cases = {
        "cap": "capitalise",
        "cap_all": "capitaliseAll",
        "lwr": "lower",
        "upr": "upper"
    }

    dict_err_msgs = {
        "cursor_exec": "Error executing data query (Is your data source file a valid one?)",
        "form_no_display": "Form can't be displayed."
    }

    def get_data_source(self):
        dbPath = st.session_state.ss_dat_loc_annots
        sourceData = db.DATA_SOURCE(self.connStr % dbPath)
        sourceData.is_ms_access_driver()
        return sourceData

    def get_connection(self, source_data):
        conn = source_data.db_connect()
        source_data.report_tables(conn.cursor())
        return conn

    def load_toml_config(self):
        config = configparser.ConfigParser()
        config.read(self.dict_config.get("toml_config"))
        return config

    def write_toml_config(self, config_data):
        with open(self.dict_config.get("toml_config"), 'w') as configfile:
            config_data.write(configfile)

    def load_ini_config(self):
        config = configparser.ConfigParser()
        config.read(self.dict_config.get("ini_config"))
        return config

    def write_ini_config(self, config_data):
        with open(self.dict_config.get("ini_config"), 'w') as configfile:
            config_data.write(configfile)

    @st.cache_data(show_spinner="Loading data from sheet...")
    def load_book_sheet(_self, sheet):
        cls = []
        if sheet == _self.dict_book_sheets.get("web_pages"):
            cls = [_self.dict_book_sheets_spec.get("web_pages").get("desc"),
                   _self.dict_book_sheets_spec.get("web_pages").get("read"),
                   _self.dict_book_sheets_spec.get("web_pages").get("url"),
                   _self.dict_book_sheets_spec.get("web_pages").get("note")]
        elif sheet == _self.dict_book_sheets.get("videos"):
            cls = [_self.dict_book_sheets_spec.get("videos").get("desc"),
                   _self.dict_book_sheets_spec.get("videos").get("watched"),
                   _self.dict_book_sheets_spec.get("videos").get("url"),
                   _self.dict_book_sheets_spec.get("videos").get("note")]
        elif sheet == _self.dict_book_sheets.get("sites"):
            cls = [_self.dict_book_sheets_spec.get("videos").get("desc"),
                   _self.dict_book_sheets_spec.get("videos").get("url")]
        try:
            sheetbook_path = st.session_state.ss_dat_loc_urls
            sheet_loaded = pd.read_excel(sheetbook_path, index_col=None, engine="openpyxl", sheet_name=str(sheet), usecols=cls)
        except Exception as ex:
            raise ex
        else:
            return sheet_loaded

    def write_book_sheet(self, sheet_web_pages, sheet_videos, sheet_sites):
        sheetbook_path = st.session_state.ss_dat_loc_urls
        try:
            with pd.ExcelWriter(sheetbook_path) as writer:
                sheet_web_pages.to_excel(writer, sheet_name=self.dict_book_sheets.get("web_pages"), index=False,
                                         columns=[self.dict_book_sheets_spec.get("web_pages").get("desc"),
                                                  self.dict_book_sheets_spec.get("web_pages").get("read"),
                                                  self.dict_book_sheets_spec.get("web_pages").get("url"),
                                                  self.dict_book_sheets_spec.get("web_pages").get("note")])
                sheet_videos.to_excel(writer, sheet_name=self.dict_book_sheets.get("videos"), index=False,
                                         columns=[self.dict_book_sheets_spec.get("videos").get("desc"),
                                                  self.dict_book_sheets_spec.get("videos").get("watched"),
                                                  self.dict_book_sheets_spec.get("videos").get("url"),
                                                  self.dict_book_sheets_spec.get("videos").get("note")])
                sheet_sites.to_excel(writer, sheet_name=self.dict_book_sheets.get("sites"), index=False,
                                         columns=[self.dict_book_sheets_spec.get("sites").get("desc"),
                                                  self.dict_book_sheets_spec.get("sites").get("url")])
        except Exception as ex:
            raise ex

    def select_edit_form(self, listHeader, listTitle, selectListDict):
        values_list = list(selectListDict.values())
        sel_opt = 'selectbox_option_' + listTitle
        sel_itms = 'selectbox_items_' + listTitle
        if sel_opt not in st.session_state:
            st.session_state[sel_opt] = 0
        if sel_itms not in st.session_state:
            st.session_state[sel_itms] = selectListDict
        if listHeader != "":
            st.header(listHeader)
        edt_selection = st.selectbox(listTitle,
            [
                value
                for value in st.session_state[sel_itms].values()
            ],
            index=st.session_state[sel_opt],
            key=listTitle
        )
        if values_list.index(edt_selection) != st.session_state[sel_opt]:
            st.session_state[sel_opt] = values_list.index(edt_selection)
            st.rerun()
        else:
            if edt_selection != "None":
                return edt_selection

    def hghlght_txt(self, srcText, searchTxts):
        retText = srcText
        if searchTxts != "":
            for txt in searchTxts:
                txt = str(txt).lstrip("%").rstrip("%")
                txt = txt.replace("''", "'")
                txt = txt.replace("[[]", "[")
                retText = str(retText).replace(txt, ":orange-background[{}]".format(txt))
                retText = str(retText).replace(txt.capitalize(),
                                          ":orange-background[{}]".format(txt.capitalize()))
                retText = str(retText).replace(txt.lower(),
                                          ":orange-background[{}]".format(txt.lower()))
                retText = str(retText).replace(txt.upper(),
                                          ":orange-background[{}]".format(txt.upper()))
                strForHghlghts = txt.split(" ")
                if len(strForHghlghts) > 1:
                    retText = self.__txtCaseHghlghtsByWrd(retText, txt, self.dict_hlght_cases.get("cap_all"))
                    retText = self.__txtCaseHghlghtsByWrd(retText, txt, self.dict_hlght_cases.get("lwr"))
                    retText = self.__txtCaseHghlghtsByWrd(retText, txt, self.dict_hlght_cases.get("upr"))
                    capAllStr = ""
                    for wrd in range(0, len(strForHghlghts)):
                        capAllStr = capAllStr + str(strForHghlghts[wrd]).capitalize() + " "
                    capAllStr = capAllStr.strip()
                    retText = self.__txtCaseHghlghtsByWrd(retText, capAllStr, self.dict_hlght_cases.get("lwr"))
                    retText = self.__txtCaseHghlghtsByWrd(retText, capAllStr, self.dict_hlght_cases.get("upr"))
        return retText

    def isValidYearFormat(self, year, format):
        try:
            res = bool(datetime.strptime(year, format))
        except ValueError:
            res = False
        return res

    def format_page_no(self, pageNo):
        return pageNo.lstrip("0")

    def format_book_no(self, bookNo):
        return bookNo.lstrip("0")

    def format_sql_wrap(self, searchDatum):
        datum = searchDatum
        if not searchDatum.startswith("%"):
            datum = "%" + datum
        if not searchDatum.endswith("%"):
            datum = datum + "%"
        datum = self.formatSQLSpecialChars(datum)
        return datum

    def formatSQLSpecialChars(self, searchDatum):
        formattedDatum = searchDatum.replace("'", "\''")
        return formattedDatum

    def rem_sql_wrap_chars(self, datum):
        return datum.strip("%")

    def has_illegal_text(self, txt_area, illegal_txt):
        is_illegal_txt = False
        for il_txt in illegal_txt:
            if txt_area.find(il_txt) != -1:
                is_illegal_txt = True
        return is_illegal_txt

    def append_for_db_write(self, fld):
        if fld != "":
            return self.format_sql_wrap(fld)
        else:
            return ""

    def conv_none_for_db(self, fld_val):
        if fld_val == None:
            return ""
        else:
            return fld_val

    def formatSearchText(self, searchText):
        searchArr = []
        if searchText.find(",") == -1:
            searchArr.append(self.format_sql_wrap(searchText))
        else:
            searchTxt = searchText.split(",")
            for txt in searchTxt:
                searchArr.append(self.format_sql_wrap(txt))
        return searchArr

    def formatSheetSearchText(self, searchText):
        searchArr = []
        if searchText.find(",") == -1:
            searchArr.append(searchText)
        else:
            searchTxt = searchText.split(",")
            for txt in searchTxt:
                searchArr.append(txt)
        return searchArr

    def show_book_entered(self, colour, bk_title, bk_author, bk_publisher, bk_date_pub, bk_year_read, bk_pub_location, bk_edition,
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

    def __txtCaseHghlghtsByWrd(self,srcText, txt, case):
        sText = srcText
        strForHghlghts = txt.split(" ")
        capAllStr = ""
        if case == self.dict_hlght_cases.get("cap_all"):
            for wrd in range(0, len(strForHghlghts)):
                capAllStr = capAllStr + str(strForHghlghts[wrd]).capitalize() + " "
            capAllStr = capAllStr.strip()
            sText = sText.replace(capAllStr,
                                  ":orange-background[{}]".format(capAllStr))
        else:
            for wrd in range(0, len(strForHghlghts)):
                tempStr = ""
                tempwrd = ""
                if case == self.dict_hlght_cases.get("cap"):
                    tempwrd = strForHghlghts[wrd].capitalize()
                elif case == self.dict_hlght_cases.get("lwr"):
                    tempwrd = strForHghlghts[wrd].lower()
                elif case == self.dict_hlght_cases.get("upr"):
                    tempwrd = strForHghlghts[wrd].upper()
                for wrdIndx in range(0, len(strForHghlghts)):
                    if wrd == wrdIndx:
                        tempStr = tempStr + " " + tempwrd
                    else:
                        tempStr = tempStr + " " + str(strForHghlghts[wrdIndx])
                tempStr = tempStr.strip()
                sText = sText.replace(tempStr,
                                      ":orange-background[{}]".format(tempStr))
        return sText