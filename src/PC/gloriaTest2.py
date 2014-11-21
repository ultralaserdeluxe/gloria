from pcModule import pcModule
import time
gloria=pcModule("192.168.99.1")
while True:
    gloria.updateSensors()
    print(gloria.getLineSensor())
    time.sleep(0.1)