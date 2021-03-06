import platform

if "arm" in platform.machine().lower():
    from spi import SPI
else:
    from spi_dummy import SPI

class sensorUnit():
    def __init__(self):
        self.__bus=SPI(3,1)
        self.__bus.msh=20000
    def getLeftDistance(self):
        self.__bus.writebytes([0x0C])
        return self.__bus.readbytes(1)[0]
    def getRightDistance(self):
        self.__bus.writebytes([0x0B])
        return self.__bus.readbytes(1)[0]
    def getLineSensor(self,temp):
        if temp<0 or temp>10:
            raise SyntaxError("Linesensor value out of bounds")
        self.__bus.writebytes([temp])
        return self.__bus.readbytes(1)[0]
    def getLeftMiddleSensor(self):
        self.__bus.writebytes([14])
        return self.__bus.readbytes(1)[0]
    def getRightMiddleSensor(self):
        self.__bus.writebytes([15])
        return self.__bus.readbytes(1)[0]

