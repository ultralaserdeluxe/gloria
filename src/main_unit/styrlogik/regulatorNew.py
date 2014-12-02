import threading
import time

#remember to remove after debugging
import matplotlib.pyplot as plt

class Regulator(threading.Thread):
    
    #a constructor for the class
    def __init__(self,sensorList):
        self.__sensorList=sensorList
        self.__sensorList.append(["regulator",[0,0]])
        self.__e0=0.0
        self.__e1=0.0
        self.__e2=0.0
        self.__updateFreq=5.0
        self.__updateTime=1.0/self.__updateFreq
        self.__P=1.0
        self.__I=1.0
        self.__D=1.0
        self.__signalOut=0.0
        self.__filtersig=0.0
        self.__oldSignalOuts=[]
        threading.Thread.__init__(self)
        
    ##if you change the pid values outside this thread
    def updatePID(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="PID":
                self.__P=self.__sensorList[i][1][0]
                self.__I=self.__sensorList[i][1][1]
                self.__D=self.__sensorList[i][1][2]
                return
        raise SyntaxError("sensor not in list")
    
    #main function
    def run(self):
        plt.axis([0, 100, -3, 3])
        plt.ion()
        plt.show()
        j=0
        while True:
            #update values if they have changed in sensorlist
            self.updatePID()
            #make sure the pid regulators updates with the freq set in constructor
            time.sleep(self.__updateTime)
            #time -1 becomes -2
            self.__e2=self.__e1
            #time -1 becomes time 0(last error)
            self.__e1=self.__e0
            #time 0 becomes the current error
            self.__e0=self.calculatePositionNew(self.getSensorValues())-0.5
            #the regulation equation see http://portal.ku.edu.tr/~cbasdogan/Courses/Robotics/projects/Discrete_PID.pdf
            a=self.__P + self.__I * (self.__updateTime/2.0) + self.__D / (self.__updateTime)
            b=-self.__P + self.__I * (self.__updateTime/2.0)-(2.0*self.__D)/(self.__updateTime)
            c=self.__D/(self.__updateTime)
            self.__signalOut=self.__signalOut+a*self.__e0+b*self.__e1+c*self.__e2
            #restrict the output signal to be to high
            if self.__signalOut>3.0:
                self.__signalOut=3.0
            if self.__signalOut<-3.0:
                self.__signalOut=-3.0
            #store the output signal
            self.__oldSignalOuts.append(self.__signalOut)
            #calculate the filtered signa
            self.__filtersig=0.0
            if len(self.__oldSignalOuts)>=10:
                while(len(self.__oldSignalOuts)>10):
                    del self.__oldSignalOuts[0]
                divider=1.0/1024
                for i in range(10):
                    self.__filtersig=self.__filtersig+self.__oldSignalOuts[i]*divider
                    divider=divider*2
            #all this is for the plot
            if abs(self.__e0)<=1.0:
                plt.scatter(j, self.__e0,color='blue')
            if abs(self.__signalOut)<=1.0:
                plt.scatter(j, self.__signalOut,color='red')
            plt.draw()
            j=j+1
            if j%100==0:
                plt.cla()
            #set the motor
            #if you dont want to use the filtered signal you can use self.setMotors()
            #self.setMotorsFilter()
            self.setMotors()
            
    #set each motorspeed to motorspeed+-motorspeed*signalout
    def setMotors(self):
        leftCurrent=self.getLeftMotor()
        rightCurrent=self.getRightMotor()
        left=leftCurrent+int(2.0*leftCurrent*self.__signalOut)
        right=rightCurrent-int(2.0*rightCurrent*self.__signalOut) 
        self.setRegMotor(left, right)
    
    #set each motorspeed to motorspeed+-motorspeed*filteredsignal the multiplicator differes because of different strength in motors, try with the same
    def setMotorsFilter(self):
        leftCurrent=self.getLeftMotor()
        rightCurrent=self.getRightMotor()
        if self.__filtersig>0:
            left=leftCurrent+int(4.0*leftCurrent*self.__filtersig)
            right=rightCurrent-int(2.0*rightCurrent*self.__filtersig)
        else:
            left=leftCurrent+int(1.5*leftCurrent*self.__filtersig)
            right=rightCurrent-int(1.5*rightCurrent*self.__filtersig)
        self.setRegMotor(left, right)
    
    #puts the calculated motorspeeds in the sensorlist
    def setRegMotor(self,left,right):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="regulator":
                self.__sensorList[i][1][0]=left
                self.__sensorList[i][1][1]=right
                return
        raise SyntaxError("sensor not in list")
    #returns the leftmotorspeed from the sensorlist
    def getLeftMotor(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="motorSpeed":
                return self.__sensorList[i][1][0]
        raise SyntaxError("sensor not in list")
    #returns the rightmotorspeed from the sensorlist
    def getRightMotor(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="motorSpeed":
                return self.__sensorList[i][1][1]
        raise SyntaxError("sensor not in list")
    def getSensorValues(self):
        for i in range(len(self.__sensorList)):
            if self.__sensorList[i][0]=="lineSensor":
                return self.__sensorList[i][1]
        raise SyntaxError("sensor not in list")
    #calculates the current position using weights on all the sensors to the left and to the right
    def calculatePositionNew(self,sensorValues):
        temp=[]
        calibrateData=[[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                     [170,230],[47,160],[103,204],[56,165],[48,178]]
        for i in range(11):
            temp.append([sensorValues[i]-calibrateData[i][0],calibrateData[i][1]-calibrateData[i][0]])
        for i in range(11):
            if temp[i][0]<0:
                temp[i][1]=temp[i][1]+abs(temp[i][0])
                temp[i][0]=0
        floatValues=[]
        for i in range(11):
            if temp[i][1]!=0:
                floatValues.append(float(temp[i][0])/float(temp[i][1]))
            else:
                floatValues.append(0.0)
        left=0.0
        for i in range(6,0,-1):
            left=left+floatValues[6-i]*i*i
        right=0
        for i in range(6,0,-1):
            right=right+floatValues[4+i]*i*i
        #print("left:" +str(left))
        #print("right:"+ str(right))
        if left<2.0 and right<2.0:
            return 0.5
        elif left>right:
            return abs((left-70)/140)
        elif left<right:
            return abs((right+70)/170)
        else:
            return 0.5
    #calculates the current position by searching for maxpoints in the array of sensorvalues
    def calculatePosition(self,sensorValues):
        temp=[]
        calibrateData=[[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                     [170,230],[47,160],[103,204],[56,165],[48,178]]
        
        for i in range(11):
            temp.append([sensorValues[i]-calibrateData[i][0],calibrateData[i][1]-calibrateData[i][0]])
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
        max1=0
        for element in temp:
            if element[1]>max1:
                max1=element[1]
                maxIndex=element[0]
        if max1<1.0:
            return 0.5
        if floatValues[maxIndex+1]!=0 and floatValues[maxIndex-1]!=0:
            return ( float(maxIndex-1)/10.0 +(floatValues[maxIndex]/floatValues[maxIndex+1])*0.05-(floatValues[maxIndex]/floatValues[maxIndex-1])*0.05)
        else:
            return (float(maxIndex-1.0)/10.0)   