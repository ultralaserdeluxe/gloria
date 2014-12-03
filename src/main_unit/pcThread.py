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
        #recevies data from the user, returns a string as described in the designspecification
        def receiveData():
            complete_data_set=""
            while not complete_data_set:
                readable, writable, exceptional = select.select([self.__conn], [self.__conn], [self.__conn])
                while self.__conn not in readable:
                    readable, writable, exceptional = select.select([self.__conn], [self.__conn], [self.__conn])
		complete_data_set=self.__package_tail
                while self.__conn in readable:
                    data=self.__conn.recv(512).decode()
                    complete_data_set=complete_data_set+data
                    readable, writable, exceptional = select.select([self.__conn], [self.__conn], [self.__conn])
                    if not data:
                        break
	    self.__package_tail=complete_data_set[(complete_data_set.rfind(";")+1):]
	    complete_data_set=complete_data_set[:(complete_data_set.rfind(";")+1)]
            return complete_data_set
        
        def isfloat(value):
  	    try:
    		float(value)
    		return True
  	    except ValueError:
    		return False
        #converts the sensorlist to a string to send to the user as described in the designspecifikation
        def checkSubelement(subelement):
            if subelement.isdigit():
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
        def convertSensorList(list):
            string=""
            for element in list:
                if not string:
                    string=element[0]+"="+str(element[1][0])
                else:
                    string=string+";"+element[0]+"="+str(element[1][0])
                first=True
                for subElement in element[1]:
                    if first:
                        first=False
                    else:
                        string=string+","+str(subElement)
            return string
        
        #a simple function that sends data to the user
        def sendData(data):
            self.__conn.sendall(data.encode())
            
        #a function not used yet but can be used to remotely shutdown the BB
        def shutDown():
            os.system("poweroff")
            
        #takes in commands from the mainloop and executes them
        def commandHandler(data):
            temp=0;
            if data[0]=="status":
                sendData(convertSensorList(self.__sensorList))
            elif data[0]=="motorSpeed" or data[0]=="armPosition" or data[0]=="autoMotor" or data[0]=="autoArm":

		#print(data)
                for i in range(len(self.__sensorList)):
                    if self.__sensorList[i][0]==data[0]:
                        for j in range(len(data[1])):
                            self.__sensorList[i][1][j]=checkSubelement(data[1][j])
                        temp=i
                self.__commandQueue.put(self.__sensorList[temp][:])
            elif data[0]=="calibrate":
                self.__commandQueue.put(data)
            elif data[0]=="start":
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
            
        
        
                
            
