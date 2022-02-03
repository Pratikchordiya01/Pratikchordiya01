# Embedded Motion Control Library

Python Stepper motor driver for TMC5160 



The library is tested and applicable on the following boards:
*  Nvidia Jetson Nano
*  Nvidia Jetson Xavier
*  Raspberry Pi 4/3B


## Getting Started

###### Installing TMC Motion Library 

> Git Clone the Library

###### Installing Dependency Libraries


##### 1.Spidev 
> pip3 install spidev


##### 2.Numpy
> pip3 install numpy


##### 3.Jetson.GPIO

Follow the link to install Jetson.GPIO : https://github.com/NVIDIA/jetson-gpio

After this the library and its dependency is installed. In order to use the library features you need to enable the SPI pins on the board.
For enabling the SPI pins on Jetson Nano/Xavier the following steps are required:

##### Enable SPI pins on Jetson Nano/Xavier

Open Terminal and write the enter the following code :

> sudo /opt/nvidia/jetson-io/jetson-io.py

Select the SPI pins and reboot. 
You are all ready to start using the library


##### 4.board package, busio package, digitalio package

Command for installing above three packages:
> pip3 install adafruit-blinka


##### 5.adafruit_mcp230xx Package

Command for installing above package:
> sudo pip3 install adafruit-circuitpython-mcp230xx

Code Referance and API documentation Link:
> https://learn.adafruit.com/using-mcp23008-mcp23017-with-circuitpython/python-circuitpython





## Lights API Example

```
import config as co
import time

pin = co.pin_control()
pin.lights(1,'ON')
pin.lights(3,'ON')
time.sleep(5)
pin.lights(1,'OFF')
pin.lights(3,'OFF')

```

## LED API Example

```
import config as co
import time

pin = co.pin_control()
pin.led('RED','ON')
time.sleep(3)
pin.led('RED','OFF')
time.sleep(3)
pin.led('BLUE','ON')
time.sleep(3)
pin.led('BLUE','OFF')
time.sleep(3)
pin.led('YELLOW','ON')
time.sleep(3)
pin.led('YELLOW','OFF')
time.sleep(3)

```


## Motion API Example
```
'''
Arguments: case,x_coordinate,y_coordinate,angle,button_spacing,press,time_press
        1. case - 'one': one plunger, 'two': two plunger
        2. x_coordinate = x-axis movement in mm [0-200]
        3. y_coordinate = y-axis movement in mm [0-250]
        4. angle = angle in degree [0-360]
        5. button_spacing = button spacing distance in mm [20-60]
        6. press = 0/1, 1-pressing. 0- not pressing
        7. time_press = press and hold time by button in seconds
Description :Function to actuate the motors
Return : True/False

'''

import motionlib as motion
import time

motion_obj = motion.motion_library()
motion_obj.run('two',100,50,0,0,1,0)
motion_obj.run('two',0,0,0,0,0,0)
    
    

```

## Motor Breaks API

```
# Example to release all motors

import config as co

obj = co.mux.mcp23017GpioControl()
pin = co.pin_control()
m4 = co.motor_init(4,obj)
m5 = co.motor_init(5,obj)
m3 = co.motor_init(3,obj)
m2 = co.motor_init(2,obj)
m1 = co.motor_init(1,obj)
m0 = co.motor_init(0,obj)
m0.disable_motors()
m1.disable_motors()
m2.disable_motors()
m3.disable_motors()
m4.disable_motors()
m5.disable_motors()
pin.breaks(1,'ON')
pin.breaks(2,'ON')

```

## LED Blinking API Example

```
import config as co
import time

pin = co.pin_control()
pin.led('RED','BLINK')
#time.sleep(1)
#pin.blink()
time.sleep(10)
pin.stop_blinking()
```
