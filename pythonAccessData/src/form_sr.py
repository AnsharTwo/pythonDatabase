from datetime import datetime
import streamlit as st

class FORM:

    def isValidYearFormat(self, year, format):
        try:
            res = bool(datetime.strptime(year, format))
        except ValueError:
            res = False
        return res

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