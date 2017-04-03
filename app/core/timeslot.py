from datetime import datetime
import calendar

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
        def to_timestamp(date_list, time):
            return calendar.timegm(datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(time)).timetuple())

        my_date_list = self.getDate().strftime('%Y/%m/%d').split('/')
        my_timestamp_start = to_timestamp(my_date_list, self.getStartTime())
        my_timestamp_end = to_timestamp(my_date_list, self.getEndTime())

        other_timeslot_date_list = other_timeslot.getDate().strftime('%Y/%m/%d').split('/')
        other_timestamp_start = to_timestamp(other_timeslot_date_list, other_timeslot.getStartTime())
        other_timestamp_end = to_timestamp(other_timeslot_date_list, other_timeslot.getEndTime())

        return (my_timestamp_start < other_timestamp_end) and (my_timestamp_end > other_timestamp_start)

    def getId(self):
        return self.timeId

    def setId(self,timeId):
        self.timeId = timeId

    def getUserId(self):
        return self.userId

    def setUserId(self,userId):
        self.userId = userId

    def to_dict(self):
        timeslot_data = {}
        timeslot_data['startTime'] = self.getStartTime()
        timeslot_data['endTime'] = self.getEndTime()
        timeslot_data['date'] = self.getDate().strftime('%Y/%m/%d')
        timeslot_data['timeId'] = self.getId()
        timeslot_data['userId'] = self.getUserId()
        return timeslot_data

