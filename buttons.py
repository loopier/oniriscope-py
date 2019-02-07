import time
import RPi.GPIO as GPIO
import thread

import logger as Logger

log = Logger.new()

GPIO.setmode(GPIO.BCM)

buttons = [17,18]
callback_button_pressed_listeners = []

def setup(gpio_input_pins):
    """Sets up the pins with button input."""
    global buttons
    buttons = gpio_input_pins
    for button in buttons:
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def addButtonPressedCallback(callback):
    """Adds callback function to list of listeners of button pressed event."""
    callback_button_pressed_listeners.append(callback)

def callbackButtonPressed(button):
    """Calls functions in the callback list."""
    log.info("Button pressed: %i", button)
    for func in callback_button_pressed_listeners:
        func(button)

def update():
    """Keeps listening for button input."""
    while True:
        for button in buttons:
            input_state = GPIO.input(button)

            if input_state == False:
                callbackButtonPressed(button)

        time.sleep(0.2)

def start():
    """Starts listening button input in a new thread."""
    thread.start_new_thread(update, ())
