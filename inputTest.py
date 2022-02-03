import embedded_motor_control
from embedded_motor_control.drivers import tmc5160_reg as reg
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
#from embedded_motor_control.motor import Motor
import time
obj = mux.mcp23017GpioControl()


def check_sensor_input_trigger():
    #sensor_input_1 = obj.read_pin(mcp_io_dict["Sensor_input_1"])
    #sensor_input_2 = obj.read_pin(mcp_io_dict["Sensor_input_2"])
    #sensor_input_3 = obj.read_pin(mcp_io_dict["Sensor_input_3"])
    input_1 = obj.read_pin(mcp_io_dict["proxi_sensor_1"])
    #input_2 = obj.read_pin(mcp_io_dict["SWITCH_4"]) 
    #input_3 = obj.read_pin(mcp_io_dict["SWITCH_3"])
    input_4 = obj.read_pin(mcp_io_dict["SWITCH_2"])

   # print("sensor_input_1:",sensor_input_1) 
   # print("sensor_input_2:",sensor_input_2) 
   # print("sensor_input_3:",sensor_input_3) 
    #if int(sensor_input_1) == 1:
        #print("J23 Sensor Detect Position sensor Detect") 
    #if int(sensor_input_2) == 1:
        #print("J27 Sensor Detect Homing Sensor Detect")
    #if int(sensor_input_3) == 1:
        #print("J28 Sensor Detect Slow Down Sensor Detect")
    if (input_1) == True:
        print("Input 1 is on")
    #if (input_2) == True:
        #print("Input 2 is on")
    #if (input_3) == True:
        #print("Input 3 is on")
    if (input_4) == True:
        print("Input4 is on")

def check_output_trigger():
    #output_1 = obj.write_pin(mcp_io_dict["OUT1"],True)
    #output_2 = obj.write_pin(mcp_io_dict["OUT2"],True)
    #output_3 = obj.write_pin(mcp_io_dict["BUZZER"],True)
    #output_4 = obj.write_pin(mcp_io_dict["BREAK2"],True)
    output_5 = obj.write_pin(mcp_io_dict["BREAK1"],True)
    output_6 = obj.write_pin(mcp_io_dict["LED_4"],True)
    #output_7 = obj.write_pin(mcp_io_dict["LED_3"],True)
    time.sleep(2)
    output_5 = obj.write_pin(mcp_io_dict["BREAK1"],False)
    output_6 = obj.write_pin(mcp_io_dict["LED_4"],False)
    time.sleep(2)
    #output_8 = obj.write_pin(mcp_io_dict["Light_1_2"],True)

if __name__ == '__main__':
    while True:
        check_sensor_input_trigger()
        check_output_trigger()
