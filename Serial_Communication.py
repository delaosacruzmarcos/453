# --------------- #
# Team Rocket 2023
# Author Marcos De La Osa Cruz
# Class to handle talking to and from the arduino

import serial
import time
import os
import json
import subprocess
import RPi.GPIO as GPIO
from pyautogui import press
from pinout import *
from pyautogui import press


#import actuator


class Serial_Coms():

    # Communication Pins
    _pins: Pinout = None

    #Holds file path and communication info for the arduino boards
    _arduinoInfo: dict = {
        "Frame": {
            "board": "mega2560",
            "port": "/dev/ttyACM0",
            "path": "/home/pi/Desktop/453/arduino/InFrame/InFrame.ino"
        },
        "Controller":{
            "board": "Arduino Uno",
            "port": "/dev/ttyACM1",
            "path": "/home/pi/Desktop/453/arduino/InController/InController.ino"
        }
    }

    # Information contained within the most recent controller-to-pi.json file
    _controller_to_pi_message: dict = {}

    # Information conatined within the most recent frame-to-pi.json
    _frame_to_pi_message: dict = {}

    # Information contained within the most recent pi-to-frame.json
    _pi_to_frame_message: dict = {}

    # information contained within the most recent pi-to-controller.json
    _pi_to_controller_message:dict = {}

    def __init__(self) -> None:
        print('debug')
        self.create_arduino_commanded()
        self.create_controller_message()
        self._pins = Pinout()
                # The actual pinout is defined in pinout.py
        frame_message_send = self._pins.getGPIOPINS("frame_message_send")
        frame_message_recieved = self._pins.getGPIOPINS("frame_message_recieved")
        controller_message_send = self._pins.getGPIOPINS("controller_message_send")
        controller_message_recieved = self._pins.getGPIOPINS("controller_message_recieved")

        # We will always be using the BCM mode
        GPIO.setmode(GPIO.BOARD)

        print (controller_message_recieved)
        # Setting them up to recieve input
        GPIO.setup(frame_message_recieved, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(controller_message_recieved, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Setting them up to produce output
        GPIO.setup(controller_message_send, GPIO.OUT)
        GPIO.setup(frame_message_send, GPIO.OUT)

        # Removing previously used call backs
        GPIO.remove_event_detect(controller_message_recieved)
        GPIO.remove_event_detect(frame_message_recieved)

        # adding the call backs
        GPIO.add_event_detect(controller_message_recieved, GPIO.RISING, 
                              callback=lambda x: self.keystroke_callback("controller_message_recieved"))
        GPIO.add_event_detect(frame_message_recieved, GPIO.RISING, 
                              callback=lambda x: self.keystroke_callback("frame_message_recieved"))
        self.create_controller_message()
        self.serial_begin()

    #keystroke call backs
    def keystroke_callback(self,key:str)->None:
        print("keystroke callback being called")
        if(key == "frame_message_recieved"): # recieved a message from the frame
            list = self._pins.getGPIOKeys().get('<<frame-message-recieved>>')
            press(list[1])
            return
        elif(key == "controller_message_recieved"):
            self.readController()
            list = self._pins.getGPIOKeys().get('<<controller-message-recieved>>')
            press(list[1])
            return


    # Uploads the .ino files, runs on start up
    def uploadSketches(self)->None:
        # (Frame) Mega sketch upload
        board = self._arduinoInfo["Frame"]["board"]
        port = self._arduinoInfo["Frame"]["port"]
        path = self._arduinoInfo["Frame"]["path"]
        result = subprocess.run(['avrdude', "-v","-p", board, "-c", "wiring", "-P", port,"-U","flash:w:"+path+":i"],capture_output=True)
        print(result.stdout.decode())

        # (Controller) Uno sketch upload
        board = self._arduinoInfo["Controller"]["board"]
        port = self._arduinoInfo["Controller"]["port"]
        path = self._arduinoInfo["Controller"]["path"]
        result = subprocess.run(['avrdude', "-v","-p", board, "-c", "wiring", "-P", port,"-U","flash:w:"+path+":i"],capture_output=True)
        print(result.stdout.decode())
        return


    def create_arduino_commanded(self) -> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON/pi-to-frame.json") #path \\ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._arduinoCommanded = json.load(controlFile)
        controlFile.close()

    # Creates dictionary data structure
    def create_controller_message(self) -> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON/controller-to-pi.json") #path \\ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._controller_to_pi_message = json.load(controlFile)
        print(self._controller_to_pi_message)
        controlFile.close()
        
    # starts serial communication
    def serial_begin(self) -> None:
        # Name of our attached arduino
        controllerBoard = self._arduinoInfo["Controller"]["port"]
        frameBoard = self._arduinoInfo["Frame"]["port"]
        # We want to keep the baud rate consistent on Arduino and RasPi
        baud = 9600
        self._uno = serial.Serial(controllerBoard, baud, timeout=5)
        self._mega = serial.Serial(frameBoard, baud, timeout=5)
        self._uno.reset_input_buffer()
        self._mega.reset_input_buffer()

        return

    # gets the Raw data for the left drum
    def get_L_arduino_info(self) -> dict:
        pass

    # gets the Raw data for the right drum
    def get_R_arduino_info(self) -> dict:
        joy = self._controller_message['joysticks']
        return joy['right']

    #---Communication---#
    # Called to update the internal  datastructure with new information
    def readFrame(self) -> None:
        pass 

    # Called to update the controller datastructure
    def readController(self) -> None:
        while self._uno.readable():
            # read from controller arduino 
            line = self._uno.readline()
            # attempt to process readings
            try:
                data = line.decode('ascii').rstrip()
                data = json.loads(data)

                #Copy the information from the json to our serial object
                self._controller_to_pi_message["Joysticks"]["left"]["x"] = data["Joysticks"]["left"]["x"]
                self._controller_to_pi_message["Joysticks"]["left"]["y"] = data["Joysticks"]["left"]["y"]
                self._controller_to_pi_message["Joysticks"]["right"]["x"] = data["Joysticks"]["right"]["x"]
                self._controller_to_pi_message["Joysticks"]["right"]["x"] = data["Joysticks"]["right"]["x"]
                self._controller_to_pi_message["Switches"]["leftOn"] = data["Switches"]["leftOn"]
                self._controller_to_pi_message["Switches"]["rightOn"] = data["Switches"]["rightOn"]
                self._controller_to_pi_message["Button"]["Pressed"] = data["Button"]["Pressed"]
                print(self._controller_to_pi_message)
                return
            except Exception as err:
                print(err, line)


    # Sends the current command to the arduino
    def write(self) -> None:
        #json_object = json.dumps(self.create_arduino_commanded)
        return

    # Handles updating the command dict with given information
    def updateCommand(self) -> None:
        pass

    # writes json bundle commanding arduino to activate Valve A (close the valve)
    def ValveManager(self, A:bool, B:bool, C:bool)->None:
        solDic:dict = self._arduinoCommanded['Solenoids']
        solDic['OpenA'] = A
        solDic['OpenB'] = B
        solDic['OpenC'] = C
        self.write()
        return

    # writes json bundle commanding arduino to turn on the air compressor
    def toggleCompressor(self, turnOn: bool)->None:
        solDic:dict = self._arduinoCommanded['Compressor']
        solDic["turnOn"] = turnOn
        self.write()
        return
        
    # writes json bundle that engages the left latch (Closes and holds)
    def toggleLatches(self, OpenLeft: bool, OpenRight: bool)->None:
        solDic:dict = self._arduinoCommanded['Latches']
        solDic["OpenRight"] = OpenRight
        solDic["OpenLeftt"] = OpenLeft 
        self.write()
        return

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


if __name__ == "__main__":
    # The testing code
    mySerial = Serial_Coms()
    print(mySerial._arduinoCommanded)
    mySerial.ValveManager(False,False,False)
    print(mySerial._arduinoCommanded)
    mySerial.toggleCompressor(True)
    print(mySerial._arduinoCommanded)
    mySerial.toggleLatches(True,True)
    print(mySerial._arduinoCommanded)
