"""a thread class that is used on the glorious Gloria storage robot to connect to a pc and receive commands and sends data back to the user"""
import threading
import socket
import select
import os
class pcThread(threading.Thread):

    #a constructor for the class
    def __init__(self,commandQueue,sensorList):
        self.__s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__s.bind(('', 1337))
        self.__commandQueue=commandQueue
        self.__sensorList=sensorList
        self.__conn=None
        self.__addr=None
        self.__package_tail=""
        threading.Thread.__init__(self)

    #when the thread is started this is started
    def run(self):

        #waits for a user to connect
        def waitForConnection():
            self.__s.listen(1)
            self.__conn, self.__addr = self.__s.accept()
            self.__s.setblocking(0)

        def resetConnection():
            self.__s.close()
            self.__s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__s.bind(('', 1337))
            self.__conn=None
            self.__addr=None
            self.__package_tail=""
            self.run()

        #recevies data from the user, returns a string as described in the designspecification
        def receiveData():
            complete_data_set=""
            while not complete_data_set:
                readable, writable, exceptional = select.select([self.__conn], [self.__conn], [self.__conn])
                while self.__conn not in readable:
                    readable, writable, exceptional = select.select([self.__conn], [self.__conn], [self.__conn])
                complete_data_set=self.__package_tail
		self.__package_tail=""
                while self.__conn in readable:
                    data=self.__conn.recv(512).decode()

                    if not data:
                        resetConnection()

                    complete_data_set=complete_data_set+data
                    readable, writable, exceptional = select.select([self.__conn], [self.__conn], [self.__conn])
                    if not data:
                        break
            self.__package_tail=complete_data_set[(complete_data_set.rfind(";")+1):]
            complete_data_set=complete_data_set[:(complete_data_set.rfind(";")+1)]
            return complete_data_set
	def isNumber(value):
	    try:
		int(value)
		return True
	    except ValueError:
		return False

        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        #converts the sensorlist to a string to send to the user as described in the designspecifikation
        def checkSubelement(subelement):
            if isNumber(subelement):
                return int(subelement)
            if isfloat(subelement):
                return float(subelement)
            else:
                if subelement=="True":
                    return True
                elif subelement=="False":
                    return False
                else:
                    return subelement
        def convertSensorList(stuff):
            s = ""

            for k, v in stuff.iteritems():
                s += str(k) + "="

                if isinstance(v, list):
                    s += ",".join([str(e) for e in v])
                else:
                    s += str(v)

                s += ";"

            return s

        #a simple function that sends data to the user
        def sendData(data):
            self.__conn.sendall(data.encode())

        #a function not used yet but can be used to remotely shutdown the BB
        def shutDown():
            os.system("poweroff")

        #takes in commands from the mainloop and executes them
        def commandHandler(data):
            if self.__commandQueue.qsize() > 5 and data[0] in ["motorSpeed", "armPosition"]:
                return

            temp=0;
            if data[0]=="status":
                ans = convertSensorList(self.__sensorList)
                sendData(ans)

            elif data[0]=="motorSpeed" or data[0]=="autoMotor" or data[0]=="autoArm" or data[0]=="hasPackage":

                checked_elements =  [checkSubelement(e) for e in data[1]]

                if len(data[1]) > 1:
                    if self.__sensorList[data[0]] != checked_elements:
                        self.__commandQueue.put([data[0]] + [checked_elements])
                else:
                    if self.__sensorList[data[0]] != checked_elements[0]:
                        self.__commandQueue.put([data[0]] + [checked_elements[0]])
            elif data[0]=="armPosition":
                checked_elements = [checkSubelement(e) for e in data[1]]

                if sum(checked_elements) != 0:
                    self.__commandQueue.put([data[0]] + [checked_elements])
            elif data[0]=="calibrateTape":
                self.__commandQueue.put(data)
            elif data[0] == "calibrateFloor":
                self.__commandQueue.put(data)
            elif data[0]=="start":
                self.__commandQueue.put(data)
            elif data[0] == "halt":
                self.__commandQueue.put(data)
            elif data[0] == "clearErrors":
                self.__commandQueue.put(data)
            else:
                pass

        #takes in a received string and converts it into a list of commands that can easily be used
        def splitCommand(data):
            commandList=[]
            data=data.split(";")
            for element in data:
                if "=" not in element:
                    commandList.append([element])
                else:
                    tempList=[]
                    element=element.split("=")
                    tempList.append(element[0])
                    temp=[]
                    element[1]=element[1].split(",")
                    for element in element[1]:
                        temp.append(element)
                    tempList.append(temp)
                    commandList.append(tempList)
            return commandList
        waitForConnection()
        while True:
            commands=splitCommand(receiveData())
            for element in commands:
                commandHandler(element)
