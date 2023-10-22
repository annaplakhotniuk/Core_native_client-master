import subprocess
import requests
import allure
from modules_for_test.video_record import VideoRec
import pytest
import re
import time
import getpass

class NetWork(VideoRec):

    def __init__(self):
        super().__init__()
        
        self.credentials: dict[str, str] = {
            "email": "xxxxxxxxx",
            "passw": "xxxxxxxxx"
            }
        
        self.card_check_text: tuple[str, str] = ("click", "search_line_click.png")   
        

        self.auth_app_images: tuple[str, str] = (
            "3_email_click.png", "4_pass_click.png", "remember_my_click.png", "sing_in_click.png", "whats_new.png"
        )
        self.run_app: tuple[str, str] = (
            "start_app.png"
        )
        self.prepare_for_the_test: tuple[str, str] = (
            "whats_new_ok_click.png", "edudc_firs_img.png", "edudc_firs_img.png", "educ_first_img_skip_click.png",
            "your_free_time.png", "allrighs_your_free_time_click.png", "search_line_click.png", "dota_click.png", "play_click.png", "ok_lets_go_click.png"
        )

        self.path_to_images: str = "/home/user/Test_Native_Client/images/games_cards"

        self.searching_field_test: tuple[str, str] = ("dota",)

        self.ip_addr: dict = {
            "185.2.108.6": "185.2.108.5",
            "185.2.108.5": "185.2.108.6"
        }
        self.root_pass:str = "123123123"
        self.target_ip:str = "192.168.122.206"
        self.network_interface: str = "enp1s0"
        self._counter: int = 0
        self.numbers_of_switches: int = 0
        self.stop_capture: bool = False
        self.protocol_type: str = 'UDP'
        self.switch_limit: int = 5
        self.previev_ip: str = None
        self.token = "XXXXXXXXXXXXXXXXXXX"  
        self.channel = "XXXXXXXXXXXXXXXXXX" 

    def packet_handler(self):
        try:            
            command = ["sudo", "tcpdump", "-i", self.network_interface, "-n", self.protocol_type.lower(), "and", "host", self.target_ip]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            

            # Read the output line by line as it becomes available
            while process.poll() is None and self.stop_capture is False:
                line = process.stdout.readline().strip()
                if line:
                    protocol, src_ip = self.process_packet_line(line)
                    self.check_ip_block_unblock(protocol=protocol, src_ip=src_ip)
                    time.sleep(1)
                else:
                    self.logger.error(f"Method 'packet_handler': error occurred. Exit code: {line}")
                    break
                return False

            # Get the exit code
            exit_code = process.poll()

            if exit_code != 0:
                self.logger.error(f"Method 'packet_handler': error occurred. Exit code: {exit_code}")

            return True

        except Exception as ex:
            self.logger.error(f"Method 'packet_handler': an error occurred: {ex}")
            return False

    def process_packet_line(self, line):
        _counter: int = 0
        pattern = r'(\d+:\d+:\d+)\.\d+ IP (\d+\.\d+\.\d+\.\d+)\.(\d+) > (\d+\.\d+\.\d+\.\d+)\.(\d+): (\w+), length (\d+)'
        match = re.search(pattern, line)

        if match:
            #time_stamp: str = match.group(1)
            src_ip: str = match.group(2)
            src_port: str = match.group(3)
            dst_ip: str = match.group(4)
            dst_port: str = match.group(5)
            protocol: str = match.group(6)
            length: str= match.group(7)

            self.logger.info(f"SrcIP: {src_ip} | SrcPort: {src_port} | Protocol: {protocol} | DstIP: {dst_ip} | DstPort: {dst_port} | Length: {length}")
            return protocol, src_ip

        else:
            _counter += 1
            self.logger.info(f"Method 'process_packet_line': counter is {_counter}")
            if _counter == 20:
                self.logger.error("Method 'process_packet_line': No match found.")
                return False
        
    def check_ip_block_unblock(self, protocol: str=None, src_ip: str=None) -> bool:
        # if protocol or src_ip is None:                       
        #     self.logger.error(f"Method 'check_ip_block_unblock': protocol is: {protocol}, src_ip is: {src_ip}")
        if not self.stop_capture:
            for hostname, unblocked in self.ip_addr.items():
                    if src_ip == hostname:
                        self._counter += 1
                        self.logger.info(f"Counter is: {self._counter}")
                        if self._counter == 20:
                            self.logger.debug("Reset counter")
                            # Try block
                            if not self.check_iptables_stdout(src_ip):
                                self.numbers_of_switches += 1
                                self.logger.debug(f"Try block on {src_ip}")
                                self.reset_all_iptable_rules()
                                self.block_ip(src_ip)  # Block IP using iptables
                            elif self.check_iptables_stdout(src_ip):
                                self.numbers_of_switches += 1
                                self.logger.debug(f"Try block: IP: {src_ip} exists in Iptables -> Reset rules for Blocked IP -> Block IP: {unblocked}")
                                self.reset_all_iptable_rules()
                                self.block_ip(unblocked)
                            self._counter = 0

                    if self.numbers_of_switches == self.switch_limit + 1:
                        self.send_slack_message(f"The switch limit of {self.switch_limit} has been reached!")
                        self.logger.debug(f"The switch limit of {self.switch_limit} has been reached!")
                        self.reset_all_iptable_rules()
                        self.stop_capture = True
                        return True, self.stop_capture
        else:
            return False
 
    def check_iptables_stdout(self, ip) -> bool:
        command = ['sudo', '-S', 'iptables', '-n', '-L']
        try:
            # Start the process with subprocess.PIPE for stdin and pass the root password as input
            result = subprocess.run(command, capture_output=True, text=True, input=self.root_pass + '\n', check=True)
            output = result.stdout
            lines = output.splitlines()

            for line in lines:
                if ip in line:                
                    return True
                
            return False
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the command: {e}")
            return False
    
    def reset_all_iptable_rules(self) -> bool:
        command = ['sudo', '-S', 'iptables', '-F']
        try:
            # Start the process with subprocess.PIPE for stdin and pass the root password as input
            result = subprocess.run(command, capture_output=True, text=True, input=self.root_pass + '\n', check=True)
            output = result.stdout
            self.logger.info(f"RESET ALL RULES {output}")
            return True
        except subprocess.CalledProcessError as e:
            # Handle any errors that occurred during the subprocess execution
            self.logger.error(f"An error occurred while resetting iptable rules: {e}")
            return False     

    def block_ip(self, ip):
        try:
            command = ['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-p', self.protocol_type, '-j', 'DROP']
            ckeck: bool = self.check_iptables_stdout(ip)
            if ckeck is True:
                self.logger.info(f"Method block_ip: ip-{ip} already exists in Iptables list")
            else:
                self.logger.info(f"Method 'block_ip':{ip}")
                subprocess.run(command, input=self.root_pass.encode('utf-8') + b'\n', check=True)
        except Exception as e:
            self.logger.error(f"Method 'block_ip': {e}")        

        
    def unblock_ip(self, ip):
        try:
            ckeck: bool = self.check_iptables_stdout(ip)
            if ckeck is False:
                self.logger.info(f"Method unblock_ip: rule for ip-{ip} does not exist")       
            else:
                self.logger.info(f"Method 'unblock_ip':{ip}")
                try:
                    subprocess.run(['iptables', '-D', 'INPUT', '-s', ip, '-p', self.protocol_type, '-j', 'DROP'], check=True)
                except subprocess.CalledProcessError as e:
                    self.logger.error(f"An error occurred while unblocking IP: {ip}")
                    self.logger.error(f"Error message: {e}")
        except Exception as e:
            print(f"Method 'unblock_ip':{e}")
            

    def start_capture(self) -> bool:
        try:            
            command = ["sudo","tcpdump", "-i", self.network_interface, "udp", "and", "host", self.target_ip]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        
            while process.poll() is None:
                line = process.stdout.readline().strip()
                if line:
                    print(line)
            
            for line in process.stdout.readlines():
                print(line.strip())
            
            exit_code = process.poll()

            if exit_code != 0:
                print(f"Error occurred. Exit code: {exit_code}")
            return True

        except Exception as ex:
            print(f"An error occurred: {ex}")
            return False     
            
    def send_slack_message(self, message) -> bool:
        try:
            payload = {"text": message}
            response = requests.post(self.token, json=payload)

            if response.status_code == 200:
                self.logger.info("Message sent successfully to Slack!")
                return True
            else:
                self.logger.info("Failed to send message to Slack.")
                return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred while sending the message: {e}")
            return False



