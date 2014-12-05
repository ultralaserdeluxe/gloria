import time
from sensorThread import sensorThread
from driveUnit import driveUnit
from regulatorNew import Regulator

sensorList = {"lineSensor" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              "distance" :  [0, 0],
              "armPosition" : [0, 0, 255, 4, 5, 5],
              "errorCodes" : ["YngveProgrammedMeWrong"],
              "motorSpeed" : [70, 70],
              "latestCalibration" : "0000-00-00-15:00",
              "autoMotor" : True,
              "autoArm" : False,
              "regulator" : [0, 0]}

driver = driveUnit()

sensorThreadObject=sensorThread(sensorList)
sensorThreadObject.daemon=True
sensorThreadObject.start()

regulator = Regulator(sensorList)
regulator.daemon = True
regulator.start()

l, r = 0, 0

while True:
    time.sleep(0.01)

    l, r = sensorList["regulator"]
    driver.setMotorLeft(l)
    time.sleep(0.001)
    driver.setMotorRight(r)
    time.sleep(0.001)
    driver.sendAllMotor()
