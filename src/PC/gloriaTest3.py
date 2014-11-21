from driveUnit import driveUnit
from joystick import Joystick
import time

drive=driveUnit()
joy=Joystick()

while True:
    driveUnit.setMotorLeft((-joy.y_axis()-joy.x_axis())*512)
    driveunit.setMotorRight((-joy.y_axis()+joy.x_axis())*512)
    time.sleep(0.1)
