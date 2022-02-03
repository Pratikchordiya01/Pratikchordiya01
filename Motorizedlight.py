import socket
import time
time.sleep(3)
import codecs
from numpy import interp
import threading
import embedded_motor_control
from embedded_motor_control.drivers import tmc5160_reg as reg
import embedded_motor_control.mux_control as mux
from embedded_motor_control.io_mapped_dict import mcp_io_dict
#host = '127.0.0.1'
host='0.0.0.0'
port = 8080
BUFFER_SIZE = 20
value='True'
res = bytes(value, 'utf-8')

class MotorRun():
    def __init__(self,n):
       self.n=n
       self.obj = mux.mcp23017GpioControl()
       
       self.m = embedded_motor_control.Motor(self.n,self.obj)
       self.m.enable_motor()
       self.m.irms_current(500,0.05)
       
    
    def homing_sequence(self,steps):
        self.m.set_VSTART(1)
        self.m.set_A1(1000)
        self.m.set_V1(1000)
        self.m.set_AMAX(5000)
        self.m.set_VMAX(5000)
        self.m.set_DMAX(5000)
        self.m.set_D1(700)
        self.m.set_VSTOP(100) 
        self.m.go_to(steps)

    def testrun(self,angle): 
        self.m.set_VSTART(1)
        self.m.set_A1(3000)
        self.m.set_V1(3000)
        self.m.set_AMAX(10000)
        self.m.set_VMAX(350000)
        self.m.set_DMAX(10000)
        self.m.set_D1(1400)
        self.m.set_VSTOP(10) 
        #steps = (interp(int(angle),[0,360],[0,51200]))
        steps=int((51200*int(angle))/360)
        self.m.go_to(steps)
        stepval=self.m.get_position()
        print("steps angle ______________________________________________________________",stepval)
        return angle
   

class synch_motor_process(threading.Thread):

    def __init__(self,motor_angle,motorobj,c,lock):
        threading.Thread.__init__(self)
        self.lock=lock
        self.motor_angle = motor_angle
        self.motorobj = motorobj
        self.c=c

    def run(self):
        self.lock.acquire()
        print("IN thread run function")
        angleVal=self.motorobj.testrun(self.motor_angle) 
        stepsval=int(interp(int(angleVal),[0,51200],[0,360]))
        #stepsval=(int(angleVal)*360)/51200
        print("stepsval in degree********************",stepsval)
        angle_value = bytes(str(stepsval),'utf-8') 
        #self.c.sendall(angle_value)  
        #time.sleep(0.175)
        self.lock.release()
        #self.lock.acquire()
        time.sleep(0.175)

def motor_homing():
    motor0steps=0
    motor1steps=0
    motor2steps=0
    motor3steps=0

    while True:
        values=proximitysensor()  
        print("values***********",values)
        if(values[0] == True and values[1] == True and values[2] == True and values[3]==True):
            break
        
        if(values[0] == False):
            motor0steps=motor0steps-100
            motorobj0.homing_sequence(motor0steps)
        
        if(values[1] == False):
            motor1steps=motor1steps-90
            motorobj1.homing_sequence(motor1steps)
        
        if(values[2] == False):
            motor2steps=motor2steps-90
            motorobj2.homing_sequence(motor2steps) 
        
        if(values[3] == False):
            motor3steps=motor3steps+30
            motorobj4.homing_sequence(motor3steps)  
        
    '''motorobj0.write(reg.XACTUAL,0)
    motorobj1.write(reg.XACTUAL,0)
    motorobj2.write(reg.XACTUAL,0)
    motorobj3.write(reg.XACTUAL,0)
    '''          
    print("homing")

def light_opeation(status):
    print("in light")
    if(status == 0):
        proxobj.write_pin(mcp_io_dict["Light_1_2"],False)
    else:
        proxobj.write_pin(mcp_io_dict["Light_1_2"],True)

    #time.sleep(2)
    #proxobj.write_pin(mcp_io_dict["Light_1_2"],False)
     
def proximitysensor():
    for i in range(5):
        proxisensor_1 = proxobj.read_pin(mcp_io_dict["proxi_sensor_1"])
        proxisensor_2 = proxobj.read_pin(mcp_io_dict["proxi_sensor_2"])
        proxisensor_3 = proxobj.read_pin(mcp_io_dict["proxi_sensor_3"])
        proxisensor_4 = proxobj.read_pin(mcp_io_dict["proxi_sensor_4"])
        # time.sleep(0.02)
    return[proxisensor_1,proxisensor_2,proxisensor_3,proxisensor_4]      

  

if __name__ == '__main__':
#work as a server
    lock = threading.Lock()
    values=[4]
    proxobj = mux.mcp23017GpioControl() 
    #objforhome=MotorRun()
    motorobj0=MotorRun(0)
    motorobj1=MotorRun(1)
    motorobj2=MotorRun(2)
    motorobj4=MotorRun(4)
  
    #light_opeation(True)
    motor_homing()
    
    motorobj0=MotorRun(0)
    motorobj1=MotorRun(1)
    motorobj2=MotorRun(2)
    motorobj4=MotorRun(4)
    
    motorobjdict = {0:motorobj0, 1:motorobj1, 2:motorobj2, 3:motorobj4}
    angle_val_homming=[0,0,0,0]
   
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    tr_dict = {}
    
    while True:
        c, addr = s.accept()
        data=c.recv(1024)
        print("*********recieved data*******************************************",data)
        if data != b'':
            data=codecs.decode(data, 'UTF-8')
            print(type(data))
            data=eval(data)
            #light_opeation(data[4])
            print("after eval",type(data))
            data[3]=-data[3]
            print("dataval***********************************************************************************",data)
            #for i in range(len(data)):
            for idx,i in enumerate(data): 
                print("THREAD WILL BE CREATED FOR **********",idx,i)
                print("*************value of angle and motor number*********************",data[idx],idx)
                if(idx==4):
                    light_opeation(data[idx])
                    time.sleep(0.175)
                else:
                    tr_dict[idx] = synch_motor_process(data[idx],motorobjdict[idx],c,lock) #angleval,motor no,connection accept,lock
                    tr_dict[idx].start()
                             
            for tr in tr_dict.keys():
                tr_dict[tr].join()
            time.sleep(0.5)
            values=proximitysensor()
           
            print(type(values))
            res = bytes(str(values),'utf-8') 
            c.sendall(res)
            c.sendall(b'END')
    print("end of code")
        #s.close()
