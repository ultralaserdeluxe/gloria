"""a thread class that fetches data from the sensorunit and puts it in the list shared with mainthread and pc-thread"""
import threading
import sensorUnit
import time
updateFreq=20.0 #Hz and must be float
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
        for i in range(len( self.__sensorList)):
            if self.__sensorList[i][0]=="distance":
                self.__sensorList[i][1][0]=self.__sensorUnit.getLeftDistance()
                self.__sensorList[i][1][1]=self.__sensorUnit.getRightDistance()
                
    def updateLineSensor(self):
        for i in range(len( self.__sensorList)):
            if self.__sensorList[i][0]=="lineSensor":
                for j in range(11):
                    self.__sensorList[i][1][j]=self.__sensorUnit.getLineSensor(j)
                    
                    
