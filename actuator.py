import arduino_com as com

class Actuator:
    def __init__(self, actuator):
        self.actuator = actuator

    def moveTo(self, pos :int):
        if(self.actuator in com.actuator_readings):
            com.actuator_control[self.actuator] = pos
            return True
        
        return False

    def getPos(self):
        if(self.actuator in com.actuator_readings):
            return com.actuator_readings[self.actuator]
        else:
            return None