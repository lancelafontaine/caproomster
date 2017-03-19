import UnitOfWork
import ReservationIdMap

from datetime import datetime
from datetime import timedelta

from app.TDG import ReservationTDG
from app.mapper import TimeslotMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper
from app.core.reservation import Reservation



def makeNewReservation(room,user,timeslot,description,repeat_amount):
    max_repetition = 2
    days_in_a_week = 7

    # safe guard if repeat amount is greater than max repetition
    if repeat_amount > max_repetition:
        repeat_amount = max_repetition

    if repeat_amount <= max_repetition:

        # filter date values
        date_split_list = timeslot.getDate().split('-')
        year = int(date_split_list[0])
        month = int(date_split_list[1])
        day = int(date_split_list[2])

        # Create datetime object
        reservation_date = datetime(year,month,day)

        # repeatAmount + 1 : because at least 1 reservation should be made
        for i in range(repeat_amount + 1):

            # create and register a timeslot object
            timeslot.setDate(reservation_date.strftime('%Y-%m-%d'))
            timeslot = TimeslotMapper.makeNew(timeslot.getStartTime(), timeslot.getEndTime(), timeslot.getDate(), timeslot.getBlock(), user.getId())
            TimeslotMapper.save(timeslot)
            timeslot_id = TimeslotMapper.findId(user.getId())
            timeslot.setId(timeslot_id)

            # create and register a reservation object
            reservation = Reservation(room, user,timeslot,description,timeslot_id)
            ReservationIdMap.addTo(reservation)
            UnitOfWork.registerNew(reservation)

            # add a week to the current reservation date
            reservation_date += timedelta(days=days_in_a_week)

            save(reservation)
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
