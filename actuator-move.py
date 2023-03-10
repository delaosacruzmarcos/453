#!/usr/bin/env python3
import serial
import time
import json


com = -1

# received from arduino
JOYSTICK_KEY = "joysticks"
joystick_readings = dict()

ACTUATOR_KEY = "actuators"
actuator_readings = dict()


# to be sent to arduino
actuator_control = dict()

# Name of our attached arduino
arduino = '/dev/ttyACM1'

# We want to keep the baud rate consistent on Arduino and RasPi
baud = 9600

if __name__ == '__main__':
    ser = serial.Serial(arduino, baud, timeout=5)
    ser.reset_input_buffer()

    while True:
        try:
            # only works when sendResponse() is commented out
            bs = bytes("{\"actuators\": {\"1\": {\"move_to\": 100}}}", 'ascii')
            ser.write(bs)
            ser.flush()

            line = ser.readline()
            Rx = line.decode('ascii').rstrip()
            print(Rx)
        except Exception as err:
            print(err)