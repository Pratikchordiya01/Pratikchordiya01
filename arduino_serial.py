import serial
import time

serialObj = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)


while True:
    try:
        data = serialObj.readline()
        string = data.decode()
        if string == 'MOVE_RIGHT':
            print(string)
        elif string == 'MOVE_LEFT':
            print("Motor Rotate left")
        elif string == 'HOME':
            print("Motor Homing")
    except:
        serialObj.close()

