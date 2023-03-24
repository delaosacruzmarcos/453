from __future__ import annotations
from abc import ABC, abstractmethod
from pyautogui import press
from pinout import Pinout

# The Launcher class is the context. It should be initiated with a default state.
class Launcher:
    # Variables of interest
    _state = None
    _joyInfo = None
    _toggle = [False, False]

    def __init__(self, state: State) -> None:
        self.setLauncher(state)
        

    # method to change the state of the object
    def setLauncher(self, state: State):
        self._state = state
        self._state.Launcher = self
        self._pins = Pinout()
        self._state.Launcher._pins = self._pins


    def presentState(self):
        print(f"State: {type(self._state).__name__}")

    # the methods for executing the Launcher functionality. These depends on the current state of the object.
    def update(self):
        dic = self._pins.getGPIOKeys()
        char = dic.get('<<update-GUI>>')
        press(char)
        return

    def pressurizeButton(self):
        self._state.pressurizeButton()

    #TODO Remove after done testing
    def userTextPhony(self)->int:
       return 100
    
    def userText(self)->str:
        return self._state.userText()
    
    def leftDrumText(self)->str:
        return self._state.leftDrumText()

    def rightDrumText(self)->str:
        return self._state.rightDrumText()

    def leftSwitchToggle(self)->None:
        self._state.leftSwitchToggle()

    def rightSwitchToggle(self)->None:
        self._state.rightSwitchToggle()

    # if both the buttons are pushed at a time, nothing should happen
    def pushUpAndDownBtns(self) -> None:
        print("Oops.. you should press one button at a time")


# The common state interface for all the states
class State(ABC):
    @property
    def Launcher(self) -> Launcher:
        return self._Launcher

    @Launcher.setter
    def Launcher(self, Launcher: Launcher) -> None:
        self._Launcher = Launcher

    #Computes the logic behind a registered press of the pressurization button
    @abstractmethod
    def pressurizeButton(self) -> None:
        pass

    #Gathers instructional text to be displayed to the user via the GUI
    @abstractmethod
    def userText(self)->str:
        pass

    #Gathers infromative text about the status of the left launch drum
    @abstractmethod
    def leftDrumText(self)->str:
        pass

    #Gathers infromative text about the status of the right launch drum
    @abstractmethod
    def rightDrumText(self)->str:
        pass

    #Computes the logic behind a toggle (ON or OFF) of left activation switch
    @abstractmethod
    def leftSwitchToggle(self)->None:
        pass

    #Computes the logic behind a toggle (ON or OFF) of right activation switch
    @abstractmethod
    def rightSwitchToggle(self)->None:
        pass




class Load(State):

      # if down button is pushed it should move one floor down and open the door
    def update(self) -> None:
        print("Launcher is changing to next state...")
        self.Launcher.setLauncher(Pressurize())

    # if up button is pushed nothing should happen
    def pressurizeButton(self) -> None:
        print("Already in the top floor")

    def userText(self)->str:
        retStr = "Instructions\n\n"
        str1 = " ***Please place your rocket onto the launch pad***\n\n"
        str2 = "After placing rocket onto the launch pad enable the rotation and tilt mechanisms by flipping the corresponding green switch\n\n"
        return retStr+str1+str2

    def leftDrumText(self)->str:
        pass

    def rightDrumText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        print("Launcher is changing to next state...")
        self.Launcher.setLauncher(AimLeft())

    def rightSwitchToggle(self)->None:
        print("Launcher is changing to next state...")
        self.Launcher.setLauncher(AimRight())

