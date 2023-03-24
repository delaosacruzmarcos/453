
# --------------- #
# Team Rocket 2023
# Author Marcos De La Osa Cruz
# Class to handle talking to and from the arduino

import serial
import time
import os
import json
import actuator


class Serial_Coms():

    #holds current ardunio state
    _arduinoInfo: dict = None
    #holds the information we want to send to the arduino
    _arduinoCommanded: dict = None

    def __init__(self) -> None:
        print('debug')
        self.create_arduino_commanded()
        self.create_arduinoInfo()
       # self.serial_begin()

    def create_arduino_commanded(self) -> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON\\arduino-control.json") #path \ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._arduinoCommanded = json.load(controlFile)
        controlFile.close()

    # Creates dictionary data structure
    def create_arduinoInfo(self) -> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON\\arduino-json-form.json") #path \ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._arduinoInfo = json.load(controlFile)
        controlFile.close()
        
    # starts serial communication
    def serial_begin(self) -> None:
        # Name of our attached arduino
        arduino = '/dev/ttyACM0'
        # We want to keep the baud rate consistent on Arduino and RasPi
        baud = 9600
        ser = serial.Serial(arduino, baud, timeout=5)
        ser.reset_input_buffer()
        return

    # gets the Raw data for the left drum
    def get_L_arduino_info(self) -> dict:
        pass

    # gets the Raw data for the right drum
    def get_R_arduino_info(self) -> dict:
        joy = self._arduinoInfo['joysticks']
        return joy['right']

    #---Communication---#
    # Called to update the internal datastructure with new information
    def read(self) -> None:
        pass

    # Sends the current command to the arduino
    def write(self) -> None:
        pass

    # Handles updating the command dict with given information
    def updateCommand(self) -> None:
        pass


def begin():
    controlFile = open("/JSON/arduino-control.json", 'r')
    START_CONTROLS = json.load(controlFile)

    # received from arduino
    JOYSTICK_KEY = "joysticks"
    joystick_readings = dict()

    ACTUATOR_KEY = "actuators"
    actuator_readings = dict()

    PRESSURE_KEY = "pressure"
    pressure_readings = dict()

    com = -1

    # to be sent to arduino
    arduino_control = START_CONTROLS
    actuator_control = START_CONTROLS[ACTUATOR_KEY]


    controlFile.close()
    # Name of our attached arduino
    arduino = '/dev/ttyACM0'

    # We want to keep the baud rate consistent on Arduino and RasPi
    baud = 9600

    ser = serial.Serial(arduino, baud, timeout=5)
    ser.reset_input_buffer()

    act1 = actuator.Actuator('1')    
    while True:
        time.sleep(0.2)
        while ser.readable():
            
            # read from arduino
            line = ser.readline()

            # attempt to process readings
            try:
                data = line.decode('ascii').rstrip()
                data = json.loads(data)

                com = data["COM"]
                joystick_readings = data[JOYSTICK_KEY]
                actuator_readings = data[ACTUATOR_KEY]
                pressure_readings = data[PRESSURE_KEY]
                print(actuator_readings, pressure_readings)
            except Exception as err:
                print(err, line)

        # attempt to write controls to arduino
            if(act1.getPos() != None):
                act1.moveTo(act1.getPos() - 50)
            else:
                print(actuator_readings, act1.actuator)

            controlData = json.dumps(arduino_control)
            try:
                ser.write(bytes(controlData, 'ascii'))
                ser.flush()
            except Exception as err:
                print(err, bytes(controlData))


