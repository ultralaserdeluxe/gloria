from regulatorNew import Regulator
import pygame
import time
from pcModule import pcModule
class Joystick():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
    def x_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(0)
    def y_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(1)
    def throttle(self):
        pygame.event.pump()
        return self.joystick.get_axis(2)
    def z_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(3)
    def get_button_0(self):
        pygame.event.pump()
        return self.joystick.get_button(0)
    def get_button_1(self):
        pygame.event.pump()
        return self.joystick.get_button(1)
    def get_button_2(self):
        pygame.event.pump()
        return self.joystick.get_button(2)
    def get_button_3(self):
        pygame.event.pump()
        return self.joystick.get_button(3)
    def get_button_4(self):
        pygame.event.pump()
        return self.joystick.get_button(4)
    def get_button_5(self):
        pygame.event.pump()
        return self.joystick.get_button(5)
    def get_button_6(self):
        pygame.event.pump()
        return self.joystick.get_button(6)
    def get_hat(self):
        pygame.event.pump()
        return self.joystick.get_hat(0)
sensorList=[["lineSensor",[67, 122, 152, 53, 181, 186, 184, 60, 100, 77, 56]],
            ["distance",[10,10]],
            ["armPosition",[1,2,3,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[10,10]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]],
            ["PID",[1.0,1.0,1.0]]
            ]
reg=Regulator(sensorList)
reg.daemon=True    
reg.start()
joy=Joystick()
gloria=pcModule("192.168.99.1")

def setLineSensor(values):
    for i in range(len(sensorList)):
        if sensorList[i][0]=="lineSensor":
            sensorList[i][1]=values
            break
def setPID(set,value):
    for i in range(len(sensorList)):
        if sensorList[i][0]=="PID":
            sensorList[i][1][set]=value
            break
def transferLinesensor():
    gloria.updateSensors()
    temp=gloria.getLineSensor()
    for i in range(len(sensorList)):
        if sensorList[i][0]=="lineSensor":
            sensorList[i][1]=temp
            break
def getRegulator():
    for i in range(len(sensorList)):
        if sensorList[i][0]=="regulator":
            return (sensorList[i][1])
    return []
P=1.32
I=0.3
D=0.01
setPID(0, P)
setPID(1, I)
setPID(2, D)
while True:
    time.sleep(0.05)
    transferLinesensor()
    if (joy.get_button_2()):
        P=P+joy.get_hat()[1]*0.01
        setPID(0, P)
    if (joy.get_button_1()):
        I=I+joy.get_hat()[1]*0.01
        setPID(1, I)
    if (joy.get_button_3()):
        D=D+joy.get_hat()[1]*0.01
        setPID(2, D)
    if joy.get_button_0():
        x=joy.x_axis() + 1
        x=int(x*5.5)
        l=[0]*11
        l[x]=255
        temp=l
        for i in range(len(sensorList)):
            if sensorList[i][0]=="lineSensor":
                sensorList[i][1]=temp
                break
    if joy.get_button_4():
        temp=[198, 225, 168, 58, 155, 65, 166, 36, 87, 70, 48]
        for i in range(len(sensorList)):
            if sensorList[i][0]=="lineSensor":
                sensorList[i][1]=temp
                break
    if joy.get_button_5():
        temp=[51, 122, 153, 48, 138, 38, 173, 41, 99, 166, 165]
        for i in range(len(sensorList)):
            if sensorList[i][0]=="lineSensor":
                sensorList[i][1]=temp
                break
            
                        
    temp=list(getRegulator())
    if temp[0]>0:
        temp[0]=temp[0]+60
    if temp[0]<0:
        temp[0]=temp[0]-60
    if temp[1]>0:
        temp[1]=temp[1]+60
    if temp[1]<0:
        temp[1]=temp[1]-60
    if temp[0]>255:
        temp[0]=255
    if temp[0]<-255:
        temp[0]=-255
    if temp[1]>255:
        temp[1]=255
    if temp[1]<-255:
        temp[1]=-255
    #print(temp)
    gloria.setMotorSpeed(temp[0], temp[1])
    print(P,I,D)
