from spi import SPI
class sensorUnit():
    def __init__(self):
        self.__bus=SPI(3,1)
	self.__bus.msh=20000
    def getLeftDistance(self):
        self.__bus.writebytes([0x0B])
        return self.__bus.readbytes(1)[0]
    def getRightDistance(self):
        self.__bus.writebytes([0x0C])
        return self.__bus.readbytes(1)[0]
    def getLineSensor(self,temp):
        if temp<0 or temp>10:
            raise SyntaxError("Linesensor value out of bounds")
        self.__bus.writebytes([temp])
        return self.__bus.readbytes(1)[0]
