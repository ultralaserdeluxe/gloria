class SPI:
    def __init__(self, x, y):
        pass

    def writebytes(self, seq):
        pass

    def readbytes(self, nbytes):
        return [0] * nbytes

class SPIDebug:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.msh = "default"
        print "SPI initialised:", x, y

    def writebytes(self, seq):
        print "SPI (%s, %s) msh=%s writebytes: %s" %(str(self.x), str(self.y), str(self.msh), str(seq))

    def readbytes(self, nbytes):
        print "SPI (%s, %s) msh=%s readbytes: %s" %(str(self.x), str(self.y), str(self.msh), str(nbytes))
        return [0] * nbytes
