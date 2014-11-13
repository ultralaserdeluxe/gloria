# -*- coding: utf-8 -*-
import threading
import random
import time
import spidev
 
line_sensordata = []
IR_right_sensordata = []
IR_left_sensordata = []

#spi = spidev.SpiDev()
#spi.open(0, 1)

boolean = [0,1]

class SensorThread(threading.Thread):
    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.delay = delay
        self.exitFlag = 0
        
    def run(self):
        print "starting sensorthread" 
        while not self.exitFlag:
            #spi.writebytes([0x0F])
            #time.sleep(self.delay)
            #data = spi.readbytes(13)
            data = testreadbytes()
            divide_data(data)
            #print_sensordata()
            time.sleep(self.delay)
        
    def kill(self, status):
        self.exitFlag = status

def testreadbytes():
    temp = []
    for i in range(0,104):
        temp.append(random.choice(boolean)) 
    return temp



def divide_data(data):
    del line_sensordata[0:]
    for i in data[0:88]:
        line_sensordata.append(i)
    del IR_right_sensordata[0:]    
    for i in data[88:96]:
        IR_right_sensordata.append(i)
    del IR_left_sensordata[0:]
    for i in data[96:104]:
        IR_left_sensordata.append(i)

def print_sensordata():
    
    temp = "line_sensordata: "
    for i in line_sensordata:
        temp += str(i)
    temp += "\nIR_right_sensordata: "
    for i in IR_right_sensordata:
        temp += str(i)
    temp += "\nIR_left_sensordata: "
    for i in IR_left_sensordata:
        temp += str(i)

    print temp    




