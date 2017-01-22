# Waiting object
class Waiting:
    # Constructor
    def __init__(self,room,holder,time,description, waitingId):
        self.user = holder
        self.time = time
        self.room = room
        self.description = description

    # Print method for debugging
    def _print(self):
        print("Waiting Info")
        print("Holder: " + str(self.user.getName()))
        self.time._print()
        print("Description: " + str(self.description))
        print("WID: " + str(self.waitingId))
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