#--------------------------#
# CSE 453: Rocket Launcher Team
# Author: Marcos
# Date: 03/7/2023
# The states Enum is used to make state transitions consistent between different files
#--------------------------#
import enum as Enum

class States(Enum):
    LOAD = 0
    AIM = 1
    PRESSURIZE = 2
    LAUNCH = 3

