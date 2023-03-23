from __future__ import annotations
from abc import ABC, abstractmethod

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


    def presentState(self):
        print(f"State: {type(self._state).__name__}")

    # the methods for executing the Launcher functionality. These depends on the current state of the object.
    def proceed(self):
        self._state.proceed()

    def pushUpBtn(self):
        self._state.pushUpBtn()

    def userTextPhony(self)->int:
       return 100

    def leftSwitchToggle(self)->None:
        self._state.leftSwitchToggle()

    def rightSwitchToggle(self)->None:
        self._state.rightSwitchToggle()

    # if both the buttons are pushed at a time, nothing should happen
    def pushUpAndDownBtns(self) -> None:
        print("Oops.. you should press one button at a time")

    # if no button was pushed, it should just wait open for guests
    def noBtnPushed(self) -> None:
        print("Press any button. Up or Down")


# The common state interface for all the states
class State(ABC):
    @property
    def Launcher(self) -> Launcher:
        return self._Launcher

    @Launcher.setter
    def Launcher(self, Launcher: Launcher) -> None:
        self._Launcher = Launcher

    @abstractmethod
    def proceed(self) -> None:
        pass

    @abstractmethod
    def pushUpBtn(self) -> None:
        pass

    @abstractmethod
    def userText(self)->str:
        pass

    @abstractmethod
    def leftSwitchToggle(self)->None:
        pass

    @abstractmethod
    def rightSwitchToggle(self)->None:
        pass


# The concrete states
# We have three states of the Launcher


class Load(State):

      # if down button is pushed it should move one floor down and open the door
    def proceed(self) -> None:
        print("Launcher is changing to next state...")
        self.Launcher.setLauncher(Pressurize())

    # if up button is pushed nothing should happen
    def pushUpBtn(self) -> None:
        print("Already in the top floor")

    def userText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        print("load toggle")

    def rightSwitchToggle(self)->None:
        pass

class Pressurize(State):

      # if down button is pushed it should move one floor down and open the door
    def proceed(self) -> None:
        print("Launcher is changing to next state...")
        self.Launcher.setLauncher(Launch())

    # if up button is pushed nothing should happen
    def pushUpBtn(self) -> None:
        print("Already in the top floor")

    def userText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        print("pressurize toggle")


    def rightSwitchToggle(self)->None:
        pass

class Launch(State):

      # if down button is pushed it should move one floor down and open the door
    def proceed(self) -> None:
        print("Launcher already fired rocket")

    # if up button is pushed nothing should happen
    def pushUpBtn(self) -> None:
        print("Already in the top floor")

    def userText(self)->str:
        pass

    def leftSwitchToggle(self)->None:
        print("launch toggle")


    def rightSwitchToggle(self)->None:
        pass

# if __name__ == "__main__":
#     # The client code.

#     myLauncher = Launcher(Load())
#     myLauncher.presentState()

#     #transition launcher to pressurize
#     myLauncher.proceed()
#     myLauncher.presentState()

#     #transition launcher to Launch
#     myLauncher.proceed()
#     myLauncher.presentState()
