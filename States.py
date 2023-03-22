#--------------------------#
# CSE 453: Rocket Launcher Team
# Author: Marcos
# Date: 03/7/2023
# The states dictionary can store information about the current state
# Also handles the transition between states, and the corresponding user text calls 
#--------------------------#

#literalls for error checking
STATEMAX = 400
STATEMIN = -1

class StateHandler():
    # variable that holds the current state value - accessed via changeState()
    STATE = 0
    def __init__(self):
        super().__init__()
        # state number matched with description and additional information in a list
        #TODO add information to each state
        self.stateDic = {
        #Key: State description, LeftSwitchState, RightSwitchState
            100:["Starting state", "additional information"],
            110:["not a state", "additional information"],
            120:["not a state", "additional information"],
            130:["not a state", "additional information"],
            140:["not a state", "additional information"],
            150:["not a state", "additional information"],
            0:["not a state", "additional information"],
            0:["not a state", "additional information"],
        }
        self.changeState(100) #change the state to unloaded launch pads

    #Checks the current status, and determines if we need to change state
    def analyzeState(self):
        # check the current state of switches & pbutton
        cls = self.Switch.gatherStateLeft()
        crs = self.Switch.gatherStateRight()
        pbs = "TODO" #not sure exactly how the push button state is taken care of
        info = self.getStateInfo(self.getState())
        if (info[1]!=cls or info[2]!=crs): # have the switches been changed?
            return True
        else:
            return False


    #determines the validity of each state, by checking if the state is within the STATEDIC
    def stateValidator(self, state):
        return state in self.stateDic

    #Safe accessor for changing the STATE
    def changeState(self,state):
        if(self.stateValidator(state)):
            self.STATE = state
        else:
            print("not a valid state change: "+str(state))

    #Returns the information stored in the state
    def getStateInfo(self, state):
        if(self.stateValidator(state)):
            return self.stateDic.get(state)
        else:
            print("Not a valid requested state: "+str(state))

    #Returns the value of the current state
    def getState(self):
        return self.STATE


            

