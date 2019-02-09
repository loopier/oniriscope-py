import time
import gaugette.gpio
import gaugette.rotary_encoder
import thread

import logger as Logger

log = Logger.new()

A_PIN = 4
B_PIN = 5
gpio = gaugette.gpio.GPIO()
encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, A_PIN, B_PIN)
encoder.start()

listeners = []
callback_listeners = []

def adddListener(listener):
    """Adds listener to the notified list."""
    listeners.append(listener)

def notifyListeners(delta):
    """Notifies listeners of the movement of the encoder."""
    log.debug("Notifying listeners: %i", delta)
    for listener in listeners:
       listener.onEncoderNotification(delta)

def addCallback(callback):
    """Adds callback functions to the notified list."""
    callback_listeners.append(callback)

def notifyCallback(delta):
    """Notifies callback functions when encoder moves."""
    log.debug("Notifying callbacks: %i", delta)
    for callback in callback_listeners:
       callback(delta)

def updateEncoder():
    while True:
        delta = encoder.get_cycles()
        if delta!=0:
            notifyListeners(delta)
            notifyCallback(delta)
            print("rotate %d", delta)
        else:
            time.sleep(0.1)

def startEncoder():
    thread.start_new_thread(updateEncoder, ())
