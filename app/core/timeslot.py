# Timeslot object
class Timeslot:

    # Constructor
    def __init__(self, startTime, endTime, date, block, userId, timeId):
        self.startTime = startTime
        self.endTime = endTime
        self.date = date
        self.block = endTime - startTime
        self.userId = userId
        self.timeId = timeId

    def __str__(self):
        return "StartTime: " + str(self.startTime) +\
          " EndTime: " + str(self.endTime) +\
          " Date: " + self.getDate().strftime('%Y/%m/%d') +\
          " Duration: " + str(self.block) +\
          " User ID: " + str(self.userId)

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

    def overlaps(self, other_timeslot):
        """

        :type other_timeslot: Timeslot
        """
        if self.getDate() != other_timeslot.getDate():
            return False

        return other_timeslot.getEndTime() > self.getStartTime() and other_timeslot.getStartTime() < self.getEndTime()



    def getId(self):
        return self.timeId

    def setId(self,timeId):
        self.timeId = timeId

    def getUserId(self):
        return self.userId

    def setUserId(self,userId):
        self.userId = userId
