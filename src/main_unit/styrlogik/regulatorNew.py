import threading
import time

#remember to remove after debugging
import matplotlib.pyplot as plt

class Regulator:
    def __init__(self, sensor_list):
        self.sensor_list=sensor_list
        self.sensor_list.append(["regulator", [0, 0]])
        self.e0 = 0.0
        self.e1 = 0.0
        self.e2 = 0.0
        self.P = 1.0
        self.I = 1.0
        self.D = 1.0
        self.calibration_data = [(74, 198), (127, 210), (150, 220), (50, 184), (140, 226), (65, 180),
                                 (170, 230), (47, 160), (103, 204), (56, 165), (48, 178)]
        self.out = 0.0
        threading.Thread.__init__(self)

        
    ##if you change the pid values outside this thread
    def updatePID(self):
        for i in range(len(self.sensor_list)):
            if self.sensor_list[i][0] == "PID":
                self.P = self.sensor_list[i][1][0]
                self.I = self.sensor_list[i][1][1]
                self.D = self.sensor_list[i][1][2]
                return
        raise SyntaxError("sensor not in list")
    
    def regulate(self, delta_seconds):
        self.updatePID()

        self.e1 = self.e0
        self.e0 = self.get_current_error()

        self.out = self.P * self.e0 + (self.D / delta_seconds) * (self.e0 - self.e1) 

        self.setMotors()
            
    def normalize(self, value, minimum, maximum):
        return float(value) / (maximum - minimum)

    def normalize_sensor_values(self, values, calibration_data):
        norm_values = []

        for i in range(len(values)):
            minimum = calibration_data[i][0]
            maximum = calibration_data[i][1]
            norm_values.append(normalize(values[i], minimum, maximum))

        return norm_values

    def calc_position(self, norm_values):
        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        # From TSEA29 lecture 5 (AVR, sensorer, Beagleboard)
        center = sum(map(lambda x, y: x*y, norm_values, weights)) / sum(norm_values)

        return center
        
    def calc_error(self, position):
        # 6 is the middle weight.
        return 6 - position

    def get_current_error(self):
        sensor_values = self.getSensorValues()
        norm_values = normalize_sensor_values(sensor_values, self.calibration_data)
        position = calc_position(norm_values)
        error = calc_error(position)
        
        return error

    #set each motorspeed to motorspeed+-motorspeed*signalout
    def setMotors(self):
        leftCurrent=self.getLeftMotor()
        rightCurrent=self.getRightMotor()
        left=leftCurrent+int(2.0*leftCurrent*self.out)
        right=rightCurrent-int(2.0*rightCurrent*self.out) 
        if self.out>0.0:
            self.setRegMotor(left, rightCurrent)
        else:
            self.setRegMotor(leftCurrent, right)

    #puts the calculated motorspeeds in the sensorlist
    def setRegMotor(self,left,right):
        for i in range(len(self.sensor_list)):
            if self.sensor_list[i][0]=="regulator":
                self.sensor_list[i][1][0]=left
                self.sensor_list[i][1][1]=right
                return
        raise SyntaxError("sensor not in list")

    #returns the leftmotorspeed from the sensorlist
    def getLeftMotor(self):
        for i in range(len(self.sensor_list)):
            if self.sensor_list[i][0]=="motorSpeed":
                return self.sensor_list[i][1][0]
        raise SyntaxError("sensor not in list")

    #returns the rightmotorspeed from the sensorlist
    def getRightMotor(self):
        for i in range(len(self.sensor_list)):
            if self.sensor_list[i][0]=="motorSpeed":
                return self.sensor_list[i][1][1]
        raise SyntaxError("sensor not in list")
 
    def getSensorValues(self):
        for i in range(len(self.sensor_list)):
            if self.sensor_list[i][0]=="lineSensor":
                return self.sensor_list[i][1]
        raise SyntaxError("sensor not in list")
