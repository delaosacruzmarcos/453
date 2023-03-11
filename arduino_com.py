#!/usr/bin/env python3
import serial
import time
import json
import actuator

controlFile = open("arduino-control.json", 'r')
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

if __name__ == '__main__':
    ser = serial.Serial(arduino, baud, timeout=5)
    ser.reset_input_buffer()

    act1 = actuator.Actuator('1')    
    while True:
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
                print(actuator_readings["1"], pressure_readings["pressure"])
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