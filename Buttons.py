# --------------- #
# Team Rocket 2023
# Author Hannah Wilcox
# Code to interact with the button for locking & pressurizing the system

import pinout as pins
import tkinter as tk 
import JSON
import RPi.GPIO as GPIO
from time import sleep

#no pushes on joysticks.

#Behavior for the button exists in here
class Button(pins.Pinout):

    #Following in Marcos' footsteps to manually set the pinout for the button?    
    def __init__(self) -> None:
        super().__init__()

        # We will always be using the BCM mode
        GPIO.setmode(GPIO.BCM)

        # Settign them up to recieve input
        GPIO.setup(button, GPIO.IN)

        # The actual pinout is defined in pinout.py
        button = pins.Pinout.activateL

        # Status of the button initialized to false
        rising_edge = False
        falling_edge = False

    # Used for GUI updates: True if button is on rising edge
    def gatherStateRising():
        # Gather information about the current situation of the switches
        jsonData = JSON.loads("arduino-json-form.json")
        risingState = jsonData["buttons"]["center"]["risingEdge"]

        return risingState
        
    # Used for GUI updates: True if button is on falling edge
    def gatherStateFalling():
        # Gather information about the current situation of the switches
        jsonData = JSON.loads("arduino-json-form.json")
        fallingState = jsonData["buttons"]["center"]["fallingEdge"]

        return fallingState

        
