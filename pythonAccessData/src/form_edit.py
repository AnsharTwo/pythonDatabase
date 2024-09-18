import streamlit as st

class EDIT_FORM:

    # def __init__(self):

    dict_edit_annot_sel = {
        "ants_edt_add": "Create new annotation",
        "ants_edt_edt": "Edit existing annotation",
        "ants_edt_dlt": "Delete an annotation"
    }
    def select_edit_form(self):
        with st.form("Edit"):
            st.header("Edit annotations data")
            editSelection = st.selectbox("Select data activity", [
                "---",
                "Create new annotation",
                "Edit existing annotation",
                "Delete an annotation"
            ])
            st.form_submit_button("Go")
            if editSelection == self.dict_edit_annot_sel.get("ants_edt_add"):
                self.edt_new_annot()

    def edt_new_annot(self):
        txt = st.text_area("Enter new annotation")
        create = st.form_submit_button("Create")
        if create:
            if txt == "":
                st.markdown(":red[no text entered.]")

