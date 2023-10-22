import datetime
import os
import threading
import time
from PIL import Image
import cv2
import numpy as np
import pyautogui
from .Base import Base


class VideoRec(Base):
        
    def __init__(self) -> None:    
        super().__init__()

        # Add video parameters 
        self.threads: list = [] 
        self.recording_thread = None
        self.stop_flag = threading.Event()
        self.test_complete: bool = True  
        self.format: str = "avi"
        self.fps: int = 3
        self.width: int = 1920
        self.height: int = 1080
        self.path_to_videos = "/home/user/Test_Native_Client/allure_video"
           
   
    def screen_record(self, file_name: str):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.file_name_video = f"{file_name}_{timestamp}.{self.format}"

            # Set the screen recording parameters
            self.width, self.height = pyautogui.size()

            # Create the directory if it doesn't exist
            if not os.path.exists(self.path_to_videos):
                os.makedirs(self.path_to_videos)

            # Create video writer object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(os.path.join(self.path_to_videos, self.file_name_video), fourcc, self.fps, (self.width, self.height))

            self.logger.info("Method 'start_video_recording' - Recording started for file: %s", self.file_name_video)
            return out
        except Exception as e:
            self.logger.error("Error method 'screen_record:'%s'", e)

    def record_video(self, recording):        
        _counter = 0
        while not self.stop_flag.is_set():
            try:
                # Capture the screenshot
                screenshot = pyautogui.screenshot()

                # Convert the screenshot to a NumPy array
                frame = np.array(screenshot)

                # Convert the color space if needed (BGR to RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the NumPy array to a PIL Image object
                pil_image = Image.fromarray(frame)

                # Write the frame to the recording
                recording.write(np.array(pil_image))

                time.sleep(0.1)

                # Increment the counter
                #_counter += 1
                #self.logger.debug("Counter numbers is:'%s'", _counter)
            except FileNotFoundError as fnf_error:
                self.logger.error(f"Error occurred during method 'record_video': {str(fnf_error)}")
                
            except Exception as e:
                self.logger.error(f"Error occurred during method 'record_video': {str(e)}")
                

        self.stop_recording(recording)


    def start_video_recording(self, file_name: str):        
        self.recording = self.screen_record(file_name)
        self.recording_thread = threading.Thread(target=self.record_video, args=(self.recording,))
        self.recording_thread.start()
        self.threads.append(self.recording_thread)
        

        return self.recording


    def stop_recording(self, out):
        try:
            # Release the video writer
            if out is not None:
                out.release()
                cv2.destroyAllWindows()                
        except Exception as e:
            self.logger.error(f"Error occurred during video release: {str(e)}")


    def stop_video_recording(self, recording):      
        self.stop_recording(recording)
        # Wait for the recording thread to finish
        if self.recording_thread is not None:
            self.recording_thread.join()

        # Stop and release the recording
        self.stop_recording(recording)
        self.logger.info("Method 'stop_video_recording' - Recording stopped '%s'", self.file_name_video)
        

    def stop_threads(self):
        # Set the stop flag to signal the threads to stop
        self.stop_flag.set()
        # Set a flag to indicate threads should stop
        for thread in self.threads:
            thread.join()
        
        self.threads = []
        self.logger.debug("Method 'stop_threads': threads -'%s'", self.threads)    
