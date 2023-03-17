# --------------- #
# Team Rocket 2023
# Author Hannah Wilcox
# Code to interact with the button for locking & pressurizing the system

import pinout as pins
import tkinter as tk 
import JSON
import RPi.GPIO as GPIO
from time import sleep


#Behavior for the button exists in here
class Joysticks(pins.Pinout):

    #Following in Marcos' footsteps to manually set the pinout for the joysticks    
    def __init__(self) -> None:
        super().__init__()

        # We will always be using the BCM mode
        GPIO.setmode(GPIO.BCM)

        # Setting them up to recieve input
        GPIO.setup(joystickL, GPIO.IN)
        GPIO.setup(joystickR, GPIO.IN)

        # The actual pinout is defined in pinout.py
        joystickL = pins.Pinout.joystickL
        joystickR = pins.Pinout.joystickR

        # Status of the left joystick default x & y positions.
        # We choose 512 over 1024, as the range is from 0 - 1023
        # ...making 512 the center and most "Default" position
        xPosLeft = 512
        yPosLeft = 512

        # Status of the right joystick default x & y positions.
        xPosRight = 512
        yPosRight = 512

    def gatherXPosLeft():
        return
    
    def gatherYPosLeft():
        return
    
    def gatherXPosRight():
        return
    
    def gatherYPosRight():
        return

    