# --------------- #
# Team Rocket 2023
# Authors Marcos De La Osa Cruz, Hannah Wilcox
# Code to interact with the LED Switches for the activation of the launch drums

from pinout import *
import tkinter as tk 
import JSON
import RPi.GPIO as GPIO
from time import sleep
from pyautogui import press



# Tucking all the behavior in a class
class Switch():
    # I wanted to override the init method to also set up the pinout for the switches
    def __init__(self,pins: Pinout) -> None:
        super().__init__()

        self.pins = pins
        # The actual pinout is defined in pinout.py
        activateLIn = self.pins.getGPIOPINS("activeLIn")
        activateRIn = self.pins.getGPIOPINS("activeRIn")
        activateLOut = self.pins.getGPIOPINS("activeLOut")
        activateROut = self.pins.getGPIOPINS("activeROut")

        # We will always be using the BCM mode
        GPIO.setmode(GPIO.BOARD)

        # Setting them up to recieve input
        GPIO.setup(activateLIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(activateRIn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Setting them up to produce output
        GPIO.setup(activateLOut, GPIO.OUT)
        GPIO.setup(activateROut, GPIO.OUT)

        GPIO.add_event_detect(activateLIn, GPIO.BOTH, 
        callback=self.keystrokeSimL, bouncetime=1000)

        GPIO.add_event_detect(activateRIn, GPIO.BOTH, 
        callback=self.keystrokeSimR, bouncetime=1000)


    # Throw the keypress interrupt 
    def keystrokeSimL(self,activeLIn):
        print("Left switch activated")
        list = self.pins.getGPIOKeys().get('<<left-switch>>')
        print(list)
        self.keystroke(list[1])
        return

    # Throw the keypress interrupt 
    def keystrokeSimR(self,activeRIn):
        print("Right switch activated")
        list = self.pins.getGPIOKeys().get('<<right-switch>>')
        self.keystroke(list[1])
        return

    # Throw the keypress interrupt
    def keystroke(self, key: str) -> None:
        press(key)
        return