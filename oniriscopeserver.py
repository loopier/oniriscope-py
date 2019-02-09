# -*- coding: utf-8 -*-
"""
Make animations from camera stream controlled by physical input (buttons and
encoder).

The order of the code is important.
Generally, there are several input managers (video, encoder, buttons), each
in a different thread that will take the input and then notify callback
functions that are in a list of listeners for each kind of input.

- Functions that will process the informtion need to be declared first.
- Then the maps (dictionaries mapping input info to processing functions).
- Callback functions are declared and added as listeners to iniput (they use
the maps, that's why they must be declared later).
- Finally the thread of every input controller is started.

I guess it's somewhat in reverse logic. (?)
"""


import cv2
import os
import pprint as pp
import numpy as np
import re

from videograbber import VideoGrabber
from videoplayer import VideoPlayer
import logger as Logger
# import encoder as encoder
# import buttons as buttons

log = Logger.new()

cam = VideoGrabber(0)
cam.start()

player = VideoPlayer(1)
player.start()

# available outputs to be rendered
outputs = [cam, player]
# output index
output = outputs[1]

draw_text = True

def destroy(args):
    """Exit the program."""
    log.info("Closing app.")
    cam.stop()
    player.stop()
    cv2.destroyAllWindows()
    exit()

def addFrame(args=None):
    """
    Takes last frame from the video stream and adds it
    to the playback stream.
    """
    frame = cam.read()
    player.addFrame(frame)
    nextFrame()

def insertFrame(args=None):
    """
    Takes the last frame from the video stream and
    inserts it in the current frame
    """
    frame = cam.read()
    player.insertFrame(frame)
    nextFrame()

def removeFrame(args=None):
    player.removeFrame()

def save(args=None):
    """Saves frames as movie."""
    # Save to usb drive.
    player.write("some/path")

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

def toggleText(args=None):
    """Toggle info display."""
    global draw_text
    draw_text = not(draw_text)

def togglePlay(args):
    player.togglePlay()

def nextFrame(args=None):
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
    "i": insertFrame,
    "r": removeFrame,
    "p": togglePlay,
    "0": setOutput,
    "1": setOutput,
    "t": toggleText,
    "h": showHelp,
    "+": increaseFramerate,
    "-": decreaseFramerate,
    "w": save,
    "a": previousFrame, # left arrow
    "d": nextFrame, # right arrow
    # 98: # up arrow
    # 104: # down arrow
}

# Map gpio buttons to functions
button_map = {
    17: insertFrame,
    18: removeFrame,
}

def encoderUpdated(delta):
    """Receives changes from the encoder."""
    log.debug("Updating frame from encoder change: %i", delta)
    for x in range(abs(delta)):
        if delta > 0:
            nextFrame(0)
        elif delta < 0:
            previousFrame(0)



def buttonPressed(button):
    """Maps button pressed events to functions."""
    log.debug("Button pressed: %i", button)
    func = button_map[button]
    func()



def keyPressed(key):
    key_char = chr(key)
    global keymap
    func = keymap.get(key_char, lambda key:"nothing")
    log.debug("Key pressed: '%c' - %i", key_char, key)
    if func == None:
        log.debug("Key not mapped: '%c' - %i", key_char, key)
    return func(key_char)

def mainThread():
    """
    Main loop.  Has to be here –in the main thread– rendering everything and
    listening to input events.
    """
    while True:
        output_frame = output.read()
        cv2.imshow('Output', output_frame)
        key = cv2.waitKey(1) & 0xFF
        if key != 255:
            keyPressed(key)

# Add gpio listeners
# buttons.addButtonPressedCallback(buttonPressed)
# encoder.addCallback(encoderUpdated)

# Initialize gpio
# buttons.setup(button_map.keys())
# buttons.addButtonPressedCallback(buttonPressed)

# buttons.start()
# encoder.startEncoder()

mainThread()
# Make sure there's a clean exit.
destroy()