"""
---AimLeft---
Left launch drum is active and taking move and elavate commands
Right launch drum can be activated (transition to aim both state)
"""
class AimLeft(State):

    def pressurizeButton(self) -> None:
        #Begin pressurization sequence
        self.Launcher.setLauncher(Pressurize())
        self.Launcher.update()
        return

    def userText(self)->str:
        retStr = "Instructions\n\n" 
        str1 = "Great job you have activated the left launch pad!\n\n"
        str2 = "Used the joystick on the left side of the controller to position the rocket\n\n"
        str3 = "If you have another rocket to launch place it on the right launch pad and activate the right green switch\n\n"
        str4 = "(optionally) when you are done positioning the launch pad press in the left joystick button to lock the position into place"
        return retStr+str1+str2+str3+str4

    def leftDrumText(self)->str:
        pass

    def rightDrumText(self)->str:
        return " Right launch pad not active"

    def leftSwitchToggle(self)->None:
        #Switch should be on, toggle means soft disable
        pass

    def rightSwitchToggle(self)->None:
        #Engage the right launch drum
        self.Launcher.setLauncher(AimBoth())
        self.Launcher.update()
        return
"""
---AimRight---
Right launch drum is active and taking move and elavate commands
Left launch drum can be activated (transition to aim both state)
"""
class AimRight(State):
    def pressurizeButton(self) -> None:
        #Begin pressurization sequence
        self.Launcher.setLauncher(Pressurize())
        self.Launcher.update()
        return

    def userText(self)->str:
        retStr = "Instructions\n\n" 
        str1 = "Great job you have activated the right launch pad!\n\n"
        str2 = "Used the joystick on the right side of the controller to position the rocket\n\n"
        str3 = "If you have another rocket to launch place it on the left launch pad and activate the left green switch\n\n"
        str4 = "(optionally) when you are done positioning the launch pad press in the right joystick button to lock the position into place"
        return retStr+str1+str2+str3+str4
    
    def leftDrumText(self)->str:
        return " Left launch pad not active"

    def rightDrumText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        #Engage the right launch drum
        self.Launcher.setLauncher(AimBoth())
        self.Launcher.update()
        return

    def rightSwitchToggle(self)->None:
        #Switch should be on, toggle means soft disable
        pass
"""
---AimBoth---
Left & Right launch drum is active and taking move and elavate commands
"""
class AimBoth(State):
    def pressurizeButton(self) -> None:
        #Begin pressurization sequence
        self.Launcher.setLauncher(Pressurize())
        self.Launcher.update()
        return

    def userText(self)->str:
        retStr = "Instructions\n\n"
        str1 = "Sure fire work captain! both rockets are ready to be aimed\n\n"
        str2 = "When you would like to pressurize the rockets for launch press the blue button at the bottom of the controller\n\n"
        str3 = "you will not be able to aim the rockets after they are pressurized for launch so choose your trajectory wisely!"
        return retStr+str1+str2+str3

    def leftDrumText(self)->str:
        pass

    def rightDrumText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        #Switch should be on, toggle means soft disable
        pass

    def rightSwitchToggle(self)->None:
        pass
    
"""
---Pressurize---
"""    
class Pressurize(State):

      # if down button is pushed it should move one floor down and open the door
    def update(self) -> None:
        print("Launcher is changing to next state...")
        self.Launcher.setLauncher(Launch())

    # if up button is pushed nothing should happen
    def pressurizeButton(self) -> None:
        print("Already in the top floor")

    def userText(self)->str:
        pass

    def leftDrumText(self)->str:
        pass

    def rightDrumText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        print("pressurize toggle")


    def rightSwitchToggle(self)->None:
        pass

class Launch(State):

      # if down button is pushed it should move one floor down and open the door
    def update(self) -> None:
        print("Launcher already fired rocket")


    def leftSwitchToggle(self)->None:
        print("launch toggle")

    def pressurizeButton(self) -> None:
        print("Already in the top floor")

    def userText(self)->str:
        pass

    def leftDrumText(self)->str:
        pass

    def rightDrumText(self)->str:
        pass

    def rightSwitchToggle(self)->None:
        pass

# if __name__ == "__main__":
#     # The client code.

#     myLauncher = Launcher(Load())
#     myLauncher.presentState()

#     #transition launcher to pressurize
#     myLauncher.update()
#     myLauncher.presentState()

#     #transition launcher to Launch
#     myLauncher.update()
#     myLauncher.presentState()
