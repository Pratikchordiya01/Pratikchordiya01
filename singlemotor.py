import embedded_motor_control
from embedded_motor_control.drivers import tmc5160_reg as reg
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
#from embedded_motor_control.motor import Motor

import time

obj = mux.mcp23017GpioControl()

'''m1 = embedded_motor_control.Motor(0,obj)
m1.enable_motor()
m1.irms_current(400,0.05)

m1.set_VSTART(1)
m1.set_A1(2000)
m1.set_V1(2000)
m1.set_AMAX(10000)
m1.set_VMAX(500000)
m1.set_DMAX(10000)
m1.set_D1(1400)
m1.set_VSTOP(10) 


m2 = embedded_motor_control.Motor(1,obj)
m2.enable_motor()
m2.irms_current(4500,0.05)
m2.set_VSTART(1)
m2.set_A1(2000)
m2.set_V1(20000)
m2.set_AMAX(10000)
m2.set_VMAX(230000)
m2.set_DMAX(10000)
m2.set_D1(1400)
m2.set_VSTOP(10)

m2.disable_motor()'''

m3 = embedded_motor_control.Motor(2,obj)
m3.enable_motor()

m3.irms_current(4500,0.05)
m3.set_VSTART(1)
m3.set_A1(1000)
m3.set_V1(5000)
m3.set_AMAX(10000)
m3.set_VMAX(100000)
m3.set_DMAX(7000)
m3.set_D1(1400)
m3.set_VSTOP(10)

m3.disable_motor()

'''m4 = embedded_motor_control.Motor(3,obj)
m4.enable_motor()
m4.irms_current(4500,0.05)
m4.set_VSTART(1)
m4.set_A1(1000)
m4.set_V1(5000)
m4.set_AMAX(10000)
m4.set_VMAX(100000)
m4.set_DMAX(7000)
m4.set_D1(1400)
m4.set_VSTOP(10)

m4.disable_motor()'''


'''while True:
    
    x=0
    x = int(input("enter"))
    for x in range(1,100):
        x+=5
        steps=((51200*x)/360)
        print("steps",steps)
        m1.go_to(int(steps))
     
   
    #m2.go_to(x)
    for i in range(50):
        steps=((51200*10000)/360)
        print("steps",steps)
        m1.go_to(int(steps)) 
        m2.go_to(int(steps)) 
        m3.go_to(int(steps))
        m4.go_to(int(steps)) 

    for i in range(50):
        steps=((51200*(-10000))/360)
        print("steps",steps)
        m1.go_to(int(steps)) 
        m2.go_to(int(steps)) 
        m3.go_to(int(steps))
        m4.go_to(int(steps))''' 
     
       
#while True: 
#    x = int(input("enter"))
#    steps=((51200*x)/360)
#    print("steps",steps)
#    m1.go_to(int(steps)) 
m3.go_to(51200*30) 
#    m3.go_to(int(steps)) 
#    m4.go_to(int(steps)) 

