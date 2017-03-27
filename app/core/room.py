
# Room Object
class Room:

    # Constructor
    def __init__(self,roomId,lock):
        self.roomId = roomId
        self.lock = lock

    def getId(self):
        return self.roomId

    def setId(self,roomId):
        self.roomId = roomId
