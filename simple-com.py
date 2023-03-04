#!/usr/bin/env python3
import serial
import time
import json

# Name of our attached arduino
arduino = '/dev/ttyACM0'

# We want to keep the baud rate consistent on Arduino and RasPi
baud = 9600

if __name__ == '__main__':
    ser = serial.Serial(arduino, baud, timeout=5)
    ser.reset_input_buffer()

    while True:
        line = ser.readline()
        try:
            print(line.decode('ascii'))
            ser.write(line)
        except Exception as err:
            print(err, line)