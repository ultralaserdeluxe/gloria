"""This module is used to communicate with and control the glorious Gloria storage robot, created by group 2 in the course tsea29"""
import socket
import select
global s
#the main class
class pcModule():
    
    #constructor for the class that creates necessary objects and connects to host, takes the host ip-adress(string) as argument
    def __init__(self,ip_adress):
        self.__s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__port=1337
        self.__ip_adress=ip_adress
        self.__package_size=512
        self.__s.connect((self.__ip_adress , self.__port))
        self.__s.setblocking(0)
        self.__sensorsList=[]
        
    #receives data from host, returns a string as described in the designspecification
    def receiveData(self):
        readable, writable, exceptional = select.select([self.__s], [self.__s], [self.__s])
        complete_data_set=""
        while not complete_data_set:
            while self.__s not in readable:
                readable, writable, exceptional = select.select([self.__s], [self.__s], [self.__s])
            if self.__s in readable:
                while self.__s in readable:
                    complete_data_set=complete_data_set+self.__s.recv(self.__package_size).decode() #decode MIGHT be needed here
                    readable, writable, exceptional = select.select([self.__s], [self.__s], [self.__s])
        return complete_data_set
    
    #if the user wants the sensorlist for debugging
    def getSensorList(self):
        return self.__sensorsList
    
    #sends data to the host. The argument data is a string as described in the designspecfication
    def sendData(self,data):
        readable, writable, exceptional = select.select([self.__s], [self.__s], [])
        while self.__s not in writable:
            readable, writable, exceptional = select.select([self.__s], [self.__s], [])
        self.__s.sendall(data.encode()) #needs decoding for python3.4
        
    #returns the errorscodes if any as a list of strings
    def getErrorCodes(self):
        for element in self.__sensorsList:
            if element[0]=="errorCodes":
                return element[1]
        raise SyntaxError("sensor not in list")
    
    #returns the values from the linesensor as a list of ints
    def getLineSensor(self):
        for element in self.__sensorsList:
            if element[0]=="lineSensor":
                return element[1]
        raise SyntaxError("sensor not in list")
    
    #returns both distancesensorvalues as a list of ints
    def getDistanceSensor(self):
        for element in self.__sensorsList:
            if element[0]=="distance":
                return element[1]
        raise SyntaxError("sensor not in list")
    
    #returns the right distancesensorvalue as an int
    def getRightDistanceSensor(self):
        for element in self.__sensorsList:
            if element[0]=="distance":
                return element[1][1]
        raise SyntaxError("sensor not in list")
    
    #returns the left distancesensorvalue as an int
    def getLeftDistanceSensor(self):
        for element in self.__sensorsList:
            if element[0]=="distance":
                return element[1][0]
        raise SyntaxError("sensor not in list")
    
    #returns the current arm position as a list of ints
    def getArmPosition(self):
        for element in self.__sensorsList:
            if element[0]=="armPosition":
                return element[1]
        raise SyntaxError("sensor not in list")
    
    #returns both motors speed as an list of ints
    def getMotorSpeed(self):
        for element in self.__sensorsList:
            if element[0]=="motorSpeed":
                return element[1]
        raise SyntaxError("sensor not in list")
    
    #returns the time the latest calibration was done as an string
    def getCalibration(self):
        for element in self.__sensorsList:
            if element[0]=="latestCalibration":
                return element[1]
        raise SyntaxError("sensor not in list")
    
    #returns a bool that tells if the arm is in auto or not
    def getArmAuto(self):
        for element in self.__sensorsList:
            if element[0]=="autoArm":
                return element[1][0]
        raise SyntaxError("sensor not in list")
    
    #returns a bool that tells if the motors are in auto or not
    def getAutoMotor(self):
        for element in self.__sensorsList:
            if element[0]=="autoMotor":
                return element[1][0]
        raise SyntaxError("sensor not in list")
            #converts the sensorlist to a string to send to the user as described in the designspecifikation
    def checkSubelement(self,subelement):
        if subelement.isdigit():
            return int(subelement)
        else:
            if subelement=="True":
                return True
            elif subelement=="False":
                return False
            else:
                return subelement
    
    #converts the string received from the host to a usable list of lists
    def convertSensorList(self,data):
        newList=[]
        data=data.split(";")
        for element in data:
            if not element:
                continue
            tempList=[]
            temp=element.split("=")
            tempList.append(temp[0])
            temp=temp[1].split(",")
            tempList.append([])
            for subElement in temp:
                tempList[1].append(self.checkSubelement(subElement))
            newList.append(tempList)
        return newList
    
    #sends a command to the host to set the motors in auto depending on temp which is a bool
    def setAutoMotor(self,temp):
        command="autoMotor="+str(temp)
        self.sendCommand(command)
        
    #sends a command to the host to set the arm in auto depending on temp which is a bool
    def setAutoArm(self,temp):
        command="autoArm="+str(temp)
        self.sendCommand(command)
        
    #sends a commands to change the left motors to leftSpeed(int) and right motors to rightSpeed(int) which both are between 100 and -100
    def setMotorSpeed(self,leftSpeed,rightSpeed):
        command="motorSpeed="+str(leftSpeed)+","+str(rightSpeed)
        self.sendCommand(command)
        
    #sends a command to change the arm to the position decribed by the arguments
	# -410<x<410,-350<y<400 -71<z<420,-90<pitch<90,-240<wrist<60,<0grip<140
    def setArmPosition(self,x,y,z,pitch,wrist,grip):
        command="armPosition="+str(x)+","+str(y)+","+str(z)+","+str(pitch)+","+str(wrist)+","+str(grip)
        self.sendCommand(command)
        
    #sends a command to the host to calibrate the linesensor
    def calibrate(self):
        command="calibrate"
        self.sendCommand(command)
        
    #sends a command to the host to start the routine
    def start(self):
        command="start"
        self.sendCommand(command)
        
    #all commands go by this method if we wan to buffer the later on and send them all together
    def sendCommand(self,data):
        self.sendData(data + ";")
        
    #sends a command to the host to sends all the current sensorvalues and updates our sensorlist
    def updateSensors(self):
        self.sendCommand("status")
        self.__sensorsList=self.convertSensorList(self.receiveData())
        
