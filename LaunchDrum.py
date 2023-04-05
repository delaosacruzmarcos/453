#--------------------------#
# CSE 453: Rocket Launcher Team
# Author: Marcos
# Date: 03/6/2023
# Launch drum class provides conversion of numbers 
# recieved by the joystick, actuators, and motors to 
# be presented to the GUI along with handline pressurization 
#--------------------------#

from Serial_Communication import *

class LaunchDrum():

    # Globals
    _serial = None
    _pressurization_stage:int = 0
    _internal_pressure: int = 0
    # we may want to change these from the gui?
    _time_at_pressure: int = 0
    _desired_pressure: int = 0

    def __init__(self):
        self._serial = Serial_Coms()

    #Right drum Information to be displayed to the user
    def getRightDrumInfo(self) -> str:
        rotation = self.getRRotation()
        launch = self.getRHeight()
        press = self.getPressure()
        (joyX, joyY) = self.getJoyRight()
        return self.formatting(rotation,launch, press, joyX, joyY)


    #left drum Information to be displayed to the user
    def getLeftDrumInfo(self) -> str:
        rotation = self.getLRotation()
        launch = self.getLHeight()
        press = self.getPressure()
        (joyX, joyY) = self.getJoyLeft()
        return self.formatting(rotation,launch, press, joyX, joyY)

    
    def formatting(self,rotation, launch, press, x, y) -> str:
        retStr = "Rotation: {}\n\n".format(rotation)
        str1 = "Angle of launch: {}\n\n".format(launch)
        str2 = "Pressurization level: {}%\n\n".format(press)
        str3 = "Joystick x: "+str(x)+"\nJoystick y: "+str(y)
        return retStr+str1+str2+str3

    
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
    
    def getJoyRight(self)->tuple:
        x = self._serial._controller_to_pi_message["Joysticks"]["right"]["x"]
        y = self._serial._controller_to_pi_message["Joysticks"]["right"]["y"]
        return (x,y)

    def getJoyLeft(self)->tuple:
        x = self._serial._controller_to_pi_message["Joysticks"]["left"]["x"]
        y = self._serial._controller_to_pi_message["Joysticks"]["left"]["y"]
        return (x,y)                                                  

    #---Pressurization subcommands---#
    def pressurize(self,right: bool, left:bool)->None:
        if(self._pressurization_stage == 0): #close the latches & solenoid A
            self.pneumaticsStatesetUp(True,True,True,False,False,False)
        if(self._pressurization_stage == 1): #close corresponding solenoids for empty rockets
            self.pneumaticsStatesetUp(True,True,True,not right,not left,False)
        if(self._pressurization_stage == 2): #turn on the air compressor
            self.pneumaticsStatesetUp(True,True,True,not right,not left,True)
        if(self._pressurization_stage == 2): #Close corresponding solenoids to trap air
            self.pneumaticsStatesetUp(True,True,True,right,left,True)
        
        

    # Simplifies the amount of function calls we have to type in the in between stages
    def pneumaticsStatesetUp(self,rlatchOn:bool,llatchOn:bool,
                             closeA:bool,closeB:bool,closeC:bool,compresOn:bool)->None:
        self._serial.ValveManager(closeA, closeB, closeC)
        self._serial.toggleCompressor(compresOn)
        self._serial.toggleLatches(llatchOn, rlatchOn)
        return


if __name__ == "__main__":
    myLaunchDrum = LaunchDrum()
    print(myLaunchDrum.getRightDrumInfo())