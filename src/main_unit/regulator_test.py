import time
from sensorThread import sensorThread
from driveUnit import driveUnit
from regulator import Regulator

sensorList = {"lineSensor" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              "distance" :  [0, 0],
              "armPosition" : [0, 0, 255, 4, 5, 5],
              "errorCodes" : ["YngveProgrammedMeWrong"],
              "motorSpeed" : [70, 70],
              "latestCalibration" : "0000-00-00-15:00",
              "autoMotor" : True,
              "autoArm" : False,
              "regulator" : [0, 0]}

drive_unit = driveUnit()

sensor_thread = sensorThread(sensorList)
sensor_thread.daemon=True
sensor_thread.start()

regulator = Regulator(sensorList)
regulator.daemon = True
regulator.start()

l, r = 0, 0

while True:
    time.sleep(0.01)

    l, r = sensorList["regulator"]
    drive_unit.setMotorLeft(l)
    time.sleep(0.001)
    drive_unit.setMotorRight(r)
    time.sleep(0.001)
    drive_unit.sendAllMotor()

    print "I didnt crash!"
