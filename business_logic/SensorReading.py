import serial

class VL53:
    def __init__(self):
        self.baudrate = 115200      #default baudrate
        self.port =  "/dev/ttyUSB0"    #default port

        self.startSerial(self.port, self.baudrate)

        self.resetSerial()

        #sync bytes for communication
        self.SYNC1 = 83
        self.SYNC2 = 102
        self.NUM_OF_AVG = 4

        self.setDefaultParameters()
        
    def setDefaultParameters(self):
        self.value_changed = 0
        self.time_dif= 0
        self.timer_counter = 0

        self.BYTE_THRESHOLD = 5

        self.sumValue = 0
        self.valueArr = []
        self.avgDistance = 0
        self.last_avgDistance = 0
        self.distance = 0
        self.drawerNum = -1
        self.last_drawer_number = -1
        self.counter = 0

        self.isDrawerClosed = 1
        self.rawData = 0
        self.incomingData = 0
        self.sum_derivative = []
        self.sum_change = 0
        self.derivative = 0
        self.drawerChanged = 0
        self.drawerNumber = 0
        
        self.filterK = 0.25

    
    def setToolboxOn(self):
        self.ser.write(b'1')
    
    def setToolboxOff(self):
        self.ser.write(b'2')

    def readOneByte(self):
        tmp = self.ser.read(1)
        return tmp

    def getCurrentDrawer(self):
        return (self.drawerNum + 1)

    def getRawDistance(self):
        return self.rawData

    def getFilteredDistance(self):
        return self.avgDistance
    
    def isDrawerOpened(self):
        return (not self.isDrawerClosed)

    def isDrawerChanged(self):
        return self.drawerChanged 

    def startSerial(self, port, baudrate):
        self.ser = serial.Serial("/dev/ttyUSB0", 115200)

    def stopSerial(self):
        self.ser.close()

    def resetSerial(self):
        self.ser.close()
        self.ser.open()

    def readBytes(self):
        while((self.ser.inWaiting()>self.BYTE_THRESHOLD)):
            sync1 = self.readOneByte()
            if(ord(sync1) == self.SYNC1):
                        sync2 = self.readOneByte()
                        if(ord(sync2) == self.SYNC2):          
                            self.getDistances()        
                            self.updateValues()     
                            self.ser.flush() 
                           

    def getDistances(self):
        self.drawerNum = ord(self.readOneByte()) 

        self.isDrawerClosed = 0       

        if self.drawerNum == 99:
            self.isDrawerClosed = 1
            return 0

        lowBytes = self.readOneByte()
        highBytes = self.readOneByte()

        receivedData = ord(lowBytes) + (ord(highBytes)<<8)
        self.rawData = receivedData

        if self.drawerNum != self.last_drawer_number: 
            self.drawerChanged = 1
            print(self.drawerNum)
            self.sumValue = 0
            self.valueArr = []
            self.avgDistance = 0
            self.last_avgDistance = 0
            self.counter = 0
            self.last_drawer_number = self.drawerNum

        self.distance = receivedData

    def updateValues(self):
        index = self.drawerNumber
        temp = self.distance
        
        self.valueArr.append(temp)

        if(len(self.valueArr) > self.NUM_OF_AVG):
            self.sumValue = sum(self.valueArr)
            self.sumValue -= self.valueArr.pop(0)

        self.avgDistance = float(self.sumValue) / len(self.valueArr)

        self.derivative = (self.avgDistance - self.last_avgDistance)
        
        if(len(self.sum_derivative) > 5):
            self.sum_change = sum(self.sum_derivative)
            self.sum_change -= self.sum_derivative.pop(0)
            
        
        self.incomingData = 1
        self.last_avgDistance = self.avgDistance
        
     


