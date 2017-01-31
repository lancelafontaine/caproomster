from hashlib import md5
from unitofwork import UnitOfWork
from identitymaps import *
from datagateways import *
from models import *

class ReservationMapper:

    def __init__(self):
        self.uow = UnitOfWork(self) 
        self.identitymap = ReservationIdentityMap() 
        self.tdg = ReservationTDG()

    def insert(self, username, roomNumber, status, timeslot, timestamp):
        r = Reservation(username, roomNumber, status, timeslot, timestamp)
        self.identitymap.add(r)
        self.uow.registerNew(r)

    def find(self, username, roomNumber, timeslot):
        r = self.identitymap.find(self.getHash(username, roomNumber, timeslot))
        if r is None:
            r = self.loadReservation(self.tdg.find(username, roomNumber, timeslot))
            if r is not None:
                self.identitymap.add(r)
        return r

    def delete(self, username, roomNumber, timeslot):
        r = self.identitymap.find(self.getHash(username, roomNumber, timeslot))
        if r is None:
            r = self.loadReservation(self.tdg.find(username, roomNumber, timeslot))
            if r is not None:
                self.uow.registerRemoved(r)
        else:
            self.identitymap.delete(r)
            self.uow.registerRemoved(r)

    def updatePendingReservation(self, roomNumber, timeslot):
        r = self.identitymap.findNextPendingReservation(roomNumber, timeslot)
        if r is None:
            r = self.loadReservation(self.tdg.findNextPendingReservation(roomNumber, timeslot))
            if r is not None:
                self.identitymap.add(r)
                self.uow.registerDirty(r)
        else:
            self.identitymap.setFilled(r)
            self.uow.registerDirty(r)

    def isTimeslotReserved(self, roomNumber, timeslot):
        isReserved = True
        r = self.identitymap.findReserved(roomNumber, timeslot)
        if r is None:
            if self.tdg.getFilledCount(roomNumber, timeslot) == 0:
                isReserved = False
        return isReserved

    def hasReservation(self, username, roomNumber, timeslot):
        hasReservation = True
        r = self.identitymap.find(self.getHash(username, roomNumber, timeslot))
        if r is None:
            if self.tdg.getReservationCount(username, roomNumber, timeslot) == 0:
                hasReservation = False
        return hasReservation

    def removeFromAllOtherWaitingLists(self, username, roomNumber, timeslot):
        reservations = self.identitymap.findAllOtherPendingReservations(username, roomNumber, timeslot)
        if reservations:
            for r in reservations:
                self.uow.registerRemoved(r)
            self.identitymap.deleteAll(reservations)
        self.tdg.deleteAllOtherPendingReservations(username, roomNumber, timeslot)

    def getReservations(self, roomNumber, startTimeslot):
        return self.tdg.getReservations(roomNumber, startTimeslot)

    def getReservationForUsername(self, username, status):
        return self.tdg.getReservationsForUsername(username, status)

    def getNumOfReservations(self, username, timeslot):
        return self.tdg.getNumOfReservations(username, timeslot)

    # Called by UnitOfWork
    def applyInsert(self, objects):
        for obj in objects:
            self.tdg.insert(obj.username, obj.roomNumber, obj.status, obj.timeslot, obj.timestamp)

    def applyDelete(self, objects):
        for obj in objects:
            self.tdg.delete(obj.username, obj.roomNumber, obj.timeslot)

    def applyUpdate(self, objects):
        # Update the status of a reservation
        for obj in objects:
            self.tdg.setFilled(obj.username, obj.roomNumber, obj.timeslot)

    def commit(self):
        self.uow.commit()

    def loadReservation(self, row):
        reservation = None
        if row:
            reservation = Reservation(row[0], row[1], row[2], row[3], row[4])
        return reservation

    def getHash(self, username, roomNumber, timeslot):
        lst = [username, roomNumber, timeslot]
        return md5(''.join(str(s) for s in lst)).hexdigest()


class RoomMapper:

    def __init__(self):
        self.uow = UnitOfWork(self)
        self.identitymap = RoomIdentityMap()
        self.tdg = RoomTDG()

    def insert(self, roomNumber):
        room = Room(roomNumber)
        self.identitymap.add(room)
        self.uow.registerNew(room)

    def commit(self):
        self.uow.commit()

    def applyInsert(self, objects):
        for obj in objects:
            self.tdg.insert(obj.roomNumber)

    def applyUpdate(self):
        pass

    def applyDelete(self):
        pass

    def getRooms(self):
        return self.tdg.getRooms()


class UserMapper:

    def __init__(self):
        self.uow = UnitOfWork(self)
        self.identitymap = UserIdentityMap()
        self.tdg = UserTDG()

    def insert(self, username, password):
        user = User(username, password)
        self.identitymap.add(user)
        self.uow.registerNew(user)

    def isRegistered(self, username, password):
        isRegistered = True
        if self.tdg.isRegistered(username, password) == 0:
            isRegistered = False
        return isRegistered

    def commit(self):
        self.uow.commit()

    def applyInsert(self, objects):
        for obj in objects:
            self.tdg.insert(obj.username, obj.password)

    def applyUpdate(self):
        pass

    def applyDelete(self):
        pass
