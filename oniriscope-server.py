import cv2
import os

from videograbber import VideoGrabber
from videoplayer import VideoPlayer
from logger import *

cam = VideoGrabber(1)
cam.start()

player = VideoPlayer(1)
player.start()

# available outputs to be rendered
outputs = [cam, player]
# output index
output = outputs[0]

def destroy(args):
    """Exit the program"""
    log.info("Closing app")
    cam.stop()
    player.stop()
    cv2.destroyAllWindows()
    exit()

def addFrame(args):
    """
    Takes last frame from the video stream and adds it
    to the playback stream.
    """
    frame = cam.read()
    player.addFrame(frame)

def setOutput(index):
    """
    Change the output to be rendered.
    index: Index of the output in the 'outputs' list
    """
    index = int(index)
    log.info("Output: %i", index)
    global output
    output = outputs[index]
    log.debug(output)

# Map keys to functions
keymap = {
    "q": destroy,
    " ": addFrame,
    "0": setOutput,
    "1": setOutput,
}

def keyPressed(key):
    key = chr(key)
    global keymap
    func = keymap.get(key, lambda key:"nothing")
    log.debug("Key pressed: %c", key)
    if func == None:
        log.debug("Key not mapped: %", key)
    return func(key)

while True:
    cam_frame = cam.read()
    animation_frame = output.read()
    gray = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Input', gray)
    cv2.imshow('Output', animation_frame)
    key = cv2.waitKey(1) & 0xFF
    if key != 255:
        keyPressed(key)
