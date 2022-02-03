import embedded_motor_control
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
import time
import os
obj = mux.mcp23017GpioControl()



'''light = obj.write_pin(mcp_io_dict["BREAK2"],True)
switch = obj.read_pin(mcp_io_dict["SWITCH_4"])
print("Switch:",switch)
while True:
    switch = obj.read_pin(mcp_io_dict["SWITCH_4"])
    if switch == True:
        light = obj.write_pin(mcp_io_dict["BREAK2"],True)
    else:
        light = obj.write_pin(mcp_io_dict["BREAK2"],False)
        os.system('poweroff')
        time.sleep(30)
        #print("Shut Down")
        #print("Switch_1:",switch)
        break'''


switch2 = obj.read_pin(mcp_io_dict["SWITCH_4"])
print("Switch2:",switch2)
while True:
    switch2 = obj.read_pin(mcp_io_dict["SWITCH_4"])
    if switch2 == True:
        print("EMERGENCY STOP")

