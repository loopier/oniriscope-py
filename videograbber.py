"""Get streamera frames"""

from threading import Thread
import cv2

from logger import *

class VideoGrabber():
    def __init__(self, sourceId=0):
        """
        Constructor.
        sourceId:   if INT, index of the camera device.
                    if STRING, path of the video file.
        """
        self.sourceId = sourceId
        # Initialize the video stream (cam or file) and
        # read the first frame.
        self.stream = cv2.VideoCapture(sourceId)
        (self.grabbed, self.frame) = self.stream.read()

        # Control threaded frame reading
        self.stopped = False

    def __del__(self):
        """Destructor"""
        self.stream.release()

    def start(self):
        """Start the thread to read frames from the video stream"""
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """Loop infinitely until the thread is stopped"""
        while True:
            if self.stopped:
                return

            # Read next frame
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        """Return the last read frame"""
        return self.frame

    def stop(self):
        """Stop the thread"""
        self.stopped = True
        log.debug("Grabber thread is stopped: %s", self.stopped)
