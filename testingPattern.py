from demo_pattern import *


def test_Drum_activation():
    myLauncher = Launcher(Load())
    if myLauncher.leftDrumActive() is True:
        print("test_Drum_activation failed")
    myLauncher.leftSwitchToggle()
    if myLauncher.leftDrumActive() is False:
        print("test_Drum_activation failed")
    if myLauncher.rightDrumActive() is True:
        print("test_Drum_activation failed")
    myLauncher.rightSwitchToggle()
    if myLauncher.rightDrumActive() is False:
        print("test_Drum_activation failed")

def test_Stage_Cycle():
    myLauncher = Launcher(Load())
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()

    #transition launcher to pressurize
    myLauncher.presentState()
    myLauncher.rightSwitchToggle()


    #transition launcher to Launch
    myLauncher.presentState()
    myLauncher.leftSwitchToggle()

if __name__ == "__main__":
    # The testing code
    test_Drum_activation()


