import threading
import time

class Regulator(threading.Thread):
    def __init__(self,sensorList):
        self.__sensorList=sensorList
        self.__e0=0.0
        self.__e1=0.0
        self.__updateFreq=50.0
        self.__updateTime=1.0/self.__updateFreq
        self.__P=32.0 # P-max = 37, ocsilleringsperiod = 0.7
        self.__D=1.2
        self.__signalOut=0.0
        self.cal_floor_1 = [[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                                 [170,230],[47,160],[103,204],[56,165],[48,178]]
        self.cal_paper = [[7, 208], [10, 225], [19, 238], [8, 199], [32, 236], [8, 193], [77, 244], [8, 193], [10, 226], [10, 194], [9, 211]]
        self.cal_floor_2 = [[75, 213], [97, 206], [126, 232], [61, 180], [147, 232], [39, 174], [154, 237], [57, 183], [80, 199], [63, 177], [50, 178]]
        self.calibration_data = self.cal_floor_2
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(self.__updateTime)

            self.__e1=self.__e0
            self.__e0=self.get_current_error()

            # PD from lecture 5
            self.__signalOut=self.__P * self.__e0 + self.__D * ((self.__e0 - self.__e1) / self.__updateTime)

            self.setMotors()

    def setMotors(self):
        leftCurrent=self.getLeftMotor()
        rightCurrent=self.getRightMotor()
        left=leftCurrent-int(self.__signalOut)
        right=rightCurrent+int(self.__signalOut) 
        self.setRegMotor(left, right)
    
    def setRegMotor(self,left,right):
        self.__sensorList["regulator"] = left, right


    def getLeftMotor(self):
        return self.__sensorList["motorSpeed"][0]

    def getRightMotor(self):
        return self.__sensorList["motorSpeed"][1]

    def getSensorValues(self):
        return self.__sensorList["lineSensor"]

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
    for i in range(0,11):
        calibrateData[i][0] = sensorList[0][1][i]
    return calibrateData

def calibrate_tape(sensorList, calibrateData):
    for i in range(0,11):
        calibrateData[i][1] = sensorList[0][1][i]
    return calibrateData
