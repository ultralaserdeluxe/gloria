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
        self.__updateFreq=20.0
        self.__updateTime=1.0/self.__updateFreq
        self.__P=20.0 # P-max = 37, ocsilleringsperiod = 0.7
        self.__I=0.0
        self.__D=1.0
        self.__signalOut=0.0
        self.__filtersig=0.0
        self.__oldSignalOuts=[]
        self.cal_floor_1 = [[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                                 [170,230],[47,160],[103,204],[56,165],[48,178]]
        self.cal_paper = [[7, 208], [10, 225], [19, 238], [8, 199], [32, 236], [8, 193], [77, 244], [8, 193], [10, 226], [10, 194], [9, 211]]
        self.cal_floor_2 = [[75, 213], [97, 206], [126, 232], [61, 180], [147, 232], [39, 174], [154, 237], [57, 183], [80, 199], [63, 177], [50, 178]]
        self.calibration_data = self.cal_floor_2
        threading.Thread.__init__(self)
        
    #main function
    def run(self):
        # print "Put robot on tape"
        # time.sleep(2)
        # calibrate_tape(self.__sensorList, self.calibration_data)
        # print "Put robot on floor"
        # time.sleep(2)
        # calibrate_floor(self.__sensorList, self.calibration_data)
        # print self.calibration_data
        # while True:
        #     pass

        e_sign_last = 0
        e_sign_now = 0

        last_time = 0
        now_time = 0
        
        while True:
            #make sure the pid regulators updates with the freq set in constructor
            time.sleep(self.__updateTime)
            self.__e1=self.__e0
            #time 0 becomes the current error
            self.__e0=self.get_current_error()

            # PD from lecture 5
            self.__signalOut=self.__P * self.__e0 + self.__D * ((self.__e0 - self.__e1) / self.__updateTime)
            

            e_sign_last = e_sign_now
            if self.__e0 >= 0:
                e_sign_now = 1
            else:
                e_sign_now = -1

            if e_sign_now != e_sign_last:
                last_time = now_time
                now_time = time.time()
#                print "now", e_sign_now, "last", e_sign_last, "diff", now_time - last_time

#            print "u", self.__signalOut, "e", self.__e0,

            #set the motor
            self.setMotors()


            
    #set each motorspeed to motorspeed+-motorspeed*signalout
    def setMotors(self):
        leftCurrent=self.getLeftMotor()
        rightCurrent=self.getRightMotor()
        left=leftCurrent-int(self.__signalOut)
        right=rightCurrent+int(self.__signalOut) 
        self.setRegMotor(left, right)
    
    #puts the calculated motorspeeds in the sensorlist
    def setRegMotor(self,left,right):
#        print "left", left, "right", right
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
                return list(self.__sensorList[i][1])
        raise SyntaxError("sensor not in list")

    def normalize(self, value, minimum, maximum):
        return float(value - minimum) / (maximum - minimum)

    def normalize_sensor_values(self, values, calibration_data):
        norm_values = []

        for i in range(len(values)):
            minimum = calibration_data[i][0]
            maximum = calibration_data[i][1]
            norm_values.append(self.normalize(values[i], minimum, maximum))

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
        norm_values = self.normalize_sensor_values(sensor_values, self.calibration_data)
        position = self.calc_position(norm_values)
        error = self.calc_error(position)
        
        return error

def calibrate_floor(sensorList, calibrateData): 
    #give floor values
    for i in range(0,11):
        calibrateData[i][0] = sensorList[0][1][i]
    return calibrateData

def calibrate_tape(sensorList, calibrateData):
    #give tape values
    for i in range(0,11):
        calibrateData[i][1] = sensorList[0][1][i]
    return calibrateData
