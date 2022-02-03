import time
import serial
import sys
import logging
from glob import glob

class receiveConfigFile():
    def __init__(self, Port):
        self.deviceSerial = serial.Serial(
                port = Port,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
               # timeout = 50
                )
        self.payload = ''
        
    def receive_config_file(self):
        if self.deviceSerial.isOpen():
            print("status:",self.deviceSerial.isOpen())
            try:
                while self.deviceSerial.inWaiting() > 0 or self.payload == '':
                    try:
                        self.payload = self.deviceSerial.readline()
                        #print(self.payload)
                        if (self.payload == ''):
                            continue
                        else:
                            break
                    except Exception as e:
                        print(e)
                if (self.payload != ''):
                   # print("Intensity:"+str(self.payload))
                    print("Received Data:",self.payload.rstrip().lstrip().decode('utf-8'))
                    returnValue = self.payload.rstrip().lstrip().decode('utf-8')
                    self.payload = ''
                    
                 #   time.sleep(0.5)
                    return returnValue
                else:
                    print("dident get any response!!")
                    raise Exception("error")

            except Exception as e:
                print(e)
                print("Error is occured!!")

if __name__ == '__main__':
   # fileObj = open("../config/config.json","r")
   # data = fileObj.read()
   # fileObj.close()
    serialObj = receiveConfigFile('/dev/ttyUSB0')  #serial port initialization
    time.sleep(2)
    while True:
        value = serialObj.receive_config_file()
        print("#############Value:",value)
    #serialObj.receive_config_file()
