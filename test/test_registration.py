import sys
import time
import allure
import json
import os
import pyautogui
import pytest
from modules_for_test.video_record import VideoRec
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class GmailLogin(VideoRec):

    def __init__(self) -> None:
        super().__init__()
        self.credentials_email: dict[str, str] = {
            "email": "xxxxxxxxxxx",
            "passw": "xxxxxxxxxxx"
        }
        self.new_credentials_email: dict[str, str] = {
            "email": "xxxxxxxxx",
            "passw": "xxxxxxxxx",
            "conf_pass": "xxxxxxxxxxx"
        }
        self.mail_images: tuple[str, str] = (
            "seln4_accep_auth_click.png", "seln5_accept_auth_click.png", "seln6_latter_click.png", "seln7_act_acn_click.png"
        )

        self.app_auth_images: tuple[str, str] = (
            "3_email_click.png", "4_pass_click.png", "remember_my_click.png", "sing_in_click.png", "11_change_log.png"
        )

        self.web_confirm_reg: tuple[str, str] = (
            "web_email_click.png", "web_pass_click.png", "remember_my_web_click.png", "web_sing_in_click.png", "web_main.png",
            "login_in_gmail_acc.png"
        )       

        self.new_user_images: tuple[str, str] = (
            "9_login_main_menu_find.png", "1_create_acc_click.png", "2_create_acc_find.png", "3_email_click.png",
            "4_pass_click.png", "5_reapet_pass_click.png", "6_sing_in_click.png", "7_need_confirm_find.png",
            "10_close_app_click.png"
        )

        self.unlockable_images: tuple[str, ...] = (
            "2_create_acc_find.png", "7_need_confirm_find.png", "9_login_main_menu_find.png", "10_close_app_click.png",
            "if_email_empty.png"
        )
        self.remove_leters: tuple[str, str] = (
            "seln4_accep_auth_click.png", "seln5_accept_auth_click.png", "check_box_del_click.png",
            "button_delete_email_click.png", "if_email_empty.png"
        )
        self.path_to_images: str = "/home/user/Test_Native_Client/images/registration"
        self.path_to_store: str = "/home/user/Test_Native_Client/store"
        self.region: tuple = None
        self.timeout: int = 60

        self.driver = None        
        self.webdriver_path: str = "/home/user/Test_Native_Client/chrome_driver/chromedriver"
        

    def write_json_cred(self, file_name=not None):
        try:
            with open(os.path.join(self.path_to_store, 'credentials.json'), 'w') as file:
                json.dump(file_name, file)
                self.logger.info(
                    "Writed data '%s' in file '%scredentials.json'", file_name, self.path_to_store)
        except Exception as e:
            self.logger.error(
                "Error occurred while writing value:'%s' - error type is:'%s'", file_name, str(e))

    def read_json_cred(self):
        try:
            with open(os.path.join(self.path_to_store, 'credentials.json'), 'r') as file:
                credentials = json.load(file)
                self.logger.info(
                    "Method 'open_google_accounts': read from '%scredentials.json'", self.path_to_store)
                return credentials
        except Exception as e:
            self.logger.error(
                "An error occurred while reading file:'%s' - '%s'", self.path_to_store, str(e))

    def increment_and_save_value(self):
        try:
            credentials = self.read_json_cred()
            number = credentials["previews_value"]
            new_value = number + 1
            credentials["previews_value"] = new_value
            credentials["email"] = f"i.zayats+{new_value}@boosteroid.com"
            self.logger.debug(
                "Method 'increment_and_save_value': read email value '%s, from 'email_result.txt'", number)
            self.write_json_cred(credentials)
            self.logger.debug(
                "Method 'increment_and_save_value': write email value '%s, from 'email_result.txt'", new_value)
            return credentials

        except Exception as e:
            self.logger.error(
                "Error occurred while incrementing and saving value:'%s'", str(e))
            return False

    def boosteroidNewUser(self) -> bool:
        success = True
        message = ""

        if self.click_image(self.new_user_images[1]):
            self.findImageAndWait(self.new_user_images[2])
            if self.increment_and_save_value():
                credentials = self.read_json_cred()
                if self.click_image(self.new_user_images[3]):
                    pyautogui.write(credentials["email"])
                    if self.click_image(self.new_user_images[4]):
                        pyautogui.write(credentials["passw"])
                        if self.click_image(self.new_user_images[5]):
                            pyautogui.write(credentials["conf_pass"])
                            if self.click_image(self.new_user_images[6]) and self.findImageAndWait(self.new_user_images[7]):
                                self.click_image(self.new_user_images[8])                                
                                message = "New user registration successful"                            
                            else:
                                success = False
                                message = "Push confirm and success registration check"
                        else:
                            success = False
                            message = "Confirmation password input failed"
                    else:
                        success = False
                        message = "Password input failed"
                else:
                    success = False
                    message = "Email input failed"
            else:
                success = False
                message = "User increment and save failed"
        else:
            success = False
            message = "New user button click failed"

        if success:
            self.logger.info(f"{message}")
            return True
        else:
            self.logger.error(f"{message}")
            return False
   
    def boosteroidAuth(self, file_name: tuple[str, str] = None, credentials=None) -> bool:
        try:
            if self.click_image(file_name[0]):
                pyautogui.write(credentials["email"])
                if self.click_image(file_name[1]):
                    pyautogui.write(credentials["passw"])
            else:
                self.logger.error(
                    "Method 'boosteroidAuth': Failed to click on the image: %s-False")
                return False

            if not self.click_image(file_name[2]) or not self.click_image(file_name[3]) or not self.findImageAndWait(file_name[4]):
                self.logger.error(
                    "Method 'boosteroidAuth': One or more images not found or clicked-False")
                return False
            else:
                self.logger.info(
                    "Method 'boosteroidAuth': Successfully authenticated with Boosteroid-True")
                return True
        except Exception as e:
            self.logger.error(
                "Method 'boosteroidAuth': Error occurred during Boosteroid authentication: '%s'-False", str(e))
            return False

    def setup(self) -> bool:
        try:
            options = Options()
            options.add_argument("--lang=en-US")
            options.add_argument("--force-dark-mode")
            options.add_argument("--force-renderer-accessibility")
            options.add_experimental_option("prefs", {"force_dark_mode": True})
            service = Service(executable_path=self.webdriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.get("https://www.google.com")
            # self.driver.set_window_position(500, 500)
            self.driver.maximize_window()
            self.logger.info(
                "Method 'setup': web browser successfully started.")
            if self.login_to_gmail():
                self.logger.info(
                    f"mAuthorization browser successful")
                return True
            else:
                self.logger.error(
                    f"Authorization browser failed")
                return False
        except Exception as e:
            self.logger.error(
                "Method 'setup': Error occurred during web driver setup: '%s'", str(e))
            return False

    def login_to_gmail(self):
        try:
            sign_in_button = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#gb > div > div.gb_Xd > a > span")))
            sign_in_button.click()
            self.logger.info(
                "Method 'login_to_gmail': Clicked on the 'Sign in' button.")

            email_field = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#identifierId")))
            email_field.send_keys(self.credentials_email['email'])
            email_field.send_keys(Keys.ENTER)
            self.logger.info(
                "Method 'login_to_gmail': Entered email address and pressed ENTER.")

            password_field = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input")))
            password_field.send_keys(self.credentials_email['passw'])
            password_field.send_keys(Keys.ENTER)
            self.logger.info(
                "Method 'login_to_gmail': Entered password and pressed ENTER.")

            if not self.findImageAndWait(self.web_confirm_reg[5]):
                self.logger.error(
                    "Method 'login_to_gmail': could find object %s-False", self.web_confirm_reg[5])
                return False
            self.logger.info(
                "Method 'login_to_gmail': Successfully logged in to Gmail.")
            return True
        except Exception as e:
            self.logger.error(
                "Method 'login_to_gmail': Error occurred during Gmail login: '%s'", str(e))            
            return False

    def open_google_accounts(self) -> bool:
        try:
            credentials = self.read_json_cred()
            success = True

            if not self.test_auth(self.mail_images[0:4], self.unlockable_images):
                success = False

            if success:
                self.findImageAndWait("confirm_email_web_url.png")
                self.logger.info(
                    "Method 'open_google_accounts': 'test_auth' done, find image 'confirm_email_web_url.png'-True")

                if not self.boosteroidAuth(self.web_confirm_reg, credentials):
                    success = False

            self.driver.quit()

            if success:
                self.logger.info(
                    "Confirming registration in browser successful")
                return True
            else:
                self.logger.error(
                    "Confirm registration 'gmaile' failed")
                return False

        except Exception as e:
            self.logger.error(
                "Method 'open_google_accounts': Could not open a new 'https://accounts.google.com' in Browser-False", str(e))
            return False

    def removeEmailLetters(self):
        if self.test_auth(self.remove_leters[0:2], self.unlockable_images):
            if self.findImageAndWait(self.remove_leters[4]):
                self.logger.info("Email list is empty")
                self.driver.quit()
                return True
            elif self.test_auth(self.remove_leters[2:5], self.unlockable_images):
                self.logger.info(
                    "Email letters is successful removed")
                self.driver.quit()
                return True
        else:
            self.logger.error("Removing letters is failed")
            self.driver.quit()
            return False


"""

if __name__ == '__main__':
    start_time = time.time()    

    gml = GmailLogin()

    if gml.setup() and gml.removeEmailLetters():
        if gml.startProcess(gml.new_user_images[0]):        
            if gml.boosteroidNewUser():
                if gml.setup():                
                    if gml.open_google_accounts():                                   
                        if gml.startProcess(gml.new_user_images[0]):                                                
                            if gml.boosteroidAuth(gml.app_auth_images, gml.read_json_cred()):
                                gml.logger.info(f"{GREEN}Authorization new user successful{RESET}")
                                gml.get_screenshot("gmail_login_done")
                            else:
                                gml.logger.error(f"{RED}Authorization new user failed{RESET}")
                                gml.get_screenshot("GmailLogi_failed")
                                sys.exit()
                        else:                        
                            gml.get_screenshot("gmail_login_faile")
                            sys.exit()
                    else:
                        gml.get_screenshot("GmailLogi_failed")
                        sys.exit()
                else:
                    gml.get_screenshot("GmailLogi_failed")
                    sys.exit()
            else:            
                gml.get_screenshot("GmailLogi_failed")
                sys.exit()
        else:        
            gml.get_screenshot("GmailLogi_failed")
            sys.exit()
    else:
        gml.get_screenshot("GmailLogi_failed")        
        sys.exit()
    
    
    end_time = time.time()
    execution_time = int(end_time - start_time)
    gml.logger.info("Test execution time: '%s' sec.", execution_time)
    print(f"\033[32mTest execution time: \033[33m'{execution_time}'\033[0m\033[32msec.\033[0m")
"""


@allure.feature("Gmail Login")
class TestGmailLogin:
    reg = None  
    

    @classmethod
    def setup_class(cls):
        if not cls.reg:
            cls.reg = GmailLogin()
        cls.reg.recording = None
    
    @classmethod
    def teardown_class(cls):
        if cls.reg.recording is not None:
            cls.reg.stop_threads()
            cls.reg.stop_video_recording(cls.reg.recording)

    @pytest.fixture(autouse=True)
    def video_recording(self):
        if self.reg.recording is None:
            self.reg.recording = self.reg.start_video_recording(self.__class__.__name__)
        yield  # Run the test methods
        # No need to stop recording here


    @allure.story("Test: New user registration and try autorization in application")  
    def test_ClearLetterList(self):
        self.reg.logger.info("Running Test1 -'test_startProcess': launching browser and remove all letters")
        try:            
            result = False           
            if self.reg.setup():
               result = self.reg.removeEmailLetters()            
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("1_remove_letter")
                allure.attach.file(screenshot_path, name="remove_letter",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("remove_letter_failed")
            allure.attach.file(screenshot_path, name="remove_letter_failed",
                               attachment_type=allure.attachment_type.PNG)
        
    
    def test_startProcess(self):
        self.reg.logger.info("Running Test2 -'test_startProcess': launching application")
        try:
            result = self.reg.startProcess(self.reg.new_user_images[0])
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("2_test_startProcess")
                allure.attach.file(screenshot_path, name="Start_application",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_startProcess_failed")
            allure.attach.file(screenshot_path, name="test_startProcess_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

        allure.attach("Expected Result:", "The user registration should be successful")
        allure.attach("Summary:", "Test the start process of the application and perform user registration")

    
    def test_boosteroidNewUser(self):
        self.reg.logger.info("Running Test3 -'boosteroidNewUser': new user registration")
        try:
            result = self.reg.boosteroidNewUser()
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("3_test_boosteroidNewUser")
                allure.attach.file(screenshot_path, name="Start_application",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_boosteroidNewUser_failed")
            allure.attach.file(screenshot_path, name="Start_application_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

   
    def test_setup(self):
        self.reg.logger.info("Running Test4 -'setup': google login")
        try:
            result = self.reg.setup()
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("4_test_setup")
                allure.attach.file(screenshot_path, name="Start_application",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_setup_failed")
            allure.attach.file(screenshot_path, name="test_setup_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

    
    def test_open_google_accounts(self):
        self.reg.logger.info("Running Test5 -'open_google_accounts': confirm email letter")
        try:
            result = self.reg.open_google_accounts()
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("5_test_open_google_accounts")
            allure.attach.file(screenshot_path, name="Start_application",
                               attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_open_google_accounts_failed")
            allure.attach.file(screenshot_path, name="test_open_google_accounts_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

    
    def test_startProcess2(self):
        self.reg.logger.info("Running Test6 -'test_startProcess': launching application")
        try:
            result = self.reg.startProcess(self.reg.new_user_images[0])
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("6_test_startProcess2")
                allure.attach.file(screenshot_path, name="Start_application",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_startProcess2_failed")
            allure.attach.file(screenshot_path, name="test_startProcess2_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise

    
    def test_boosteroidAuth(self):
        self.reg.logger.info("Running Test7 -'boosteroidAuth': launching application and login check")
        try:
            credentials = self.reg.read_json_cred()
            result = self.reg.boosteroidAuth(self.reg.app_auth_images, credentials)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot("7_test_boosteroidAuth")
                allure.attach.file(screenshot_path, name="test_boosteroidAuth",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot("test_boosteroidAuth_failed")
            allure.attach.file(screenshot_path, name="test_boosteroidAuth_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise
