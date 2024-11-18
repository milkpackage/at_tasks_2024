"""
just video recorder conf
"""

import cv2
import numpy as np
from PIL import ImageGrab
import logging

logger = logging.getLogger(__name__)


class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.writer = None

    def start_recording(self, filename):
        if not self.recording:
            try:
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
                logger.info(f"Started recording: {filename}")
            except Exception as e:
                logger.error(f"Failed to start recording: {e}")

    def capture_frame(self):
        if self.recording and self.writer:
            try:
                screen = ImageGrab.grab()
                frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
                self.writer.write(frame)
            except Exception as e:
                logger.error(f"Failed to capture frame: {e}")

    def stop_recording(self):
        if self.recording:
            try:
                self.recording = False
                if self.writer:
                    self.writer.release()
                    logger.info("Recording stopped")
            except Exception as e:
                logger.error(f"Failed to stop recording: {e}")