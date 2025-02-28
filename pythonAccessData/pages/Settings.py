import streamlit as st

class SETTINGS():

    def __init__(self):
        super().__init__()

    def form_settings(self):

        # if "authentication_status" not in st.session_state:
        #     st.session_state["authentication_status"] = False
        # if not st.session_state["authentication_status"]:
        #     st.info('Please Login from the Home page and try again.')
        #     st.stop()

        ##########################
        qp = st.query_params
        if qp:
            if {qp["auth_stat"]}:
        ##########################

                with st.form("settings"):
                    st.header("Settings")
                    st.form_submit_button("Submit")

setts = SETTINGS()
setts.form_settings()