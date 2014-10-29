import logging as log
import threading
import time

import sensorUnit
import distance

updateFreq=200.0 #Hz and must be float

class sensorThread(threading.Thread):
    """A thread class that fetches data from the sensorunit and puts it in the dict shared with mainthread and pc-thread."""

    def __init__(self, shared):
        self.shared=shared
        self.__sensorUnit=sensorUnit.sensorUnit()
	threading.Thread.__init__(self)
        self.__distanceListLeft = [0,0,0,0,0,0,0,0,0,0]
        self.__distanceListRight = [0,0,0,0,0,0,0,0,0,0]

    def run(self):
        while True:
            time.sleep(1.0/updateFreq)
            self.updateDistance()
            self.updateLineSensor()
            self.updateMiddleSensor()

    def updateDistance(self):
        del self.__distanceListLeft[0]
        del self.__distanceListRight[0]

        unfiltered_l = self.__sensorUnit.getLeftDistance()
        unfiltered_r = self.__sensorUnit.getRightDistance()

        self.__distanceListLeft.append(unfiltered_l)
        self.__distanceListRight.append(unfiltered_r)
    
        l = filteredValue(self.__distanceListLeft)
        r = filteredValue(self.__distanceListRight)

        self.shared["distance"] = [distance.distance_left(l) , distance.distance_right(r)]
            
    def normalize(self, value, mini, maxi):
        try:
            norm_value = float(value - mini) / (maxi - mini)
        except ZeroDivisionError:
            norm_value = 0

        if norm_value < 0:
            norm_value = 0
        elif norm_value > 1:
            norm_value = 1

        return norm_value

    def updateLineSensor(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)

            mini = self.shared["lineCalMin"][i]
            maxi = self.shared["lineCalMax"][i]

            norm_value = self.normalize(value, mini, maxi)
            
            self.shared["lineSensor"][i] = norm_value

    def updateMiddleSensor(self):
        left = self.__sensorUnit.getLeftMiddleSensor()
        right = self.__sensorUnit.getRightMiddleSensor()

        left_mini = self.shared["middleCalMin"][0]
        left_maxi = self.shared["middleCalMax"][0]
        right_mini = self.shared["middleCalMin"][1]
        right_maxi = self.shared["middleCalMax"][1]

        norm_left = self.normalize(left, left_mini, left_maxi)
        norm_right = self.normalize(right, right_mini, right_maxi)

        self.shared["middleSensor"][0] = norm_left
        self.shared["middleSensor"][1] = norm_right

    def calibrateTape(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)
            self.shared["lineCalMax"][i] = value

        self.shared["middleCalMax"][0] = self.__sensorUnit.getLeftMiddleSensor()
        self.shared["middleCalMax"][1] = self.__sensorUnit.getRightMiddleSensor()

        log.info("New tape calibration: %s %s" %(str(self.shared["lineCalMax"]), str(self.shared["middleCalMax"])))

    def calibrateFloor(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)
            self.shared["lineCalMin"][i] = value

        self.shared["middleCalMin"][0] = self.__sensorUnit.getLeftMiddleSensor()
        self.shared["middleCalMin"][1] = self.__sensorUnit.getRightMiddleSensor()

        log.info("New floor calibration: %s %s" %(str(self.shared["lineCalMin"]), str(self.shared["middleCalMin"])))

def filteredValue(list):
    divider = 0.5
    sum = 0
    for i in range(9,-1,-1):
        sum += (list[i] * divider)
        divider *= 0.5
    return sum

