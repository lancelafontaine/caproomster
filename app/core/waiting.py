# Waiting object
class Waiting:
    # Constructor
    def __init__(self,room,holder,time,description, waitingId):
        self.user = holder
        self.time = time
        self.room = room
        self.description = description
        self.waitingId = waitingId

    # Print method for debugging
    def __str__(self):
        return "Waiting Info: \n Holder: " +\
               str(self.user.getName())+str(self.time)+"Description: " +\
               str(self.description)+"WID: " + str(self.waitingId)

    # Accessors and Mutators
    def getId(self):
        return self.waitingId

    def setId(self,waitingId):
        self.waitingId = waitingId

    def getTimeslot(self):
        return self.time

    def setTimeslot(self, time):
        self.time = time

    def getRoom(self):
        return self.room

    def setRoom(self,room):
        self.room = room

    def getUser(self):
        return self.user

    def setUser(self, user):
        self.user = user

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def to_dict(self):
        waiting_data = {}
        waiting_data['room'] = {}
        waiting_data['room']['roomId'] = self.getRoom().getId()
        waiting_data['user'] = {}
        waiting_data['user']['username'] = self.getUser().getId()
        waiting_data['timeslot'] = {}
        waiting_data['timeslot']['startTime'] = self.getTimeslot().getStartTime()
        waiting_data['timeslot']['endTime'] = self.getTimeslot().getEndTime()
        waiting_data['timeslot']['date'] = self.getTimeslot().getDate()
        waiting_data['timeslot']['timeId'] = self.getTimeslot().getId()
        waiting_data['description'] = self.getDescription()
        waiting_data['waitingId'] = self.getId()
        return waiting_data
