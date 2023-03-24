from demo_pattern import *

if __name__ == "__main__":
    # The client code.

    myLauncher = Launcher(Load())
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()

    #transition launcher to pressurize
    myLauncher.presentState()
    myLauncher.rightSwitchToggle()


    #transition launcher to Launch
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()
