#import embedded_motor_control
#from embedded_motor_control.drivers import tmc5160_reg as reg
#import embedded_motor_control.mux_control as mux
#from embedded_motor_control.io_mapped_dict import mcp_io_dict
#from pyads_files.shared_dict import write_register_map as msd
#import threading
import multiprocessing
import sys
import time
from serialTest import receiveConfigFile
import os
import switch
from switch import *
#from switch import power_off

def main():
    obj = storageRack()
    print("\r\nHoming Start")
    obj.homing_sequence()
    positionBit = False
    homingBit = obj.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
    if homingBit == True:
        counter = 0
    slowDownBit = obj.gpioObj.read_pin(mcp_io_dict["Slow_down_sensor"])
    obj.position_reset()
    serialObj = receiveConfigFile('/dev/ttyUSB0')
    #obj.start_thread()
    #t1 = threading.Thread(target=obj.power_off)
    #t1.start()
    print ("In Main Thread")
    while True:
        print("In Main While Loop")
        obj.position_reset()
        value = serialObj.receive_config_file()
        print(value)
        if value == 'RIGHT':
            #print(value)
            if counter == 0:
                #print("Motor Rotate right")
                motor_position_to_go = (-51200*30*22.5)
                #obj.position_reset()
                obj.motor_start(int(motor_position_to_go))
                print("motor start moving")
                #obj.position_reset()
                time.sleep(0.5)
                positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                #time.sleep(1)
                print("position sensor",positionBit)
                while positionBit == False:
                    switch1 = obj.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
                    if switch1 == False:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],True)
                        positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                        #print("position sensor",positionBit)
                    else:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],False)
                        obj.homing_sequence()
                        os.system('poweroff')
                    #positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                    #print("position sensor",positionBit)
                obj.stop_motor()
                counter +=1
                print("motor Stop")
                #obj.motor_start(positionBit)
            else:
                motor_position_to_go = (-51200*30*45)
                #obj.position_reset()
                obj.motor_start(int(motor_position_to_go))
                #obj.position_reset()
                time.sleep(0.5)
                positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                #time.sleep(1)
                while positionBit == False:
                    switch1 = obj.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
                    if switch1 == False:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],True)
                        positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                        #print("position sensor",positionBit)
                    else:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],False)
                        obj.homing_sequence()
                        os.system('poweroff')
                    #positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                    #print("position sensor",positionBit)
                obj.stop_motor()
        elif value == 'LEFT':
            if counter == 0:
                #print("Motor Rotate left")
                motor_position_to_go = (51200*30*22.5)
                obj.motor_start(int(motor_position_to_go))
                time.sleep(0.5)
                positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                print("position sensor",positionBit)
                while positionBit == False:
                    switch1 = obj.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
                    if switch1 == False:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],True)
                        positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                        #print("position sensor",positionBit)
                    else:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],False)
                        obj.homing_sequence()
                        os.system('poweroff')
                    #positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                    #print("position sensor",positionBit)
                obj.stop_motor()
                counter +=1
                #positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                #obj.motor_start(positionBit)
            else:
                motor_position_to_go = (51200*30*45)
                obj.motor_start(int(motor_position_to_go))
                time.sleep(0.5)
                positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                #time.sleep(1)
                while positionBit == False:
                    switch1 = obj.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
                    if switch1 == False:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],True)
                        positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                        #print("position sensor",positionBit)
                    else:
                        light = obj.gpioObj.write_pin(mcp_io_dict["BREAK2"],False)
                        obj.homing_sequence()
                        os.system('poweroff')
                    #positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                    #print("position sensor",positionBit)
                obj.stop_motor()
        elif value == 'HOME':
            print("Motor Homing")
            obj.homing_sequence()
            positionBit = False
            counter = 0
            homingBit = obj.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
            slowDownBit = obj.gpioObj.read_pin(mcp_io_dict["Slow_down_sensor"])
            obj.position_reset()
            
if __name__ == '__main__':
    obj = storageRack()
    #print("start")
    #t1 = threading.Thread(target=main)
    #t2 = threading.Thread(target=obj.power_off)
    #t1.start()
    #time.sleep(1)
    #t2.start()
    p1 = multiprocessing.Process(target=main)
    p2 = multiprocessing.Process(target=obj.power_off)
    p1.start()
    time.sleep(1)
    p2.start()
