import threading
import time
import station_functions as sf

class Regulator(threading.Thread):
    def __init__(self,sensorList):
        self.__sensorList=sensorList
        self.__e0=0.0
        self.__e1=0.0
        self.__updateFreq=50.0
        self.__updateTime=1.0/self.__updateFreq
        self.__P=28.6 # P-max = 37, ocsilleringsperiod = 0.7
        #self.__P=25.6 # P-max = 37, ocsilleringsperiod = 0.7
        self.__D=0.7
        #self.__D=0.5
        self.__signalOut=0.0
        self.linedet = sf.LineDetector()
        threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(self.__updateTime)

            self.__e1=self.__e0
            self.__e0=self.get_current_error()

            # PD from lecture 5
            self.__signalOut=self.__P * self.__e0 + self.__D * ((self.__e0 - self.__e1) / self.__updateTime)

            self.setMotors()

            self.__sensorList["error"] = self.__e0

    def setMotors(self):
        left=50-int(self.__signalOut)
        right=50+int(self.__signalOut)
        self.setRegMotor(left, right)

    def setRegMotor(self,left,right):
        self.__sensorList["regulator"] = [left, right]

    def getLeftMotor(self):
        return self.__sensorList["motorSpeed"][0]

    def getRightMotor(self):
        return self.__sensorList["motorSpeed"][1]

    def getSensorValues(self):
        return self.__sensorList["lineSensor"]

    def calc_position(self, norm_values):
        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        # From TSEA29 lecture 5 (AVR, sensorer, Beagleboard)
        try:
            center = sum(map(lambda x, y: x*y, norm_values, weights)) / sum(norm_values)
        except ZeroDivisionError:
            return 6

        return center

    def calc_error(self, position):
        # 6 is the middle weight.
        return 6 - position

    def get_current_error(self):
        sensor_values = self.getSensorValues()
        converted_values = self.linedet.convert_line_values(sensor_values)
        station = self.linedet.station_front_one(converted_values)
        mask = []
        if self.linedet.all_equal_one(converted_values):
            mask = [0] * 11
        elif station != sf.NO_STATION:
            mask = [0] * 4 + [1] * 3 + [0] * 4
        else:
            mask = [1] * 11

        sensor_values = map(lambda x, y: x * y, sensor_values, mask)
        position = self.calc_position(sensor_values)
        error = self.calc_error(position)

        return error
