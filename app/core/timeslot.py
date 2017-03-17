# Timeslot object
class Timeslot:

    # Constructor
    def __init__(self, startTime, endTime, date, block, timeId):
        self.startTime = startTime
        self.endTime = endTime
        self.date = date
        self.block = endTime - startTime
        self.timeId = timeId

    def __str__(self):
        return "StartTime: " + str(self.startTime) +\
          " EndTime: " + str(self.endTime) +\
          " Date: " + str(self.date) +\
          " Duration: " + str(self.block) +\
          " TID: " + str(self.timeId)

    # Accessors and Mutators
    def getStartTime(self):
        return self.startTime

    def setStartTime(self,startTime):
        self.startTime = startTime

    def getEndTime(self):
        return self.endTime

    def setEndTime(self,endTime):
        self.endTime = endTime

    def getDate(self):
        return self.date

    def setDate(self,date):
        self.date = date

    def getBlock(self):
        return self.block

    def setBlock(self, block):
        self.block = block

    def getId(self):
        return self.timeId

    def setId(self,timeId):
        self.timeId = timeId