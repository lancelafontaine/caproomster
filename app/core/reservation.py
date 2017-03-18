# Reservation object
class Reservation:

    # Constructor
    def __init__(self, room,holder,time,description,reservationId):
        self.user = holder
        self.time = time
        self.room = room
        self.description = description
        self.reservationId = reservationId

    # Print method for debugging
    def __str__(self):
        return "Reservation Info" +\
        "Holder: " + str(self.user.getName()) +\
        str(self.time) +\
        "Description: " + str(self.description) +\
        "RID: " + str(self.reservationId)

    # Accessors and Mutators
    def getId(self):
        return self.reservationId

    def setId(self,reservationId):
        self.reservationId = reservationId

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

