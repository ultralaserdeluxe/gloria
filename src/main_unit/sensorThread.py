"""a thread class that fetches data from the sensorunit and puts it in the list shared with mainthread and pc-thread"""
import threading
import sensorUnit
import time
import Queue

updateFreq=200.0 #Hz and must be float


class sensorThread(threading.Thread):
    def __init__(self,sensorList):
        self.__sensorList=sensorList
        self.__sensorUnit=sensorUnit.sensorUnit()
	threading.Thread.__init__(self)
        self.__distanceListLeft =  [0,0,0,0,0,0,0,0,0,0]
        self.__distanceListRight = [0,0,0,0,0,0,0,0,0,0]
        
    def run(self):
        while True:
            time.sleep(1.0/updateFreq)
            self.updateDistance()
            self.updateLineSensor()
            self.updateMiddleSensor()

    # def updateDistance(self):
    #     l = self.__sensorUnit.getLeftDistance()
    #     r = self.__sensorUnit.getRightDistance()
    #     self.__sensorList["distance"] = [l , r]
    
    def updateDistance(self):
        del self.__distanceListLeft[0]
        del self.__distanceListRight[0]
        self.__distanceListRight.append(self.__sensorUnit.getRightDistance())
        self.__distanceListLeft.append(self.__sensorUnit.getLeftDistance())
    
        l = filteredValue(distanceListLeft)
        r = filteredValue(distanceListRight)

        self.__sensorList["distance"] = [l , r]
            

    def updateLineSensor(self):
        for i in range(11):
            self.__sensorList["lineSensor"][i]=self.__sensorUnit.getLineSensor(i)

    def updateMiddleSensor(self):
        left = self.__sensorUnit.getLeftMiddleSensor()
        right = self.__sensorUnit.getRightMiddleSensor()
        self.__sensorList["middleSensor"][0] = left
        self.__sensorList["middleSensor"][1] = right


def filteredValue(list):
    divider = 0.5
    sum = 0
    for i in range(10,-1,-1):
        sum += (list[i] * divider)
        divider *= 0.5
    return sum
