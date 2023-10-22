import sys
import time
from modules_for_test.video_record import VideoRec
from typing import Optional, Tuple
import allure
import pytest


class UpdateApp(VideoRec):

    def __init__(self) -> None:
        super().__init__()

        self.credentials_app: dict[str, str] = {
            "email": "XXXXXXXXXXXXXXXXXXXXXX",
            "passw": "XXXXXXXXXXXXXXXXXXXXXX"
        }

        self.path_to_images: str = "/home/user/Test_Native_Client/images/update_app"
        self.images_tuple: tuple[str, str] = (
            "update_window.png", "update_click.png", "updating_progress.png", "enter_pass_confirm.png",
            "password_input_click.png",	"authenticate_click.png", "app_log_in_main.png"
        )
        self.check_text: tuple[str, str] = (
            "click", "password_input_click.png"
        )
        self.write_text: tuple[str, str] = (
            "123123123", ""
        )
        self.image_auth: tuple[str, str] = (
            "email_input_click.png", "password_auth_input_click.png", "remember_click.png", "login_button_click.png",
            "whats_new.png"
        )
        self.image_accaunt: tuple[str, str] = (
            "whats_new_ok_click.png", "edu_1.png", "edu_1_click.png", "wour_free_time.png", "your_free_time_alright_click.png", "prod_accaunt_button_click.png",
            "accaunt_menu_settings_click.png", "booste_games_s.r.l.png"
		)
        self.timeout: int = 45
        

    def environment_preparation(self) -> bool:
        self.checks_if_app_running()
        self.check_if_app_installed()
        self.remove_boosteroid()
        return True
    
    def compare_app_ver(self) -> bool:
        app_versions = self.update_application()

        if app_versions is None:
            self.logger.error("\033[31mMethod 'compare_ver_values': application version is '%s' application updating failed\033[0m", app_versions)
            return False

        ver_app_defore_update, ver_app_after_updating = app_versions

        
            
        if ver_app_defore_update['ver_without_dots'] < ver_app_after_updating['ver_without_dots']:
            self.logger.info(f"\033[32mPrevious version:{ver_app_defore_update['ver']}, is less than new version:{ver_app_after_updating['ver']}\033[0m")
            if self.boosteroidAuth(file_name=self.image_auth, credentials=self.credentials_app):
                self.click_write_or_findAndWait(file_name=self.image_accaunt, find_text=self.check_text)
                self.get_screenshot("update_app")
                self.logger.info("\033[32mThe client is successfully updating,old version is '%s' existing version is: '%s'\033[0m", ver_app_defore_update['ver'], ver_app_after_updating['ver'])
                return True
        else:
            self.get_screenshot('failed_ver_app_defore_update')
            self.logger.error(f"\033[31mPrevious version:{ver_app_defore_update['ver']}, is not less than new version:{ver_app_after_updating['ver']}\033[0m")
            return False
        
                
                
    def update_application(self) -> Optional[Tuple[dict, dict]]:
               
        if not self.installation_app():
            self.logger.error("\033[31mMethod 'update_application' failed: 'installation_app' returned False\033[0m")
            return None

        if not self.check_if_app_installed():
            self.logger.error("\033[31mMethod 'update_application' failed: 'check_if_app_installed' returned False\033[0m")
            return None

        if not self.startProcess(self.images_tuple[0]):
            self.logger.error("\033[31mMethod 'update_application' failed: 'startProcess' returned False\033[0m")
            return None
        
        if not self.click_write_or_findAndWait(file_name=self.images_tuple, write_text=self.write_text, find_text=self.check_text):
            self.logger.error("\033[31mMethod 'update_application' failed: 'click_write_or_findAndWait' returned False\033[0m")
            return None
        
        if not self.checks_if_app_running():
            self.logger.error("\033[31mMethod 'update_application' failed: 'checks_if_app_running' returned False\033[0m")
            return None
        
        if not self.startProcess(self.images_tuple[6]):
            self.logger.error("\033[31mMethod 'update_application' failed: 'startProcess-2' returned False\033[0m")
        
        ver_app_defore_update = self.check_app_version()
        ver_app_after_updating = self.find_values_in_file(self.boostroid_logs, "Using UA")
        return ver_app_defore_update, ver_app_after_updating


@allure.feature("Update app")
class TestUpdateApp:
    up = None

    @pytest.fixture(autouse=True)
    def init(self):

        if not TestUpdateApp.up:
            TestUpdateApp.up = UpdateApp()
        self.reg = TestUpdateApp.up

    @allure.story("Test 1:Updating 'boosteroid' application")
    @pytest.mark.run(order=1)
    def test_environment_preparation(self):
        self.reg.logger.info(
            "\tRunning Test1 -'test_environment_preparation': close 'Boosteroid' app -> remove them from os -> update app\n")
        recording = None
        try:
            recording = self.reg.start_video_recording(self.__class__.__name__)           
            result = self.up.environment_preparation() 
            result2 = self.up.compare_app_ver()
            assert result is True
            assert result2 is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot(
                    "1_update_app.png")
                allure.attach.file(screenshot_path, name="update_app",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot(
                "update_app_failed.png")
            allure.attach.file(screenshot_path, name="update_app_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise
        finally:
            if recording is not None:
                    self.reg.stop_threads()
                    self.reg.stop_video_recording(recording)

        allure.attach("Expected Result:",
                      "Boosteroid application will be closed, Boosteroid application will be \
                        removed, after removing old version application will be installed and updated to later version")
        allure.attach(
            "Summary:", "Test installed 'boosteroid' application and update it")

"""

if __name__ == '__main__':
    start_time = time.time()

    up = UpdateApp()

    if not up.environment_preparation():
        up.get_screenshot('environment_preparation_boosteroid')
        up.logger.info("\033[31mEnvironment preparation failed\033[0m")           
    if not up.compare_app_ver():
        up.get_screenshot('failed_remove_boosteroid')
        up.logger.info("\033[31mApplication updating failed\033[0m") 

    else:
        up.logger.error("\033[32mApplication updating successful\033[0m") 
        up.get_screenshot('failed_remove_boosteroid')
                 

    
    end_time = time.time()
    execution_time = int(end_time - start_time)
    up.logger.info("Test execution time: '%s' sec.", execution_time)
    print(f"\033[32mTest execution time: \033[33m'{execution_time}'\033[0m\033[32msec.\033[0m")
"""
