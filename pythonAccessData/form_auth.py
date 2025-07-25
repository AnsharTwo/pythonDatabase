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
import shutil
from dotenv import load_dotenv
from random import randint
import form_sr
import sidebar

class LOGIN(form_sr.FORM):

    def __init__(self):
        super().__init__()

    dict_auth = {
        "auth_path": "auth/auths.YAML",
        "cap_len": 5,
        "cap_path": "caps/",
        "ver_code_len": 6,
        "ver_code_min": 100000,
        "ver_code_max": 999999,
        "max_ver_code_resends": 3
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
        if "show_reg_usr" not in st.session_state:
            st.session_state.show_reg_usr = True
        if "pwd_current" not in st.session_state:
            st.session_state.pwd_current = ""
        if "pwd_new" not in st.session_state:
            st.session_state.pwd_new = ""
        if "pwd_new_confirm" not in st.session_state:
            st.session_state.pwd_new_confirm = ""
        if "pwd_tmp_changed" not in st.session_state:
            st.session_state.pwd_tmp_changed = False
        if "new_user_login" not in st.session_state:
            st.session_state.new_user_login = False
        if "email_code_sent" not in st.session_state:
            st.session_state.email_code_sent = False
        if "swapped_ini" not in st.session_state:
            st.session_state.swapped_ini = False
        if "usrs_ini" not in st.session_state:
            st.session_state.usrs_ini = ""
        if "usrs_toml" not in st.session_state:
            st.session_state.usrs_toml = ""
        if "reg_username" not in st.session_state:
            st.session_state.reg_username = ""
        if "reg_name" not in st.session_state:
            st.session_state.reg_name = ""
        if "reg_email" not in st.session_state:
            st.session_state.reg_email = ""
        if "usr_registered" not in st.session_state:
            st.session_state.usr_registered = False
        if "randomize_cap" not in st.session_state:
            st.session_state.randomize_cap = True
        if "random_cap" not in st.session_state:
            st.session_state.random_cap = ""
        if "cap_ans" not in st.session_state:
            st.session_state.cap_ans = ""
        if "cap_ans_val" not in st.session_state:
            st.session_state.cap_ans_val = ""
        if "email_code_gen" not in st.session_state:
            st.session_state.email_code_gen = None
        if "email_code_entered" not in st.session_state:
            st.session_state.email_code_entered = None
        if "email_code_resent" not in st.session_state:
            st.session_state.email_code_resent = 1
        auth_config = self.create_auth_ojb()
        authenticator = self.create_authenticator(auth_config)
        st.header(":blue[Librotate]")
        authenticator.login(location='main', max_concurrent_users=100, captcha=False, single_session=False, clear_on_submit=False,
                            key="lbrtt_auth_01")
        if st.session_state["authentication_status"]:
            if not st.session_state.swapped_ini:
                st.session_state.usrs_ini = str(self.dict_config.get("ini_config_usr")) + st.session_state.username + "_.ini"
                os.remove(self.dict_config.get("ini_config"))
                shutil.copy(st.session_state.usrs_ini, str(self.dict_config.get("ini_config")))
                st.session_state.usrs_toml = str(self.dict_config.get("toml_config_usr")) + st.session_state.username + "_.toml"
                os.remove(self.dict_config.get("toml_config"))
                shutil.copy(st.session_state.usrs_toml, str(self.dict_config.get("toml_config")))
                st.session_state.swapped_ini = True
            config_data = self.load_ini_config()
            if "ss_dat_loc_annots" not in st.session_state:
                st.session_state.ss_dat_loc_annots = str(config_data["data locations"]["annotations"])
            if "ss_dat_loc_urls" not in st.session_state:
                st.session_state.ss_dat_loc_urls = str(config_data["data locations"]["urls"])
            if str(config_data["forgot_password"]["one_time_login"]) == "1":
                st.session_state.pwd_tmp_changed = True
            if str(config_data["new_user"]["first_time_login"]) == "1":
                st.session_state.new_user_login = True
            st.session_state.show_frgt_psswd = False
            st.session_state.show_reg_usr = False
            if not st.session_state.pwd_tmp_changed:
                if not st.session_state.new_user_login:
                    sbar = sidebar.SIDEBAR(st.session_state.name, authenticator)
                    sbar.init_sidebars()
                else:
                    if not st.session_state.email_code_sent:
                        st.session_state.email_code_gen = randint(self.dict_auth.get("ver_code_min"), self.dict_auth.get("ver_code_max"))
                        st.session_state.email_code_sent = True
                        self.send_verify_email_msg(auth_config, st.session_state.username, st.session_state.email_code_gen)
                    with st.form("Verify new user email"):
                        st.markdown(":blue[Verify your email address]")
                        st.write("Enter the " + str(self.dict_auth.get("ver_code_len")) +
                                 "-digit code sent (just now) to your registered email address.")
                        cols_txt_verify_email = st.columns(8, gap="small", vertical_alignment="center")
                        st.session_state.email_code_entered = cols_txt_verify_email[0].write(":orange[Verify:]")
                        st.session_state.email_code_entered = cols_txt_verify_email[1].text_input("Code", label_visibility="hidden",
                                                                                                  key="vereml34w", max_chars=6)
                        cols_verify_email = st.columns(4, gap="small", vertical_alignment="center")
                        btn_ver_eml = cols_verify_email[0].form_submit_button("Verify")
                        btn_ver_resend = cols_verify_email[1].form_submit_button("Resend")
                        if btn_ver_eml:
                            if st.session_state.email_code_entered == "":
                                st.markdown(":red[Enter the verification code to continue.]")
                            elif not st.session_state.email_code_entered.isdigit():
                                st.markdown(":red[The verification code contains only numbers.]")
                            elif int(st.session_state.email_code_entered) != st.session_state.email_code_gen:
                                    st.markdown(":red[The verification code you entered does not match the code sent to you by email.]")
                            else:
                                st.session_state.email_code_sent = False
                                st.session_state.new_user_login = False
                                config_data["new_user"]["first_time_login"] = "0"
                                self.write_ini_config(config_data)
                                self.send_wlcm_msg(auth_config, st.session_state.username)
                                st.rerun()
                        if btn_ver_resend:
                            st.session_state.email_code_resent += 1
                            if st.session_state.email_code_resent <= self.dict_auth.get("max_ver_code_resends"):
                                st.session_state.email_code_sent = False
                                st.rerun()
                            else:
                                st.markdown(":red[You can't resend the verification code more than " +
                                            str(self.dict_auth.get("max_ver_code_resends")) + " three times in one session.]")
            else:
                if self.chng_tmp_pwd(authenticator, auth_config,
                                  auth_config["credentials"]["usernames"][st.session_state.username]["password"]):
                    st.session_state.pwd_tmp_changed = False
                    config_data["forgot_password"]["one_time_login"] = "0"
                    self.write_ini_config(config_data)
                    st.session_state.pwd_current = "" # these 3 ss are used in change password too.
                    st.session_state.pwd_new = ""
                    st.session_state.pwd_new_confirm = ""
                    st.rerun()
            authenticator.logout(location="sidebar")
            if st.session_state["authentication_status"] is None:
                os.remove(st.session_state.usrs_ini)
                shutil.copy(str(self.dict_config.get("ini_config")), st.session_state.usrs_ini)
                os.remove(st.session_state.usrs_toml)
                shutil.copy(str(self.dict_config.get("toml_config")), st.session_state.usrs_toml)
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
                        os.remove(self.dict_config.get("ini_config"))
                        shutil.copy(str(self.dict_config.get("ini_config_usr")) + username_forgot_pw + "_.ini",
                                    str(self.dict_config.get("ini_config")))
                        config_data = self.load_ini_config()
                        config_data["forgot_password"]["one_time_login"] = "1"
                        self.write_ini_config(config_data)
                        os.remove(str(self.dict_config.get("ini_config_usr")) + username_forgot_pw + "_.ini")
                        shutil.copy(str(self.dict_config.get("ini_config")),
                                    str(self.dict_config.get("ini_config_usr")) + username_forgot_pw + "_.ini")
                    elif username_forgot_pw == False:
                        st.error('Username not found')
                except Exception as e:
                    st.error(e)
        if st.session_state.show_reg_usr:
            if st.session_state.usr_registered:
                with st.form("Register success"):
                    st.success("You are now registered as a Librotate user.")
                    st.write("User name: :green[" + st.session_state.reg_username + "]")
                    st.write("Name: :green[" + st.session_state.reg_name + "]")
                    st.write("Email address: :green[" + st.session_state.reg_email + "]")
                    st.session_state.usr_registered = False
                    st.session_state.cap_ans = ""
                    st.session_state.cap_ans_val = ""
                    st.session_state.reg_username = ""
                    st.session_state.reg_name = ""
                    st.session_state.reg_email = ""
                    st.session_state.randomize_cap = True
                    st.session_state.random_cap = ""
                    btn_registered_ok = st.form_submit_button("Done")
                    if btn_registered_ok:
                        st.rerun()
            else:
                cckb_reg_usr = st.checkbox("No account? Register")
                if cckb_reg_usr:
                    with st.form("Register as new user"):
                        st.session_state.reg_username = st.text_input("User name", value=st.session_state.reg_username,
                                                                      max_chars=self.dict_user_details.get("username"))
                        st.session_state.reg_name = st.text_input("Name", value=st.session_state.reg_name,
                                                                  max_chars=self.dict_user_details.get("name"))
                        st.session_state.reg_email = st.text_input("Email address", value=st.session_state.reg_email,
                                                                   max_chars=self.dict_user_details.get("name"))
                        reg_conf_email = st.text_input("Confirm email address", max_chars=self.dict_user_details.get("email_addr"))
                        reg_pwd = st.text_input("Password", type="password",
                                                               max_chars=self.dict_pwd_chng.get("length"))
                        reg_conf_pwd = st.text_input("Confirm password", type="password",
                                                                    max_chars=self.dict_pwd_chng.get("length"))
                        st.divider()
                        cap_files = []
                        if st.session_state.randomize_cap:
                            cap_files = os.listdir(self.dict_auth.get("cap_path"))
                            st.session_state.random_cap = str(cap_files[randint(0, len(cap_files) - 1)])
                            st.session_state.randomize_cap = False
                        cols_reg_cap = st.columns(4, gap="small", vertical_alignment="center")
                        cols_reg_cap[0].image(self.dict_auth.get("cap_path") + st.session_state.random_cap,
                                              caption="Enter the code shown in the image", width=125)
                        cap_files.clear()
                        st.session_state.cap_ans = cols_reg_cap[1].text_input("Answer", max_chars=self.dict_auth.get("cap_len"),
                                                                              key="ticpns", value=st.session_state.cap_ans_val,
                                                                              help=self.captcha_help_msg)
                        st.divider()
                        btn_reg_new_usr = st.form_submit_button("Register")
                        if btn_reg_new_usr:
                            can_reg_usr = True
                            if st.session_state.reg_username == "":
                                st.markdown(":red[Enter a user name.]")
                                can_reg_usr = False
                            elif not self.is_unique_username(auth_config, st.session_state.reg_username):
                                st.markdown(":red[The user name already exists. Please specify another user name.]")
                                can_reg_usr = False
                            elif st.session_state.reg_name == "":
                                st.markdown(":red[Enter a name.]")
                                can_reg_usr = False
                            elif st.session_state.reg_email == "":
                                st.markdown(":red[Enter your email address.]")
                                can_reg_usr = False
                            elif not self.is_valid_eml_addr(st.session_state.reg_email):
                                st.markdown(":red[Enter a valid email address.]")
                                can_reg_usr = False
                            elif not self.is_unique_em_addr(auth_config, st.session_state.reg_email,
                                                            st.session_state.reg_username,False):
                                st.markdown(":red[The email address is already in use. Please specify another email address.]")
                                can_reg_usr = False
                            elif reg_conf_email == "":
                                st.markdown(":red[Enter your confirmation email address.]")
                                can_reg_usr = False
                            elif reg_conf_email != st.session_state.reg_email:
                                st.markdown(":red[email and confirmation email addresses do not match.]")
                                can_reg_usr = False
                            elif not authenticator.authentication_controller.validator.validate_password(reg_pwd):
                                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_new_pwd") + "]")
                                can_reg_usr = False
                            elif reg_pwd != reg_conf_pwd:
                                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_conf_new_pwd") + "]")
                                can_reg_usr = False
                            elif st.session_state.cap_ans == "":
                                st.markdown(":red[Enter the captcha value]")
                                can_reg_usr = False
                            elif st.session_state.cap_ans != st.session_state.random_cap[0:5]:
                                st.session_state.randomize_cap = True
                                st.session_state.cap_ans = ""
                                st.session_state.cap_ans_val = ""
                                st.rerun()
                            if can_reg_usr:
                                new_user = {
                                    st.session_state.reg_username.lower(): {
                                        "email": st.session_state.reg_email,
                                        "name": st.session_state.reg_name,
                                        "password": stauth.Hasher.hash(reg_pwd)
                                    }
                                }
                                auth_config["credentials"]["usernames"].update(new_user)
                                self.write_auth_obj(auth_config)
                                shutil.copy(str(self.dict_config.get("ini_config_def")),
                                            str(self.dict_config.get("ini_config_usr")) + st.session_state.reg_username.lower() + "_.ini")
                                shutil.copy(str(self.dict_config.get("toml_config_def")),
                                            str(self.dict_config.get("toml_config_usr")) + st.session_state.reg_username.lower() + "_.toml")
                                st.session_state.usr_registered = True
                                st.rerun()

    def send_pwd_msg(self, auth_config, username_forgot_pw, random_password):
        message = MIMEMultipart()
        message['From'] = self.__Load_lib_adr()
        message['To'] = auth_config["credentials"]["usernames"][username_forgot_pw]["email"]
        message['Subject'] = "Forgot password - your new password from Librotate"
        body = self.dict_frgt_pwd_txts.get("frgt_pwd_email_msg").format(
                                                     name=auth_config["credentials"]["usernames"][username_forgot_pw]["name"],
                                                     pwd=str(random_password))
        message.attach(MIMEText(body, 'plain'))
        try:
            self.__process_msg(auth_config["credentials"]["usernames"][username_forgot_pw]["email"], message)
            st.success('New password sent securely')
        except Exception as ex:
            st.write("Error sending email: " + str(ex))

    def send_verify_email_msg(self, auth_config, username, verify_code):
        message = MIMEMultipart()
        message['From'] = self.__Load_lib_adr()
        message['To'] = auth_config["credentials"]["usernames"][username]["email"]
        message['Subject'] = "Verify your email address - your new account with Librotate"
        body = self.dict_verify_email_msg.format(name=auth_config["credentials"]["usernames"][username]["name"],
                                                     code=str(verify_code))
        message.attach(MIMEText(body, 'plain'))
        try:
            self.__process_msg(auth_config["credentials"]["usernames"][username]["email"], message)
        except Exception as ex:
            st.write("Error sending email: " + str(ex))

    def send_wlcm_msg(self, auth_config, username):
        message = MIMEMultipart()
        message['From'] = self.__Load_lib_adr()
        message['To'] = auth_config["credentials"]["usernames"][username]["email"]
        message['Subject'] = "Welcome to Librotate"
        body = self.dict_wlcm_msg.format(name=auth_config["credentials"]["usernames"][username]["name"])
        message.attach(MIMEText(body, 'plain'))
        try:
            self.__process_msg(auth_config["credentials"]["usernames"][username]["email"], message)
        except Exception as ex:
            st.write("Error sending email: " + str(ex))

    def __process_msg(self, email, message):
        server = None
        try:
            server = smtplib.SMTP_SSL(self.__Load_lib_server_nm(),
                                      self.__Load_lib_server_prt())  # Or can use smtp.gmail.com for port 587 and .starttls()
            server.login(self.__Load_lib_adr(),
                         self.decrypt(self.__Load_lib_server_creds()))  # THIS ACCOUNT IS ALSO PROTECTED BY MFA
            server.sendmail(self.__Load_lib_adr(), email, message.as_string())
        except Exception as ex:
            raise ex
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
                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_curr_pwd") + "]")
                can_change = False
            elif not authenticator.authentication_controller.validator.validate_password(st.session_state.pwd_new):
                st.markdown(
                    ":red["  + self.dict_chng_pwd_err_msgs.get("valid_new_pwd") + "]")
                can_change = False
            elif st.session_state.pwd_new == st.session_state.pwd_current:
                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_uniq_new_pwd") + "]")
                can_change = False
            elif st.session_state.pwd_new != st.session_state.pwd_new_confirm:
                st.markdown(":red[" + self.dict_chng_pwd_err_msgs.get("valid_conf_new_pwd") + "]")
                can_change = False
            if can_change:
                hashed_password = stauth.Hasher.hash(st.session_state.pwd_new)
                auth_config["credentials"]["usernames"][st.session_state.username]["password"] = hashed_password
                self.write_auth_obj(auth_config)
                return True

    def is_unique_username(self, auth_config, usrname):
        is_unique_usrnm = True
        for usernames in auth_config["credentials"]["usernames"]:
            if usernames == usrname:
                is_unique_usrnm = False
        return is_unique_usrnm

    dict_frgt_pwd_txts = {
        "frgt_pwd_info": """Enter your user name and submit the below form. You will then receive an email to your email address
                             (the one you have specified in your profile account), which will contain a one-time password. You can
                             then login with this temporary password and change it to a regular-use one in your profile settings.""",
        "frgt_pwd_email_msg": """Hello, {name}. Your one-time password to login to Librotate is:
                              \r\r{pwd}
                              \r\rRegards,
                              \r\rThe Librotate team."""
    }

    dict_verify_email_msg = ("Hello, {name}. Your one-time " +
                             str(dict_auth.get("ver_code_len")) +
                             "-digit code to verify your Librotate email address is: \r\r{code}\r\rRegards,\r\rThe Librotate team.")

    dict_wlcm_msg = ("""Hello, {name}. Welcome to Librotate! \r\r
                     Librotate enables you to build and manage a comprehensive store of your academic projects' data.  
                     Select either 'View' or 'Do' from the left-hand sidebar in order to see or add, update your 
                     academic or school project notes - then select from your annotated, database-stored records, book entries, 
                     or online URL-referenced pages. Make use of the multiple data search facilities, and dredge-search the Internet 
                     using your stored URLs for single or multi search terms.
                     \r\rSee the full user guide <COMPLETE> here.
                     \r\rHave fun and regards,\r\rThe Librotate team.""")

    BLOCK_SIZE = 32  # Bytes

    captcha_help_msg = """Enter the 5-character code you see in the image to the left. If you are not directed 
                          to the confrmation-new-user-created page, then the code you entered did not match 
                          the code shown in the image. So you need to try again."""