# Waiting object
class Waiting:
    # Constructor
    def __init__(self, room, user, timeslot, description, waitingId):
        self.user = user
        self.timeslot = timeslot
        self.room = room
        self.description = description
        self.waitingId = waitingId

    # Print method for debugging
    def __str__(self):
        return "Waiting Info: \n Holder: " +\
               str(self.user.getName())+\
               str(self.timeslot) +\
               "Description: " + str(self.description)+\
               "Equipment needed: " + ("YES" if self.equipment.__len__() == 0 else "NO") + \
               "WID: " + str(self.waitingId)

    # Accessors and Mutators
    def getId(self):
        return self.waitingId
    def setId(self,waitingId):
        self.waitingId = waitingId
    def getTimeslot(self):
        return self.timeslot
    def setTimeslot(self, time):
        self.timeslot = time
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