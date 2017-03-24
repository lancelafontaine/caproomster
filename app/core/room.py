
# Room Object
class Room:

    # Constructor
    def __init__(self,roomId,lock):
        self.roomId = roomId
        self.lock = lock

    # Print method for debugging
    def __str__(self):
        return "Room " + str(self.roomId) + " is lock? " + str(self.lock)

    # Accessors and Mutators
    def getLock(self):
        return self.lock

    def setLock(self, bool):
        self.lock = bool

    def getId(self):
        return self.roomId

    def setId(self,roomId):
        self.roomId = roomId