# --------------- #
# Team Rocket 2023
# Author Marcos De La Osa Cruz
# Class to handle talking to and from the arduinos

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
        self.create_controller_to_pi()
        self.create_pi_to_frame()
        self.create_frame_to_pi()
        self._pins = Pinout()
                # The actual pinout is defined in pinout.py
        self._frame_message_send = self._pins.getGPIOPINS("frame_message_send")
        self._frame_message_recieved = self._pins.getGPIOPINS("frame_message_recieved")
        self._controller_message_send = self._pins.getGPIOPINS("controller_message_send")
        self._controller_message_recieved = self._pins.getGPIOPINS("controller_message_recieved")

        # We will always be using the BCM mode
        GPIO.setmode(GPIO.BOARD)

        print (self._controller_message_recieved)
        # Setting them up to recieve input
        GPIO.setup(self._frame_message_recieved, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._controller_message_recieved, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Setting them up to produce output
        GPIO.setup(self._controller_message_send, GPIO.OUT)
        GPIO.setup(self._frame_message_send, GPIO.OUT)

        # Removing previously used call backs
        GPIO.remove_event_detect(self._controller_message_recieved)
        GPIO.remove_event_detect(self._frame_message_recieved)

        # adding the call backs
        GPIO.add_event_detect(self._controller_message_recieved, GPIO.RISING, 
                              callback=lambda x: self.keystroke_callback("controller_message_recieved"))
        GPIO.add_event_detect(self._frame_message_recieved, GPIO.RISING, 
                              callback=lambda x: self.keystroke_callback("frame_message_recieved"))
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
        elif(key == 'pressurization_button_pressed'):
            list = self._pins.getGPIOKeys().get('<<frame-message-recieved>>')
            press(list[1])
            return  
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

#-----------Create the dictionaries----------
    def create_pi_to_frame(self, printout:bool = False) -> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON/pi-to-frame.json") #path \\ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._pi_to_frame_message = json.load(controlFile)
        if (printout):
            print(self._pi_to_frame_message)
        controlFile.close()

    def create_controller_to_pi(self, printout:bool = False)-> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON/controller-to-pi.json") #path \\ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._pi_to_controller_message = json.load(controlFile)
        if (printout):
            print(self._pi_to_controller_message)
        controlFile.close()

    # Creates dictionary data structure
    def create_frame_to_pi(self, printout:bool = False) -> None:
        filePath = os.getcwd()
        filePath = os.path.join(filePath,"JSON/frame-to-pi.json") #path \\ must be replaced with / for linux
        controlFile = open(filePath, 'r')
        self._frame_to_pi_message = json.load(controlFile)
        if (printout):
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
    # TODO make sure to update this when we add more stuff to the communication

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

                if self._controller_to_pi_message["Switches"]["leftOn"] != data["Switches"]["leftOn"]:
                    self.keystroke_callback('left-switch')
                    self._controller_to_pi_message["Switches"]["leftOn"] = data["Switches"]["leftOn"]
                
                if self._controller_to_pi_message["Switches"]["rightOn"] != data["Switches"]["rightOn"]:
                    self.keystroke_callback('right-switch')
                    self._controller_to_pi_message["Switches"]["rightOn"] = data["Switches"]["rightOn"]

                if self._controller_to_pi_message["Button"]["Pressed"] != data["Button"]["Pressed"]:
                    self.keystroke_callback('pressurization_button_pressed')
                    self._controller_to_pi_message["Button"]["Pressed"] = data["Button"]["Pressed"]
                
                print(self._controller_to_pi_message)
                return
            except Exception as err:
                print(err, line)


    # Called in response to the fram interrupt to parse the frame json message
    def readFrame(self) -> None:
        while self._mega.readable():
            # read from controller arduino 
            line = self._mega.readline()
            # attempt to process readings
            try:
                data = line.decode('ascii').rstrip()
                data = json.loads(data)

                #Copy the information from the json to our serial object
                self._frame_to_pi_message["Solenoids"]["OpenA"] = data["Solenoids"]["OpenA"]
                self._frame_to_pi_message["Solenoids"]["OpenB"] = data["Solenoids"]["OpenB"]
                self._frame_to_pi_message["Solenoids"]["OpenC"] = data["Solenoids"]["OpenC"] 
                self._frame_to_pi_message["Compressor"]["turnOn"] = data["Compressor"]["turnOn"]
                print(self._controller_to_pi_message)
                return
            except Exception as err:
                print(err, line)


    # Sends the current commands to their respective arduino
    def write(self) -> None:
        #json_object = json.dumps(self.create_arduino_commanded)

        # use these two dicts
        self._pi_to_frame_message
        self._pi_to_controller_message

        frameData = self._pi_to_frame_message
        controllerData = self._pi_to_controller_message
        frameData = json.dumps(frameData)
        controllerData = json.dumps(controllerData)

        print("This is the json sending to the frame\n", frameData)
        print("This is the json sending to the controller\n", controllerData)

        #Code to open and read from the frame connection
        if self._mega.isOpen():
            self._mega.write(frameData.encode('ascii'))
            self._mega.flush()
        else:
            print('Something up, mega serial port is not open')

        #Code to open and read from the controller connection
        #TODO update thos
        if self._uno.isOpen():
            self._uno.write(controllerData.encode('ascii'))
            self._uno.flush()
        else:
            print("Something up, uno serial port is not open'")

        if self._mega.isOpen():
            self._mega.write(frameData.encode('ascii'))
            self._mega.flush()
        else:
            print("Something up, mega serial port is not open'")
        
        # Generate I/O interrupt for arduinos
        GPIO.output(self._frame_message_send, True)
        GPIO.output(self._controller_message_send, True)
        time.delay(1)
        GPIO.output(self._frame_message_send, False)
        GPIO.output(self._controller_message_send, False)



    # Handles updating the command dict with given information
    def updateCommand(self) -> None:
        pass

    # writes json bundle commanding arduino to activate Valve A (close the valve)
    def ValveManager(self, openA:bool, openB:bool, openC:bool)->None:
        self._pi_to_frame_message["Solenoids"]["OpenA"] = openA
        self._pi_to_frame_message["Solenoids"]["OpenB"] = openB
        self._pi_to_frame_message["Solenoids"]["OpenC"] = openC
        self.write()
        return

    # writes json bundle commanding arduino to turn on the air compressor
    def toggleCompressor(self, turnOn: bool)->None:
        self._pi_to_frame_message["Compressor"]["turnOn"] = turnOn
        self.write()
        return
        
    # writes json bundle that engages the left latch (Closes and holds)
    def toggleLatches(self, OpenLeft: bool, OpenRight: bool)->None:
        self._pi_to_frame_message["Latches"]["OpenLeft"] = OpenLeft
        self._pi_to_frame_message["Latches"]["OpenRight"] = OpenRight
        self.write()
        return
    
    #---Verification---#
    #Called during pressurization to check that frame recieved and updated appropriately
    def compare_frame_commanded_to_frame_response(self)->bool:
        recieved = self._frame_to_pi_message
        sent = self._pi_to_frame_message
        for key in sent.keys:
            sentValue = sent[key]
            recievedValue = recieved[key]
            if sentValue != recievedValue:
                return False
        return True



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
