import numpy as np
import cv2
from threading import Thread
import os

from logger import *

class VideoPlayer():
    def __init__(self, sourceId=0):
        log.debug("Created new video player")
        self.frames = []
        data_path = os.path.dirname(__file__) + "/data"
        self.default_img_path = data_path + "/imgs/default.jpg"
        self.default_img = cv2.imread(self.default_img_path, 0)
        # log.debug(data_path)
        self.currentframe = 0
        self.frame = self.default_img
        self.stopped = False

    def addFrame(self, img):
        """Sets image as last frame"""
        self.frames.append(img)

    def start(self):
        """Start the thread to paint frames"""
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            if len(self.frames) < 1:
                self.frame = self.default_img
            else:
                self.frame = self.frames[self.currentframe]

    def read(self):
        return self.frame


    def stop(self):
        """Stop the thread"""
        self.stopped = True
        log.debug("Player thread is stopped: %s", self.stopped)
