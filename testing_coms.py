# --------------- #
# Team Rocket 2023
# Author Marcos De La Osa Cruz
# Testing the serial communication methods

from Serial_Communication import *
import time

def test_valves(serial: Serial_Coms)-> None:
    print("Testing valve communications")
    #Close A
    serial.ValveManager(False,True,True)
    print("Valve A is closed")
    time.sleep(30)
    
    #Close B
    serial.ValveManager(True,False,True)
    print("Valve B is closed")
    time.sleep(30)

    
    #Close C
    serial.ValveManager(True,True,False)
    print("Valve C is closed")
    time.sleep(30)


    #Close A & B & C
    serial.ValveManager(False,False,False)
    print("Valves A & B & C are closed")
    time.sleep(30)


    #Open A & B & C
    serial.ValveManager(True,True,True)
    print("Valves A & B & C are open")
    time.sleep(30)

    return

def test_reading_from_json_docs()->None:
    ser: Serial_Coms = Serial_Coms()
    ser.create_pi_to_frame(True)
    ser.create_controller_to_pi(True)
    ser.create_frame_to_pi(True)
    return


if __name__ == "__main__":
    s: Serial_Coms = Serial_Coms()
    test_reading_from_json_docs()
    while True:
        test_valves(s)