"""a simple testprogram for the pcThread class that is used to connects to a user and receives commands and sends data back"""
from pcThread import pcThread
import Queue
import time
import copy
commandQueue=Queue.Queue()
sensorList=[["lineSensor",[0,0,20,0,512,0,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[0,0,255,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[0,0]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]]]

pcThreadObject=pcThread(commandQueue,sensorList)
pcThreadObject.daemon=True
pcThreadObject.start()
while True:
    time.sleep(0.001)
    print(commandQueue.qsize())
    if not commandQueue.empty():
        command=(commandQueue.get())
        if command[0]=="motorSpeed":
            left=int(command[1][0])
            right=int(command[1][1])
           # print("setting motor to:")
           # print(left,right)
        if command[0]=="armPosition":
            #print("setting arm to:")
           # print(command[1])
	    pass
			
		
