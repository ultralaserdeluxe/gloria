"""a simple testprogram for the pcThread class that is used to connects to a user and receives commands and sends data back"""
from pcThread import pcThread
import Queue
import time
from sensorThread import sensorThread
from driveUnit import driveUnit
from arm import Arm
driver=driveUnit()
robot_arm=Arm()
commandQueue=Queue.Queue()
sensorList=[["lineSensor",[0,0,20,0,512,0,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[0,0,255,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[50,50]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]]]
#sensorThreadObject=sensorThread(sensorList)
#sensorThreadObject.daemon=True
#sensorThreadObject.start()
pcThreadObject=pcThread(commandQueue,sensorList)
pcThreadObject.daemon=True
pcThreadObject.start()
while True:
    if not commandQueue.empty():
        command=commandQueue.get()
	if command[0]=="motorSpeed":
		#print(command)
		left=int(command[1][0])
		right=int(command[1][1])
		if left>0 and left<70:
			left=80
		if right>0 and right<70:
			right=80
		if left<0 and left>(-70):
			left=-80
		if right<0 and right>(-70):
			right=-80
		print(left,right)
		driver.setMotorLeft(left)
		driver.setMotorRight(right)
		driver.sendAllMotor()
	if command[0]=="armPosition":
		robot_arm.updateX(command[1][0])
		robot_arm.updateY(command[1][1])
		robot_arm.updateZ(command[1][2])
		servoValues=robot_arm.getServoValues()
		print(servoValues)
		for i in range(6):
			driver.setArmAxis(i+1,servoValues[i])
			driver.sendAllAxis()
			
		
