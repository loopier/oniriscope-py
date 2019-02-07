# -*- coding: utf-8 -*-

import cv2
import os
import pprint as pp
import numpy as np
import re

from videograbber import VideoGrabber
from videoplayer import VideoPlayer
import logger as Logger
import encoder as encoder
import buttons as buttons

log = Logger.new()

cam = VideoGrabber(0)
cam.start()

player = VideoPlayer(1)
player.start()

encoder.startEncoder()
buttons.setup([17,18])
buttons.start()

# available outputs to be rendered
outputs = [cam, player]
# output index
output = outputs[1]

draw_text = True

def encoderUpdated(delta):
    """Receives changes from the encoder."""
    log.debug("Updating frame from encoder change: %i", delta)
    for x in range(abs(delta)):
        if delta > 0:
            nextFrame(0)
        elif delta < 0:
            previousFrame(0)

encoder.addCallback(encoderUpdated)

def buttonPressed(button):
    log.debug("Button pressed: %i", button)

buttons.addButtonPressedCallback(buttonPressed)

def destroy(args):
    """Exit the program."""
    log.info("Closing app.")
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

def toggleText(args):
    """Toggle info display."""
    global draw_text
    draw_text = not(draw_text)

def togglePlay(args):
    player.togglePlay()

def nextFrame(args):
    player.nextFrame()

def previousFrame(args):
    player.previousFrame()

def increaseFramerate(args):
    player.increaseFramerate()

def decreaseFramerate(args):
    player.decreaseFramerate()

def drawText(img, msg):
    """
    Draws text on the image.
    img: Image where the text will be printed.
    msg: Message to be printed.
    """
    cv2.putText(img, msg, (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.imshow("Message", img)

def showHelp(args):
    """Dislpay commands."""
    help_string = pp.pformat(keymap)
    help_string = help_string.replace("<function", "")
    print(help_string)


# Map keys to functions
keymap = {
    "q": destroy,
    " ": addFrame,
    "p": togglePlay,
    "0": setOutput,
    "1": setOutput,
    "t": toggleText,
    "h": showHelp,
    "w": increaseFramerate,
    "s": decreaseFramerate,
    "a": previousFrame, # left arrow
    "d": nextFrame, # right arrow
    # 98: # up arrow
    # 104: # down arrow
}

def keyPressed(key):
    key = chr(key)
    global keymap
    func = keymap.get(key, lambda key:"nothing")
    log.debug("Key pressed: %c", key)
    if func == None:
        log.debug("Key not mapped: %", key)
    return func(key)

# Main loop.  Has to be here –in the main thread– rendering everything and
# listening to input events.
while True:
    output_frame = output.read()
    cv2.imshow('Output', output_frame)
    key = cv2.waitKey(1) & 0xFF
    if key != 255:
        keyPressed(key)
