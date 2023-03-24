# --------------- #
# Team Rocket 2023
# Author unknown, Marcos De La Osa Cruz
# class contains the pinouts for the raspberry pi pins


class Pinout():
    def __init__(self) -> None:
        # Event name : [key, function call]
        self.GPIOKEYS = {
            '<<custom-test>>': ['<t>',"t"], #testing string print to console
            '<<update-GUI>>': ['<u>',"u"],  #causes refresh of gui elements triggered by state change
            '<<left-switch>>': ['<l>',"l"], #triggered by GPIO interrupt to update state
            '<<right-switch>>': ['<r>',"r"],#triggered by GPIO interrupt to update state
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
    def getGPIOKeys(self) -> dict[str, list[str]]:
        return self.GPIOKEYS