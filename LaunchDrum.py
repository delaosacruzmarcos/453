#--------------------------#
# CSE 453: Rocket Launcher Team
# Author: Marcos
# Date: 03/6/2023
# Launch drum class provides simple way for the serial comunication to package 
# data about the state of each launch drum to the MasterGUI
#--------------------------#

# TODO replace the json string with imported serial communication 
exampleJson = '{"name":"John", "age":30, "car":null}'

class LaunchDrum():
    def __init__(self,json):
        # TODO find a way to populate this object with relative information from the JSON
        pass

    # returns the angle of elevation of the launch drum
    def getHeight(self):
        return "30%"
    
    # returns the rotation of the launch drum
    def getRotation(self):
        return "180"
    
    # returns true when the corresponding green switch has been activated
    def getActivationStatus(self):
        return False
    
    # returns the pressurization status for the launch drum
    def getPressurizationStatus(self):
        return False
    
    # Eventually we will use this Class to give highlevel commands 