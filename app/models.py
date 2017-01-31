from hashlib import md5


class Item:
    def __init__(self, category):
        self.category = category

    def hashCode(self):
        lst = [self.category]
        return md5(''.join(str(s) for s in lst)).hexdigest()


class Room:
    def __init__(self, roomNumber):
        self.roomNumber = roomNumber

    def hashCode(self):
        lst = [self.roomNumber]
        return md5(''.join(str(s) for s in lst)).hexdigest()


class Registry:
    def __init__(self):
        self.reservationMapper = ReservationMapper()
        self.userMapper = UserMapper()
        self.roomMapper = RoomMapper()

    def makeReservation(self):
        pass

    def modifyReservation(self):
        pass

    def cancelReservation(self):
        pass


class Reservation:
    def __init__(self, username, roomNumber, status, timeslot, timestamp):
        self.username = username
        self.roomNumber = roomNumber
        self.status = status
        self.timeslot = timeslot
        self.timestamp = timestamp

    def hashCode(self):
        lst = [self.username, self.roomNumber, self.timeslot]
        return md5(''.join(str(s) for s in lst)).hexdigest()


class User:
    def __init__(self, username, password, category):
        self.username = username
        self.password = password
        self.category = category

    def hashCode(self):
        lst = [self.username]
        return md5(''.join(str(s) for s in lst)).hexdigest()
