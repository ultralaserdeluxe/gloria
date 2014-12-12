import logging as log
import threading
import time

import sensorUnit

updateFreq=200.0 #Hz and must be float

class sensorThread(threading.Thread):
    """A thread class that fetches data from the sensorunit and puts it in the dict shared with mainthread and pc-thread."""

    def __init__(self, shared):
        self.shared=shared
        self.__sensorUnit=sensorUnit.sensorUnit()
	threading.Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(1.0/updateFreq)
            self.updateDistance()
            self.updateLineSensor()
            self.updateMiddleSensor()

    def updateDistance(self):
        l = self.__sensorUnit.getLeftDistance()
        r = self.__sensorUnit.getRightDistance()
        self.shared["distance"] = [l , r]
                
    def updateLineSensor(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)

            mini = self.shared["lineCalMin"][i]
            maxi = self.shared["lineCalMax"][i]

            norm_value = float(value - mini) / (maxi - mini)

            if norm_value < 0:
                norm_value = 0
            elif norm_value > 1:
                norm_value = 1

            self.shared["lineSensor"][i] = norm_value

    def updateMiddleSensor(self):
        left = self.__sensorUnit.getLeftMiddleSensor()
        right = self.__sensorUnit.getRightMiddleSensor()
        self.shared["middleSensor"][0] = left
        self.shared["middleSensor"][1] = right

        # TODO: Normalize middleSensor

    def calibrateTape(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)
            self.shared["lineCalMax"][i] = value

        log.info("New tape calibration: %s" %str(self.shared["lineCalMax"]))
        # TODO: Calibrate middleSensor

    def calibrateFloor(self):
        for i in range(11):
            value = self.__sensorUnit.getLineSensor(i)
            self.shared["lineCalMin"][i] = value

        log.info("New floor calibration: %s" %str(self.shared["lineCalMin"]))
        # TODO: Calibrate middleSensor
