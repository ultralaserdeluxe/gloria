from regulator import Regulator
import pygame
import time
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
    
joy=Joystick()


sensorList=[["lineSensor",[0,0,20,0,255,128,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[1,2,3,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[50,50]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]],
            ["PID",[1.0,1.0,1.0]]
            ]
reg=Regulator(sensorList)
def setLineSensor(values,sensorList):
    for i in range(len(sensorList)):
        if sensorList[i][0]=="lineSensor":
            sensorList[i][1]=values
            break
def getRegulator():
    for i in range(len(sensorList)):
        if sensorList[i][0]=="regulator":
            return (sensorList[i][1])
    return []
def setPID(set,value):
    for i in range(len(sensorList)):
        if sensorList[i][0]=="PID":
            sensorList[i][1][set]=value
            break
reg.daemon=True    
reg.start()
P=1.0
I=1.0
D=1.0
while True:
    time.sleep(0.01)
    x=joy.x_axis() + 1
    x=int(x*5.5)
    l=[0]*11
    l[x]=255
    if (joy.get_button_2()):
        P=P+joy.get_hat()[1]*0.1
        setPID(0, P)
    if (joy.get_button_1()):
        I=I+joy.get_hat()[1]*0.1
        setPID(1, I)
    if (joy.get_button_3()):
        D=D+joy.get_hat()[1]*0.1
        setPID(2, D)
        
    #print l
    setLineSensor(l, sensorList)
    print(getRegulator())
    
    
