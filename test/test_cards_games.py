import re
import time
import pyautogui
import pytest
from modules_for_test.video_record import VideoRec
import allure


class CardsGames(VideoRec):

    def __init__(self) -> None:
        super().__init__()

    # RED = "\033[31m"
    # GREEN = "\033[32m"
    # RESET = "\033[0m"


        self.card_check_text: tuple[str, str] = (
            "click", "search_line_click.png"
        )

        self.path_to_images: str = "/home/user/Test_Native_Client/images/games_cards"

        self.credentials_app: dict[str, str] = {
            "email": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "passw": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
        self.auth_app_images: tuple[str, str] = (
            "3_email_click.png", "4_pass_click.png", "remember_my_click.png", "sing_in_click.png", "whats_new.png"
        )
        self.run_app: tuple[str, str] = (
            "start_app.png"
        )
        self.prepare_for_the_test: tuple[str, str] = (
            "whats_new_ok_click.png", "edudc_firs_img.png", "edudc_firs_img.png", "educ_first_img_skip_click.png",
            "your_free_time.png", "allrighs_your_free_time_click.png"
        )
        """Check the games in order: Dota, CS, Fortnite, Crossout"""
        self.find_and_check_games: tuple[str, str] = (
            "whats_new_ok_click.png", "edudc_firs_img.png", "edudc_firs_img.png", "educ_first_img_skip_click.png",
            "your_free_time.png", "allrighs_your_free_time_click.png",
            "search_line_click.png", "dota_click.png", "dota_card.png", "dota_card_inside.png", "search_line_click.png",
            "counter_strike_click.png", "counter_strike_card.png", "counter_strike_card_inside.png", "search_line_click.png",
            "fortnite_click.png", "fortnite_card.png", "fortnite_card_inside.png", "search_line_click.png",
            "crossout_click.png", "crossout_card.png", "crossout_card_inside.png", "full_screen_click.png", "search_line_click.png",
            "dota_click.png", "dota_card_full.png", "dota_card_inside_full.png", "search_line_click.png", "counter_strike_click.png",
            "counter_strike_card_full.png", "counter_strike_inside_full.png", "search_line_click.png", "fortnite_click.png",
            "fortnite_card_full.png", "fortnite_card__inside_full.png", "search_line_click.png", "crossout_click.png",
            "crossout_card_full.png", "crossout_card_inside_full.png", "return_back_click.png", "prod_accaun_settings_click.png",
            "log_out_click.png", "log_out_confirm.png", "log_out_botton_confirm_click.png", "close_app_click.png"
        )
        self.searching_field_test: tuple[str, str] = (
            "dota", "counter", "fortnite", "crossout", "dota", "counter", "fortnite", "crossout"
        )
        self._counter: int = 0





class TestCardsGames:
    cg = None

    @pytest.fixture(autouse=True)
    def init(self):
        if not TestCardsGames.cg:
            TestCardsGames.cg = CardsGames()
        self.cg = TestCardsGames.cg

    @allure.story("Test: Run application, Login, and Check cards")   
    def test_runApplication(self):
        self.cg.logger.info("Running Test: Run application, Login, and Check cards")
        recording = None
        try:
            recording = self.cg.start_video_recording(self.__class__.__name__)
            self.run_application()
            self.login_application()
            self.check_cards()
        finally:
            if recording is not None:
                self.cg.stop_threads()
                self.cg.stop_video_recording(recording)

    def run_application(self):
        self.cg.logger.info("Running sub-test: Run application")
        try:
            result = self.cg.startProcess(self.cg.run_app)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.cg.get_screenshot("run_application.png")
                allure.attach.file(screenshot_path, name="run_application", attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.cg.get_screenshot("run_application_failed.png")
            allure.attach.file(screenshot_path, name="run_application_failed", attachment_type=allure.attachment_type.PNG)
            raise

    def login_application(self):
        self.cg.logger.info("Running sub-test: Login application")
        try:
            result = self.cg.boosteroidAuth(self.cg.auth_app_images, self.cg.credentials_app)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.cg.get_screenshot("login_application.png")
                allure.attach.file(screenshot_path, name="login_application", attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.cg.get_screenshot("login_application_failed.png")
            allure.attach.file(screenshot_path, name="login_application_failed", attachment_type=allure.attachment_type.PNG)
            raise

    def check_cards(self):
        self.cg.logger.info("Running sub-test: Check cards")
        try:
            result = self.cg.click_write_or_findAndWait(self.cg.find_and_check_games, self.cg.searching_field_test, self.cg.card_check_text)
            assert result is True
            with allure.step("Attach screenshot"):
                screenshot_path = self.cg.get_screenshot("check_cards.png")
                allure.attach.file(screenshot_path, name="check_cards", attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.cg.get_screenshot("check_cards_failed.png")
            allure.attach.file(screenshot_path, name="check_cards_failed", attachment_type=allure.attachment_type.PNG)
            raise
"""

if __name__ == '__main__':
    start_time = time.time()
    
    cg = CardsGames()
    recording = cg.start_video_recording(cg.__class__.__name__)
    if not cg.startProcess(cg.run_app):
        cg.logger.error("Failed to start process")
        cg.get_screenshot("Not started")    

    if not cg.boosteroidAuth(cg.auth_app_images, cg.credentials_app):
        cg.logger.error("Failed to authenticate")
        cg.get_screenshot("auth_error")
    
    if not cg.click_write_or_findAndWait(
        cg.find_and_check_games, cg.searching_field_test, cg.card_check_text):
        cg.logger.error("Failed check card")
        cg.get_screenshot("check card")
        
    else:
        cg.logger.info("Success start -> Success auth -> Success check card")        
        
    cg.stop_threads()
    cg.stop_video_recording(recording)
    end_time = time.time()
    execution_time = int(end_time - start_time)
    cg.logger.info("Test execution time: '%s' sec.", execution_time)
    print(f"\033[32mTest execution time: \033[33m'{execution_time}'\033[0m\033[32msec.\033[0m")
"""
