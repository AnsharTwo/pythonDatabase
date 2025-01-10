from datetime import datetime

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