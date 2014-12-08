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
        
    def run(self):
        while True:
            time.sleep(1.0/updateFreq)
            self.updateDistance()
            self.updateLineSensor()

    def updateDistance(self):
        l = self.__sensorUnit.getLeftDistance()
        r = self.__sensorUnit.getRightDistance()
        self.__sensorList["distance"] = [l , r]
                
    def updateLineSensor(self):
        for i in range(11):
            self.__sensorList["lineSensor"][i]=self.__sensorUnit.getLineSensor(i)
