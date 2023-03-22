# --------------- #
# Team Rocket 2023
# Authors Marcos De La Osa Cruz, Hannah Wilcox
# Code to interact with the LED Switches for the activation of the launch drums

import pinout as pins
import tkinter as tk 
import JSON
import RPi.GPIO as GPIO
from time import sleep


# Tucking all the behavior in a class
class Switch(pins.Pinout):
    # I wanted to override the init method to also set up the pinout for the switches
    def __init__(self) -> None:
        super().__init__()

        # We will always be using the BCM mode
        GPIO.setmode(GPIO.BCM)

        # Settign them up to recieve input
        GPIO.setup(activateL, GPIO.IN)
        GPIO.setup(activateR, GPIO.IN)

        # The actual pinout is defined in pinout.py
        activateL = pins.Pinout.activateL
        activateR = pins.Pinout.activateR
        # States of the switches initialized to false
        self.leftDrumActive_state = False
        self.rightDrumActive_state = False

    # Used for GUI updates: True if left is active
    def gatherStateLeft():
        # Gather information about the current situation of the switches
        jsonData = JSON.loads("arduino-json-form.json")
        curLState = jsonData["switches"]["left"]["on"]

        #Update the state of the switches only if nessisary
        if (curLState != leftDrumActive_state):
            print("Updating left drum to", curLState)
            leftDrumActive_state = curLState
        return leftDrumActive_state
        
    # Used for GUI updates: True if right is active
    def gatherStateRight():
        # Gather information about the current situation of the switches
        jsonData = JSON.loads("arduino-json-form.json")
        curRState = jsonData["switches"]["right"]["on"]

        #Update the state of the switches only if necessary
        if (curRState != rightDrumActive_state):
            print("Updating right drum to", curRState)
            rightDrumActive_state = curRState
        return rightDrumActive_state



