import numpy as np
import logging as log
from math import atan2,sqrt
class Arm():     
    def __init__(self):
        SEGMENTS = int(4) #number joints
        self.l = np.array([0, 150, 145, 120])# length of sections
        self.w = np.array([0]*SEGMENTS,dtype=float) #horizontal coordinate
        self.z = np.array([0]*SEGMENTS,dtype=float) #vertical coordinate
        self.x = np.array([0]*SEGMENTS,dtype=float) #x axis components
        self.y = np.array([0]*SEGMENTS,dtype=float) #y axis components
        self.a = np.array([np.pi]*SEGMENTS,dtype=float) #angle for the link, reference is previous link
        #todo rewrite gripper angle
        self.gripper_angle = np.array([90])
        self.tw = 0.0 # w axis position depth
        self.tz = 0.0 # z axis starting position height
        self.l12 = 0.0 # hypotenuse belween a1 & a2
        self.a12 = 0.0 #inscribed angle between hypotenuse, w   
        
    def calc_p2(self):#calculates position 2
        self.w[3] = self.tw
        self.z[3] = self.tz
        self.w[2] = self.tw-np.cos(np.radians(self.gripper_angle[0]))*self.l[3]
        self.z[2] = self.tz-np.sin(np.radians(self.gripper_angle[0]))*self.l[3]
        self.l12 = np.sqrt(np.square(self.w[2])+np.square(self.z[2]))
        
    def calc_p1(self):#calculate position 1
        self.a12 = np.arctan2(self.z[2],self.w[2])#return the appropriate quadrant 
        self.a[1] = np.arccos((np.square(self.l[1])+np.square(self.l12)-np.square(self.l[2]))
                              /(2*self.l[1]*self.l12))+self.a12
        self.w[1] = np.cos(self.a[1])*self.l[1]
        self.z[1] = np.sin(self.a[1])*self.l[1]
        
    def calc_x_y(self):#calc x_y Pcoordinates
        for i in range(len(self.x)):
            self.x[i] = self.w[i]*np.cos(self.a[0])
            self.y[i] = self.w[i]*np.sin(self.a[0])
        
    def get_angles(self): #get all of the motor angles see diagram
        self.a[2] = np.arctan((self.z[2]-self.z[1])/(self.w[2]-self.w[1]))-self.a[1]
        self.a[3] = np.deg2rad(self.gripper_angle[0])-self.a[1]-self.a[2] 
        angles = np.array(self.a).tolist()
        return angles
    
    
class robotArm():
    def __init__(self, shared):
        self.shared = shared
        self.arm=Arm()
        self.closed=False
        self.__limits=[[0,1023],[205,813],[210,940],[180,810],[0,1023],[0,512]]
	self.__totalLimits=[ [-410,410],[-350,400] ,[-71,420],[-90,90],[0,360],[0,140]]
        self.claw=0
        self.gripperOffset=0
        self.xyz=[100.0,100.0,100.0]
        self.__outOfBound=False
        self.__toReturn=[]
        self.draw_robot()#draw function to draw robot
    def checkRobotBounds(self):
        return abs(self.xyz[0])<140 and self.xyz[1]<170 and self.xyz[2]<11
    def getServoValues(self):
            self.update_a0_joy()
            self.update_tw_joy()
            self.update_z_joy()
            self.draw_robot()
            temp=self.__toReturn

            for i in range(len(temp)):
                if temp[i]>self.__limits[i][1]:
                    temp[i]=self.__limits[i][1]
                    self.handleError("axis "+str(i+1)+" value too high, set to maximum value instead")
                if temp[i]<self.__limits[i][0]:
                    temp[i]=self.__limits[i][0]
                    self.handleError("axis "+str(i+1)+" value too low, set to minimum value instead")
            return temp
    def handleError(self,error):
        self.shared["errorCodes"].append(error)
        log.warning(error)

    def setX(self,x):
        if self.checkRobotBounds():
            if (x<self.xyz[0] and self.xyz[0]<0) or (x>self.xyz[0] and self.xyz[0]>0):
                self.xyz[0]=x
            else:
                self.handleError("arm is heading into the body of the robot")
            
        else:
            if not self.__outOfBound:
                self.xyz[0]=x
            else:
                self.handleError("should not increase x if robot out of bounds")
                self.xyz[0]=x
    def setY(self,y):
        if self.checkRobotBounds():
            if (y>self.xyz[1]):
                self.xyz[1]=y
            else:
                self.handleError("arm is heading into the body of the robot")
            
        else:
            if not self.__outOfBound:
                self.xyz[1]=y
            else:
                self.handleError("should increase y if robot out of bounds")
                self.xyz[1]=y
    def setZ(self,z):
        if self.checkRobotBounds():
            if (z>self.xyz[2]):
                self.xyz[2]=z
            else:
                self.handleError("arm is heading into the body of the robot")
            
        else:
            if not self.__outOfBound:
                self.xyz[2]=z
            else:
                self.handleError("should not increase z if robot out of bounds")
                self.xyz[2]=z
    def setGripperAngle(self,gripper):
        self.arm.gripper_angle[0]=gripper
    def setGripper(self,gripper):
        self.claw=gripper
    def setGripperRotationOffset(self,rotation):
        self.gripperOffset=rotation
    
    def setAll(self, servo_values):
        self.setX(servo_values[0])
        self.setY(servo_values[1])
        self.setZ(servo_values[2])
        self.setGripperAngle(servo_values[3])
        self.setGripperRotationOffset(servo_values[4])
        self.setGripper(servo_values[5])

    def update_a0_joy(self): 
        self.arm.a[0] =atan2(self.xyz[1],self.xyz[0])
    def update_tw_joy(self):#extension w Slider Event
        self.arm.tw = sqrt((self.xyz[1])**2 +(self.xyz[0])**2)
    def update_z_joy(self):#height z slider event
        self.arm.tz = self.xyz[2]

    def draw_robot(self):#draw and update the 3D panel
        self.arm.calc_p2()
        self.arm.calc_p1()
        self.arm.calc_x_y()
        if self.arm.l12 < (self.arm.l[1]+self.arm.l[2]):#check boundaries
            if self.__outOfBound:
                self.__outOfBound=False
            temp=np.around(np.rad2deg(self.arm.get_angles()),2)
            toReturn=[]
            if self.xyz[0] < 0 and self.xyz[1] < 0:
                temp[0] = 360 + temp[0]
            toReturn.append(temp[0])
            toReturn.append(temp[1])
            toReturn.append(-temp[2])
            toReturn.append(-temp[3])
            toReturn.append(self.gripperOffset)
            toReturn.append(self.claw)
            toReturn[0]=toReturn[0]+60
            toReturn[1]=240-toReturn[1]
            toReturn[2]=240-toReturn[2]
            toReturn[3]=150-toReturn[3]
            toReturn[4]=toReturn[4]
            toReturn[5]=toReturn[5]
            for i in range(len(toReturn)):
                toReturn[i]=int(toReturn[i]*3.41)
            self.__toReturn=toReturn
        else:
            self.__outOfBound=True
