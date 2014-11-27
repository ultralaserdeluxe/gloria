from sensorThread import *
from driveUnit import *
from distance import *

linesensor_c_data = [[54,201],[122,225],[141,238],[66,177],[136,231],[76,185],
                     [171,228],[44,175],[97,195],[60,173],[43,168]]

sensorList = [["lineSensor",[0,0,0,0,0,0,0,0,0,0,0]],
              ["distance",[0,0]]]

speed = 30

def main():
    
    driver = driveUnit()
    sensorthread = sensorThread(sensorList)
    sensorthread.start()
    
    while True:
        if not (has_package_right() or has_package_left()):
            drive.setMotorLeft(speed)
            drive.setMotorRight(speed)
            drive.sendAllMotor()
    

def has_package_right():
    distance = distance_right(sensorList[1][1][1])
    if distance >= 8.0 and distance <= 20.0:
        return True
    return False

def has_package_left():
    distance = distance_left(sensorList[1][1][0])
    if distance >= 8.0 and distance <= 20.0:
        return True
    return False

main()
