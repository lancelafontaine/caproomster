
import UserMapper
import RoomMapper
import ReservationMapper
import WaitingMapper
import TimeslotMapper

from app.core.user import User
from app.core.room import Room
from app.core.reservation import Reservation
from app.core.waiting import Waiting
from app.core.timeslot import Timeslot

newList = []
changedList = []
deletedList = []

def __int__(self):
	pass

def registerNew(object):
    newList.append(object)

def registerDirty(object):
    changedList.append(object)

def registerDeleted(object):
    deletedList.append(object)



def commit():

    for index, object in enumerate(newList):
        if type(object) is User:
            UserMapper.save(object)
        if type(object) is Room:
            RoomMapper.save(object)
        if type(object) is Reservation:
            ReservationMapper.save(object)
        if type(object) is Waiting:
            WaitingMapper.save(object)
        if type(object) is Timeslot:
            TimeslotMapper.save(object)

    for index, object in enumerate(changedList):
        if type(object) is User:
            UserMapper.update(object)
        if type(object) is Room:
            RoomMapper.update(object)
        if type(object) is Reservation:
            ReservationMapper.update(object)
        if type(object) is Waiting:
            WaitingMapper.update(object)
        if type(object) is Timeslot:
            TimeslotMapper.update(object)

    for index, object in enumerate(deletedList):
        if type(object) is User:
            UserMapper.erase(object)
        if type(object) is Room:
            RoomMapper.erase(object)
        if type(object) is Reservation:
            ReservationMapper.erase(object.getId())
        if type(object) is Waiting:
            WaitingMapper.erase(object)
        if type(object) is Timeslot:
            TimeslotMapper.erase(object.getId())

    del newList[:]
    del changedList[:]
    del deletedList[:]
