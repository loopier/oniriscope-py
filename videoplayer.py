import numpy as np
import cv2
from threading import Thread
import os
from time import sleep

import logger as Logger

log = Logger.new()

class VideoPlayer():
    def __init__(self, sourceId=0):
        log.debug("Created new video player")
        self.frames = []
        data_path = os.path.dirname(__file__) + "/data"
        self.default_img_path = data_path + "/imgs/default.jpg"
        self.default_img = cv2.imread(self.default_img_path, 0)
        # log.debug(data_path)
        self.current_frame = 0
        self.frame = self.default_img
        self.stopped = False
        self.paused = True
        self.fps = 12
        self.play_speed = 1.0 / self.fps

    def addFrame(self, img):
        """Sets image as last frame"""
        self.frames.append(img)

    def insertFrame(self, img):
        """Inserts a frame at the current frame position."""
        self.frames.insert(self.current_frame, img)
        # self.nextFrame()
        self.previousFrame()

    def removeFrame(self):
        """Remove the current frame"""
        if len(self.frames) <= 0:
            return

        self.frames.pop(self.current_frame)
        self.current_frame = max(0, self.current_frame - 1)

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
                if self.paused:
                    pass
                else:
                    self.nextFrame()
                self.frame = self.frames[self.current_frame]

            sleep(self.play_speed)

    def read(self):
        """Returns current frame."""
        return self.frame

    def write(self, save_path):
        """Exports frames as video."""
        log.info("Saved frames to: %s", save_path)

    def togglePlay(self):
        self.paused = not(self.paused)

    def stop(self):
        """Stop the thread"""
        self.stopped = True
        log.debug("Player thread is stopped: %s", self.stopped)

    def nextFrame(self):
        self.current_frame += 1
        if (self.current_frame > len(self.frames) - 1):
            self.current_frame = 0

    def previousFrame(self):
        self.current_frame -= 1
        if (self.current_frame < 0):
            self.current_frame = len(self.frames)-1

    def setFramerate(self, fps):
        self.fps = max(1, fps)
        log.info("FPS: %i", self.fps)
        self.play_speed = float(1.0 / self.fps)
        log.debug("Play speed: %f", self.play_speed)

    def increaseFramerate(self):
        self.fps += 1
        self.setFramerate(self.fps)

    def decreaseFramerate(self):
        self.fps -= 1
        self.setFramerate(self.fps)

    def getNumFrames(self):
        """Returns the number of frames."""
        return len(self.frames)
