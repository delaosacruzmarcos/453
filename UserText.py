# --------------- #
# Team Rocket 2023
# Author Marcos De La Osa Cruz
# Updates the user text depending on the state of the controller

from States import *

#literalls for error checking
STATEMAX = 400
STATEMIN = -1


# control flow for the text generation, based on first two digits
def getText(state):
    state = int(state)
    if (state < STATEMIN or state > STATEMAX):
        return "Error state out of bounds: " + state
    if (state < 199 and state >= 100):
        return loadUpdate(state)
    if (state < 299 and state >= 200):
        return pressurizationUpdate(state)
    if (state < 399 and state >= 300):
        return launchUpdate(state)


#gets the tens digit of a number (corresponding to text)
def gatherOnes(state):
    sub = str(state)
    print(sub[len(sub)-2])
    return int(sub[len(sub)-2])


#load state numbers include 100-190
def loadUpdate(state):
    sub = gatherOnes(state)
    retStr = "Instructions\n\n"
    if (sub==0): #100 - Starting state
        str1 = " ***Please place your rocket onto the launch pad***\n\n"
        str2 = "After placing rocket onto the launch pad enable the rotation and tilt mechanisms by flipping the corresponding green switch\n\n"
        return retStr+str1+str2
    if (sub==1): #110 - placed right rocket
        str1 = "Great job you have activated the right launch pad!\n\n"
        str2 = "Used the joystick on the right side of the controller to position the rocket\n\n"
        str3 = "If you have another rocket to launch place it on the left launch pad and activate the left green switch\n\n"
        str3 = "(optionally) when you are done positioning the launch pad press in the right joystick button to lock the position into place"
        return retStr+str1+str2+str3+str4
    if (sub==2): #120 - placed left rocket
        str1 = "Great job you have activated the left launch pad!\n\n"
        str2 = "Used the joystick on the left side of the controller to position the rocket\n\n"
        str3 = "If you have another rocket to launch place it on the right launch pad and activate the right green switch\n\n"
        str4 = "(optionally) when you are done positioning the launch pad press in the left joystick button to lock the position into place"
        return retStr+str1+str2+str3+str4
    if (sub==3): #130 - both rockets are placed
        str1 = "Sure fire work captain! both rockets are ready to be aimed\n\n"
        str2 = "When you would like to pressurize the rockets for launch press the blue button at the bottom of the controller\n\n"
        str3 = "you will not be able to aim the rockets after they are pressurized for launch so choose your trajectory wisely!"
        return retStr+str1+str2+str3
    if (sub):
        pass

#pressurization numbers include 20-29
def pressurizationUpdate(state): 
    sub = gatherOnes(state)
    retStr = "Stand by for pressurization and safety checks"
    if (sub==0): #20 - pressurization started
        str1 = "Fueling up the rockets commander! please wait while our system pressurizes"
        return retStr+str1
    if (sub==1): #21 - pressurization reached desired psi
        str1 = "We have reached the desired internal pressure in the rockets\n\n"
        str2 = "Next we will be testing the integrity of the rockets"
        return retStr+str1+str2
    if (sub==2): #22 - pressurization held desired psi 
        str1 = "rockets held desired pressure for the alloted time, they are safe to launch on your command"
    if (sub==3): #23 - right rocket is pressurized
        str1 = "Right rocket is fueled and ready to launch on your command!\n\n"
        str2 = "To launch the right rocket move the right green switch to the off position\n\n"
        return retStr+str1+str2
    if (sub==4): #24 - left rocket is pressurized
        str1 = "Left rocket is fueled and ready to launch on your command!\n\n"
        str2 = "To launch the left rocket move the left green switch to the off position\n\n"
        return retStr+str1+str2        
    if (sub==5): #25 - both rockets pressurized
        str1 = "Both rockets are fueled and ready to launch on your command!\n\n"
        str2 = "To launch rockets move the corresponding green switch to the off position\n\n"
        return retStr+str1+str2
    if (sub==6): #26 - failed to meet desired pressure in time
        pass
    if (sub): #27 - failed to maintain desired pressure for time period
        pass




#launch numbers include 30-39
def launchUpdate(state):
 #I think I will be using a different method to preform the launch countdown
 sub = gatherOnes(state)
 retStr = "***Launching***"
 return retStr




