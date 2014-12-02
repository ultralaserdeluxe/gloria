from sensorThread import *
from driveUnit import *
from distance import *

linesensor_c_data = [[54,201],[122,225],[141,238],[66,177],[136,231],[76,185],
                     [171,228],[44,175],[97,195],[60,173],[43,168]]

sensorList = [["lineSensor",[0,0,0,0,0,0,0,0,0,0,0]],
              ["distance",[0,0]]]

speed = 0x70
new_speed = 0x00

def main():
    
    drive = driveUnit()
    sensorthread = sensorThread(sensorList)
    sensorthread.start()
   
    while True:
        time.sleep(0.1)
        if (has_package_left() or has_package_left()):
            new_speed = 0x00
        else:
            new_speed = 0x70
        if speed != new_speed:
            change_speed() 

def change_speed():
    speed = new_speed
    drive.setMotorLeft(speed)
    drive.setMotorRight(speed)
    drive.sendAllMotor()

def has_package_left():
    distance = distance_left(sensorList[1][1][1])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False

def has_package_right():
    distance = distance_right(sensorList[1][1][0])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False

main()
