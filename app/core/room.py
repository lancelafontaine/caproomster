# Room Object
class Room:

    # Constructor
    def __init__(self, roomId):
        self.roomId = roomId

    # Print method for debugging
    def __str__(self):
        return "Room " + str(self.roomId)

    def getId(self):
        return self.roomId

    def setId(self,roomId):
        self.roomId = roomId