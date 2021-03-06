import UnitOfWork

from app.TDG import ReservationTDG
from app.mapper import TimeslotMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper
from app.mapper import EquipmentMapper
from app.core.reservation import Reservation


def makeNew(room, user, timeslot, description, equipment, reservationId):
    reservation = Reservation(room, user, timeslot, description, equipment, reservationId)
    UnitOfWork.registerNew(reservation)
    return reservation

def find(reservationId):
    result = ReservationTDG.find(reservationId)
    if not result:
        return None
    else:
        # must make a reference to timeslottable and create a timeslot object
        room = RoomMapper.find(result[0][1])
        holder = UserMapper.find(result[0][3])
        timeslot = TimeslotMapper.find(result[0][4])
        equipment = EquipmentMapper.find(result[0][5])
        return Reservation(room, holder, timeslot, result[0][2], equipment, result[0][0])


def findAll():
    result = ReservationTDG.findAll()
    allReservations = []
    if not result:
        return []
    else:
        for index, r in enumerate(result):
            room = RoomMapper.find(result[index][1])
            holder = UserMapper.find(result[index][3])
            timeslot = TimeslotMapper.find(result[index][4])
            equipment = EquipmentMapper.find(result[index][5])
            reservation = Reservation(room, holder, timeslot, result[index][2], equipment, result[index][0])
            allReservations.append(reservation)
        return allReservations


def find_time_slot_ids(userId):
    timeslot_ids = []
    reservation_list = ReservationTDG.findByUserId(userId)
    for reservation in reservation_list:
        timeslot_ids.append(reservation[4])
    return timeslot_ids


def findByUser(userId):
    userReservation = []
    result = ReservationTDG.findByUserId(userId)
    for index, userR in enumerate(result):
        userReservation.append(find(userR[0]))
    return userReservation

def findByRoom(roomId):
    roomReservations = []
    result = ReservationTDG.findByRoom(roomId)
    for index, roomR in enumerate(result):
        roomReservations.append(find(roomR[0]))
    return roomReservations

def setReservation(reservationId):
    reservation = find(reservationId)
    reservation.setId(reservationId)
    UnitOfWork.registerDirty(reservationId)


def delete(reservationId):
    UnitOfWork.registerDeleted(find(reservationId))


# save all work
def done():
    UnitOfWork.commit()


# Saves reservation
def save(reservation):
    ReservationTDG.insert(
        reservation.getId(),
        reservation.getRoom().getId(),
        reservation.getDescription(),
        reservation.getUser().getId(),
        reservation.getTimeslot().getId(),
	    reservation.getEquipment().getId()
      )


# updates room Object
def update(reservation):
    ReservationTDG.update(
        reservation.getId(),
        reservation.getRoom().getId(),
        reservation.getUser().getId(),
        reservation.getDescription(),
        reservation.getTimeslot().getId(),
        reservation.getEquipment().getId()
    )


# deletes room object
def erase(reservation):
    ReservationTDG.delete(reservation.getId())
