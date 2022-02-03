import embedded_motor_control
from embedded_motor_control.drivers import tmc5160_reg as reg
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
import time
import serial
from serialTest import receiveConfigFile
import os
import threading
#import pyads
#from motherboard_version.pyads_files.sensor_poller_ads import sensor_poller
#from pyads_files import *
#from pyads_files.shared_dict import write_register_map as msd
#from embedded_motor_control.motor import Motor


class storageRack():
    def __init__(self):
        self.gpioObj = mux.mcp23017GpioControl()
        self.motorObj = embedded_motor_control.Motor(2,self.gpioObj)
        self.motorObj.enable_motor()
        self.motorObj.irms_current(4500,0.05)
        self.normal_rotation_configuration()

    def normal_rotation_configuration(self):
        self.motorObj.set_VSTART(1)
        self.motorObj.set_A1(2000)
        self.motorObj.set_V1(20000)
        self.motorObj.set_AMAX(10000)
        self.motorObj.set_VMAX(110000)
        self.motorObj.set_DMAX(100000)
        self.motorObj.set_D1(1400)
        self.motorObj.set_VSTOP(10)

    def slowdown_rotation_configuration(self):
        self.motorObj.set_VSTART(1)
        self.motorObj.set_A1(1000)
        self.motorObj.set_V1(5000)
        self.motorObj.set_AMAX(10000)
        self.motorObj.set_VMAX(100000)
        self.motorObj.set_DMAX(7000)
        self.motorObj.set_D1(1400)
        self.motorObj.set_VSTOP(10)

    def homing_rotation_configuration(self):
        self.motorObj.set_VSTART(1)
        self.motorObj.set_A1(1000)
        self.motorObj.set_V1(5000)
        self.motorObj.set_AMAX(10000)
        self.motorObj.set_VMAX(100000)
        self.motorObj.set_DMAX(7000)
        self.motorObj.set_D1(1400)
        self.motorObj.set_VSTOP(10)

    def motor_start(self,requiredSteps):
    #        print("Inside Motor Start")
        self.motorObj.go_to(requiredSteps)

    def position_reached(self):
        val = self.motorObj.position_reached()
        return val

    def homing_sequence(self):
        self.homing_rotation_configuration()
        homingBit = self.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
        print("Homing Bit First:",homingBit)
        if homingBit == False:
            #self.plc.write_by_name('GVL_PC_TO_PLC.PC_TO_PLC_3',False)
            self.motor_start(51200*60)
            while homingBit == False:
                homingBit = self.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
            print("Got Homing Sensor!!")
            self.stop_motor()
            #self.plc.write_by_name('GVL_PC_TO_PLC.PC_TO_PLC_3',True)
            homingBit = self.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
            print("Homing Bit Last:",homingBit)
            time.sleep(3)
           # self.motorObj.position_mode()
        if homingBit == True:
            print("Already Home!!!")
            #self.plc.write_by_name('GVL_PC_TO_PLC.PC_TO_PLC_3',True)

    def stop_motor(self):
        self.motorObj.stop_motor()
        time.sleep(0.005)
        self.motorObj.position_mode()

    def position_reset(self):
        self.motorObj.reset_position()

    def shortestpath (self, origin, target):
        signedDiff = 0.0
        if origin > target:
            raw_diff = origin - target
        else:
            raw_diff = target - origin
        mod_diff = (raw_diff % 8.0)
        if mod_diff > 4.0:
            signedDiff = (8.0 - mod_diff)
            if target > origin:
                signedDiff = signedDiff* -1
        else:
            signedDiff = mod_diff
            if origin > target:
                signedDiff = signedDiff* -1
        return signedDiff
    
    def power_off(self):
        light = self.gpioObj.write_pin(mcp_io_dict["BREAK2"],True)
        switch1 = self.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
        print("Switch1:",switch1)
        while True:
            switch1 = self.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
            if switch1 == False:
                light = self.gpioObj.write_pin(mcp_io_dict["BREAK2"],True)
            else:
                light = self.gpioObj.write_pin(mcp_io_dict["BREAK2"],False)
                self.homing_sequence()
                os.system('poweroff')
                time.sleep(30)
                #print("Shut Down")
                #print("Switch_1:",switch)
                break

    '''def stop_thread(self):
        self.t1.join()

    def start_thread(self):
        self.t1 = threading.Thread(target = self.power_off)
        self.t1.start()'''


if __name__ == '__main__':
    obj = storageRack()
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
    #t1.join()

    while True:
        obj.position_reset()
        value = serialObj.receive_config_file()
        print(value)
        if value == 'RIGHT':
            print(value)
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
                #print("position sensor",positionBit)
                while   positionBit == False:
                    positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
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
                while   positionBit == False:
                    positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                    #print("position sensor",positionBit)
                obj.stop_motor()
        elif value == 'LEFT':
            if counter == 0:
                #print("Motor Rotate left")
                motor_position_to_go = (51200*30*22.5)
                obj.motor_start(int(motor_position_to_go))
                time.sleep(0.5)
                positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
                #print("position sensor",positionBit)
                while   positionBit == False:
                    positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
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
                while   positionBit == False:
                    positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"])
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
