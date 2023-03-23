# --------------- #
# Team Rocket 2023
# Author unknown, Marcos De La Osa Cruz
# class contains the pinouts for the raspberry pi pins

from MasterGUI import *

class Pinout():
    def __init__(self) -> None:
        # Event name : [key, function call]
        self.GPIOKEYS = {
            '<<custom-test>>': ['<t>',"t", testEvent],
            '<<left-switch>>': ['<l>',"l", leftSwitchToggle],
            '<<right-switch>>': ['<r>',"r", rightSwitchToggle],
        }

        #Pins of the raspberry pi
        self.GPIOPINS = {
            "activeLIn":11, 
            "activeRIn":13,
            "activeLOut":15,
            "activeROut":16,
        }

    # Returns the GPIO pin associated with name in dictionary if possible    
    def getGPIOPINS(self, name: str):
        if name in self.GPIOPINS:
            return self.GPIOPINS.get(name)
        else:
            print("No pin with corresp ")

    # Returns the GPIO Pin dictionary
    def getGPIOKeys(self):
        return self.GPIOKEYS