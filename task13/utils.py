import logging
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np
from PIL import ImageGrab
import json


class CustomLogger:
    def __init__(self):
        Path('logs').mkdir(exist_ok=True)

        self.logger = logging.getLogger('TestLogger')
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            f'logs/test_execution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)


class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.writer = None
        Path('video_records').mkdir(exist_ok=True)

    def start_recording(self, test_name):
        if not self.recording:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'video_records/failed_test_{test_name}_{timestamp}.mp4'

            screen = ImageGrab.grab()
            screen_size = screen.size

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(
                filename,
                fourcc,
                10.0,
                screen_size,
                isColor=True
            )
            self.recording = True
            print(f"Started recording: {filename}")

    def capture_frame(self):
        if self.recording and self.writer:
            try:
                screen = ImageGrab.grab()
                frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
                self.writer.write(frame)
            except Exception as e:
                print(f"Error capturing frame: {e}")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.writer:
                self.writer.release()
                print("Recording stopped")


class ResultStorage:
    def __init__(self):
        self.results = []

    def add_result(self, test_name, status, additional_info=None):
        result = {
            'test_name': test_name,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'additional_info': additional_info
        }
        self.results.append(result)

        with open('test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)