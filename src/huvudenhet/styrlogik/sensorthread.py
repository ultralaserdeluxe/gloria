# -*- coding: utf-8 -*-
import threading
import random
import time
import spidev

boolean = [0,1]

class SensorThread(threading.Thread):
    def __init__(self, sensorList, delay):
        threading.Thread.__init__(self)
        self.sensorList = sensorList
        self.delay = delay
        self.exitFlag = 0
        #self.spi = spidev.SpiDev()
        #self.spi.open(0,1)

    def run(self):
        print "starting sensorthread" 
        while not self.exitFlag:
            #self.spi.writebytes([0x0F]) 
            #data = self.spi.readbytes(13)
            data = testreadbytes()
            self.divide_data(data)
            time.sleep(self.delay)
        
    def kill(self, status):
        self.exitFlag = status

    def divide_data(self, data):
        temp = []
        counter = 0
        del self.sensorList[0][1][0:]
        #lägger till linjesensordatan i sensorList 
        for i in data[0:88]:
            temp.append(i)
            counter+=1
            if counter == 8:
                self.sensorList[0][1].append(binary_to_int(temp))
                counter = 0
                del temp[0:]
        #lägger till avståndsensordata i sensorList
        del self.sensorList[1][1][0:]
        self.sensorList[1][1].append(binary_to_int(data[88:96]))
        self.sensorList[1][1].append(binary_to_int(data[96:104]))
        

def testreadbytes():
    temp = []
    for i in range(0,104):
        temp.append(random.choice(boolean)) 
    return temp

#tar en lista med ett binärtal och gör om det till ett heltal
def binary_to_int(seq):
    temp = ""
    for i in seq:
        temp += str(i)
    return int(temp,2) 

