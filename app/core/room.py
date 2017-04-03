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

    def to_dict(self):
        room_data = {}
        room_data['roomId'] = self.getId()
        return room_data