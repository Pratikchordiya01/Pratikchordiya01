import embedded_motor_control
from embedded_motor_control.drivers import tmc5160_reg as reg
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
import time


class storageRack():
    def __init__(self):
        self.gpioObj = mux.mcp23017GpioControl()
        self.motorObj = embedded_motor_control.Motor(2,self.gpioObj)
        self.motorObj.enable_motor()
        self.motorObj.irms_current(4500,0.05)
        self.normal_rotation_configuration()
        self.read_flag = True
        self.motorObj.set_stall(10)

    def normal_rotation_configuration(self):
        self.motorObj.set_VSTART(1)
        self.motorObj.set_A1(2000)
        self.motorObj.set_V1(20000)
        self.motorObj.set_AMAX(10000)
        self.motorObj.set_VMAX(100000)
        self.motorObj.set_DMAX(10000)
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

    def read_position(self):
        position_read_value = self.motorObj.get_position()
        return position_read_value

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
    startFlagAfterHoming = 0
    positionBit = False
    reached_position = False
    homingBit = obj.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
    slowDownBit = obj.gpioObj.read_pin(mcp_io_dict["Slow_down_sensor"])
    obj.position_reset()


    while True:
        print("Flag Value after Homing ", startFlagAfterHoming)
        rackinput = int(input("\nEnter Rack Postion: "))
        if startFlagAfterHoming == 0:
            shortestPathValue = obj.shortestpath(counter,rackinput)
            print("Shortest Path after homing ", shortestPathValue)
            if shortestPathValue < 0:
                motor_position_to_go = (-51200*30*22.5)/360
                print("Motor Position after Homing to go in if ", int(motor_position_to_go))
                obj.motor_start(int(motor_position_to_go))
                time.sleep(3)
                counter = 8
                print("counter value after homing to go in if ", counter)
            else:
                motor_position_to_go = (51200*30*22.5)/360
                print("Motor Position after Homing to go in else ",int(motor_position_to_go))
                obj.motor_start(int(motor_position_to_go))
                time.sleep(3)
                counter = 1
                print("counter value after homing to go in else ", counter)
            startFlagAfterHoming = 1
        homingBit = obj.gpioObj.read_pin(mcp_io_dict["Homing_sensor"])
        slowDownBit = obj.gpioObj.read_pin(mcp_io_dict["Slow_down_sensor"])
        shortestPathValue = obj.shortestpath(counter,rackinput)
        print("Shortest Path ", shortestPathValue)
        if 0 < int(rackinput) <= 8:
            while rackinput !=counter:
                obj.normal_rotation_configuration()
                obj.position_reset()
                motor_position_to_go = (51200*30*45*shortestPathValue)/360
                print("Position = ",motor_position_to_go)
                obj.motor_start(int(motor_position_to_go))
                if shortestPathValue <0:
                    counter -=1
                    print("shortest path counter ", counter)
                    if counter <1:
                        # print("if counter ", counter)
                        counter = 8
                        print("if counter", counter)
                else:
                    counter +=1
                    print("shortestpath else ", counter)

                if counter > 8:
                    counter =1
                    print("counter >8", counter)
                    
            print("Current_Rack_Position:",rackinput)
