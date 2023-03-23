# --------------- #
# Team Rocket 2023
# Author unknown, Marcos De La Osa Cruz
# class contains the pinouts for the raspberry pi pins

from MasterGUI import *

class Pinout():
    def __init__(self) -> None:
        # Event name : [key, function call]
        self.GPIOKEYS = {
            '<<custom-test>>': ['<t>', testEvent],
            '<<left-switch>>': ['<l>', leftSwitchToggle],
            '<<right-switch>>': ['<r>', rightSwitchToggle],
        }

    # Returns the GPIO dictionary     
    def getGPIOKeys(self):
        return self.GPIOKEYS