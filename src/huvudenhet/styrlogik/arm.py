import numpy as np
from math import atan2,sqrt
class Arm():     
    def __init__(self):
        #number of joints
        SEGMENTS = int(4)
        #length of joints
        self.l = np.array([0, 150, 145, 120])
        self.w = np.array([0]*SEGMENTS,dtype=float) 
        self.z = np.array([0]*SEGMENTS,dtype=float) 
        self.x = np.array([0]*SEGMENTS,dtype=float) 
        self.y = np.array([0]*SEGMENTS,dtype=float) 
        self.a = np.array([np.pi]*SEGMENTS,dtype=float)
        self.gripper_angle = np.array([90])
        self.tw = 0.0 
        self.tz = 0.0 
        self.l12 = 0.0 
        self.a12 = 0.0
        #starting position
        self.xyz=[0.0,0.0,244.0]
        self.wrist_angle=0
        self.gripper=150
        
    #math!!! used internal
    def calcP2(self):
        self.w[3] = self.tw
        self.z[3] = self.tz
        self.w[2] = self.tw-np.cos(np.radians(self.gripper_angle[0]))*self.l[3]
        self.z[2] = self.tz-np.sin(np.radians(self.gripper_angle[0]))*self.l[3]
        self.l12 = np.sqrt(np.square(self.w[2])+np.square(self.z[2]))
    
    #math!!! used internal
    def calcP1(self):
        self.a12 = np.arctan2(self.z[2],self.w[2])
        self.a[1] = np.arccos((np.square(self.l[1])+np.square(self.l12)-np.square(self.l[2]))
                              /(2*self.l[1]*self.l12))+self.a12
        self.w[1] = np.cos(self.a[1])*self.l[1]
        self.z[1] = np.sin(self.a[1])*self.l[1]
    
    #calculates x and y, used internal
    def calCXY(self):
        for i in range(len(self.x)):
            self.x[i] = self.w[i]*np.cos(self.a[0])
            self.y[i] = self.w[i]*np.sin(self.a[0])
    
    #returns the angles of the arm in radians, used internal
    def getAngles(self): 
        self.a[2] = np.arctan((self.z[2]-self.z[1])/(self.w[2]-self.w[1]))-self.a[1]
        self.a[3] = np.deg2rad(self.gripper_angle[0])-self.a[1]-self.a[2] 
        angles = np.array(self.a).tolist()
        return angles
    
    #used internal
    def updateA0Joy(self): 
        self.a[0] =atan2(self.xyz[1],self.xyz[0])
        
    #used internal
    def updateTwJoy(self):#extension w Slider Event
        self.tw = sqrt((self.xyz[1])**2 +(self.xyz[0])**2)
        
    #used internal
    def updateZJoy(self):#height z slider event
        self.tz = self.xyz[2]
        
    #set the wrist angle
    def updatePitch(self,pitch):
        self.gripper_angle[0]=pitch
        
    #set the x-value
    def updateX(self,x):
        self.xyz[0]=x
        
    #set the y-value
    def updateY(self,y):
        self.xyz[1]=y
    
    #set the z-value
    def updateZ(self,z):
        self.xyz[2]=z
    
    #set the value for the gripper
    def updateGripper(self,gripper):
        self.gripper=gripper
     
    #increase the gripper with the value argument
    def increaseGripper(self,value):
        self.gripper=self.gripper+value
        
    #decrease the gripper with the value argument
    def decreaseGripper(self,value):
        self.gripper=self.gripper-value
    
    #sets the angle offset for the wristrotation
    def updateWristRotation(self,angle):
        self.wrist_rotation=angle
    
    #makes the internal calculations
    def calculateAngles(self):
        self.updateA0Joy()
        self.updateTwJoy()
        self.updateZJoy()
        self.calcP2()
        self.calcP1()
        self.calCXY()
        
        #return[base angle to positive x axis,joint 1 angle to xy plane, joint 2 angle to joint 1, joint 3 angle to joint 2(wrist angle),wrist rotations]
    def getCalculatedAngles(self):
        self.calculateAngles()
        toReturn=[]
        temp=np.around(np.rad2deg(self.getAngles()),2)
        toReturn.append(temp[0])
        toReturn.append(temp[1])
        toReturn.append(-temp[2])
        toReturn.append(-temp[3])
        toReturn.append(90-temp[0]+self.wrist_rotation)
        toReturn.append(self.gripper)
        return toReturn
    
    #takes to calculated values and adds an offset for the servos which zero is not where my zero is
    def getCalculatedAnglesWithOffset(self):
        temp=self.getCalculatedAngles()
        temp[0]=temp[0]+60
        temp[1]=temp[1]+60
        temp[2]=240-temp[2]
        temp[3]=150-temp[3]
        temp[4]=150+temp[4]
        temp[5]=temp[5]
        return temp
    
    #returns values to servos which should range from 0 to 1023
    def getServoValues(self):
        temp=self.getCalculatedAnglesWithOffset()
        for i in range(len(temp)):
            temp[i]=int(round(temp[i]*3.41333))
        return temp
#arm=Arm()
#arm.updateX(150)
#arm.updateY(150)
#arm.updateZ(150)
#print(arm.getCalculatedAngles())