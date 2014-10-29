"""a simple testprogram for the pcThread class that is used to connects to a user and receives commands and sends data back"""
from pcThread import pcThread
import Queue
import time
import copy
import driveUnit
import arm
robot_arm=arm.robotArm()
driver=driveUnit.driveUnit()
commandQueue=Queue.Queue()
sensorList= {"lineSensor" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                "distance" :  [0, 0],
                "armPosition" : [0, 0, 255, 4, 5, 5],
                "errorCodes" : ["YngveProgrammedMeWrong"],
                "motorSpeed" : [70, 70],
                "latestCalibration" : "0000-00-00-15:00",
                "autoMotor" : True,
                "autoArm" : False,
                "regulator" : [0, 0],
                "error" : 0}

pcThreadObject=pcThread(commandQueue,sensorList)
pcThreadObject.daemon=True
pcThreadObject.start()
while True:
    if not commandQueue.empty():
        command=(commandQueue.get())
        if command[0]=="motorSpeed":
            left=int(command[1][0])
            right=int(command[1][1])
	    driver.setMotorLeft(left)
	    driver.setMotorRight(right)
	    print(left,right)
	    driver.sendAllMotor()
        if command[0]=="armPosition":
	    robot_arm.setX(command[1][0])
	    robot_arm.setY(command[1][1])
	    robot_arm.setZ(command[1][2])
	    robot_arm.setGripperAngle(command[1][3])
	    robot_arm.setGripperRotationOffset(command[1][4])
	    robot_arm.setGripper(command[1][5])
	    temp=robot_arm.getServoValues()
	    print(temp)
	    for i in range(6):
		driver.setArmAxis(i+1,temp[i])
		time.sleep(0.001)
	    	driver.sendAllAxis()
		time.sleep(0.001)
			
		