@allure.feature("Switch between SG")
class TestSwitchBetweenSg:
    up = None

    @pytest.fixture(autouse=True)
    def init(self):

        if not TestSwitchBetweenSg.up:
            TestSwitchBetweenSg.up = NetWork()
        self.reg = TestSwitchBetweenSg.up

    @allure.story("Test:Run app 'Boosteroid', run session and switch between SG")
    @pytest.mark.run(order=1)
    def test_environment_preparation(self):
        self.reg.logger.info(
            "\tRunning Test -'Switch between SG': running app 'Boosteroid' -> start session -> switching between SG\n")
        recording = None
        try:
            # recording = self.reg.start_video_recording(self.__class__.__name__)            
            # result = self.reg.startProcess(self.reg.run_app)
            # assert result is True
            # result1 = self.reg.boosteroidAuth(file_name=self.up.auth_app_images, credentials=self.up.credentials)
            # assert result1 is True
            # result2 = self.reg.click_write_or_findAndWait(self.up.prepare_for_the_test,
            #             write_text=self.up.searching_field_test , find_text=self.up.card_check_text)
            # assert result2 is True
            result3 = self.up.packet_handler()           
            assert result3 is True            

            with allure.step("Attach screenshot"):
                screenshot_path = self.reg.get_screenshot(
                    "switch_sg.png")
                allure.attach.file(screenshot_path, name="switch_sg",
                                   attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            screenshot_path = self.reg.get_screenshot(
                "switch_sg_failed.png")
            allure.attach.file(screenshot_path, name="switch_sg_failed",
                               attachment_type=allure.attachment_type.PNG)
            raise
        finally:
            if recording is not None:
                    self.reg.stop_threads()
                    self.reg.stop_video_recording(recording)

        allure.attach(f"Expected Result:",
                      f"Boosteroid application should be running, start sessinon should be successful, numbers of switches must be '{self.reg.switch_limit}'")
        allure.attach(
            "Summary:", "Test 'Switch between SG': running app 'Boosteroid' -> start session -> switching between SG")

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
