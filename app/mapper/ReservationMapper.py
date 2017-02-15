import UnitOfWork
import ReservationIdMap

from app.mapper import TimeslotMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper

from app.core.room import Room
from app.core.user import User
from app.core.timeslot import Timeslot
from app.core.reservation import Reservation


def makeNewReservation(room,holder,time,description,reservationId):
    reservation = Reservation(room, holder,time,description,reservationId)
    ReservationIdMap.addTo(reservation)
    UnitOfWork.registerNew(reservation)
    return reservation

def find(reservationId):
    reservation = ReservationIdMap.find(reservationId)
    result = []
    if reservation == None:
        result = ReservationTDG.find(reservationId)
        if result == None:
            return
        else:
            #must make a reference to timeslottable and create a timeslot object
            room = RoomMapper.find(result[0][1])
            holder = UserMapper.find(result[0][3])
            timeslot = TimeslotMapper.find(result[0][4])
            reservation = Reservation(room, holder,timeslot,result[0][2],timeslot.getId())
            ReservationIdMap.addTo(reservation)
    return reservation

def findAll():
    result = ReservationTDG.findAll()
    allReservations= []
    if result == None:
        return
    else:
        for index, r in enumerate(result):
            reservation = ReservationIdMap.find(r[0])
            if reservation == None:
                room = RoomMapper.find(result[0][1])
                holder = UserMapper.find(result[0][3])
                timeslot = TimeslotMapper.find(result[0][4])
                reservation = Reservation(room, holder, timeslot, result[0][2], timeslot.getId())
                allReservations.append(reservation)
                ReservationIdMap.addTo(reservation)
    return allReservations

def findByDate(date):
    return ReservationTDG.findByDate(date)

def findByUser(userId):
    userReservation = []
    result = ReservationTDG.findByUserId(userId)
    for index, userR in enumerate(result):
        userReservation.append(find(userR[0]))
    return userReservation

def setReservation(reservationId):
    reservation = find(reservationId)
    reservation.setId(reservationId)
    UnitOfWork.registerDirty(reservationId)

def delete(reservationId):
    reservation = ReservationIdMap.find(reservationId)
    if reservation is not None:
        ReservationIdMap.removeFrom(reservation)
    UnitOfWork.registerDeleted(reservation)
    UnitOfWork.commit()

#save all work
def done():
    UnitOfWork.commit()

# Saves reservation
def save(reservation):
    ReservationTDG.insert(reservation.getRoom().getId(),
        reservation.getDescription(),
        reservation.getUser().getId(),
        reservation.getTimeslot().getId()
    )

#updates room Object
def update(reservation):
    ReservationTDG.update(
        reservation.getId(),
        reservation.getRoom().getId(),
        reservation.getUser().getId(),
        reservation.getDescription(),
        reservation.getTimeslot().getId()
    )

#deletes room object
def erase(reservationid):
    ReservationTDG.delete(reservationid)
