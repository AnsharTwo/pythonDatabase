import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import base64
import os
from dotenv import load_dotenv
import form_sr
import sidebar

class LOGIN(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_auth = {
        "auth_path": "auth/auths.YAML"
    }

    def create_auth_ojb(self):
        with open(self.dict_auth.get("auth_path")) as file:
            ath_cnfg = yaml.load(file, Loader=SafeLoader)
            return ath_cnfg

    def write_auth_obj(self, ath_config):
        with open(self.dict_auth.get("auth_path"), 'w') as file:
            yaml.dump(ath_config, file, default_flow_style=False, indent=4)

    def create_authenticator(self, auth_config):
        authent = stauth.Authenticate(
            auth_config['credentials'],
            auth_config['cookie']['name'],
            auth_config['cookie']['key'],
            auth_config['cookie']['expiry_days'],
        )
        return authent

    def login_to_app(self):
        if "show_frgt_psswd" not in st.session_state:
            st.session_state.show_frgt_psswd = True

        if "pwd_current" not in st.session_state:
            st.session_state.pwd_current = ""
        if "pwd_new" not in st.session_state:
            st.session_state.pwd_new = ""
        if "pwd_new_confirm" not in st.session_state:
            st.session_state.pwd_new_confirm = ""
        if "pwd_tmp_changed" not in st.session_state:
            st.session_state.pwd_tmp_changed = False

        auth_config = self.create_auth_ojb()
        authenticator = self.create_authenticator(auth_config)
        st.header(":blue[Librotate]")
        authenticator.login(location='main', max_concurrent_users=100, captcha=False, single_session=False, clear_on_submit=False,
                            key="lbrtt_auth_01")
        if st.session_state["authentication_status"]:
            config_data = self.load_ini_config()
            if "ss_dat_loc_annots" not in st.session_state:
                st.session_state.ss_dat_loc_annots = str(config_data["data locations"]["annotations"])
            if "ss_dat_loc_urls" not in st.session_state:
                st.session_state.ss_dat_loc_urls = str(config_data["data locations"]["urls"])
            st.session_state.show_frgt_psswd = False

            if not st.session_state.pwd_tmp_changed:
                sbar = sidebar.SIDEBAR(st.session_state.name, authenticator)
                sbar.init_sidebars()

            else:
                if self.chng_tmp_pwd(authenticator, auth_config,
                                  auth_config["credentials"]["usernames"][st.session_state.username]["password"]):
                    st.session_state.pwd_tmp_changed = False
                    st.session_state.pwd_current = ""
                    st.session_state.pwd_new = ""
                    st.session_state.pwd_new_confirm = ""
                    st.rerun()

            authenticator.logout(location="sidebar")
            if st.session_state["authentication_status"] is None:
                st.session_state.clear()
                st.rerun()
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')
        elif not st.session_state["authentication_status"]:
            st.error('Username/password is incorrect')
        if st.session_state.show_frgt_psswd:
            chkbx_frgt_pwd = st.checkbox("Forgot password?")
            if chkbx_frgt_pwd:
                try:
                    st.write(self.dict_frgt_pwd_txts.get("frgt_pwd_info"))
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password(location="main")
                    if username_forgot_pw:
                        hashed_password = stauth.Hasher.hash(random_password)
                        auth_config["credentials"]["usernames"][username_forgot_pw]["password"] = hashed_password
                        self.write_auth_obj(auth_config)
                        self.send_pwd_msg(auth_config, username_forgot_pw, random_password)
                    elif username_forgot_pw == False:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)




    def chng_tmp_pwd(self, authenticator, auth_config, pwd_hashed_curr):
        st.markdown(f"**:blue[Change one-time password]**")
        st.session_state.pwd_current = st.text_input("Current password", type="password",
                                                     max_chars=self.dict_pwd_chng.get("length"))
        st.session_state.pwd_new = st.text_input("New password", type="password",
                                                 max_chars=self.dict_pwd_chng.get("length"))
        st.session_state.pwd_new_confirm = st.text_input("Confirm new password", type="password",
                                                         max_chars=self.dict_pwd_chng.get("length"))
        btn_chng_pwd = st.button("Change")
        if btn_chng_pwd:
            can_change = True
            if not stauth.Hasher.check_pw(st.session_state.pwd_current, pwd_hashed_curr):
                st.markdown(":red[Enter current password.]")
                can_change = False
            elif not authenticator.authentication_controller.validator.validate_password(st.session_state.pwd_new):
                st.markdown(
                    """:red[New password must be between 8 and 20 characters long, contain at least: one uppercase letter,
                     one lowercase letter, one number, and one special chararcter from the set @$!%*?&.]""")
                can_change = False
            elif st.session_state.pwd_new != st.session_state.pwd_new_confirm:
                st.markdown(":red[New and confirmed passwords don't match.]")
                can_change = False
            if can_change:
                hashed_password = stauth.Hasher.hash(st.session_state.pwd_new)
                auth_config["credentials"]["usernames"][st.session_state.username]["password"] = hashed_password
                self.write_auth_obj(auth_config)
                return True




    def send_pwd_msg(self, auth_config, username_forgot_pw, random_password):
        message = MIMEMultipart()
        message['From'] = self.__Load_lib_adr()
        message['To'] = auth_config["credentials"]["usernames"][username_forgot_pw]["email"]
        message['Subject'] = "Forgot password - your new password from Librotate"
        body = self.dict_frgt_pwd_txts.get("frgt_pwd_email_msg").format(
                                                     name=auth_config["credentials"]["usernames"][username_forgot_pw]["name"],
                                                     pwd=str(random_password))
        message.attach(MIMEText(body, 'plain'))
        server = None
        try:
            server = smtplib.SMTP_SSL(self.__Load_lib_server_nm(), self.__Load_lib_server_prt())  # Or can use smtp.gmail.com for port 587 and .starttls()
            server.login(self.__Load_lib_adr(), self.decrypt(self.__Load_lib_server_creds()))  # THIS ACCOUNT IS ALSO PROTECTED BY MFA
            server.sendmail(self.__Load_lib_adr(),
                            auth_config["credentials"]["usernames"][username_forgot_pw]["email"], message.as_string())
            st.success('New password sent securely')
        except Exception as ex:
            st.write("Error sending email: " + str(ex))
        finally:
            server.quit()

    def decrypt(self, encoded_text):
        D_CIPHER = AES.new(self.__Load_s_key(), AES.MODE_ECB)
        return unpad(D_CIPHER.decrypt(base64.b64decode(encoded_text)), self.BLOCK_SIZE).decode(
            "utf-8")

    def __Load_s_key(self):
        load_dotenv()
        return str(os.getenv("FRGT_PSSWRD_SRVR_CRYPT_KEY")).encode("utf-8")

    def __Load_lib_server_creds(self):
        load_dotenv()
        return os.getenv("FRGT_PSSWD_SRVR_PSSWRD")

    def __Load_lib_adr(self):
        load_dotenv()
        return os.getenv("LIBROTATE_ADMIN_EMAIL")

    def __Load_lib_server_nm(self):
        load_dotenv()
        return os.getenv("LIBROTATE_EMAIL_SERVER")

    def __Load_lib_server_prt(self):
        load_dotenv()
        return int(os.getenv("LIBROTATE_EMAIL_SERVER_PORT"))

    dict_frgt_pwd_txts = {
        "frgt_pwd_info": """Enter your user name and submit the below form. You will then receive an email to your email address
                             (the one you have specified in your profile account), which will contain a one-time password. You can
                             then login with this temporary password and change it to a regular-use one in your profile settings.""",
        "frgt_pwd_email_msg": """Hello, {name}. Your one-time password to login to Librotate is:
                              \r\r{pwd}
                              \r\rRegards,
                              \r\rThe Librotate team."""
    }

    BLOCK_SIZE = 32  # Bytes