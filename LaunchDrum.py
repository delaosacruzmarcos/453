#--------------------------#
# CSE 453: Rocket Launcher Team
# Author: Marcos
# Date: 03/6/2023
# Launch drum class provides conversion of numbers 
# recieved by the joystick, actuators, and motors to 
# be presented to the GUI along with formatting json responses to the arduino
#--------------------------#

from Serial_Communication import *

class LaunchDrum():

    # Globals
    _serial = None

    def __init__(self):
        self._serial = Serial_Coms()

    #Right drum Information to be displayed to the user
    def getRightDrumInfo(self) -> str:
        rotation = self.getRRotation()
        launch = self.getRHeight()
        press = self.getPressure()
        return self.formatting(rotation,launch, press)


    #left drum Information to be displayed to the user
    def getLeftDrumInfo(self) -> str:
        rotation = self.getLRotation()
        launch = self.getLHeight()
        press = self.getPressure()
        return self.formatting(rotation,launch, press)

    
    def formatting(self,rotation, launch, press) -> str:
        retStr = "Rotation: {}\n\n".format(rotation)
        str1 = "Angle of launch: {}\n\n".format(launch)
        str2 = "Pressurization level: {}%\n\n".format(press)
        return retStr+str1+str2

    
    # returns the angle of elevation of the right launch drum
    def getRHeight(self):
        return "30%"
    
    # returns the rotation of the right launch drum
    def getRRotation(self) -> str:
        return "180"
    
    # returns the angle of elevation of the Left launch drum
    def getLHeight(self):
        return "30%"
    
    # returns the rotation of the left launch drum
    def getLRotation(self) -> str:
        return "180"
    
    # returns the current pressure in the system drum
    def getPressure(self) -> str:
        return "0"

if __name__ == "__main__":
    myLaunchDrum = LaunchDrum()
    print(myLaunchDrum.getRightDrumInfo())