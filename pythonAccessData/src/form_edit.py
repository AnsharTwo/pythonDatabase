import streamlit as st

class EDIT_FORM:

    # def __init__(self):

    dict_edit_annot_sel = {
        "ants_edt_add": "Create new annotation",
        "ants_edt_edt": "Edit existing annotation",
        "ants_edt_dlt": "Delete an annotation",
        "ants_add_bk": "Add a new book"
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
        book_title = st.text_input("Book title")
        author = st.text_input("Author")
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
        st.write("Add new book")
        book_title = st.text_input("Book title")
        author = st.text_input("Author")
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
            st.write("temp")