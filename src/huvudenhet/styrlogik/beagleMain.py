"""a simple testprogram for the pcThread class that is used to connects to a user and receives commands and sends data back"""
from pcThread import pcThread
import queue
import time
from sensorThread import sensorThread
commandQueue=Queue.Queue()
sensorList=[["lineSensor",[0,0,20,0,512,0,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[1,2,3,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[50,50]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]]]
sensorThreadObject=sensorThread(sensorList)
sensorThreadObject.daemon=True
sensorThreadObject.start()
pcThreadObject=pcThread(commandQueue,sensorList)
pcThreadObject.daemon=True
pcThreadObject.start()
while True:
    time.sleep(1)
    if not commandQueue.empty():
        print("executing stuff")
        print(commandQueue.get())
