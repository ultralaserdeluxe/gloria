import threading
import time
from scipy.integrate import simps
import numpy as np
class Regulator(threading.Thread):
    
    #a constructor for the class
    def __init__(self,sensorList):
        #self.__calibrateData=calibrate_data
        #self.__calibrateData=[[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255]]
        self.__calibrateData=[[54,201],[122,225],[141,238],[66,177],[136,231],[76,185],
                     [171,228],[44,175],[97,195],[60,173],[43,168]]
        #self.__sensorList=sensorList
        
        self.__position=0.0
        self.__sensorList=sensorList
        self.__sensorList.append(["regulator",[0,0]])
        #print(self.__sensorList)
        self.__weights=np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45])
        self.__previousValues=[]
        self.__P=1.0
        self.__I=1.0
        self.__integratedValue=0.0
        self.__proportional=0.0
        self.__currentPosition=0.0
        self.__error=0.0
        self.__filteredValues=[]
        self.__derivatedValue = 0.0
        self.__D = 1.0
        threading.Thread.__init__(self)
    def run(self):
        while True:
            time.sleep(0.001)
            self.calculatePosition()
            if len(self.__previousValues)>=10:
                self.filterValues()
                if len(self.__filteredValues)>=10:
                    self.updatePID()
                    self.integrate()
                    self.proportional()
                    self.derivate()
                    self.piReg()
                    self.setMotors()
                    #print(self.__sensorList[0])
                    #print(self.__P,self.__I,self.__D)
                    
    def updatePID(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="PID":
                self.__P=self.__sensorList[i][1][0]
                self.__I=self.__sensorList[i][1][1]
                self.__D=self.__sensorList[i][1][2]
                return
        raise SyntaxError("sensor not in list")
        
    def setMotors(self):
        left=self.getLeftMotor()+int(self.getLeftMotor()*self.__error)
        right=self.getRightMotor()-int(self.getRightMotor()*self.__error)
        if left>255:
            left=255
        if left<-255:
            left=-255
        if right>255:
            right=255
        if right<-255:
            right=-255
        self.setRegMotor(left, right)
    def piReg(self):
        self.__error=self.__P*self.__proportional+self.__I*self.__integratedValue+self.__D*self.__derivatedValue
    def integrate(self):
        y = np.array([v - 0.5 for v in self.__filteredValues])
        self.__integratedValue = simps(y, self.__weights)
        
    def proportional(self):
        self.__proportional=self.__currentPosition-0.5
        
    def derivate(self):
        y = np.array([v - 0.5 for v in self.__filteredValues])
        self.__derivatedValue = np.average(np.diff(y) / self.__weights[1])
        
    def calibrate(self,calibrateData):
        self.__calibrateData=calibrateData
        
    def getSensorValues(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="lineSensor":
                return self.__sensorList[i][1]
        raise SyntaxError("sensor not in list")
    
    def setRegMotor(self,left,right):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="regulator":
                self.__sensorList[i][1][0]=left
                self.__sensorList[i][1][1]=right
                return
        raise SyntaxError("sensor not in list")
        
    def getLeftMotor(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="motorSpeed":
                return self.__sensorList[i][1][0]
        raise SyntaxError("sensor not in list")
    def getRightMotor(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="motorSpeed":
                return self.__sensorList[i][1][1]
        raise SyntaxError("sensor not in list")
    
    def filterValues(self):
        self.calculatePosition()
        if len(self.__previousValues)<10:
            self.__currentPosition= self.__previousValues[-1]
        while len(self.__previousValues)>10:
            del self.__previousValues[0]
        value=0.0
        divider=1.0/1024.0
        for i in range(10):
            value=value+self.__previousValues[i]*divider
            divider=divider*2
        self.__filteredValues.append(value)
        while len(self.__filteredValues)>10:
            del self.__filteredValues[0]
        self.__currentPosition=value
    
            
                
    def calculatePosition(self):
        temp=[]
        sensorValues=self.getSensorValues()
        for i in range(11):
            temp.append([sensorValues[i]-self.__calibrateData[i][0],self.__calibrateData[i][1]-self.__calibrateData[i][0]])
        for i in range(11):
            if temp[i][0]<0:
                temp[i][1]=temp[i][1]+abs(temp[i][0])
                temp[i][0]=0
        floatValues=[0.0]
        for i in range(11):
            if temp[i][1]!=0:
                floatValues.append(float(temp[i][0])/float(temp[i][1]))
            else:
                floatValues.append(0.0)
        floatValues.append(0.0)
        temp=[]
        for i in range(1,13):
            if floatValues[i]>floatValues[i-1] and floatValues[i]>floatValues[i+1]:
                temp.append([i,2.0*floatValues[i]-floatValues[i-1]-floatValues[i+1]])
        maxIndex=0
        max=0
        for element in temp:
            if element[1]>max:
                max=element[1]
                maxIndex=element[0]
        if floatValues[maxIndex+1]!=0 and floatValues[maxIndex-1]!=0:
            self.__previousValues.append( float(maxIndex)/12.0 +(floatValues[maxIndex]/floatValues[maxIndex+1])*0.05-(floatValues[maxIndex]/floatValues[maxIndex-1])*0.05)
        else:
            self.__previousValues.append(float(maxIndex)/12.0)   