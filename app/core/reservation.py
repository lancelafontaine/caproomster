# Reservation object
class Reservation:

    # Constructor
    def __init__(self, room, holder, time, description, reservationId):
        self.user = holder
        self.time = time
        self.room = room
        self.description = description
        self.reservationId = reservationId

    # Print method for debugging
    def __str__(self):
        return "Reservation Info" +\
        "Holder: " + str(self.user.getId()) +\
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

    def to_dict(self):
        reservation_data = {}
        reservation_data['room'] = {}
        reservation_data['room']['roomId'] = self.getRoom().getId()
        reservation_data['user'] = {}
        reservation_data['user']['username'] = self.getUser().getId()
        reservation_data['timeslot'] = {}
        reservation_data['timeslot']['startTime'] = self.getTimeslot().getStartTime()
        reservation_data['timeslot']['endTime'] = self.getTimeslot().getEndTime()
        reservation_data['timeslot']['date'] = self.getTimeslot().getDate()
        reservation_data['timeslot']['timeId'] = self.getTimeslot().getId()
        reservation_data['description'] = self.getDescription()
        reservation_data['reservationId'] = self.getId()
        return reservation_data

