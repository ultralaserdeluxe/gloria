class regulator():
    
    #a constructor for the class
    def __init__(self):
        #self.__calibrateData=calibrate_data
        self.__calibrateData=[[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255],[0,255]]
        #self.__sensorList=sensorList
        self.__position=0.0
        self.__sensorList=[["lineSensor",[0,0,20,0,255,128,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[1,2,3,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[50,50]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]]]
        self.__previousValues=[]
        self.__currentPosition=0.0
        
    def calibrate(self,calibrateData):
        self.__calibrateData=calibrateData
        
    def getSensorValues(self):
        for i in range(11):
            if self.__sensorList[i][0]=="lineSensor":
                return self.__sensorList[i][1]
        raise SyntaxError("sensor not in list")
    
    def filterValues(self):
        self.calculatePosition()
        if len(self.__previousValues)<10:
            return self.__previousValues[-1]
        while len(self.__previousValues)>10:
            del self.__previousValues[0]
        value=0.0
        divider=1.0/1024.0
        for i in range(10):
            value=value+self.__previousValues[i]*divider
            divider=divider*2
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