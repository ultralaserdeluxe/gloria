"""a thread class that fetches data from the sensorunit and puts it in the list shared with mainthread and pc-thread"""
import threading
import sensorUnit
import time
updateFreq=200.0 #Hz and must be float
class sensorThread(threading.Thread):
    def __init__(self,sensorList):
        self.__sensorList=sensorList
        self.__sensorUnit=sensorUnit.sensorUnit()
	threading.Thread.__init__(self)
        self.cal_max = [255] * 11
        self.cal_min = [0] * 11

    def run(self):
        while True:
            time.sleep(1.0/updateFreq)
            self.updateDistance()
            self.updateLineSensor()
            self.updateMiddleSensor()

    def updateDistance(self):
        l = self.__sensorUnit.getLeftDistance()
        r = self.__sensorUnit.getRightDistance()
        self.__sensorList["distance"] = [l , r]
                
    def updateLineSensor(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)

            norm_value = float(value - self.cal_min[i]) / (self.cal_max[i] - self.cal_min[i])

            if norm_value < 0:
                norm_value = 0
            elif norm_value > 1:
                norm_value = 1

            self.__sensorList["lineSensor"][i] = norm_value

    def updateMiddleSensor(self):
        left = self.__sensorUnit.getLeftMiddleSensor()
        right = self.__sensorUnit.getRightMiddleSensor()
        self.__sensorList["middleSensor"][0] = left
        self.__sensorList["middleSensor"][1] = right
