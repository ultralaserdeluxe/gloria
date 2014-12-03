import threading
import time

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
        self.calibration_data = [[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                                 [170,230],[47,160],[103,204],[56,165],[48,178]]
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
            self.__e0=self.get_current_error()
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

    def normalize(self, value, minimum, maximum):
        return float(value) / (maximum - minimum)

    def normalize_sensor_values(self, values, calibration_data):
        norm_values = []

        for i in range(len(values)):
            minimum = calibration_data[i][0]
            maximum = calibration_data[i][1]
            norm_values.append(normalize(values[i], minimum, maximum))

        return norm_values

    def calc_position(self, norm_values):
        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        # From TSEA29 lecture 5 (AVR, sensorer, Beagleboard)
        center = sum(map(lambda x, y: x*y, norm_values, weights)) / sum(norm_values)

        return center
        
    def calc_error(self, position):
        # 6 is the middle weight.
        return 6 - position

    def get_current_error(self):
        sensor_values = self.getSensorValues()
        norm_values = normalize_sensor_values(sensor_values, self.calibration_data)
        position = calc_position(norm_values)
        error = calc_error(position)
        
        return error
