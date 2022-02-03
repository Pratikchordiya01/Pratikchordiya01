import embedded_motor_control
from embedded_motor_control.drivers import tmc5160_reg as reg
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
import time
#import pyads
#import pyads_files
#from pyads_files import *
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
        self.motorObj.set_VMAX(150000)
        self.motorObj.set_DMAX(10000)
        self.motorObj.set_D1(1400)
        self.motorObj.set_VSTOP(10)

    def slowdown_rotation_configuration(self):
        self.motorObj.set_VSTART(1)
        self.motorObj.set_A1(1000)
        self.motorObj.set_V1(5000)
        self.motorObj.set_AMAX(10000)
        self.motorObj.set_VMAX(120000)
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
            self.motor_start(51200*60)
            while homingBit == False:
                homingBit = self.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
            print("Got Homing Sensor!!")
            self.stop_motor()
            homingBit = self.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
            print("Homing Bit Last:",homingBit)
            time.sleep(3)
           # self.motorObj.position_mode()
        if homingBit == True:
            print("Already Home!!!")

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


if __name__ == '__main__':
    obj = storageRack()
    obj.homing_sequence()
    counter = 0
    positionBit = False
    lowBit = 0
    runBit = 0
    homingBit = obj.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
    slowDownBit = obj.gpioObj.read_pin(mcp_io_dict["Slow_down_sensor"])
    obj.position_reset()

    while True:
        inputpulse = obj.gpioObj.read_pin(mcp_io_dict["proxi_sensor_1"])
        #print("InputPulse",inputpulse)
        if inputpulse == True and lowBit == 1:
            lowBit = 0
            outputBit = obj.gpioObj.write_pin(mcp_io_dict["BREAK1"],False)
            print("OutputBit",outputBit)
            time.sleep(1)
            if counter == 1:
                motor_position_to_go = (51200*30*45)
                print("Motor position",motor_position_to_go)
                #time.sleep(1)
            if counter == 0:
                motor_position_to_go = (51200*30*22.5)
                print("Motor position_1",motor_position_to_go)
                #time.sleep(1)
                counter +=1
            obj.position_reset()
            #motor_position_to_go = (51200*30*22.5)
            #print("Motor Position",motor_position_to_go)
            obj.motor_start(int(motor_position_to_go))
            time.sleep(0.5)
            #if counter >= 8:
                #counter = 0
            runBit = 1
        positionBit = obj.gpioObj.read_pin(mcp_io_dict["Position_sensor"]) 
        #time.sleep(3)
        if positionBit == True and runBit == 1:
            runBit = 0
            obj.stop_motor()
            outputBit = obj.gpioObj.write_pin(mcp_io_dict["BREAK1"],True)
        if inputpulse == False:
            lowBit = 1
                    

