import sys
from datetime import datetime
import streamlit as st
import configparser
import yaml
from yaml.loader import SafeLoader
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

    dict_auth = {
        "auth_path": "auth/auths.YAML"
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

    def get_data_source(self):
        dbPath = sys.argv[1] + sys.argv[2]
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

    def create_auth_ojb(self):
        with open(self.dict_auth.get("auth_path")) as file:
            ath_cnfg = yaml.load(file, Loader=SafeLoader)
            return ath_cnfg

    def select_edit_form(self, listHeader, listTitle, selectListDict):
        values_list = list(selectListDict.values())
        sel_opt = 'selectbox_option_' + listTitle
        if sel_opt not in st.session_state:
            st.session_state[sel_opt] = 0
        if listHeader != "":
            st.header(listHeader)
        edt_selection = st.selectbox(listTitle,
            [
                value
                for value in selectListDict.values()
            ],
            index=st.session_state[sel_opt]
        )
        if values_list.index(edt_selection) != st.session_state[sel_opt]:
            st.session_state[sel_opt] = values_list.index(edt_selection)
            st.rerun()
        else:
            if edt_selection != "None":
                return edt_selection

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