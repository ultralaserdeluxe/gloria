"""a simple testprogram for the pcThread class that is used to connects to a user and receives commands and sends data back"""
from pcThread import pcThread
import Queue
import time
from sensorThread import sensorThread
from driveUnit import driveUnit
from arm import RobotArm
import regulatorNew as regulator
import copy
driver=driveUnit()
arm=RobotArm()
commandQueue=Queue.Queue()
sensorList=[["lineSensor",[0,0,20,0,512,0,0,100,0,0,0]],
            ["distance",[30,40]],
            ["armPosition",[0,0,255,4,5,5]],
            ["errorCodes",["YngveProgrammedMeWrong"]],
            ["motorSpeed",[30,30]],
            ["latestCalibration",["0000-00-00-15:00"]],
            ["autoMotor",[True]],
            ["autoArm",[False]]]
#reg=regulator.Regulator(sensorList)
#reg.daemon=True
#reg.start()
#sensorThreadObject=sensorThread(sensorList)
#sensorThreadObject.daemon=True
#sensorThreadObject.start()
pcThreadObject=pcThread(commandQueue,sensorList)
pcThreadObject.daemon=True
pcThreadObject.start()
def getReg():
        for element in sensorList:
                if element[0] == "regulator":
                        return list(element[1])
        raise Exception("Clusterfuk > 9000")
		
while True:
    time.sleep(0.001)

 #   left, right = getReg()
  #  if left>0 and left<65:
#	left=65
 #   if right>0 and right<65:
#	right=65
#    if left<0 and left>(-65):
#	left=-65
#    if right<0 and right>(-65):
#	right=-65

 #   driver.setMotorLeft(left)
 #   driver.setMotorRight(right)
 #   driver.sendAllMotor()

    if not commandQueue.empty():
        command=copy.deepcopy(commandQueue.get())
	#print(command)
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
		arm.setX(command[1][0])
		arm.setY(command[1][1])
		arm.setZ(command[1][2])
		arm.setGripperAngle(command[1][3])
		arm.setGripperRotationOffset(command[1][4])
		arm.setGripper(command[1][5])
		temp=arm.getServoValues()
		driver.setArmAxis(1,temp[0])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(2,temp[1])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(3,temp[2])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(4,temp[3])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(5,temp[4])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)
		driver.setArmAxis(6,temp[5])
		time.sleep(0.01)
		driver.sendAllAxis()
		time.sleep(0.01)

			
		
