"""a simple testprogram for the pcThread class that is used to connects to a user and receives commands and sends data back"""
from pcThread import pcThread
import Queue
import time
from sensorThread import sensorThread
from driveUnit import driveUnit
from arm import Arm
import regulatorNew as regulator
import copy
driver=driveUnit()
robot_arm=Arm()
commandQueue=Queue.Queue()
sensorList=[["lineSensor",[0,0,20,0,512,0,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[0,0,255,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[30,30]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]]]
reg=regulator.Regulator(sensorList)
reg.daemon=True
reg.start()
sensorThreadObject=sensorThread(sensorList)
sensorThreadObject.daemon=True
sensorThreadObject.start()
pcThreadObject=pcThread(commandQueue,sensorList)
pcThreadObject.daemon=True
pcThreadObject.start()
def getReg():
        for element in sensorList:
                if element[0] == "regulator":
                        return list(element[1])
        raise Exception("Clusterfuk > 9000")
		
while True:
    time.sleep(0.01)

    left, right = getReg()
    if left>0 and left<65:
	left=65
    if right>0 and right<65:
	right=65
    if left<0 and left>(-65):
	left=-65
    if right<0 and right>(-65):
	right=-65

    driver.setMotorLeft(left)
    driver.setMotorRight(right)
    driver.sendAllMotor()

    if not commandQueue.empty():
        command=copy.deepcopy(commandQueue.get())
	print(command)
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
		#robot_arm.updateX(command[1][0])
		#robot_arm.updateY(command[1][1])
		#robot_arm.updateZ(command[1][2])

		#sensor_values=robot_arm.getServoValues()
		#for i in range(6):
		limits=[[0,1023],[205,813],[210,940],[180,810],[0,1023],[0,512]]
		for i in range(len(command[1])):
			if command[1][i]>limits[i][1]:
				command[1][i]=limits[i][1]
			if command[1][i]<limits[i][0]:
				command[1][i]=limits[i][0]
		driver.setArmAxis(1,command[1][0])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(2,command[1][1])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(3,command[1][2])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(4,command[1][3])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(5,command[1][4])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		print(command[1][5])
		driver.setArmAxis(6,command[1][5])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)

			
		
