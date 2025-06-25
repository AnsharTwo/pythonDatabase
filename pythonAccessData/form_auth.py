import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#################################
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
#################################

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
            sbar = sidebar.SIDEBAR(st.session_state.name, authenticator)
            sbar.init_sidebars()
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

                    ########################
                    # BLOCK_SIZE = 32  # Bytes
                    # key = 'abcdefghijklmnop'
                    # cipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
                    # msg = cipher.encrypt(pad(b'myPassword99', BLOCK_SIZE))
                    # print("encrypted is: " + msg.hex())
                    # decipher = AES.new(key.encode('utf8'), AES.MODE_ECB)
                    # msg_dec = decipher.decrypt(msg)
                    # print("decrypted is:")
                    # print(unpad(msg_dec, BLOCK_SIZE))
                    ########################

                    st.write(self.dict_frgt_pwd_txts.get("frgt_pwd_info"))
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password(location="main")
                    if username_forgot_pw:
                        hashed_password = stauth.Hasher.hash(random_password)
                        auth_config["credentials"]["usernames"][username_forgot_pw]["password"] = hashed_password
                        self.write_auth_obj(auth_config)
                        print("pwd " + random_password) # TEMP ####################################
                        self.send_pwd_msg(auth_config, username_forgot_pw, random_password)
                    elif username_forgot_pw == False:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)

    def send_pwd_msg(self, auth_config, username_forgot_pw, random_password):
        message = MIMEMultipart()
        message['From'] = self.LIBROTATE_ADMIN_EMAIL
        message['To'] = auth_config["credentials"]["usernames"][username_forgot_pw]["email"]
        message['Subject'] = "Forgot password - your new password from Librotate"
        body = self.dict_frgt_pwd_txts.get("frgt_pwd_email_msg").format(
                                                     name=auth_config["credentials"]["usernames"][username_forgot_pw]["name"],
                                                     pwd=str(random_password))
        message.attach(MIMEText(body, 'plain'))
        server = None
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Or can use smtp.gmail.com for port 587 and .starttls()
            server.login(self.LIBROTATE_ADMIN_EMAIL, "oepp zezu xudh cxqp") # THIS PASSWORD IS PROTECTED BY MFA
            server.sendmail(self.LIBROTATE_ADMIN_EMAIL,
                            auth_config["credentials"]["usernames"][username_forgot_pw]["email"], message.as_string())
            st.success('New password sent securely')
        except Exception as ex:
            st.write("Error sending email: " + str(ex))
        finally:
            server.quit()

    dict_frgt_pwd_txts = {
        "frgt_pwd_info": """Enter your user name and submit the below form. You will then receive an email to your email address
                             (the one you have specified in your profile account), which will contain a one-time password. You can
                             then login with this temporary password and change it to a regular-use one in your profile settings.""",
        "frgt_pwd_email_msg": """Hello, {name}. Your one-time password to login to Librotate is:
                              \r\r{pwd}
                              \r\rRegards,
                              \r\rThe Librotate team."""
    }

    LIBROTATE_ADMIN_EMAIL = "no.reply.librotate@gmail.com"