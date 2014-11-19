from spi import SPI
class styrUnit():
    def __init__(self):
        self.__bus=SPI(3,0)
        self.__bus.msh=20000
    def setMotorLeft(self,direction,speed):
        self.send_startbit()
        #längd
        self.__bus.writebytes([0x03])
        #kommandot
        self.__bus.writebytes([0x11])
        self.__bus.writebytes(direction)
        self.__bus.writebytes(speed)

    def setMotorRight(self,direction,speed):
        self.send_startbit()
        #längd
        self.__bus.writebytes([0x03])
        #kommandot
        self.__bus.writebytes([0x10])
        self.__bus.writebytes(direction)
        self.__bus.writebytes(speed)

    def send_to_motor(self):
        self.send_startbit()
        #längd
        self.__bus.writebytes([0x01])
        #action
        self.__bus.writebytes([0x3D])
    
    def send_startbit(self):
        self.__bus.writebytes([0xFF])
        self.__bus.writebytes([0xFF])
        
