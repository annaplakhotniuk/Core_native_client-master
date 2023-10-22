import re
import datetime
import subprocess
import numpy as np
import pyautogui
import time
import os
import logging




class Base:

    
    def __init__(self) -> None:

        # Initialization for class names
        class_name = self.__class__.__name__

        # preparation of the log tape structure
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s  [%(name)s]  %(levelname)s - %(message)s')

        # Create a file handler
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_test: str =  (f"{class_name}_logs_{timestamp}.log")
        logs_test_directory: str = "/home/user/Test_Native_Client/logs_test/"
        test_logs: str = os.path.join(logs_test_directory, log_file_test)

        # Create the logs_test directory if it doesn't exist
        if not os.path.exists(logs_test_directory):
            os.makedirs(logs_test_directory)
        
        fh = logging.FileHandler(test_logs)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # Create a stream handler for stdout
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        
        # Add the file handler to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

        # path and name of log file 'logs' for aplication
        self.boostroid_logs: str = "/home/user/Test_Native_Client/logs/"      
        if not os.path.exists(self.boostroid_logs):
            os.makedirs(self.boostroid_logs)  
        self.log_file_name = f"Boost_Test:'{class_name}'{timestamp}.log"
        self.log_file_path = os.path.join(self.boostroid_logs, self.log_file_name)

        # Paths and names for components 
        self.root_pass: str = "123123123"
        self.app_name: str = "Boosteroid"
        self.path_to_boost_deb: str = "/home/user/Downloads/"
        self.boost_app: str = "boosteroid-install-x64.deb"
        self.bin_app_path: str = ("/opt/BoosteroidGamesS.R.L./bin/Boosteroid")
        self.screenshot_directory: str = "/home/user/Test_Native_Client/screenshot"
        self.config_file_path: str = '/home/user/.config/Boosteroid Games S.R.L./Boosteroid.conf'        
        
        # Data for 'click_image' and 'findImageAndWait'       
        self.region: tuple = (0, 0, 1920, 1080)
        self.timeout: int = 30
        #self.image_location: tuple = None
        self._counter: int = 0

        
        
    
    def startProcess(self, file_name: str) -> bool:
        self.logger.debug("Start 'checks_if_app_running': checking if the app '%s' is running", self.app_name)
        if not self.checks_if_app_running():
            self.logger.debug("Start 'applicationLaunching': no running application '%s' detected in the system", self.app_name)
        if (self.remove_conf_file() and self.applicationLaunching()):
            self.logger.debug("Start 'startProcess': checking the presence of an element '%s' on the screen", file_name)            
            if self.findImageAndWait(file_name) is True:
                self.logger.info(f"\033[32mStart application successful\033[0m")
                return True
            else:
                self.logger.error(f"\033[31mStart application failed\033[0m")
                return False
        else:
            self.logger.debug("\tMethod 'startProcess', can't launch application '%s'-False", self.app_name)
            return False


    def find_values_in_file(self, path_to_file: str, find_value: str, file_name: str = None):        
        command = f"ls -ltr {path_to_file}"
        result = subprocess.check_output(command, shell=True, text=True)
        lines = result.strip().split('\n') 
        last_line = lines[-1]
        file_name = last_line.split()[-1]        
        self.logger.debug("Method 'find_values_in_file': view the last created file '%s'\n in the directory '%s'", lines, self.boostroid_logs)
        path = os.path.join(path_to_file, file_name)
        try:
            with open(path, 'r', encoding='UTF-8') as file:
                lines = file.readlines()
                found_lines = []
                for line in lines:
                    if re.search(find_value, line):
                        found_lines.append(line)
                        self.logger.debug("Method 'find_values_in_file': try to find '%s' in '%s'", find_value, path)                    
                if found_lines:
                    for line in found_lines:
                        ver = re.search(r"(\d+\.\d+\.\d+)", line)
                        ver_text =  ver.group(1)
                        version_output = {'ver': ver_text, 'ver_without_dots': ver_text.replace(".", "")}
                        self.logger.debug("Method 'find_values_in_file': found '%s' in '%s'", ver_text, path)
                        return version_output 
                else:
                    self.logger.error("Method 'find_values_in_file': could find '%s' in '%s'", find_value, path)             
        except Exception as e:
            self.logger.info("Fail to openong file '%s', error inf '%s'", path, e)        
        

    def test_auth(self, clickable_images: tuple[str, ...]=None, unlockable_images: tuple[str, ...]=None, start_index=0, end_index: int = None) -> bool:
        success = True
        for index, image_name in enumerate(clickable_images[start_index:end_index], start=start_index):
            if image_name in unlockable_images:
                if not self.findImageAndWait(image_name):
                    self.logger.debug("Method 'test_auth': object '%s' in: Unlockable list-False", image_name)
                    success = False
                    break
            elif self.click_image(image_name):
                self.logger.debug("Method 'test_auth': object '%s' in: Clickable list", image_name)                
            else:                
                self.logger.debug("Method 'test_auth': could not find '%s'-False", image_name)
                success = False
                break
            
        if success:
            self.logger.info("\033[32mMethod 'test_auth': Test auth successful\033[0m")
            return True
        else:
            self.logger.error("\033[31mMethod 'test_auth': Test auth failed\033[0m")
            return False


    def preparation_before_install(self) -> bool:
        self.logger.debug(
                f"Method 'preparation_before_install':  try find already instaled app 'boosteroid'")
        command = 'apt list --installed | grep boosteroid'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode == 0:
            output = output.decode('utf-8')
            match = re.search(r'boosteroid', output)
            if match:
                self.logger.debug("Method 'preparation_before_install': find already instaled app '%s'-True", match)
                return True
            else:
                return False            
        if process.returncode == 1:
            error = error.decode('utf-8')
            self.logger.debug(f"Method 'preparation_before_install': could find already instaled app 'Boosteroid' {error}")
            return False           


    def check_if_app_installed(self) -> bool:
        result = subprocess.run(['dpkg', '-s', self.app_name.lower()], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.lower()
            if 'status: install ok installed' in output:
                self.logger.info("Method 'check_if_app_installed': '%s' installed in OS-True", self.app_name)
                self.logger.debug("STDERR 'check_if_app_installed' command: installed in OS '%s'-True", result.stdout)
                return True
        self.logger.info("Method 'check_if_app_installed': '%s' not installed in OS-False", self.app_name)
        self.logger.debug("STDERR 'check_if_app_installed': '%s' not installed in OS-False", result.stdout)
        return False    


    def check_app_version(self) -> dict:
        command = ['dpkg', '-s', self.app_name.lower()]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            match = re.search(r"Version:\s+(\S+)", result.stdout)
            if match:
                  version = match.group(1)
                  version_without_dots = version.replace(".", "")
                  self.logger.debug("Method 'check_app_version': version of '%s' is: '%s'", self.app_name, version)
                  version_output = {'ver': version, 'ver_without_dots': version_without_dots}
                  return version_output
            else:
                self.logger.error("Method 'check_app_version': version of '%s' is: '%s'", self.app_name, version)
                return None
        else:
            self.logger.error("Method 'check_app_version': error '%s' application name '%s'", result, self.app_name)
            return None


    def remove_boosteroid(self) -> bool:
        command = ['sudo', '-S', 'apt', 'remove', '-y', self.app_name.lower()]
        process = subprocess.run(command, capture_output=True,
                                 text=True, input=self.root_pass+'\n', encoding='utf-8')
        if process.returncode == 0:
            #self.logger.debug(process.stdout)
            self.logger.info(
                "Method 'remove_boosteroid: '%s' removed successfully-True", self.app_name)
            self.logger.debug("STDOUT 'apt remove' command: %s-True", process.stdout)
            return True
        else:
            self.logger.info(
                "Method 'remove_boosteroid: failed to remove %s-False", self.app_name)
            self.logger.debug("STDERR 'apt remove' command: %s-False", process.stderr)
            return False


    def installation_app(self) -> bool:
        os.chdir(self.path_to_boost_deb)
        result = subprocess.run(['ls', '-ls'], capture_output=True, text=True)
        output_lines = result.stdout.split('\n')
        self.logger.debug("Method 'installation_app': checking the contents of the directory '%s', result is:'%s,",self.path_to_boost_deb, result.stdout)
        for line in output_lines:
            if self.boost_app in line:
                self.logger.debug("\tFound '%s'", self.boost_app)
                self.logger.info("Method 'installation_app': find '%s' and start istalattion ", line.split()[-1])
                install_result = subprocess.run(
                    ['sudo', '-S', 'dpkg', '-i', line.split()[-1]], capture_output=True, text=True, input=self.root_pass+'\n')
                self.logger.debug(install_result.stdout)
                if install_result.returncode == 0:
                    self.logger.info("Method 'installation_app': installation successful:'%s'-True", self.boost_app)                    
                    return True
                else:
                    self.logger.error("STRDERR 'installation_app': installation failed with error:'%s'-True ", install_result.stderr)
                    return False
        self.logger.error("Method 'installation_app:'%s' not found-True\n STDOUT:'%s' ", self.boost_app, result.stdout)
        return False
    
    
    def checks_if_app_running(self) -> bool:
        result = subprocess.run(['pgrep', self.app_name], capture_output=True, text=True)
        pids = result.stdout.split('\n')
        self.logger.debug("Method 'checks_if_app_running': pids: %s, result: %s", pids, result.stdout)
        for pid in pids:
            if pid:
                try:
                    self.logger.warning("Method 'checks_if_app_running': the process '%s' with PID '%s' is already running", self.app_name, pid)
                    subprocess.run(['kill', '-9', pid])                    
                except OSError as e:
                    self.logger.error("Method 'checks_if_app_running': failed to kill process '%s', with PID '%s': '%s'-False", self.app_name, pid, str(e))
                    return False
                else:
                    self.logger.warning("Method 'checks_if_app_running': the process '%s' with PID '%s' was killed-True", self.app_name, pid)
                    time.sleep(1)
                    return True       
        #self.logger.debug("Method 'checks_if_app_running': the process '%s' is not already running-False", self.app_name)
        #return False
    

    def remove_conf_file(self) -> bool:
        if os.path.exists(self.config_file_path):             
            os.remove(self.config_file_path)
            self.logger.info("Method 'remove_conf_file': file '%s' exists, proceed with removal-True", self.config_file_path)            
        else:            
            self.logger.warning("Method 'remove_conf_file': config file '%s' doesn't exist-False", self.config_file_path)   
        return True        


    def applicationLaunching(self) -> bool:
        try:
            directory = os.path.dirname(self.config_file_path)
            os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

            with open(self.config_file_path, 'w'):
                self.logger.debug(f"Create new log file: '{self.config_file_path}'")
        except Exception as e:
            self.logger.error("Failed to create log file: '%s': '%s'", self.config_file_path, str(e))
            return False
        try:
            with open(self.log_file_path, 'w') as stdout_file:
                self.logger.debug("Start application: '%s'", self.app_name)
                process = subprocess.Popen(self.bin_app_path, stdout=stdout_file, stderr=subprocess.STDOUT)
                time.sleep(5)
                self.logger.debug("Method 'applicationLaunching': check if the program '%s' is running", self.app_name)

                if process.poll() is None:
                    self.logger.debug("Method 'applicationLaunching': before starting the application '%s', no running", self.app_name)

                if not os.path.exists(self.screenshot_directory):
                    os.makedirs(self.screenshot_directory)
                    self.logger.debug("Method 'applicationLaunching': created directory: '%s'", self.screenshot_directory)
                os.chdir(self.screenshot_directory)
                self.logger.debug("Method 'applicationLaunching': change current directory to: '%s'", self.screenshot_directory)
                return True

        except Exception as e:
            self.logger.debug("Method 'applicationLaunching': program '%s' not running-False: %s", self.app_name, str(e))
            return False
        

    def findImageAndWait(self, file_name: tuple[str, ...]=None, image_location: tuple = None, _counter: int = 0) -> bool:        
        while image_location is None:
            image_location = pyautogui.locateCenterOnScreen(os.path.join(self.path_to_images, file_name), confidence=0.8, region=self.region)
            pyautogui.moveTo(image_location)
            _counter += 1
            if _counter > 2:
                self.logger.warning("Try '%s': could find object '%s'", _counter, file_name)
            if _counter == self.timeout:
                self.logger.error("Method: 'findImageAndWait': Can't find item '%s', timeout is '%s'sec.-False", file_name, _counter)                
                return False          
        self.logger.info("Found element '%s', location is '%s'-True", file_name, image_location)
        return True


    def click_image(self, file_name: str=None, image_location: tuple = None, _counter: int=0):
        while image_location is None:
            image_location = pyautogui.locateCenterOnScreen(os.path.join(self.path_to_images, file_name),\
                                                             confidence=0.8, region=self.region)             
            _counter += 1
            if _counter > 2:
                self.logger.warning("Try '%s': could click on object '%s'", _counter, file_name)
            if _counter == self.timeout:
                self.logger.error("Method 'click_image': Can't find item '%s', location is '%s', timeout is '%s' sec-False", file_name, image_location, _counter)                
                return False     
        if image_location is None:
            self.logger.error("Method: 'click_image' not found '%s'-False", file_name)            
            return False
        else:            
            self.logger.info("Click '%s', which is located at '%s'-True", file_name, image_location)
            pyautogui.moveTo(image_location)    
            pyautogui.click(image_location)
            time.sleep(0.8)
            return True


    def get_screenshot(self, file_name: str = None) -> str:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{file_name}_{timestamp}.png"
        screenshot_path = os.path.join(self.screenshot_directory, file_name)
        pyautogui.screenshot(screenshot_path)        
        self.logger.info("Screenshot saved to: '%s'", screenshot_path)
        return screenshot_path
    
    
    def boosteroidAuth(self, file_name: tuple[str, str] = None, credentials=None) -> bool:
        try:
            if self.click_image(file_name[0]):
                pyautogui.write(credentials["email"])
                if self.click_image(file_name[1]):
                    pyautogui.write(credentials["passw"])
            else:
                self.logger.error(
                    f"\033[31mMethod 'boosteroidAuth': Failed to click on the image: %s-False\033[0m")
                return False

            if not self.click_image(file_name[2]) or not self.click_image(file_name[3]) or not self.findImageAndWait(file_name[4]):
                self.logger.error(
                    f"\033[31mMethod 'boosteroidAuth': One or more images not found or clicked-False\033[0m")
                return False
            else:
                self.logger.info(
                    f"\033[32mMethod 'boosteroidAuth': Successfully authenticated with Boosteroid-True\033[0m")
                return True
        except Exception as e:
            self.logger.error(
                "Method 'boosteroidAuth': Error occurred during Boosteroid authentication: '%s'-False", str(e))
            return False
        
        
    def click_write_or_findAndWait(self, file_name: tuple[str, str], write_text: tuple[str, str] = None, find_text: tuple[str, str] = None) -> bool:
        for x in file_name:
            try:
                if write_text is not None:
                    if re.search(find_text[0], x):
                        if re.search(find_text[1], x):
                            self.click_image(x)
                            pyautogui.write(write_text[self._counter])                        
                            self._counter = (
                                self._counter + 1) % len(write_text)
                            self.logger.debug(
                                "Method 'click_write_or_findAndWait': find '%s' in tuple 'find_and_check_games'- Click", x)
                        else:
                            self.logger.debug(
                                "Method 'click_write_or_findAndWait': find '%s' in tuple 'find_and_check_games'- Click", x)
                            self.click_image(x)
                    elif not self.findImageAndWait(x):
                        self.logger.error(
                            f"\033[31mMethod 'click_write_or_findAndWait' failed on '%s'\033[0m", x)
                        return False
                else:
                    if re.search(find_text[0], x):
                        self.click_image(x)
                        self.logger.info(
                            "Method 'click_write_or_findAndWait': find '%s' in tuple 'find_and_check_games'- Click", x)
                    elif not self.findImageAndWait(x):
                        self.logger.error(
                            f"\033[31m'Click_write_or_findAndWait' failed - '%s'\033[0m", x)
                        return False
            except Exception as e:
                self.logger.error(f"Exception occurred: {e}")
                return False
        self.logger.info(f"\033[32m'Click_write_or_findAndWait' successful\033[0m")
        return True

    def press_key_combination(self, *keys):
        """
        Simulate a key combination press.
        :param keys: The combination of keys to press, e.g., 'ctrl', 'f2', 'shift', etc.
        """
        try:
            # Convert the keys to lowercase to ensure consistency
            keys = [key.lower() for key in keys]
            
            # Check if 'ctrl' and 'shift' are in the keys list and convert them to their respective pyautogui constants
            if 'ctrl' in keys:
                keys[keys.index('ctrl')] = 'ctrlleft'
            if 'shift' in keys:
                keys[keys.index('shift')] = 'shiftleft'

            # Join all the keys with '+' to form the combination
            combination = '+'.join(keys)
            
            # Use pyautogui.hotkey() to press the key combination
            pyautogui.hotkey(combination)
            self.logger.info(f"Key combination '{combination}' pressed.")
            
        except ValueError:
            self.logger.error(f"Invalid key combination." )
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
    