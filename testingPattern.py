from demo_pattern import *

if __name__ == "__main__":
    # The client code.

    myLauncher = Launcher(Load())
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()

    #transition launcher to pressurize
    myLauncher.proceed()
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()


    #transition launcher to Launch
    myLauncher.proceed()
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()
