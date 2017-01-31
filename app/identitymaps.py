import datetime


class IdentityMap:
    def __init__(self):
        self.ids = {}

    def find(self, hashCode):
        try:
            obj = self.ids[hashCode]
        except KeyError:
            obj = None
        return obj

    def add(self, obj):
        self.ids[obj.hashCode()] = obj
    
    def delete(self, obj):
        try:
            del self.ids[obj.hashCode()]
        except KeyError:
            pass

    def deleteAll(self, objects):
        for obj in objects:
            try:
                del self.ids[obj.hashCode()]
            except KeyError:
                pass

class ReservationIdentityMap(IdentityMap):

    def findNextPendingReservation(self, roomNumber, timeslot):
        reservation = None
        lowest = datetime.datetime.max
        format = "%Y-%m-%d %H:%M:%S"
        for key, value in self.ids.iteritems():
            if (value.roomNumber == roomNumber
                    and value.timeslot == timeslot 
                    and value.status == 'pending'):
                timestamp = datetime.datetime.strptime(value.timestamp, format)
                if timestamp < lowest:
                    lowest = timestamp
                    reservation = value
        return reservation

    def findReserved(self, roomNumber, timeslot):
        reservation = None
        for key, value in self.ids.iteritems():
            if (value.status =='filled'
                    and value.roomNumber == roomNumber 
                    and value.timeslot == timeslot):
                reservation = value
        return reservation

    def findAllOtherPendingReservations(self, username, roomNumber, timeslot):
        reservations = []
        for key, value in self.ids.iteritems():
            if (value.username == username 
                    and value.timeslot == timeslot 
                    and value.roomNumber != roomNumber):
                reservations.append(value)
        return reservations

    def setFilled(self, obj):
        self.ids[obj.hashCode()].status = 'filled'

    
class RoomIdentityMap:
    pass


class UserIdentityMap:
    pass
