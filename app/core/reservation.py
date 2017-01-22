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
    def _print(self):
        print("Reservation Info")
        print("Holder: " + str(self.user.getName()))
        self.time._print()
        print("Description: " + str(self.description))
        print("RID: " + str(self.reservationId))

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

