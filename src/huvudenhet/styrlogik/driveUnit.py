from spi import SPI
class driveUnit():
    def __init__(self):
        self.__bus=SPI(3,0)
        self.__bus.msh=20000

    def setMotorLeft(self,speed):
        if speed >= 0:
            direction = 1
        else:
            direction = 0
        self.send_startbit()
        #length
        self.__bus.writebytes([0x03])
        #commando
        self.__bus.writebytes([0x11])
        self.__bus.writebytes([direction])
        self.__bus.writebytes([abs(speed)])

    def setMotorRight(self,speed):
        if speed >= 0:
            direction = 1
        else:
            direction = 0
        self.send_startbit()
        #length
        self.__bus.writebytes([0x03])
        #commando
        self.__bus.writebytes([0x10])
        self.__bus.writebytes([direction])
        self.__bus.writebytes([abs(speed)])

    def setArmAxis(self, id, value):
        self.send_startbit()
        #length
        self.__bus.writebytes([0x03])
        #commando
        self.__bus.writebytes([16+(id+1)])
        self.__bus.writebytes([value])

    def sendAxis(self,id):
        self.send_startbit()
        self.__bus.writebytes([0x01])
        self.__bus.writebytes([48+(id+1)])

    def sendAllAxis(self):
        self.send_startbit()
        self.__bus.writebytes([0x01])
        self.__bus.writebytes([0x3E])
        
    def sendAllMotor(self):
        self.send_startbit()
        #length
        self.__bus.writebytes([0x01])
        #action
        self.__bus.writebytes([0x3D])

    def sendMotorRight(self):
        self.send_startbit()
        self.__bus.writebytes([0x01])
        self.__bus.writebytes([0x30])
    
    def sendMotorLeft(self):
        self.send_startbit()
        self.__bus.writebytes([0x01])
        self.__bus.writebytes([0x31])

    def send_startbit(self):
        self.__bus.writebytes([0xFF])
        self.__bus.writebytes([0xFF])
